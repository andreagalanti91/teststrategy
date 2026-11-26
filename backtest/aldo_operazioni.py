"""Rapporto operazione per operazione sul canale di Aldo (12/05/2023 – 18/03/2024) ed esempio con 10.000 € di capitale.

Per ogni operazione: rendimento sul controvalore (movimento del prezzo pesato per le quote, dopo i costi) con i prezzi del trader,
per chi copiava con ordini limite sui livelli annunciati e per chi copiava a mercato dopo il messaggio.
Esempio: capitale 10.000 €, margine fisso per operazione (500 € o 1.000 €) con leva 5x o 10x (quella tipica di Aldo):
guadagno o perdita = margine × leva × rendimento. Margine fisso: niente interesse composto.
"""
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REV = os.environ.get("TELEGRAM_REVISIONE") == "1"            # 1 = operazioni ricostruite dagli eventi rivisti
D = ROOT / "results" / ("telegram_rev" if REV else "telegram")
OLD = ROOT / "results" / "telegram"
OUT = D
RANK = {"alta": 0, "media": 1, "bassa": 2}
pct = lambda x, d=1: "–" if x is None or not np.isfinite(x) else f"{x * 100:+.{d}f}%".replace(".", ",")
eur = lambda x: "–" if x is None or not np.isfinite(x) else (("+" if x > 0 else "−" if x < 0 else "") + f"{abs(x):,.0f} €".replace(",", "."))
eur0 = lambda x: f"{x:,.0f} €".replace(",", ".")


def fonte_cat(x: str) -> str:
    x = str(x).lower()
    if x.startswith(("card", "screenshot")):
        return "schermata"
    if "grafico" in x or "marker" in x:
        return "grafico"
    if x.startswith("testo"):
        return "testo"
    if x.startswith("dedott"):
        return "dedotto"
    return "dati di mercato" if "binance" in x or "dati" in x else "altro"


def eventi_rivisti() -> pd.DataFrame:
    ev = []
    for p in "ABC":
        f = ROOT / "telegram" / "revisione" / f"eventi_{p}_rev.json"
        if f.exists():
            ev += json.load(open(f, encoding="utf-8"))
    return pd.DataFrame(ev)


def affidabilita(ev: pd.DataFrame) -> dict:
    out = {}
    for tid, g in ev.groupby("trade"):
        g = g[g.tipo.isin(["apertura", "aumento", "chiusura_parziale", "chiusura_totale", "stop_preso", "target_preso"])]
        r = [RANK.get(str(a), 1) for a in g.affidabilita]
        out[tid] = ["alta", "media", "bassa"][max(r)] if r else "–"
    return out


def main():
    t = pd.read_csv(D / "operazioni_trader.csv", parse_dates=["apertura", "chiusura"])
    ev = eventi_rivisti() if REV else pd.DataFrame()
    aff = affidabilita(ev) if REV else {}
    old = pd.read_csv(OLD / "operazioni_trader.csv").set_index("trade").rendimento if REV else pd.Series(dtype=float)
    lim = pd.read_csv(D / "operazioni_follower_limite.csv").set_index("trade")
    mer = pd.read_csv(D / "operazioni_follower.csv").set_index("trade")
    T = []
    T.append("## O1 elenco\n")
    T.append("Rendimento sul controvalore, dopo i costi. Con leva 10x l'effetto sul margine è dieci volte tanto (colonna «Sul margine a 10x»).\n")
    if REV:
        T.append("| # | Operazione | Asset | Verso | Apertura | Durata | Aldo | Esito | Sul margine a 10x | Prima stima | Affidabilità | Copia con ordini limite | Copia a mercato | Note |")
        T.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    else:
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
        if isinstance(r.note, str) and "aperta a fine" in r.note:
            note.append("ancora aperta il 18/03/24")
        lc = pct(l, 2) if np.isfinite(l) else "non copiabile"
        mc = pct(m, 2) if np.isfinite(m) else "non copiabile"
        if REV:
            o = old.get(r.trade, np.nan)
            T.append(f"| {i} | {r.trade} | {r.asset} | {r.verso} | {r.apertura:%d/%m/%y} | {dur} | {pct(r.rendimento, 2)} | {'✅' if r.rendimento > 0 else '❌'} | {pct(10 * r.rendimento)} | "
                     f"{pct(o, 2) if np.isfinite(o) else 'nuova'} | {aff.get(r.trade, '–')} | {lc} | {mc} | {'; '.join(note)} |")
        else:
            T.append(f"| {i} | {r.asset} | {r.verso} | {r.apertura:%d/%m/%y} | {dur} | {pct(r.rendimento, 2)} | {'✅' if r.rendimento > 0 else '❌'} | {pct(10 * r.rendimento)} | "
                     f"{lc} | {mc} | {'; '.join(note)} |")

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
    if REV:
        T += revisione(t, ev, aff, old)
    (OUT / "tables_operazioni.md").write_text("\n".join(T) + "\n")
    print("\n".join(T))


