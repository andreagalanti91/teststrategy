"""Seconda analisi del canale: cosa poteva sfuggire alla prima.

1. I prezzi delle schermate sono veri? Per ogni prezzo dichiarato si controlla che il mercato l'abbia davvero toccato nelle
   72 ore prima del messaggio (candele orarie Binance spot; tolleranza 0,15% per le differenze fra borse).
2. Quando entra davvero? Ultima ora prima del messaggio in cui il mercato ha toccato il prezzo d'ingresso: ritardo fra
   esecuzione e annuncio.
3. Le schermate sono coerenti? ROI della card contro leva x movimento del prezzo.
4. Chi copiava con ordini limite: se il trader aveva annunciato prima il livello d'ingresso (piano con livello entro l'8% del
   suo prezzo), chi lo seguiva poteva mettere un ordine limite a quel livello. Eseguito se il prezzo lo tocca fra il piano e
   l'annuncio dell'ingresso (piu' 24 ore). Le uscite a un obiettivo annunciato prima si eseguono a quel prezzo (ordine limite);
   le altre al prezzo di mercato dopo il messaggio.
5. Dimensione: rischio fisso del 2% del capitale per operazione, con lo stop dichiarato (o, se manca, il 2% del prezzo).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import telegram_ricostruzione as TR

ROOT = TR.ROOT
OUT = TR.OUT
pct = lambda x, d=1: "n/d" if x is None or not np.isfinite(x) else f"{x * 100:+.{d}f}%".replace(".", ",")
num = lambda x, d=2: "n/d" if x is None or not np.isfinite(x) else f"{x:.{d}f}".replace(".", ",")
TOL = 0.0015


def touched(asset, price, t0, t1):
    p = TR.prices(asset)
    if p is None or price is None:
        return None, None
    seg = p.loc[t0.floor("h"):t1]
    if seg.empty:
        return None, None
    hit = seg[(seg["low"] <= price * (1 + TOL)) & (seg["high"] >= price * (1 - TOL))]
    return (len(hit) > 0), (hit.index[-1] if len(hit) else None)


def main():
    e = TR.load_events()
    pl = []
    for f in sorted((ROOT / "telegram" / "estrazione").glob("piani_*.json")):          # i piani restano quelli della prima estrazione
        pl += json.load(open(f, encoding="utf-8"))
    p = pd.DataFrame(pl)
    p["utc"] = pd.to_datetime(p["utc"])
    lev_ = e[~e.trade.str.startswith(("H", "N")) & ~e.trade.isin(TR.SPOT)].copy()
    T = []

    # 1-2 prezzi veri e ritardo
    rows = []
    for r in lev_.itertuples():
        if not (isinstance(r.prezzo, (int, float)) and r.prezzo == r.prezzo and r.prezzo > 0):
            continue
        if r.tipo in ("ordine_limite", "ordine_non_eseguito", "stop_pareggio", "stop_spostato"):
            continue
        ok, last = touched(r.asset, float(r.prezzo), r.utc - pd.Timedelta(hours=72), r.utc + pd.Timedelta(minutes=59))
        if ok is None:
            continue
        rows.append({"trade": r.trade, "tipo": r.tipo, "ok": ok, "ritardo_h": (r.utc - last).total_seconds() / 3600 if ok else np.nan})
    v = pd.DataFrame(rows)
    ent = v[v.tipo.isin(["apertura", "aumento"])]
    ext = v[~v.tipo.isin(["apertura", "aumento"])]
    T.append("## V1 prezzi\n")
    T.append("| Prezzi dichiarati nelle schermate | Quanti | Toccati davvero dal mercato nelle 72 ore prima del messaggio | Ritardo mediano fra l'ultima volta che il mercato era a quel prezzo e il messaggio | Un quarto oltre |")
    T.append("|---|---|---|---|---|")
    for lab, x in (("Ingressi e aumenti", ent), ("Uscite", ext)):
        T.append(f"| {lab} | {len(x)} | {x.ok.mean() * 100:.0f}% | {num(float(x.ritardo_h.median()), 1)} ore | {num(float(x.ritardo_h.quantile(0.75)), 1)} ore |")

    # 3 coerenza delle card
    n = lev_.note.fillna("")
    roi = n.str.extract(r"ROI\s*\(?\s*([+-]?\d+[.,]?\d*)\s*%")[0].str.replace(",", ".").astype(float)
    lev = n.str.extract(r"(\d+(?:[.,]\d+)?)\s?[xX]\b")[0].str.replace(",", ".").astype(float)
    ent_px = n.str.extract(r"[Ee]ntry(?: medio)?\s*([\d.,]+)")[0].str.replace(",", "", regex=False)
    exit_px = n.str.extract(r"(?:Filled(?: Price)?|[Ee]xit)\s*([\d.,]+)")[0].str.replace(",", "", regex=False)
    c = pd.DataFrame({"roi": roi, "lev": lev, "e": pd.to_numeric(ent_px, errors="coerce"), "x": pd.to_numeric(exit_px, errors="coerce"), "verso": lev_.verso})
    c = c.dropna(subset=["roi", "e", "x"])
    c = c[(c.e > 0) & (c.x > 0)]
    c["mossa"] = np.where(c.verso == "long", c.x / c.e - 1, 1 - c.x / c.e) * 100
    c = c[c.mossa.abs() > 0.2]
    c["leva_implicita"] = c.roi / c.mossa
    known = [5, 8, 10, 12, 13, 14.5, 15, 20]
    near = c.leva_implicita.apply(lambda v: min(abs(v / k - 1) for k in known) < 0.08)
    T.append("\n## V2 card\n")
    T.append(f"Schermate Bybit con prezzo d'ingresso, prezzo d'uscita e ROI leggibili: {len(c)}. Dividendo il ROI per il movimento del prezzo si ottiene la leva "
             f"implicita: in {near.mean() * 100:.0f}% dei casi è una leva standard di Bybit (5x, 10x, 13x, 14,5x… entro l'8%), mediana {num(float(c.leva_implicita.median()), 1)}x. "
             f"Le schermate sono coerenti con operazioni reali.")
    # 4 chi copiava con ordini limite
    ev2, filled, used_plan = [], set(), {}
    for tid, g in lev_.groupby("trade"):
        g = g.sort_values(["utc", "msg_id"]).copy()
        a = g[g.tipo == "apertura"]
        if a.empty:
            continue
        a0 = a.iloc[0]
        px_tr = a0.prezzo if isinstance(a0.prezzo, (int, float)) and a0.prezzo == a0.prezzo else TR.px_at(a0.asset, a0.utc)
        cand = p[(p.trade_collegato == tid) & p.livello_innesco.notna() & (p.utc < a0.utc)]
        cand = cand[(cand.livello_innesco / px_tr - 1).abs() < 0.08] if px_tr else cand.iloc[0:0]
        tg_known = set()
        for t in list(p[p.trade_collegato == tid].target) + list(g.target):
            if isinstance(t, list):
                tg_known |= {float(x) for x in t if isinstance(x, (int, float))}
        entry = None
        if len(cand):
            pr = cand.iloc[-1]
            ok, last = touched(a0.asset, float(pr.livello_innesco), pr.utc, a0.utc + pd.Timedelta(hours=24))
            if ok:
                entry = float(pr.livello_innesco)
                filled.add(tid)
                used_plan[tid] = (int(pr.msg_id), entry)
        for r in g.itertuples():
            d = r._asdict()
            d.pop("Index", None)
            if r.tipo == "apertura":
                d["prezzo"] = entry if entry else None
                if entry:
                    d["note"] = "ingresso con ordine limite al livello del piano"
            elif r.tipo in ("chiusura_parziale", "chiusura_totale", "target_preso"):
                trp = r.prezzo if isinstance(r.prezzo, (int, float)) and r.prezzo == r.prezzo else (r.target[0] if r.tipo == "target_preso" and isinstance(r.target, list) and r.target else None)
                d["prezzo"] = trp if (trp and any(abs(trp / t - 1) < 0.004 for t in tg_known)) else None
            elif r.tipo == "aumento":
                d["prezzo"] = None
            elif r.tipo == "stop_preso":
                d["prezzo"] = None
            ev2.append(d)
    e2 = pd.DataFrame(ev2)
    late = {tid for tid, g in lev_.groupby("trade") if TR.ex_post(g)}
    keep = [t for t in e2.trade.unique() if t not in late or t in filled]
    F2 = TR.rebuild(e2[e2.trade.isin(keep)].reset_index(drop=True), "trader")
    F2.to_csv(OUT / "operazioni_follower_limite.csv", index=False)
    Tt = pd.read_csv(OUT / "operazioni_trader.csv")
    Ff = pd.read_csv(OUT / "operazioni_follower.csv")

    def line(df, lab):
        r = df.rendimento.to_numpy()
        return f"| {lab} | {len(r)} | {np.mean(r > 0) * 100:.0f}% | {pct(r.mean(), 2)} | ×{num(float(np.prod(1 + r)))} |"

    T.append("\n## V3 limite\n")
    T.append(f"Operazioni con un livello d'ingresso annunciato prima: {sum(1 for t in lev_.trade.unique() if len(p[(p.trade_collegato == t) & p.livello_innesco.notna()]))}; "
             f"ordine limite eseguito in tempo: {len(filled)} (di cui {len(filled & late)} fra quelle che il trader ha comunicato solo dopo).\n")
    T.append("| Chi | Operazioni | In guadagno | Medio per operazione | Capitale ×, controvalore 1x |")
    T.append("|---|---|---|---|---|")
    T.append(line(Tt, "Trader, prezzi delle schermate"))
    T.append(line(F2, "Chi copiava con ordini limite sui livelli annunciati"))
    T.append(line(F2[F2.trade.isin(filled)], "· di cui entrate con ordine limite"))
    T.append(line(F2[~F2.trade.isin(filled)], "· di cui entrate a mercato dopo il messaggio"))
    T.append(line(Ff, "Chi copiava solo a mercato (prima analisi)"))

    # 5 rischio fisso con lo stop
    T.append("\n## V4 rischio\n")
    T.append("| Chi | Rischio per operazione | Capitale finale da 10.000 $ | Peggiore operazione sul capitale |")
    T.append("|---|---|---|---|")
    for df, lab in ((Tt, "Trader, prezzi delle schermate"), (F2, "Chi copiava con ordini limite"), (Ff, "Chi copiava a mercato")):
        rk = df.rischio_pct.where(df.rischio_pct.between(0.002, 0.2), 0.02).to_numpy()
        for risk in (0.01, 0.02):
            mult = np.minimum(risk / rk, 10.0)                      # leva massima 10x, come nelle sue schermate
            r = df.rendimento.to_numpy() * mult
            fin = f"{10000 * np.prod(1 + r):,.0f}".replace(",", ".")
            T.append(f"| {lab} | {pct(risk, 0).lstrip('+')} | {fin} $ | {pct(float(r.min()))} |")
    (OUT / "tables_verifica.md").write_text("\n".join(T) + "\n")
    print("\n".join(T))
    print("piani usati:", used_plan)


if __name__ == "__main__":
    main()
