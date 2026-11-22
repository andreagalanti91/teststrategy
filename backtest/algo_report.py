"""Report dell'algoritmo 'MACD a regime': versione finale, vicini, ablazioni, meta' delle monete, leva, confronto con W3,
trade su SOL e TAO, stato attuale. Scrive results/algo/."""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import algo as A
import macd_rsi as M
import support_study as S

OUT = S.ROOT / "results" / "algo"
OUT.mkdir(parents=True, exist_ok=True)
pct = lambda x, d=1: "n/d" if x is None or not np.isfinite(x) else f"{x * 100:+.{d}f}%".replace(".", ",")
usd = lambda x: f"{x:,.0f}".replace(",", ".")
FINAL = dict(trail=0.30, cap=0.15, short=False)     # nucleo: solo long (la gamba short non aggiunge rendimento, vedi A1)
BASE = dict(trail=0.30, cap=0.15)
T = []
data = A.universe()
runs = {}


def line(name, r, bold=False):
    k, a, b = A.stats(r), A.stats(r, None, "2023-12-31"), A.stats(r, "2024-01-01", None)
    n = f"**{name}**" if bold else name
    T.append(f"| {n} | {usd(10000 * k['final'])} | {pct(k['cagr'])} | {pct(k['dd'])} | " + f"{k['sharpe']:.2f}".replace(".", ",") +
             f" | {k['n']} | {k['wr'] * 100:.0f}% | {pct(a['cagr'], 0)} / {pct(a['dd'], 0)} | {pct(b['cagr'], 0)} / {pct(b['dd'], 0)} | {pct(k['worst_year'], 0)} |")
    return k


HDR = "| Versione | 10.000 $ → | CAGR | Max DD | Sharpe | Trade | Vincenti | 2020–23: CAGR / DD | 2024–26: CAGR / DD | Anno peggiore |\n|---|---|---|---|---|---|---|---|---|---|"
T.append("## A1 versioni\n")
T.append(HDR)
VARS = {"Nucleo: solo long, filtri di regime, trailing 30%, tetto 15%, 30 monete più liquide": FINAL,
        "con anche gli short (long + short)": BASE, "solo short": dict(long=False, **BASE),
        "senza trailing e senza tetto": dict(short=False), "senza filtri di regime (MACD puro, long + short)": dict(btc_filter=False, own_filter=False, **BASE),
        "solo filtro sulla moneta": dict(btc_filter=False, **FINAL), "solo filtro su BTC": dict(own_filter=False, **FINAL),
        "15 monete più liquide": dict(top_k=15, **FINAL), "60 monete più liquide": dict(top_k=60, **FINAL),
        "trailing 25%": dict(trail=0.25, cap=0.15), "trailing 35%": dict(trail=0.35, cap=0.15),
        "stop 15%": dict(stop=0.15, **FINAL), "stop 25%": dict(stop=0.25, **FINAL),
        "media a 30 settimane": dict(sma=30, **FINAL), "media a 50 settimane": dict(sma=50, **FINAL)}
for i, (n, kw) in enumerate(VARS.items()):
    runs[n] = A.run(data, **kw)
    line(n, runs[n], bold=(i == 0))
names = sorted(k for k in data if k != "BTC")
for lab, half in (("metà A delle monete (ordine alfabetico, posti dispari)", names[0::2]), ("metà B delle monete (posti pari)", names[1::2])):
    line(lab, A.run({k: data[k] for k in half + ["BTC"]}, **FINAL))
fin = runs[next(iter(VARS))]
fin["equity"].to_frame("equity").to_csv(OUT / "equity_finale.csv")
tr = fin["trades"].copy()
tr.to_csv(OUT / "trade_finale.csv", index=False)

T.append("\n## A2 anni\n")
k = A.stats(fin)
kb = A.stats(runs["senza filtri di regime (MACD puro, long + short)"])
btc = data["BTC"]["close"].reindex(fin["equity"].index).ffill()
by = (btc.groupby(btc.index.year).last() / btc.groupby(btc.index.year).last().shift(1).fillna(btc.iloc[0]) - 1).to_dict()
ys = sorted(k["years"])
T.append("| | " + " | ".join(map(str, ys)) + " |")
T.append("|---|" + "---|" * len(ys))
T.append("| Nucleo solo long | " + " | ".join(pct(k["years"][y], 0) for y in ys) + " |")
T.append("| MACD puro, senza filtri | " + " | ".join(pct(kb["years"][y], 0) for y in ys) + " |")
T.append("| BTC comprato e tenuto | " + " | ".join(pct(by[y], 0) for y in ys) + " |")

