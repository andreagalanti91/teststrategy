"""Livelli di BTC (supporti, resistenze, liquidazioni) e verifica: cosa succede quando un supporto cede?

Supporto = minimo di swing settimanale (estremo delle 5 settimane prima e dopo, noto 5 settimane dopo), valido 3 anni e finche'
una chiusura giornaliera non lo rompe. Resistenza = massimo di swing, specchiato. Evento "rottura" = prima chiusura giornaliera
oltre il livello. Dati giornalieri Binance dal 2018; mappe di liquidazione stimate dal 12/2021 (results/liq/mappe_21g.csv)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import btc_ta as B

ROOT = B.ROOT
OUT = ROOT / "results" / "livelli"
OUT.mkdir(parents=True, exist_ok=True)
K, LIFE = 5, 365 * 3
pct = lambda x, d=1: "n/d" if x is None or not np.isfinite(x) else f"{x * 100:+.{d}f}%".replace(".", ",")
usd = lambda x: f"{x:,.0f}".replace(",", ".")
num = lambda x, d=2: f"{x:.{d}f}".replace(".", ",")

# livelli di liquidazione letti dalla schermata Coinglass del 24/11/2026 ore 09:01 (BTC, modello 3, 1 anno): prezzo, miliardi di $
COINGLASS = {"quando": "24/11/2026 09:01", "prezzo": 60388,
             "short": [(76915, 0.7208), (91076, 0.8396), (92742, 0.9299), (93853, 0.8866)],
             "long": [(54145, 0.7487), (53312, 0.7117), (51368, 1.18), (50535, 0.9971)]}


def swings(d: pd.DataFrame):
    """Lista di (data del punto, prezzo, data di conferma, tipo) dai massimi e minimi di swing settimanali."""
    w = B.weekly(d)
    hi, lo = w["high"].to_numpy(), w["low"].to_numpy()
    out = []
    for j in range(K, len(w) - K):
        conf = w.index[j + K] + pd.Timedelta(days=1)
        if lo[j] == lo[j - K:j + K + 1].min():
            out.append((w.index[j], float(lo[j]), conf, "supporto"))
        if hi[j] == hi[j - K:j + K + 1].max():
            out.append((w.index[j], float(hi[j]), conf, "resistenza"))
    return out


def events(d: pd.DataFrame, sw) -> pd.DataFrame:
    """Per ogni livello: primo tocco dopo la conferma (minimo entro l'1% sopra un supporto / massimo entro l'1% sotto una
    resistenza) e prima rottura in chiusura."""
    C, H, L = d["close"], d["high"], d["low"]
    rows = []
    for t0, lvl, conf, kind in sw:
        seg = d.loc[conf:conf + pd.Timedelta(days=LIFE)]
        if len(seg) < 2:
            continue
        sgn = -1 if kind == "supporto" else 1
        beyond = (seg["close"] < lvl) if kind == "supporto" else (seg["close"] > lvl)
        if beyond.iloc[0]:
            continue                                            # gia' oltre il livello alla conferma
        touch = (seg["low"] <= lvl * 1.01) if kind == "supporto" else (seg["high"] >= lvl * 0.99)
        tt = touch[touch].index[0] if touch.any() else pd.NaT
        tb = beyond[beyond].index[0] if beyond.any() else pd.NaT
        rows.append({"tipo": kind, "livello": lvl, "formato": t0, "confermato": conf, "tocco": tt, "rottura": tb})
    return pd.DataFrame(rows)


def main():
    B.END = "2026-12-31"                      # qui servono i prezzi piu' recenti, non il taglio usato nei backtest
    d = B.load()
    C, H, L = d["close"], d["high"], d["low"]
    sw = swings(d)
    ev = events(d, sw)
    ev = ev[ev.confermato >= "2018-01-01"]
    T = []

    def fwd(t, n):
        i = d.index.get_loc(t)
        return float(C.iloc[i + n] / C.iloc[i] - 1) if i + n < len(d) else np.nan

    def ext(t, n, kind):
        i = d.index.get_loc(t)
        seg = d.iloc[i + 1:i + 1 + n]
        if len(seg) < n:
            return np.nan
        return float(seg["low"].min() / C.iloc[i] - 1) if kind == "supporto" else float(seg["high"].max() / C.iloc[i] - 1)

    # ---------------- 1: i livelli tengono?
    T.append("## V1 tengono\n")
    T.append("| Livello | Quanti (dal 2018) | Toccati entro 3 anni | Di quelli toccati: rotti in chiusura entro 10 giorni dal primo tocco | Rotti prima o poi | Mai rotti |")
    T.append("|---|---|---|---|---|---|")
    for kind in ("supporto", "resistenza"):
        x = ev[ev.tipo == kind]
        t = x[x.tocco.notna()]
        quick = ((t.rottura - t.tocco).dt.days <= 10) & t.rottura.notna()
        T.append(f"| {kind.capitalize()} | {len(x)} | {len(t)} ({len(t) / len(x) * 100:.0f}%) | {int(quick.sum())} su {len(t)} ({quick.mean() * 100:.0f}%) | "
                 f"{x.rottura.notna().sum()} ({x.rottura.notna().mean() * 100:.0f}%) | {x.rottura.isna().sum()} |")

    # ---------------- 2: dopo la rottura il movimento accelera?
    br = ev[ev.rottura.notna()].copy()
    br = br.sort_values("rottura").drop_duplicates(["tipo", "rottura"])          # piu' livelli rotti nello stesso giorno = un evento
    for n in (1, 3, 7, 14, 30):
        br[f"f{n}"] = [fwd(t, n) for t in br.rottura]
    br["ext14"] = [ext(t, 14, k) for t, k in zip(br.rottura, br.tipo)]
    br["giorno"] = [float(C.loc[t] / C.shift(1).loc[t] - 1) for t in br.rottura]
    br["rientro5"] = [bool(((C.iloc[d.index.get_loc(t) + 1:d.index.get_loc(t) + 6] > lv) if k == "supporto" else (C.iloc[d.index.get_loc(t) + 1:d.index.get_loc(t) + 6] < lv)).any())
                      for t, lv, k in zip(br.rottura, br.livello, br.tipo)]
    br.to_csv(OUT / "rotture.csv", index=False)
    r1 = C.pct_change()
    allf = {n: C.shift(-n) / C - 1 for n in (1, 3, 7, 14, 30)}
    allf = {n: v.loc["2018-01-01":] for n, v in allf.items()}
    T.append("\n## V2 dopo\n")
    T.append("| Evento | Casi | Variazione nel giorno della rottura | Dopo 3 giorni | Dopo 7 giorni | Dopo 14 giorni | Dopo 30 giorni | Prosegue a 7 giorni (stesso verso) | Rientra oltre il livello entro 5 giorni | Massimo movimento ulteriore in 14 giorni (mediana) |")
    T.append("|---|---|---|---|---|---|---|---|---|---|")
    for kind, lab in (("supporto", "Rottura di un supporto"), ("resistenza", "Rottura di una resistenza")):
        x = br[br.tipo == kind]
        same = (x.f7 < 0) if kind == "supporto" else (x.f7 > 0)
        T.append(f"| {lab} | {len(x)} | {pct(x.giorno.mean())} | {pct(x.f3.mean())} | {pct(x.f7.mean())} | {pct(x.f14.mean())} | {pct(x.f30.mean())} | {same.mean() * 100:.0f}% | "
                 f"{x.rientro5.mean() * 100:.0f}% | {pct(x.ext14.median())} |")
    # riferimenti: giorni di calo/rialzo simile che NON sono rotture
    bdays = set(br.rottura)
    for kind, lab, m in (("supporto", "Riferimento: giorni con un calo simile (oltre −4%) senza rottura", (r1 <= -0.04)), ("resistenza", "Riferimento: giorni con un rialzo simile (oltre +4%) senza rottura", (r1 >= 0.04))):
        m = m & ~m.index.isin(bdays) & (m.index >= "2018-01-01")
        idx = m[m].index
        e14 = pd.Series([ext(t, 14, kind) for t in idx])
        same = (allf[7].reindex(idx) < 0) if kind == "supporto" else (allf[7].reindex(idx) > 0)
        T.append(f"| {lab} | {len(idx)} | {pct(r1.reindex(idx).mean())} | {pct(allf[3].reindex(idx).mean())} | {pct(allf[7].reindex(idx).mean())} | {pct(allf[14].reindex(idx).mean())} | "
                 f"{pct(allf[30].reindex(idx).mean())} | {same.mean() * 100:.0f}% | – | {pct(e14.median())} |")
    T.append(f"| Riferimento: tutti i giorni dal 2018 | {len(allf[7].dropna())} | {pct(r1.loc['2018-01-01':].mean(), 2)} | {pct(allf[3].mean())} | {pct(allf[7].mean())} | {pct(allf[14].mean())} | {pct(allf[30].mean())} | – | – | – |")

    # per regime e per periodo
    T.append("\n## V3 regime\n")
    s200 = B.sma(C, 200)
    T.append("| Rottura di un supporto | Casi | Dopo 7 giorni | Dopo 14 giorni | Dopo 30 giorni | Prosegue al ribasso a 7 giorni | Ulteriore calo massimo in 14 giorni (mediana) |")
    T.append("|---|---|---|---|---|---|---|")
    x = br[br.tipo == "supporto"]
    below = pd.Series([bool(C.loc[t] < s200.loc[t]) for t in x.rottura], index=x.index)
    for lab, m in (("Con prezzo sotto la SMA 200 (come oggi)", below), ("Con prezzo sopra la SMA 200", ~below), ("2018–2021", x.rottura < "2022-01-01"), ("2022–2026", x.rottura >= "2022-01-01")):
        y = x[m]
        T.append(f"| {lab} | {len(y)} | {pct(y.f7.mean())} | {pct(y.f14.mean())} | {pct(y.f30.mean())} | {(y.f7 < 0).mean() * 100:.0f}% | {pct(y.ext14.median())} |")

    # ---------------- 3: con le liquidazioni sotto?
    T.append("\n## V4 liquidazioni\n")
    mp = pd.read_csv(ROOT / "results" / "liq" / "mappe_21g.csv", index_col=0, parse_dates=True)
    y = x[x.rottura >= mp.index[0]].copy()
    y["long15"] = [mp["long15"].reindex([t + pd.Timedelta(days=1)]).iloc[0] if t + pd.Timedelta(days=1) in mp.index else np.nan for t in y.rottura]   # mappa delle 00:00 dopo la chiusura
    y["dn_dist"] = [mp["dn_dist"].reindex([t + pd.Timedelta(days=1)]).iloc[0] if t + pd.Timedelta(days=1) in mp.index else np.nan for t in y.rottura]
    y = y.dropna(subset=["long15"])
    med = mp["long15"].median()
    T.append(f"Rotture di supporto dal {mp.index[0].date()} con mappa disponibile: {len(y)}. \"Molte liquidazioni sotto\" = long stimati entro il 15% sotto il prezzo sopra la mediana storica ({usd(med / 1e6)} M$).\n")
    T.append("| Alla rottura | Casi | Dopo 3 giorni | Dopo 7 giorni | Dopo 14 giorni | Prosegue al ribasso a 7 giorni | Ulteriore calo massimo in 14 giorni (mediana) |")
    T.append("|---|---|---|---|---|---|---|")
    for lab, m in (("Molte liquidazioni di long sotto", y.long15 > med), ("Poche liquidazioni di long sotto", y.long15 <= med),
                   ("Fascia grande di long entro il 5% sotto", y.dn_dist <= 0.05), ("Nessuna fascia grande entro il 5%", ~(y.dn_dist <= 0.05))):
        z = y[m]
        T.append(f"| {lab} | {len(z)} | {pct(z.f3.mean())} | {pct(z.f7.mean())} | {pct(z.f14.mean())} | {(z.f7 < 0).mean() * 100:.0f}% | {pct(z.ext14.median())} |" if len(z) else f"| {lab} | 0 | – | – | – | – | – |")

    # ---------------- 4: livelli di oggi
    px, last = float(C.iloc[-1]), d.index[-1]
    act = ev[(ev.rottura.isna()) & (ev.confermato + pd.Timedelta(days=LIFE) >= last)]
    wk = B.weekly(d)
    lv = [{"prezzo": r.livello, "tipo": r.tipo, "cosa": f"{'minimo' if r.tipo == 'supporto' else 'massimo'} di swing settimanale del {r.formato.strftime('%m/%Y')}", "fonte": "prezzo"} for r in act.itertuples()]
    # minimi/massimi recenti non ancora confermati (ultime 5 settimane)
    rec = d.iloc[-35:]
    lv.append({"prezzo": float(rec["low"].min()), "tipo": "supporto", "cosa": f"minimo delle ultime 5 settimane ({rec['low'].idxmin().strftime('%d/%m')}), non ancora confermato", "fonte": "prezzo"})
    ath, lo_c = float(d["high"].max()), float(d.loc["2022-06-01":"2023-03-01", "low"].min())
    for f_, nm in ((0.5, "50%"), (0.618, "61,8%"), (0.786, "78,6%")):
        lv.append({"prezzo": ath - f_ * (ath - lo_c), "tipo": "fibonacci", "cosa": f"ritracciamento di Fibonacci {nm} del ciclo 2022–2025", "fonte": "prezzo"})
    for nm, v in (("SMA 200 settimane", B.sma(wk["close"], 200).iloc[-1]), ("SMA 40 settimane", B.sma(wk["close"], 40).iloc[-1]), ("SMA 200 giorni", B.sma(C, 200).iloc[-1]), ("SMA 50 giorni", B.sma(C, 50).iloc[-1])):
        lv.append({"prezzo": float(v), "tipo": "media", "cosa": nm, "fonte": "prezzo"})
    lv.append({"prezzo": float(d.loc[:"2022-01-01", "high"].max()), "tipo": "resistenza", "cosa": "massimo del ciclo 2021", "fonte": "prezzo"})
    for p, b in COINGLASS["long"]:
        lv.append({"prezzo": p, "tipo": "liq_long", "cosa": f"liquidazioni di long stimate: {num(b)} miliardi $", "fonte": "Coinglass " + COINGLASS["quando"], "usd": b})
    for p, b in COINGLASS["short"]:
        lv.append({"prezzo": p, "tipo": "liq_short", "cosa": f"liquidazioni di short stimate: {num(b)} miliardi $", "fonte": "Coinglass " + COINGLASS["quando"], "usd": b})
    lv = [x_ for x_ in lv if px * 0.6 <= x_["prezzo"] <= px * 1.6]
    for x_ in lv:
        x_["ruolo"] = "sopra" if x_["prezzo"] > px else "sotto"
        x_["dist"] = x_["prezzo"] / px - 1
    lv.sort(key=lambda x_: -x_["prezzo"])
    # zone: livelli entro il 3% l'uno dall'altro, con almeno 3 elementi
    zones, cur = [], []                       # zona = livelli consecutivi a meno del 3,2% l'uno dall'altro, almeno due
    for x_ in sorted(lv, key=lambda q: q["prezzo"]):
        if cur and x_["prezzo"] / cur[-1]["prezzo"] - 1 > 0.032:
            if len(cur) >= 2:
                zones.append(cur)
            cur = []
        cur.append(x_)
    if len(cur) >= 2:
        zones.append(cur)
    zl = [{"da": z[0]["prezzo"], "a": z[-1]["prezzo"], "n": len(z), "ruolo": "sopra" if z[0]["prezzo"] > px else "sotto" if z[-1]["prezzo"] < px else "a cavallo",
           "tipi": sorted({q["tipo"] for q in z}), "liq": round(sum(q.get("usd", 0) for q in z), 2)} for z in zones]
    atr = float(B.atr(d).iloc[-1])
    oggi = {"data": str(last.date()), "prezzo": px, "atr": atr, "livelli": lv, "zone": zl, "coinglass": COINGLASS["quando"],
            "candele": [{"d": str(t.date()), "o": round(r.open), "h": round(r.high), "l": round(r.low), "c": round(r.close)} for t, r in d.iloc[-420:].iterrows()]}
    (OUT / "oggi.json").write_text(json.dumps(oggi, ensure_ascii=False))

    T.append("\n## V5 scala\n")
    T.append(f"Prezzo di riferimento: {usd(px)} $ (chiusura del {last.strftime('%d/%m/%Y')}). ATR giornaliero: {usd(atr)} $ ({num(atr / px * 100, 1)}%).\n")
    T.append("| Livello | Distanza | Tipo | Che cos'è | Fonte |")
    T.append("|---|---|---|---|---|")
    NAME = {"supporto": "supporto", "resistenza": "resistenza", "fibonacci": "Fibonacci", "media": "media mobile", "liq_long": "liquidazioni long", "liq_short": "liquidazioni short"}
    done = False
    for x_ in lv:
        if not done and x_["prezzo"] < px:
            T.append(f"| **{usd(px)} $** | – | **prezzo** | – | – |")
            done = True
        T.append(f"| {usd(x_['prezzo'])} $ | {pct(x_['dist'], 0)} | {NAME[x_['tipo']]} | {x_['cosa']} | {x_['fonte']} |")
    T.append("\n## V6 zone\n")
    T.append("| Zona | Distanza dal prezzo | Livelli che coincidono | Di che tipo | Liquidazioni stimate nella zona |")
    T.append("|---|---|---|---|---|")
    for z in sorted(zl, key=lambda q: -q["a"]):
        T.append(f"| {usd(z['da'])}–{usd(z['a'])} $ | {pct(z['a'] / px - 1, 0)} / {pct(z['da'] / px - 1, 0)} | {z['n']} | {', '.join(NAME[t] for t in z['tipi'])} | {num(z['liq']) + ' miliardi $' if z['liq'] else '–'} |")
    (OUT / "tables.md").write_text("\n".join(T) + "\n")
    print("\n".join(T))


if __name__ == "__main__":
    main()
