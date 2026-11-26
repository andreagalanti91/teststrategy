"""Rapporto operazione per operazione sul canale di Aldo (12/05/2023 – 18/03/2024) ed esempio con 10.000 € di capitale.

Per ogni operazione: rendimento sul controvalore (movimento del prezzo pesato per le quote, dopo i costi) con i prezzi del trader,
per chi copiava con ordini limite sui livelli annunciati e per chi copiava a mercato dopo il messaggio.
Esempio: capitale 10.000 €, margine fisso per operazione (500 € o 1.000 €) con leva 5x o 10x (quella tipica di Aldo):
guadagno o perdita = margine × leva × rendimento. Margine fisso: niente interesse composto.
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "results" / "telegram"
OUT = D
pct = lambda x, d=1: "–" if x is None or not np.isfinite(x) else f"{x * 100:+.{d}f}%".replace(".", ",")
eur = lambda x: "–" if x is None or not np.isfinite(x) else (("+" if x > 0 else "−" if x < 0 else "") + f"{abs(x):,.0f} €".replace(",", "."))
eur0 = lambda x: f"{x:,.0f} €".replace(",", ".")


def main():
    t = pd.read_csv(D / "operazioni_trader.csv", parse_dates=["apertura", "chiusura"])
    lim = pd.read_csv(D / "operazioni_follower_limite.csv").set_index("trade")
    mer = pd.read_csv(D / "operazioni_follower.csv").set_index("trade")
    T = []
    T.append("## O1 elenco\n")
    T.append("Rendimento sul controvalore, dopo i costi. Con leva 10x l'effetto sul margine è dieci volte tanto (colonna «Sul margine a 10x»).\n")
    T.append("| # | Asset | Verso | Apertura | Durata | Trader | Esito | Sul margine a 10x | Copia con ordini limite | Copia a mercato | Note |")
    T.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(t.itertuples(), 1):
        h = r.giorni * 24
        dur = f"{h:.0f} ore" if h < 48 else f"{r.giorni:.0f} giorni"
        l = lim.rendimento.get(r.trade, np.nan)
        m = mer.rendimento.get(r.trade, np.nan)
        note = []
        if r.comunicata_dopo:
            note.append("comunicata dopo l'ingresso")
        if isinstance(r.note, str) and "residuo" in r.note:
            note.append("residuo chiuso dalla ricostruzione")
        if isinstance(lim.note.get(r.trade, ""), str) and "limite" in str(lim.note.get(r.trade, "")):
            note.append("copiabile con limite")
        T.append(f"| {i} | {r.asset} | {r.verso} | {r.apertura:%d/%m/%y} | {dur} | {pct(r.rendimento, 2)} | {'✅' if r.rendimento > 0 else '❌'} | {pct(10 * r.rendimento)} | "
                 f"{pct(l, 2) if np.isfinite(l) else 'non copiabile'} | {pct(m, 2) if np.isfinite(m) else 'non copiabile'} | {'; '.join(note)} |")

    T.append("\n## O2 sintesi\n")
    T.append("| Chi | Operazioni | Vinte | Perse | % vinte | Guadagno medio delle vinte | Perdita media delle perse | Migliore | Peggiore |")
    T.append("|---|---|---|---|---|---|---|---|---|")
    for nm, r in (("Aldo, prezzi suoi", t.rendimento), ("Copia con ordini limite", lim.rendimento), ("Copia a mercato", mer.rendimento)):
        w, l = r[r > 0], r[r <= 0]
        T.append(f"| {nm} | {len(r)} | {len(w)} | {len(l)} | {len(w) / len(r) * 100:.0f}% | {pct(w.mean(), 2)} | {pct(l.mean(), 2)} | {pct(r.max(), 1)} | {pct(r.min(), 1)} |")
    T.append("\nPercentuali sul controvalore (movimento del prezzo). Sul margine vanno moltiplicate per la leva.")

    T.append("\n## O3 esempio\n")
    T.append("Capitale iniziale 10.000 €, un margine fisso per operazione, tutte le operazioni in sequenza (12/05/2023 – 18/03/2024).\n")
    T.append("| Chi copia | Margine per operazione | Leva | Capitale finale | Guadagno | Operazione migliore | Operazione peggiore | Peggior calo del capitale | Operazioni |")
    T.append("|---|---|---|---|---|---|---|---|---|")
    rows = []
    for nm, df in (("Aldo, prezzi suoi (riferimento)", t.set_index("trade")), ("Copia con ordini limite", lim), ("Copia a mercato", mer)):
        d = df.sort_values("chiusura") if "chiusura" in df else df
        for marg in (500, 1000):
            for lev in (5, 10):
                pnl = marg * lev * d.rendimento.to_numpy()
                eq = 10000 + np.cumsum(pnl)
                peak = np.maximum.accumulate(np.concatenate([[10000], eq]))[1:]
                dd = float(((eq - peak) / peak).min())
                rows.append((nm, marg, lev, eq[-1]))
                T.append(f"| {nm} | {eur0(marg)} | {lev}x | {eur0(eq[-1])} | {pct(eq[-1] / 10000 - 1, 0)} | {eur(pnl.max())} | {eur(pnl.min())} | {pct(dd)} | {len(pnl)} |")
    T.append("\nIl calo del capitale è misurato alla chiusura delle operazioni: dentro un'operazione la perdita latente può essere maggiore.")

    T.append("\n## O4 euro\n")
    T.append("Lo stesso esempio, operazione per operazione: margine 1.000 €, leva 5x, guadagno o perdita in euro.\n")
    T.append("| # | Asset | Verso | Apertura | Aldo | Copia con ordini limite | Copia a mercato |")
    T.append("|---|---|---|---|---|---|---|")
    tot = [0.0, 0.0, 0.0]
    for i, r in enumerate(t.itertuples(), 1):
        a = 5000 * r.rendimento
        l = 5000 * lim.rendimento.get(r.trade, np.nan)
        m = 5000 * mer.rendimento.get(r.trade, np.nan)
        for k, v in enumerate((a, l, m)):
            tot[k] += 0 if not np.isfinite(v) else v
        T.append(f"| {i} | {r.asset} | {r.verso} | {r.apertura:%d/%m/%y} | {eur(a)} | {eur(l) if np.isfinite(l) else '–'} | {eur(m) if np.isfinite(m) else '–'} |")
    T.append(f"| | | | **Totale** | **{eur(tot[0])}** | **{eur(tot[1])}** | **{eur(tot[2])}** |")
    (OUT / "tables_operazioni.md").write_text("\n".join(T) + "\n")
    print("\n".join(T))


if __name__ == "__main__":
    main()