TIPO = {"apertura": "apertura", "aumento": "aumento", "chiusura_parziale": "chiusura parziale", "chiusura_totale": "chiusura",
        "stop_preso": "stop colpito", "target_preso": "obiettivo preso", "stop_pareggio": "stop a pareggio", "stop_spostato": "stop spostato",
        "ordine_limite": "ordine limite", "ordine_non_eseguito": "ordine non eseguito"}


def revisione(t, ev, aff, old):
    T = ["\n## R1 cambiate\n"]
    T.append("Operazioni il cui esito è cambiato di almeno mezzo punto rispetto alla prima ricostruzione (rendimento di Aldo sul controvalore, dopo i costi).\n")
    T.append("| Operazione | Asset | Verso | Prima | Adesso | Differenza | Affidabilità |")
    T.append("|---|---|---|---|---|---|---|")
    ch = []
    for r in t.itertuples():
        o = old.get(r.trade, np.nan)
        if not np.isfinite(o) or abs(r.rendimento - o) >= 0.005:
            ch.append((r.trade, r.asset, r.verso, o, r.rendimento))
    for tid, a, v, o, n in sorted(ch, key=lambda x: -abs(x[4] - (x[3] if np.isfinite(x[3]) else 0))):
        T.append(f"| {tid} | {a} | {v} | {pct(o, 2) if np.isfinite(o) else 'assente'} | {pct(n, 2)} | {pct(n - o, 2) if np.isfinite(o) else '–'} | {aff.get(tid, '–')} |")
    gone = sorted(set(old.index) - set(t.trade))
    T.append(f"\nOperazioni modificate: {len(ch)} su {len(t)}. Tolte perché non calcolabili (chiusura mai dichiarata, prezzo ignoto): {', '.join(gone) if gone else 'nessuna'}.")
    a = pd.Series(aff).reindex(t.trade)
    T.append("\n## R2 affidabilita\n")
    T.append("| Affidabilità della ricostruzione | Operazioni | In guadagno | Medio per operazione |")
    T.append("|---|---|---|---|")
    for k in ("alta", "media", "bassa"):
        x = t[a.to_numpy() == k].rendimento
        if len(x):
            T.append(f"| {k} | {len(x)} | {np.mean(x > 0) * 100:.0f}% | {pct(x.mean(), 2)} |")
    T.append("\nAlta: prezzi d'ingresso e d'uscita leggibili nelle schermate, ROI coerente. Media: un prezzo ricavato (medio, stima su dati di mercato). Bassa: un ingresso o un'uscita mai dichiarati, ricostruiti.")
    T.append("\n## R3 schede\n")
    for r in t.itertuples():
        g = ev[ev.trade == r.trade]
        T.append(f"**{r.trade} · {r.asset} {r.verso}** — esito {pct(r.rendimento, 2)} (dopo i costi), prezzo medio {r.prezzo_medio:.6g}, affidabilità {aff.get(r.trade, '–')}\n")
        T.append("| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |")
        T.append("|---|---|---|---|---|---|---|")
        for x in g.itertuples():
            d = getattr(x, "utc_effettivo", None)
            d = d if isinstance(d, str) and d else x.utc
            p = f"{x.prezzo:.6g}" if isinstance(x.prezzo, (int, float)) and x.prezzo == x.prezzo else "–"
            q = f"{x.quota:g}" if isinstance(x.quota, (int, float)) and x.quota == x.quota else "–"
            T.append(f"| {d} | #{x.msg_id} | {TIPO.get(x.tipo, x.tipo)} | {p} | {q} | {fonte_cat(x.fonte)} | {x.affidabilita} |")
        T.append("")
    return T


if __name__ == "__main__":
    main()