T.append("\n## A3 trade\n")
c = tr[tr.why != "aperto"].copy()
c["net"] = c.move - np.where(c.side > 0, 2 * A.COST_L, 2 * A.COST_S)
c["giorni"] = (c.t1 - c.t0).dt.days
T.append("| Gruppo | Trade | Vincenti | Guadagno medio | Mediano | Vincita media | Perdita media | Migliore | Peggiore | Giorni medi |")
T.append("|---|---|---|---|---|---|---|---|---|---|")
for lab, x in (("Tutti", c), ("Long", c[c.side > 0]), ("Short", c[c.side < 0]), ("Usciti per segnale MACD", c[c.why == "segnale"]),
               ("Usciti per trailing", c[c.why == "trailing"]), ("Usciti per stop", c[c.why == "stop"])):
    if len(x):
        T.append(f"| {lab} | {len(x)} | {(x.net > 0).mean() * 100:.0f}% | {pct(x.net.mean())} | {pct(x.net.median())} | {pct(x.net[x.net > 0].mean())} | "
                 f"{pct(x.net[x.net <= 0].mean())} | {pct(x.net.max(), 0)} | {pct(x.net.min(), 0)} | {x.giorni.mean():.0f} |")
top = c.sort_values("net", ascending=False).head(5)
T.append(f"\nI 5 trade migliori ({', '.join(f'{r.sym} {pct(r.net, 0)}' for r in top.itertuples())}) valgono il "
         f"{top.net.sum() / c.net.sum() * 100:.0f}% della somma dei guadagni per trade.")

T.append("\n## A4 leva\n")
T.append(HDR.replace("Versione", "Rischio per trade / esposizione massima"))
for risk, mg in ((0.01, 0.5), (0.015, 0.75), (0.02, 1.0), (0.03, 1.5), (0.04, 2.0), (0.06, 3.0), (0.10, 5.0)):
    line(f"{risk * 100:g}% / {mg:g}x".replace(".", ","), A.run(data, risk=risk, max_gross=mg, trail=0.30, cap=0.15 * risk / 0.02, short=False))

# confronto e combinazione con W3 del repo radar
T.append("\n## A5 w3\n")
sys.path.insert(0, str(S.ROOT / "backtest"))
import strategies as ST
w3, _ = ST.radar_w3(0.25)
w3 = w3["equity"]
e = fin["equity"].loc[w3.index[0]:w3.index[-1]]
both = pd.DataFrame({"algo": e / e.iloc[0], "w3": w3 / w3.iloc[0]}).dropna()
rr = both.pct_change().fillna(0.0)
corr = rr.resample("ME").apply(lambda x: (1 + x).prod() - 1).corr().iloc[0, 1]
T.append("| Dal 01/2021 al 10/11/2026 | 10.000 $ → | CAGR | Max DD | Sharpe |")
T.append("|---|---|---|---|---|")
def srow(name, eq):
    yrs = (eq.index[-1] - eq.index[0]).days / 365.25
    r = eq.pct_change().dropna()
    T.append(f"| {name} | {usd(10000 * eq.iloc[-1])} | {pct(eq.iloc[-1] ** (1 / yrs) - 1)} | {pct(float((eq / eq.cummax() - 1).min()))} | " + f"{r.mean() / r.std() * np.sqrt(365):.2f}".replace(".", ",") + " |")
srow("Nucleo solo long (alt + BTC)", both["algo"])
srow("W3 radar su BTC, rischio 25%", both["w3"])
srow("50% + 50%, ribilanciato ogni giorno", (1 + 0.5 * rr["algo"] + 0.5 * rr["w3"]).cumprod())
T.append(f"\nCorrelazione dei rendimenti mensili fra i due: {corr:.2f}".replace(".", ",") + ".")

