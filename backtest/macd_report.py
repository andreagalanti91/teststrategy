"""MACD/RSI: confronto con i trade dell'utente su SOL, verifica su TAO, BTC, ETH e su ~165 altcoin. Scrive results/tao/tables_macd.md."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import macd_rsi as M
import support_study as S
from fetch_alts import ALTS

OUT = S.ROOT / "results" / "tao"
pct = lambda x, d=0: "n/d" if x is None or not np.isfinite(x) else f"{x * 100:+.{d}f}%".replace(".", ",")
T = []
sol = S.load("SOL")
START = "2021-06-01"

# ---------------------------------------------------------------- trade dell'utente contro la regola
USER = [("Short 180 → 30", -1, 180, 30), ("Long 20 → 160", 1, 20, 160), ("Short 160, stop a 160", -1, 160, 160), ("Long 170 → 200", 1, 170, 200),
        ("Short 200 → 95", -1, 200, 95), ("Long 160 → 200", 1, 160, 200), ("Short 200 → 80", -1, 200, 80)]
eq, tr = M.simulate(sol, "MACD incrocio", start=START)
match = {0: 3, 1: 6, 2: 7, 3: 8, 4: 11, 5: 12, 6: 13}       # indice del trade della regola che corrisponde a quello dell'utente
T.append("## M1 sol trade\n")
T.append("| Regola: incrocio MACD settimanale | Entra | Esce | Prezzi della regola | Mossa regola | Tuo trade | Tua mossa |")
T.append("|---|---|---|---|---|---|---|")
inv = {v: k for k, v in match.items()}
ucomp, rcomp = 1.0, 1.0
for i, r in tr.iterrows():
    u = USER[inv[i]] if i in inv else None
    um = (u[1] * (u[3] / u[2] - 1)) if u else None
    if u:
        ucomp *= 1 + um
    rcomp *= 1 + r.mossa
    T.append(f"| {'Long' if r.verso > 0 else 'Short'} | {r.entra.date()} | {r.esce.date() if pd.notna(r.esce) else 'aperto'} | {r.prezzo_in:.0f} → {r.prezzo_out:.0f} | {pct(r.mossa)} | "
             f"{u[0] if u else '**non fatto**'} | {pct(um) if u else '–'} |")
T.append(f"\nComposto senza costi: regola x{rcomp:.1f} su {len(tr)} trade; i tuoi 7 trade x{ucomp:.1f}.")

# ---------------------------------------------------------------- regole su SOL, TAO, BTC, ETH
def load_any(sym):
    return S.load(sym)


VARS = [(r, None) for r in M.RULES] + [("MACD incrocio", 0.15), ("MACD incrocio", 0.25), ("MACD + RSI 50, mantiene", 0.15), ("MACD + RSI 50, mantiene", 0.25)]
name = lambda r, st: r + (f", stop {st * 100:.0f}%" if st else "")
T.append("\n## M2 regole\n")
T.append("| Regola (settimanale, 1x) | SOL | DD | Trade / vincenti | TAO | DD | BTC | DD | ETH | DD |")
T.append("|---|---|---|---|---|---|---|---|---|---|")
big = {s: load_any(s) for s in ("SOL", "TAO", "BTC", "ETH")}
for r, st in VARS:
    cells = []
    for s in ("SOL", "TAO", "BTC", "ETH"):
        e, t = M.simulate(big[s], r, start="2024-06-01" if s == "TAO" else START, stop=st)
        k = M.stats(e, t)
        cells.append(f"x{k['final']:.1f} ({pct(k['cagr'])}/anno) | {pct(k['dd'])}" + (f" | {k['n']} / {k['wr'] * 100:.0f}%" if s == "SOL" else ""))
    T.append(f"| {name(r, st)} | " + " | ".join(cells) + " |")
bh = []
for s in ("SOL", "TAO", "BTC", "ETH"):
    c = big[s]["close"].loc["2024-06-01" if s == "TAO" else START:]
    e = c / c.iloc[0]
    bh.append(f"x{e.iloc[-1]:.1f} | {pct(float((e / e.cummax() - 1).min()))}" + (" | –" if s == "SOL" else ""))
T.append("| Comprare e tenere | " + " | ".join(bh) + " |")

# ---------------------------------------------------------------- universo
T.append("\n## M3 universo\n")
T.append("| Regola (settimanale, 1x, dal 2021 o dalla quotazione) | Monete | In guadagno | Capitale finale mediano | CAGR mediano | DD mediano | Meglio di comprare e tenere | In guadagno 2021–23 | In guadagno 2024–26 |")
T.append("|---|---|---|---|---|---|---|---|---|")
data = {}
for s in sorted(set(ALTS)):
    try:
        d = S.load(s)
        if len(d) >= 700:
            data[s] = d
    except FileNotFoundError:
        pass
rows = []
for r, st in VARS:
    res, curves = [], {}
    for s, d in data.items():
        st0 = max(pd.Timestamp("2021-01-01"), d.index[0] + pd.Timedelta(weeks=36))
        e, t = M.simulate(d, r, start=str(st0.date()), stop=st)
        if len(e) < 300:
            continue
        k = M.stats(e, t)
        c = d["close"].loc[e.index[0]:]
        a, b = e.loc[:"2023-12-31"], e.loc["2024-01-01":]
        res.append({"sym": s, **k, "bh": float(c.iloc[-1] / c.iloc[0]), "a": float(a.iloc[-1] / a.iloc[0]) if len(a) > 100 else np.nan,
                    "b": float(b.iloc[-1] / b.iloc[0]) if len(b) > 100 else np.nan})
        curves[s] = e.pct_change().fillna(0.0)
    x = pd.DataFrame(res)
    rows.append({"regola": name(r, st), "n": len(x), "pos": (x.final > 1).mean(), "med": x.final.median(), "cagr": x.cagr.median(), "dd": x.dd.median(),
                 "beat": (x.final > x.bh).mean(), "a": (x.a.dropna() > 1).mean(), "b": (x.b.dropna() > 1).mean()})
    q = rows[-1]
    T.append(f"| {q['regola']} | {q['n']} | {q['pos'] * 100:.0f}% | x{q['med']:.2f} | {pct(q['cagr'])} | {pct(q['dd'])} | {q['beat'] * 100:.0f}% | {q['a'] * 100:.0f}% | "
             f"{q['b'] * 100:.0f}% |")
    if r == "MACD incrocio" and st is None:
        x.to_csv(OUT / "macd_incrocio_per_moneta.csv", index=False)
pd.DataFrame(rows).to_csv(OUT / "macd_universo.csv", index=False)
bhx = []
for s, d in data.items():
    c = d["close"].loc[max(pd.Timestamp("2021-01-01"), d.index[0] + pd.Timedelta(weeks=36)):]
    if len(c) > 300:
        bhx.append((c.iloc[-1] / c.iloc[0], float((c / c.cummax() - 1).min())))
bhx = pd.DataFrame(bhx, columns=["f", "dd"])
T.append(f"| Comprare e tenere | {len(bhx)} | {(bhx.f > 1).mean() * 100:.0f}% | x{bhx.f.median():.2f} | – | {pct(bhx.dd.median())} | – | – | – |")

# ---------------------------------------------------------------- stato attuale
T.append("\n## M4 stato\n")
T.append("| Moneta | Ultima candela settimanale chiusa | MACD rispetto al segnale | RSI settimanale | Posizione della regola | Dal |")
T.append("|---|---|---|---|---|---|")
for s in ("SOL", "TAO", "BTC", "ETH"):
    b = M.bars(big[s], "W-SUN")
    m, sg = M.macd(b["close"])
    r = M.rsi(b["close"])
    e, t = M.simulate(big[s], "MACD incrocio", start="2024-06-01")
    last = t.iloc[-1]
    T.append(f"| {s} | {b.index[-1].date()} a {b.close.iloc[-1]:,.0f} | {'sopra' if m.iloc[-1] > sg.iloc[-1] else 'sotto'} | {r.iloc[-1]:.0f} | "
             f"{'long' if last.verso > 0 else 'short'} da {last.prezzo_in:,.0f} | {last.entra.date()} |")
(OUT / "tables_macd.md").write_text("\n".join(T) + "\n")
print("\n".join(T))
