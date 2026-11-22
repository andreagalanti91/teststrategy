"""Verifiche finali sui candidati scelti in IS (2018-2021): OOS, costi, placebo, dati OKX, leva. Scrive results/intraday/."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import intraday as I
from intraday_research import IS0, IS1, OOS1, features, sig_limit, sig_placebo, sig_pull4h

OUT = Path(__file__).resolve().parent.parent / "results" / "intraday"
pct = lambda x, d=1: "n/d" if x is None or not np.isfinite(x) else f"{x * 100:+.{d}f}%".replace(".", ",")
num = lambda x, d=2: f"{x:.{d}f}".replace(".", ",")
T = []

# ---------------------------------------------------------------- riepilogo delle griglie
NAMES = {"pullback": "Ritracciamento RSI 1h nel trend", "breakout": "Rottura dei massimi 1h nel trend", "ora": "Ora del giorno (long)",
         "limite": "Ordine limite contro il movimento", "pull4h": "Ritracciamento RSI 4h nel trend"}
T.append("## I1 famiglie\n")
T.append("| Famiglia | Configurazioni | WR ≥ 65% in 2018–21 | Guadagna in 2018–21 | Guadagna in 2022–26 | Guadagna in entrambi | WR mediano | Miglior t in 2018–21 |")
T.append("|---|---|---|---|---|---|---|---|")
tot = np.zeros(5, int)
allg = []
for fam, name in NAMES.items():
    g = pd.read_csv(OUT / f"griglia_{fam}.csv")
    allg.append(g)
    v = [len(g), int((g.is_wr >= .65).sum()), int((g.is_exp > 0).sum()), int((g.oos_exp > 0).sum()), int(((g.is_exp > 0) & (g.oos_exp > 0)).sum())]
    tot += v
    T.append(f"| {name} | {v[0]} | {v[1]} | {v[2]} | {v[3]} | {v[4]} | {g.is_wr.median() * 100:.0f}% | {num(g.is_tstat.max())} |")
T.append(f"| **Totale** | **{tot[0]}** | **{tot[1]}** | **{tot[2]}** | **{tot[3]}** | **{tot[4]}** | | |")
g = pd.concat(allg)
both = g[(g.is_exp > 0) & (g.oos_exp > 0)]
both.to_csv(OUT / "positive_in_entrambi.csv", index=False)

b = I.load("binance")
h = features(b)
CAND = {"A · Ritracciamento 4h (scelto)": (sig_pull4h, dict(reg="w", thr=35, k_tp=0.75, k_sl=4.0, hold=24), "w"),
        "B · Ordine limite": (sig_limit, dict(reg=50, k_in=1.0, k_tp=1.5, k_sl=3.0, hold=48), 50)}


def row(name, t, lev=1.0):
    a, o, f = I.stats(t, lev, IS0, IS1), I.stats(t, lev, IS1, OOS1), I.stats(t, lev, IS0, OOS1)
    return (f"| {name} | {f['n']} | {f['per_year']:.0f} | {f['wr'] * 100:.0f}% | {pct(f['avg_win'], 2)} | {pct(f['avg_loss'], 2)} | {num(f['pf'])} | "
            f"{pct(a['exp'], 3)} | {pct(o['exp'], 3)} | {pct(a['cagr'])} | {pct(o['cagr'])} | {pct(f['cagr'])} | {pct(f['dd'])} |"), f


HDR = ("| Variante | Trade | per anno | WR | Vincita media | Perdita media | Profit factor | Media per trade 2018–21 | Media per trade 2022–26 | "
       "CAGR 2018–21 | CAGR 2022–26 | CAGR totale | Max DD |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|")
T.append("\n## I2 candidati\n")
T.append(HDR)
TR = {}
for name, (fn, p, reg) in CAND.items():
    TR[name] = I.backtest(b, fn(h, **p))
    T.append(row(name + ", leva 1x", TR[name])[0])
    TR[name].df.to_csv(OUT / f"trades_{name[0]}.csv", index=False)

# ---------------------------------------------------------------- anni
T.append("\n## I3 anni\n")
for name, t in TR.items():
    f = I.stats(t, 1.0, IS0, OOS1)
    d = t.df[(t.df.entry_time >= IS0)]
    by = d.groupby(d.entry_time.dt.year)
    T.append(f"**{name}, leva 1x**\n")
    T.append("| | " + " | ".join(str(y) for y in by.groups) + " |")
    T.append("|---|" + "---|" * len(by.groups))
    T.append("| Trade | " + " | ".join(str(len(x)) for _, x in by) + " |")
    T.append("| WR | " + " | ".join(f"{(x.ret > 0).mean() * 100:.0f}%" for _, x in by) + " |")
    T.append("| Rendimento | " + " | ".join(pct(float(np.prod(1 + x.ret) - 1)) for _, x in by) + " |\n")

# ---------------------------------------------------------------- costi
T.append("\n## I4 costi\n")
T.append(HDR)
base = (I.TAKER, I.MAKER, I.SLIP, I.FUND_8H)
COSTS = {"costi zero (irrealistico)": (0, 0, 0, 0), "OKX VIP alto: taker 0,03%, maker 0,00%, slippage 0,01%": (.0003, 0, .0001, .0001),
         "OKX base: taker 0,05%, maker 0,02%, slippage 0,02%": base, "prudente: slippage 0,05%": (.0005, .0002, .0005, .0001)}
for name, (fn, p, reg) in CAND.items():
    for cn, cv in COSTS.items():
        I.TAKER, I.MAKER, I.SLIP, I.FUND_8H = cv
        T.append(row(f"{name[0]} · {cn}", I.backtest(b, fn(h, **p)))[0])
I.TAKER, I.MAKER, I.SLIP, I.FUND_8H = base

# ---------------------------------------------------------------- placebo
T.append("\n## I5 placebo\n")
T.append("| Candidato | WR reale | WR con ingressi casuali (mediana) | Media per trade reale | Media per trade casuale (mediana) | Percentile del reale |")
T.append("|---|---|---|---|---|---|")
rng = np.random.default_rng(7)
name, (fn, p, reg) = list(CAND.items())[0]
real = fn(h, **p)
real = real[(real.index >= IS0)]
rs = I.stats(I.backtest(b, real), 1.0, IS0, OOS1)
wr, ex = [], []
for _ in range(200):
    s = I.stats(I.backtest(b, sig_placebo(h, real, reg, rng)), 1.0, IS0, OOS1)
    wr.append(s["wr"]); ex.append(s["exp"])
pd.DataFrame({"wr": wr, "exp": ex}).to_csv(OUT / "placebo_A.csv", index=False)
T.append(f"| {name} | {rs['wr'] * 100:.0f}% | {np.median(wr) * 100:.0f}% | {pct(rs['exp'], 3)} | {pct(float(np.median(ex)), 3)} | {(np.array(ex) < rs['exp']).mean() * 100:.0f}° |")

# ---------------------------------------------------------------- OKX
T.append("\n## I6 okx\n")
bo = I.load("okx")
ho = features(bo.combine_first(b[b.index < bo.index[0]]))          # storia precedente da Binance solo per gli indicatori
T.append("| Candidato | Dati | Periodo | Trade | WR | Media per trade | CAGR 1x | Max DD 1x |")
T.append("|---|---|---|---|---|---|---|---|")
for name, (fn, p, reg) in CAND.items():
    for lab, bb, hh in (("Binance spot", b, h), ("OKX BTC-USDT-SWAP", bo, ho)):
        s = I.stats(I.backtest(bb, fn(hh, **p)), 1.0, "2020-01-01", OOS1)
        T.append(f"| {name[0]} | {lab} | 2020–2026 | {s['n']} | {s['wr'] * 100:.0f}% | {pct(s['exp'], 3)} | {pct(s['cagr'])} | {pct(s['dd'])} |")

# ---------------------------------------------------------------- leva
T.append("\n## I7 leva\n")
T.append("| Candidato | Leva | 10.000 $ → (2018–2026) | CAGR | Max DD | Trade peggiore | CAGR 2018–21 | CAGR 2022–26 | DD entro −35%? |")
T.append("|---|---|---|---|---|---|---|---|---|")
for name, t in TR.items():
    for lev in (1, 2, 3, 5):
        f, a, o = I.stats(t, lev, IS0, OOS1), I.stats(t, lev, IS0, IS1), I.stats(t, lev, IS1, OOS1)
        T.append(f"| {name[0]} | {lev}x | {f"{10000 * f['final']:,.0f}".replace(",", ".")} | {pct(f['cagr'])} | {pct(f['dd'])} | {pct(f['worst'])} | {pct(a['cagr'])} | {pct(o['cagr'])} | {'sì' if f['dd'] >= -0.35 else 'no'} |")
    T.append(f"| {name[0]} | leva massima con DD ≤ 35% | {num(I.best_leverage(t, start=IS0, end=OOS1))}x | | | | | | |")
(OUT / "tables.md").write_text("\n".join(T) + "\n")
print("\n".join(T))
print(both.round(4).to_string())