# SOL e TAO con le regole dell'algoritmo (moneta singola)
T.append("\n## A6 sol tao\n")
for sym in ("SOL", "TAO"):
    r1 = A.run({sym: data[sym], "BTC": data["BTC"]}, top_k=None, risk=0.2, max_gross=1.0, only=(sym,), start="2021-06-01" if sym == "SOL" else "2024-03-01", **BASE)
    t = r1["trades"]
    t = t[t.sym == sym]
    T.append(f"**{sym}**: trade dell'algoritmo\n")
    T.append("| Verso | Entra | Esce | Prezzo | Mossa | Uscita |")
    T.append("|---|---|---|---|---|---|")
    for q in t.itertuples():
        T.append(f"| {'Long' if q.side > 0 else 'Short'} | {q.t0.date()} | {q.t1.date() if pd.notna(q.t1) else 'aperto'} | {q.entry:.0f} → {q.exit:.0f} | {pct(q.move, 0)} | {q.why} |")
    T.append(f"\nComposto senza costi: x{float(np.prod(1 + t.move)):.1f} su {len(t)} trade, vincenti {(t.move > 0).mean() * 100:.0f}%.\n".replace(".", ",", 1))

# stato attuale
T.append("\n## A7 stato\n")
last_mon = max(t for t in A.weekly(data["BTC"], 40).index)
bw = A.weekly(data["BTC"], 40).loc[last_mon]
bc = M.bars(data["BTC"], "W-SUN")["close"]
T.append(f"Ultima settimana chiusa: domenica {(last_mon - pd.Timedelta(days=1)).date()}. BTC ha chiuso a {usd(bc.iloc[-1])} $, "
         f"{'sopra' if bw['above'] else 'sotto'} la media a 40 settimane ({usd(bc.rolling(40).mean().iloc[-1])} $): regime "
         f"**{'rialzista: long ammessi' if bw['above'] else 'ribassista: nessun long ammesso'}**.\n")
op = tr[tr.why == "aperto"]
T.append("| Posizioni aperte del nucleo (solo long) | Verso | Dal | Ingresso | Ultimo prezzo | Mossa |")
T.append("|---|---|---|---|---|---|")
for q in op.itertuples():
    T.append(f"| {q.sym} | {'long' if q.side > 0 else 'short'} | {q.t0.date()} | {q.entry:.5g} | {q.exit:.5g} | {pct(q.move, 0)} |")
if not len(op):
    T.append("| nessuna | | | | | |")
ops = runs["con anche gli short (long + short)"]["trades"]
ops = ops[ops.why == "aperto"]
T.append("\n| Posizioni che aprirebbe la gamba short (non validata) | Dal | Ingresso | Ultimo prezzo | Mossa |")
T.append("|---|---|---|---|---|")
for q in ops.itertuples():
    T.append(f"| {q.sym} | {q.t0.date()} | {q.entry:.5g} | {q.exit:.5g} | {pct(q.move, 0)} |")
T.append("\n| Moneta | Chiusura settimanale | Rispetto alla media a 40 settimane | MACD settimanale | Cosa dice l'algoritmo |")
T.append("|---|---|---|---|---|")
for sym in ("BTC", "ETH", "SOL", "TAO"):
    w = A.weekly(data[sym], 40)
    r = w.iloc[-1]
    c_ = M.bars(data[sym], "W-SUN")["close"]
    if not bw["above"]:
        say = "nessun long (regime ribassista); short ammesso solo nella gamba short" if (not r["up"] and not r["above"]) else "nessun long (regime ribassista)"
    else:
        say = "long aperto o ammesso" if (r["up"] and r["above"]) else "nessuna posizione"
    cross = "incrocio al ribasso questa settimana" if r["cross_dn"] else "incrocio al rialzo questa settimana" if r["cross_up"] else ("sopra il segnale" if r["up"] else "sotto il segnale")
    T.append(f"| {sym} | {c_.iloc[-1]:.5g} | {pct(c_.iloc[-1] / c_.rolling(40).mean().iloc[-1] - 1, 0)} | {cross} | {say} |")
