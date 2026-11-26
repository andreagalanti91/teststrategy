"""Tabelle del rapporto sul canale Telegram: operazioni ricostruite (prezzi del trader e di chi copiava), gruppi, setup, confronto."""
from __future__ import annotations

import glob
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "results" / "telegram"
pct = lambda x, d=1: "n/d" if x is None or not np.isfinite(x) else f"{x * 100:+.{d}f}%".replace(".", ",")
num = lambda x, d=2: "n/d" if x is None or not np.isfinite(x) else f"{x:.{d}f}".replace(".", ",")
A0, A1 = pd.Timestamp("2023-05-12 16:00"), pd.Timestamp("2024-03-18 11:00")


def row(t: pd.DataFrame, lab: str) -> str:
    r = t.rendimento.to_numpy()
    if not len(r):
        return f"| {lab} | 0 | – | – | – | – | – |"
    return (f"| {lab} | {len(r)} | {np.mean(r > 0) * 100:.0f}% | {pct(r.mean(), 2)} | {pct(float(np.median(r)), 2)} | ×{num(float(np.prod(1 + r)))} | "
            f"×{num(float(np.prod(1 + 3 * r)))} |")


def main():
    ev, pl = [], []
    for f in sorted(glob.glob(str(ROOT / "telegram" / "estrazione" / "eventi_*.json"))):
        ev += json.load(open(f, encoding="utf-8"))
    for f in sorted(glob.glob(str(ROOT / "telegram" / "estrazione" / "piani_*.json"))):
        pl += json.load(open(f, encoding="utf-8"))
    e, p = pd.DataFrame(ev), pd.DataFrame(pl)
    Tt = pd.read_csv(OUT / "operazioni_trader.csv", parse_dates=["apertura", "chiusura"])
    Ff = pd.read_csv(OUT / "operazioni_follower.csv", parse_dates=["apertura", "chiusura"])
    T = []
    head = "| Gruppo | Operazioni | In guadagno | Medio per operazione | Mediana | Capitale ×, controvalore 1x | Capitale ×, controvalore 3x |\n|---|---|---|---|---|---|---|"

    T.append("## T1 quadro\n")
    lev = e.note.fillna("").str.extract(r"(\d+(?:[.,]\d+)?)\s?[xX]\b")[0].dropna().str.replace(",", ".").astype(float)
    nh = e[e.trade.str.startswith("H") | e.trade.isin(["C00a", "C00b", "C04", "C09"])].trade.nunique()
    T.append("| Voce | Valore |\n|---|---|")
    T.append(f"| Messaggi letti | 812 (11/05/2023 – 18/03/2024), 458 con grafico o schermata |")
    T.append(f"| Operazioni a leva ricostruite | {len(Tt)} ({(Tt.asset == 'BTC').sum()} su BTC, {(Tt.asset != 'BTC').sum()} su altcoin; {(Tt.verso == 'long').sum()} long, {(Tt.verso == 'short').sum()} short) |")
    T.append(f"| Comunicate solo dopo l'ingresso | {int(Tt.comunicata_dopo.sum())} su {len(Tt)}: chi legge il canale non poteva copiarle |")
    T.append(f"| Accumuli spot tenuti a parte | {nh} (TAO, RNDR, INJ, PYR, 0x0, PAAL, ORAI, ARC, BAI, ETH spot) |")
    T.append(f"| Piani annunciati prima che il prezzo arrivasse | {len(p)}: {int((p.eseguito.astype(str) == 'True').sum())} eseguiti, {int((p.eseguito.astype(str) == 'False').sum())} no, "
             f"{int((p.eseguito.astype(str) == 'non chiaro').sum())} senza esito dichiarato |")
    T.append(f"| Leva nelle schermate Bybit | da {num(lev.min(), 1)}x a {num(lev.max(), 1)}x, mediana {num(lev.median(), 0)}x |")
    T.append(f"| Durata mediana di un'operazione | {num(float(Tt.giorni.median()) * 24, 0)} ore |")

    T.append("\n## T2 risultati\n")
    T.append("Rendimento sul controvalore di ogni operazione (movimento del prezzo pesato per le quote aperte e chiuse), al netto di 0,16% di costi "
             "andata e ritorno. Le colonne con il simbolo × compongono le operazioni in sequenza con controvalore pari a 1 o 3 volte il capitale.\n")
    T.append(head)
    T.append(row(Tt, "Prezzi dichiarati dal trader, tutte"))
    T.append(row(Tt[~Tt.comunicata_dopo], "Prezzi del trader, solo annunciate in tempo"))
    T.append(row(Tt[Tt.comunicata_dopo], "Prezzi del trader, comunicate dopo"))
    T.append(row(Ff, "Chi copiava in tempo reale"))
    m = Tt.merge(Ff[["trade", "rendimento"]], on="trade", suffixes=("_t", "_f"))
    T.append(f"\nSulle {len(m)} operazioni copiabili, il prezzo del trader è stato migliore di quello disponibile a chi leggeva il messaggio di "
             f"{num(float((m.rendimento_t - m.rendimento_f).mean() * 100))} punti per operazione in media.")

    T.append("\n## T3 gruppi\n")
    T.append(head.replace("Gruppo", "Gruppo (trader → chi copiava)"))
    for lab, ft, ff in (("BTC", Tt.asset == "BTC", Ff.asset == "BTC"), ("Altcoin", Tt.asset != "BTC", Ff.asset != "BTC"),
                        ("Long", Tt.verso == "long", Ff.verso == "long"), ("Short", Tt.verso == "short", Ff.verso == "short")):
        T.append(row(Tt[ft], f"{lab} · trader"))
        T.append(row(Ff[ff], f"{lab} · chi copiava"))
    for lab, a, b in (("Mag–ago 2023", "2023-05", "2023-09"), ("Set–dic 2023", "2023-09", "2023-12-16"), ("Dic 2023–mar 2024", "2023-12-16", "2024-04")):
        T.append(row(Tt[(Tt.apertura >= a) & (Tt.apertura < b)], f"{lab} · trader"))
        T.append(row(Ff[(Ff.apertura >= a) & (Ff.apertura < b)], f"{lab} · chi copiava"))

    T.append("\n## T4 setup\n")
    txt = {}
    for tid, g in e.groupby("trade"):
        s = " ".join((g.testo.fillna("") + " " + g.note.fillna("")).tolist())
        s += " " + " ".join((p[p.trade_collegato == tid].innesco.fillna("") + " " + p[p.trade_collegato == tid].testo.fillna("")).tolist())
        txt[tid] = s.lower()
    K = {"Rottura di supporto/resistenza diagonale e retest": r"diagonal|trendline|cuneo|wedge", "Retest o riconquista di un livello orizzontale": r"retest|reclaim|riconquist",
         "Presa di liquidità / falsa rottura": r"liquidity|liquid|fake ?out|falso|swing failure|deviaz|sfp|stop hunt", "Media a 200 (EMA o MA)": r"ema ?200|ma ?200|media mobile",
         "Divergenza RSI": r"divergen", "Range (massimo/minimo)": r"\brange\b", "Gap del future CME": r"gap|cme", "Figure (testa-spalle, doppio massimo)": r"testa|spalle|doppio|double",
         "Notizie macro (CPI, FOMC, ETF, SEC)": r"cpi|fomc|etf|powell|sec\b|notizi", "Alt long finché BTC regge": r"dominance|btc\.d|finch[eé] btc|se btc"}
    T.append("| Setup citato | Operazioni | In guadagno (trader) | Medio, prezzi del trader | Operazioni copiabili | Medio, chi copiava |\n|---|---|---|---|---|---|")
    for k, rx in K.items():
        ids = [t for t, s in txt.items() if re.search(rx, s)]
        a, b = Tt[Tt.trade.isin(ids)], Ff[Ff.trade.isin(ids)]
        T.append(f"| {k} | {len(a)} | {(a.rendimento > 0).mean() * 100:.0f}% | {pct(a.rendimento.mean(), 2)} | {len(b)} | {pct(b.rendimento.mean(), 2) if len(b) else '–'} |")
    T.append("\nUn'operazione può citare più setup. Classificazione per parole chiave nei messaggi e nei piani collegati.")

    T.append("\n## T5 elenco\n")
    T.append("| # | Asset | Verso | Apertura (UTC) | Ore | Prezzo medio del trader | Trader | Chi copiava | Note |\n|---|---|---|---|---|---|---|---|---|")
    fm = Ff.set_index("trade").rendimento
    for r in Tt.itertuples():
        note = ("comunicata dopo; " if r.comunicata_dopo else "") + (str(r.note).split(":")[0] if isinstance(r.note, str) and r.note else "")
        pm = f"{r.prezzo_medio:,.0f}".replace(",", ".") if r.prezzo_medio >= 100 else f"{r.prezzo_medio:.4g}".replace(".", ",")
        T.append(f"| {r.trade} | {r.asset} | {r.verso} | {r.apertura:%d/%m/%y %H:%M} | {r.giorni * 24:.0f} | {pm} | {pct(r.rendimento)} | "
                 f"{pct(fm.get(r.trade)) if r.trade in fm.index else '–'} | {note.strip('; ')} |")

    T.append("\n## T6 riferimenti\n")
    w = pd.read_csv(ROOT / "results" / "w32" / "equity.csv", index_col=0, parse_dates=True)
    T.append("| Nello stesso periodo (12/05/2023 – 18/03/2024) | Capitale × | Max DD |\n|---|---|---|")
    for c, nm in (("BTC comprato e tenuto", "BTC comprato e tenuto"), ("W3.2 radar (rischio 25%)", "W3.2 del radar"), ("v1 · voto di 17 indicatori", "v1 · voto di 17 indicatori")):
        x = w[c].loc[A0.normalize():A1.normalize()]
        T.append(f"| {nm} | ×{num(float(w[c].asof(A1) / w[c].asof(A0)))} | {pct(float((x / x.cummax() - 1).min()))} |")
    (OUT / "tables.md").write_text("\n".join(T) + "\n")
    print("\n".join(T))


if __name__ == "__main__":
    main()