# da dove nascono i filtri: tutti i trade MACD settimanali, per condizione all'ingresso
import algo_research as AR
x = AR.build()
x.to_csv(OUT / "trade_macd_tutti.csv", index=False)
L, Sh = x.side > 0, x.side < 0
T.append("\n## A8 filtri\n")
T.append(f"{len(x)} trade chiusi su {x.sym.nunique()} monete (incrocio MACD settimanale senza filtri, costi inclusi).\n")
T.append("| Condizione all'ingresso | Trade | Guadagno medio | Mediano | Vincenti | Medio 2020–23 | Medio 2024–26 |")
T.append("|---|---|---|---|---|---|---|")
for lab, m in (("Long, tutti", L), ("Long con BTC sopra la media a 40 settimane", L & (x.btc_sma40 > 0)), ("Long con BTC sotto", L & (x.btc_sma40 < 0)),
               ("Long con moneta sopra la sua media a 40 settimane", L & (x.sma40 > 0)), ("Long con moneta sotto", L & (x.sma40 < 0)),
               ("**Long con moneta e BTC sopra**", L & (x.sma40 > 0) & (x.btc_sma40 > 0)),
               ("Short, tutti", Sh), ("Short con BTC sotto la media a 40 settimane", Sh & (x.btc_sma40 < 0)), ("Short con BTC sopra", Sh & (x.btc_sma40 > 0)),
               ("Short con moneta sotto la sua media", Sh & (x.sma40 < 0)), ("Short con moneta sopra", Sh & (x.sma40 > 0)),
               ("**Short con moneta e BTC sotto**", Sh & (x.sma40 < 0) & (x.btc_sma40 < 0)),
               ("Long con MACD sotto zero (inversione dal basso)", L & (x.macd_n < 0)), ("Short con MACD sopra zero (inversione dall'alto)", Sh & (x.macd_n > 0))):
    y = x[m]
    a, b = y[y.t < "2024-01-01"], y[y.t >= "2024-01-01"]
    T.append(f"| {lab} | {len(y)} | {pct(y.net.mean())} | {pct(y.net.median())} | {(y.net > 0).mean() * 100:.0f}% | {pct(a.net.mean())} | {pct(b.net.mean())} |")
(OUT / "tables.md").write_text("\n".join(T) + "\n")
print("\n".join(T))

# grafico
INK, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED,
                     "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "savefig.facecolor": SURF})
fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 7.6), sharex=True, gridspec_kw={"height_ratios": [3, 2], "hspace": 0.12})
series = [("Nucleo solo long", fin["equity"], "#2a78d6"), ("MACD puro, senza filtri", runs["senza filtri di regime (MACD puro, long + short)"]["equity"], "#eb6834"),
          ("BTC comprato e tenuto", btc / btc.iloc[0], "#1baf7a")]
for lab, s_, col in series:
    s_ = s_ / s_.iloc[0] * 10000
    a1.plot(s_.index, s_, color=col, lw=2, label=lab)
    a2.plot(s_.index, (s_ / s_.cummax() - 1) * 100, color=col, lw=1.3)
    a1.annotate(f"{lab} · {usd(s_.iloc[-1])} $", (s_.index[-1], s_.iloc[-1]), xytext=(8, 0), textcoords="offset points", fontsize=9, color=INK, va="center")
a1.set_yscale("log")
a1.set_yticks([5000, 10000, 20000, 50000, 100000])
a1.set_yticklabels(["5k", "10k", "20k", "50k", "100k"])
a1.minorticks_off()
a1.grid(axis="y", color=GRID, lw=0.8)
a1.legend(frameon=False, loc="upper left", fontsize=9)
a1.set_title("10.000 $ dal 06/2020 al 21/11/2026 (scala logaritmica, costi inclusi)", loc="left", color=INK, fontsize=12, fontweight="bold")
a2.grid(axis="y", color=GRID, lw=0.8)
a2.set_title("Drawdown dal massimo (%)", loc="left", color=INK, fontsize=11, fontweight="bold")
a2.set_xlim(fin["equity"].index[0], fin["equity"].index[-1] + pd.Timedelta(days=520))
a2.set_xticks([pd.Timestamp(f"{y}-01-01") for y in range(2021, 2027)])
a2.set_xticklabels([str(y) for y in range(2021, 2027)])
fig.savefig(OUT / "algoritmo.png", dpi=160, bbox_inches="tight")
