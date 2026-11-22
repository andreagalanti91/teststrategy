"""Esegue tutte le strategie, la robustezza e i portafogli; scrive results/*.csv, results/tables.md e i grafici."""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import strategies as S
from common import CAPITAL, COINS, END, ROOT, START, fed_funds, lever, leverage_for, metrics

RES = ROOT / "results"
RES.mkdir(exist_ok=True)
TARGET = 0.70
BORROW = fed_funds() + 0.01

# nome -> (funzione, giorni/anno per le metriche, famiglia, leva)
w31, w31_tr = S.radar_w3(0.10)
w3, _ = S.radar_w3(0.25)
RUNS = {
    "BTC buy & hold": (S.btc_hold(), 365, "BTC", "1x"),
    "W3.1 radar (rischio 10%)": (w31, 365, "BTC", "1x"),
    "W3 radar (rischio 25%)": (w3, 365, "BTC", "1x"),
    "BTC sopra SMA200": (S.btc_sma200(), 365, "BTC", "1x"),
    "BTC ensemble Donchian": (S.btc_ensemble(), 365, "BTC", "1x"),
    "BTC TSMOM long/short perp": (S.btc_tsmom_ls(), 365, "BTC", "≤1x"),
    "Paniere trend 11 crypto": (S.crypto_trend_basket(), 365, "Crypto", "1x"),
    "Rotazione momentum crypto": (S.crypto_rotation(), 365, "Crypto", "1x"),
    "Rotazione a rischio controllato": (S.crypto_rotation(vol_ref=0.60), 365, "Crypto", "1x"),
    "Carry funding sempre attivo": (S.funding_carry(), 365, "Carry", "neutrale"),
    "Carry funding selettivo": (S.funding_carry(smart=True), 365, "Carry", "neutrale"),
    "SPY buy & hold": (S.etf_hold("SPY"), 252, "Azioni", "1x"),
    "QQQ buy & hold": (S.etf_hold("QQQ"), 252, "Azioni", "1x"),
    "Dual momentum SPY/QQQ/GLD": (S.dual_momentum(), 252, "Azioni", "1x"),
    "QQQ 3x sintetico + SMA200": (S.qqq3x_sma200(), 252, "Azioni", "3x"),
    "Momentum 10 mega-cap (*)": (S.megacap_rotation(), 252, "Azioni", "1x"),
}
CURVES = {k: v[0]["equity"].loc[START:END] for k, v in RUNS.items()}
BLENDS = {
    "P1 Prudente: 50% W3.1 + 50% carry selettivo": {"W3.1 radar (rischio 10%)": .5, "Carry funding selettivo": .5},
    "P2 Bilanciato: W3 25% + paniere trend + carry (1/3)": {"W3 radar (rischio 25%)": 1/3, "Paniere trend 11 crypto": 1/3, "Carry funding selettivo": 1/3},
    "P3 Crescita: W3 25% + rotazione + carry (1/3)": {"W3 radar (rischio 25%)": 1/3, "Rotazione momentum crypto": 1/3, "Carry funding selettivo": 1/3},
    "P4 Aggressivo: 50% W3 25% + 50% rotazione": {"W3 radar (rischio 25%)": .5, "Rotazione momentum crypto": .5},
}
for k, wts in BLENDS.items():
    RUNS[k] = (S.blend(CURVES, wts), 365, "Portafoglio", "1x")
    CURVES[k] = RUNS[k][0]["equity"].loc[START:END]

pct = lambda x, d=1: "n/d" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x * 100:+.{d}f}%".replace(".", ",")
usd = lambda x: f"{x:,.0f}".replace(",", ".")
num = lambda x, d=2: f"{x:.{d}f}".replace(".", ",")

rows, M = [], {}
for k, (o, per, fam, lv) in RUNS.items():
    m = metrics(o["equity"], o["gross"], o["turnover"], per)
    M[k] = m
    rows.append({"strategia": k, "famiglia": fam, "leva": lv, **{a: b for a, b in m.items() if a != "years"},
                 **{f"y{y}": v for y, v in m["years"].items()}})
pd.DataFrame(rows).to_csv(RES / "summary.csv", index=False)
idx = pd.date_range(START, END, freq="D")
eq = pd.DataFrame({k: (v / v.iloc[0]).reindex(idx.union(v.index)).ffill().reindex(idx) for k, v in CURVES.items()}) * CAPITAL
eq.round(2).to_csv(RES / "equity.csv", index_label="date")
pd.DataFrame(w31_tr)[["signal", "entry", "side", "entry_px", "expo", "exit", "exit_px", "reason", "pnl"]].to_csv(RES / "w31_trades.csv", index=False)

T = []
T.append("## T1 confronto\n")
T.append("| Strategia | Famiglia | 10.000 $ → | Totale | CAGR | Max DD | Sharpe | MAR | Anno peggiore | Tempo a mercato | ≥ 70% annuo? |")
T.append("|---|---|---|---|---|---|---|---|---|---|---|")
for k, m in M.items():
    T.append(f"| {k} | {RUNS[k][2]} | {usd(m['final'])} | {pct(m['total'], 0)} | {pct(m['cagr'])} | {pct(m['dd'])} | {num(m['sharpe'])} | "
             f"{num(m['mar'])} | {pct(m['worst_year'], 0)} | {'–' if RUNS[k][2] == 'Portafoglio' else format(m['time_in'] * 100, '.0f') + '%'} | {'sì' if m['cagr'] >= TARGET else 'no'} |")
T.append("\n## T2 anni\n")
ys = sorted({y for m in M.values() for y in m["years"]})
T.append("| Strategia | " + " | ".join(map(str, ys)) + " | CAGR 2021–23 | DD 2021–23 | CAGR 2024–26 | DD 2024–26 |")
T.append("|---|" + "---|" * (len(ys) + 4))
for k, m in M.items():
    T.append(f"| {k} | " + " | ".join(pct(m["years"].get(y), 0) for y in ys) +
             f" | {pct(m['cagr_a'], 0)} | {pct(m['dd_a'], 0)} | {pct(m['cagr_b'], 0)} | {pct(m['dd_b'], 0)} |")

# leva necessaria per il 70% annuo
T.append("\n## T3 leva per il 70%\n")
T.append("| Strategia | CAGR 1x | DD 1x | Leva per ≥ 70% annuo | CAGR con leva | DD con leva | CAGR 2021–23 | CAGR 2024–26 |")
T.append("|---|---|---|---|---|---|---|---|")
lev_rows = []
for k, m in M.items():
    if RUNS[k][2] == "Carry" or "3x" in k or "buy & hold" in k:
        continue
    per = RUNS[k][1]
    e = CURVES[k] if per == 365 else CURVES[k]
    r = leverage_for(e, TARGET, BORROW, per)
    if r is None:
        T.append(f"| {k} | {pct(m['cagr'])} | {pct(m['dd'])} | non raggiungibile | – | – | – | – |")
        lev_rows.append({"strategia": k, "leva": None})
        continue
    L, c, d = r
    el = lever(e, L, BORROW, per)
    ml = metrics(el, periods=per)
    T.append(f"| {k} | {pct(m['cagr'])} | {pct(m['dd'])} | {num(L)}x | {pct(c)} | {pct(d)} | {pct(ml['cagr_a'], 0)} | {pct(ml['cagr_b'], 0)} |")
    lev_rows.append({"strategia": k, "leva": L, "cagr": c, "dd": d, "cagr_a": ml["cagr_a"], "cagr_b": ml["cagr_b"]})
pd.DataFrame(lev_rows).to_csv(RES / "leva_per_70.csv", index=False)

# robustezza della rotazione
def mrow(o):
    m = metrics(o["equity"], o["gross"], o["turnover"])
    return m
rob = []
for lb in (14, 21, 30, 45, 60, 90):
    for top in (1, 2, 3, 5):
        for reg in (100, 200):
            m = mrow(S.crypto_rotation(lb, top, reg))
            rob.append({"test": "griglia", "lookback": lb, "top": top, "regime": reg, "dow": 6, "universo": "11", **{a: m[a] for a in ("final", "cagr", "dd", "mar", "cagr_a", "cagr_b")}})
for d in range(7):
    m = mrow(S.crypto_rotation(dow=d))
    rob.append({"test": "giorno", "lookback": 30, "top": 3, "regime": 200, "dow": d, "universo": "11", **{a: m[a] for a in ("final", "cagr", "dd", "mar", "cagr_a", "cagr_b")}})
UNIV = {"senza ZEC": [c for c in COINS if c != "ZEC"], "senza ZEC e SOL": [c for c in COINS if c not in ("ZEC", "SOL")],
        "senza ZEC, SOL, DOGE": [c for c in COINS if c not in ("ZEC", "SOL", "DOGE")],
        "solo top-20 di gennaio 2021 (BTC ETH XRP ADA LINK BNB XMR TRX)": ["BTC", "ETH", "XRP", "ADA", "LINK", "BNB", "XMR", "TRX"],
        "solo BTC ETH SOL": ["BTC", "ETH", "SOL"]}
for u, cs in UNIV.items():
    m = mrow(S.crypto_rotation(coins=cs, top=min(3, len(cs))))
    rob.append({"test": "universo", "lookback": 30, "top": 3, "regime": 200, "dow": 6, "universo": u, **{a: m[a] for a in ("final", "cagr", "dd", "mar", "cagr_a", "cagr_b")}})
rob = pd.DataFrame(rob)
rob.to_csv(RES / "robustezza_rotazione.csv", index=False)
g = rob[rob.test == "griglia"]
T.append("\n## T4 robustezza rotazione\n")
T.append(f"Griglia di {len(g)} combinazioni (lookback 14–90 giorni × 1–5 monete × regime SMA 100/200): CAGR mediano {pct(g.cagr.median())}, "
         f"minimo {pct(g.cagr.min())}, massimo {pct(g.cagr.max())}; DD mediano {pct(g.dd.median())}, migliore {pct(g.dd.max())}, peggiore {pct(g.dd.min())}; "
         f"combinazioni con CAGR ≥ 70%: {(g.cagr >= TARGET).sum()}/{len(g)}; con CAGR ≥ 70% e DD migliore di −35%: {((g.cagr >= TARGET) & (g.dd > -0.35)).sum()}/{len(g)}; "
         f"con DD migliore di −35%: {(g.dd > -0.35).sum()}/{len(g)}.\n")
T.append("| Lookback \\ monete | " + " | ".join(f"top {t}" for t in (1, 2, 3, 5)) + " |")
T.append("|---|---|---|---|---|")
for lb in (14, 21, 30, 45, 60, 90):
    T.append(f"| {lb} giorni | " + " | ".join(
        f"{pct(g[(g.lookback == lb) & (g.top == t) & (g.regime == 200)].cagr.iloc[0], 0)} / {pct(g[(g.lookback == lb) & (g.top == t) & (g.regime == 200)].dd.iloc[0], 0)}"
        for t in (1, 2, 3, 5)) + " |")
d = rob[rob.test == "giorno"]
T.append("\n| Giorno di decisione | " + " | ".join(["lun", "mar", "mer", "gio", "ven", "sab", "dom"]) + " | mediana |")
T.append("|---|" + "---|" * 8)
T.append("| 10.000 $ → | " + " | ".join(usd(v) for v in d.final) + f" | {usd(d.final.median())} |")
T.append("| CAGR | " + " | ".join(pct(v, 0) for v in d.cagr) + f" | {pct(d.cagr.median(), 0)} |")
T.append("| Max DD | " + " | ".join(pct(v, 0) for v in d.dd) + f" | {pct(d.dd.median(), 0)} |")
u = rob[rob.test == "universo"]
T.append("\n| Universo | 10.000 $ → | CAGR | Max DD | CAGR 2021–23 | CAGR 2024–26 |")
T.append("|---|---|---|---|---|---|")
m0 = M["Rotazione momentum crypto"]
T.append(f"| 11 monete (base) | {usd(m0['final'])} | {pct(m0['cagr'])} | {pct(m0['dd'])} | {pct(m0['cagr_a'], 0)} | {pct(m0['cagr_b'], 0)} |")
for _, r in u.iterrows():
    T.append(f"| {r.universo} | {usd(r.final)} | {pct(r.cagr)} | {pct(r.dd)} | {pct(r.cagr_a, 0)} | {pct(r.cagr_b, 0)} |")

# robustezza del carry e del paniere
T.append("\n## T5 robustezza carry e paniere\n")
T.append("| Variante | 10.000 $ → | CAGR | Max DD | Sharpe | CAGR 2021–23 | CAGR 2024–26 |")
T.append("|---|---|---|---|---|---|---|")
VAR = {"Carry selettivo solo BTC": lambda: S.funding_carry(("BTC",), smart=True),
       "Carry selettivo BTC+ETH": lambda: S.funding_carry(("BTC", "ETH"), smart=True),
       "Carry selettivo, soglia 0,0002/g": lambda: S.funding_carry(smart=True, enter=0.0002),
       "Carry selettivo, media 7 g": lambda: S.funding_carry(smart=True, n=7),
       "Carry selettivo, media 30 g": lambda: S.funding_carry(smart=True, n=30),
       "Carry selettivo, 11 monete": lambda: S.funding_carry(tuple(COINS), smart=True),
       "Paniere trend, senza ZEC": lambda: S.crypto_trend_basket(coins=[c for c in COINS if c != "ZEC"]),
       "Paniere trend, top-20 di gennaio 2021": lambda: S.crypto_trend_basket(coins=["BTC", "ETH", "XRP", "ADA", "LINK", "BNB", "XMR", "TRX"]),
       "Paniere trend, solo orizzonti ≥ 30 g": lambda: S.crypto_trend_basket(lookbacks=[30, 60, 90, 150, 250, 360]),
       "Paniere trend, vol di riferimento 40%": lambda: S.crypto_trend_basket(vol_ref=0.40),
       "Paniere trend, vol di riferimento 80%": lambda: S.crypto_trend_basket(vol_ref=0.80)}
vr = []
for k, fn in VAR.items():
    m = mrow(fn())
    vr.append({"variante": k, **{a: m[a] for a in ("final", "cagr", "dd", "sharpe", "cagr_a", "cagr_b")}})
    T.append(f"| {k} | {usd(m['final'])} | {pct(m['cagr'])} | {pct(m['dd'])} | {num(m['sharpe'])} | {pct(m['cagr_a'], 0)} | {pct(m['cagr_b'], 0)} |")
pd.DataFrame(vr).to_csv(RES / "robustezza_varianti.csv", index=False)

# correlazioni mensili fra le strategie principali
core = ["W3 radar (rischio 25%)", "Paniere trend 11 crypto", "Rotazione momentum crypto", "Carry funding selettivo",
        "Dual momentum SPY/QQQ/GLD", "QQQ 3x sintetico + SMA200", "BTC buy & hold"]
mr = eq[core].resample("ME").last().pct_change().dropna()
c = mr.corr()
c.round(2).to_csv(RES / "correlazioni_mensili.csv")
short = ["W3 25%", "Paniere", "Rotazione", "Carry", "Dual mom.", "QQQ 3x", "BTC"]
T.append("\n## T6 correlazioni mensili\n")
T.append("| | " + " | ".join(short) + " |")
T.append("|---|" + "---|" * len(short))
for a, sa in zip(core, short):
    T.append(f"| {sa} | " + " | ".join(num(c.loc[a, b]) for b in core) + " |")
# portafogli con la rotazione sull'universo noto a gennaio 2021 (senza le monete entrate in classifica dopo)
U21 = ["BTC", "ETH", "XRP", "ADA", "LINK", "BNB", "XMR", "TRX"]
C2 = dict(CURVES)
C2["Rotazione momentum crypto"] = S.crypto_rotation(coins=U21)["equity"].loc[START:END]
C2["Paniere trend 11 crypto"] = S.crypto_trend_basket(coins=U21)["equity"].loc[START:END]
T.append("\n## T7 portafogli con universo di gennaio 2021\n")
T.append("| Portafoglio | 10.000 $ → | CAGR | Max DD | MAR | CAGR 2021–23 | CAGR 2024–26 | Leva per 70% | DD con leva |")
T.append("|---|---|---|---|---|---|---|---|---|")
b7 = []
for k, wts in BLENDS.items():
    if "P1" in k:
        continue
    o = S.blend(C2, wts)
    m = metrics(o["equity"])
    r = leverage_for(o["equity"].loc[START:END], TARGET, BORROW)
    b7.append({"portafoglio": k, **{a: m[a] for a in ("final", "cagr", "dd", "mar", "cagr_a", "cagr_b")}, "leva70": r[0] if r else None, "dd_leva": r[2] if r else None})
    T.append(f"| {k.split(':')[0]} | {usd(m['final'])} | {pct(m['cagr'])} | {pct(m['dd'])} | {num(m['mar'])} | {pct(m['cagr_a'], 0)} | {pct(m['cagr_b'], 0)} | "
             + (f"{num(r[0])}x | {pct(r[2])} |" if r else "non raggiungibile | – |"))
pd.DataFrame(b7).to_csv(RES / "portafogli_universo2021.csv", index=False)
# W3 del repo radar con rischio e leva diversi (motore originale: long 2x = meta' spot e meta' perp, funding reale)
T.append("\n## T8 W3 rischio e leva\n")
T.append("| Rischio allo stop | Leva | 10.000 $ → | CAGR | Max DD | MAR | Trade peggiore | CAGR 2021–23 | CAGR 2024–26 | ≥ 70% annuo? |")
T.append("|---|---|---|---|---|---|---|---|---|---|")
w8 = []
for risk, lv in ((0.10, 1), (0.10, 2), (0.25, 1), (0.25, 2), (0.50, 1), (0.50, 2)):
    o, tr = S.radar_w3(risk, lv)
    m = metrics(o["equity"])
    wt = min(t["pnl"] for t in tr)
    w8.append({"rischio": risk, "leva": lv, **{a: m[a] for a in ("final", "cagr", "dd", "mar", "cagr_a", "cagr_b")}, "peggior_trade": wt})
    T.append(f"| {risk * 100:.0f}% | {lv}x | {usd(m['final'])} | {pct(m['cagr'])} | {pct(m['dd'])} | {num(m['mar'])} | {pct(wt)} | {pct(m['cagr_a'], 0)} | {pct(m['cagr_b'], 0)} | {'sì' if m['cagr'] >= TARGET else 'no'} |")
pd.DataFrame(w8).to_csv(RES / "w3_rischio_leva.csv", index=False)
(RES / "tables.md").write_text("\n".join(T) + "\n")

# ------------------------------------------------------------------ grafici
INK, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb"
PAL = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6"]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF})
show = [("Rotazione momentum crypto", "Rotazione crypto"), ("W3 radar (rischio 25%)", "W3 (25%)"),
        ("P3 Crescita: W3 25% + rotazione + carry (1/3)", "P3 Crescita"), ("Paniere trend 11 crypto", "Paniere trend"),
        ("W3.1 radar (rischio 10%)", "W3.1 (10%)"), ("Carry funding selettivo", "Carry selettivo"), ("BTC buy & hold", "BTC buy & hold")]
fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 8.4), sharex=True, gridspec_kw={"height_ratios": [3, 2], "hspace": 0.12})
ends = []
for (k, lab), col in zip(show, PAL):
    e = eq[k]
    a1.plot(e.index, e, color=col, lw=2 if k != "BTC buy & hold" else 1.4, label=lab)
    a2.plot(e.index, (e / e.cummax() - 1) * 100, color=col, lw=1.3)
    ends.append((float(e.iloc[-1]), lab, col))
a1.set_yscale("log")
a1.set_yticks([5000, 10000, 20000, 50000, 100000, 200000, 400000])
a1.set_yticklabels(["5k", "10k", "20k", "50k", "100k", "200k", "400k"])
a1.minorticks_off()
a1.grid(axis="y", color=GRID, lw=0.8)
a1.set_title("10.000 $ dal 01/01/2021 al 10/11/2026 (scala logaritmica, costi inclusi)", loc="left", color=INK, fontsize=12, fontweight="bold")
ends.sort()
ypos = []
for v, lab, col in ends:                       # etichette dirette senza sovrapposizioni
    y = v if not ypos else max(v, ypos[-1] * 1.17)
    ypos.append(y)
    a1.annotate(f"{lab} · {usd(v)} $", xy=(eq.index[-1], v), xytext=(eq.index[-1] + pd.Timedelta(days=25), y), color=INK, fontsize=9,
                va="center", arrowprops=dict(arrowstyle="-", color=col, lw=1.2))
a1.legend(loc="upper left", frameon=False, ncol=2, fontsize=9)
a2.grid(axis="y", color=GRID, lw=0.8)
a2.set_title("Drawdown dal massimo (%)", loc="left", color=INK, fontsize=11, fontweight="bold")
a2.set_xlim(eq.index[0], eq.index[-1] + pd.Timedelta(days=560))
a2.set_xticks([pd.Timestamp(f"{y}-01-01") for y in range(2021, 2027)])
a2.set_xticklabels([str(y) for y in range(2021, 2027)])
fig.savefig(RES / "equity.png", dpi=160, bbox_inches="tight")
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 6.4))
FAM = {"BTC": PAL[0], "Crypto": PAL[1], "Carry": PAL[2], "Azioni": PAL[3], "Portafoglio": PAL[6]}
MK = {"BTC": "o", "Crypto": "s", "Carry": "D", "Azioni": "^", "Portafoglio": "P"}
ax.axhspan(70, 100, xmin=0, xmax=20 / 85, color="#1baf7a", alpha=0.10, lw=0)
ax.text(0.6, 96, "Obiettivo: ≥ 70% annuo con DD entro −20%\n(nessuna strategia qui dentro)", color=MUTED, fontsize=9, va="top")
ax.axhline(70, color=MUTED, lw=1, ls=(0, (4, 3)))
for fam in FAM:
    ks = [k for k in M if RUNS[k][2] == fam]
    ax.scatter([-M[k]["dd"] * 100 for k in ks], [M[k]["cagr"] * 100 for k in ks], s=70, color=FAM[fam], marker=MK[fam], label=fam,
               edgecolor=SURF, linewidth=1.5, zorder=3)
LAB = {"W3.1 radar (rischio 10%)": "W3.1", "W3 radar (rischio 25%)": "W3 (25%)", "Rotazione momentum crypto": "Rotazione crypto",
       "Rotazione a rischio controllato": "Rotazione rischio contr.", "Paniere trend 11 crypto": "Paniere trend", "Carry funding selettivo": "Carry selettivo",
       "QQQ 3x sintetico + SMA200": "QQQ 3x + SMA200", "Dual momentum SPY/QQQ/GLD": "Dual momentum",
       "SPY buy & hold": "SPY", "P1 Prudente: 50% W3.1 + 50% carry selettivo": "P1", "P2 Bilanciato: W3 25% + paniere trend + carry (1/3)": "P2",
       "P3 Crescita: W3 25% + rotazione + carry (1/3)": "P3", "P4 Aggressivo: 50% W3 25% + 50% rotazione": "P4"}
for k, lab in LAB.items():
    ax.annotate(lab, (-M[k]["dd"] * 100, M[k]["cagr"] * 100), xytext=(7, 5), textcoords="offset points", fontsize=9, color=INK)
ax.annotate("BTC buy & hold", (-M["BTC buy & hold"]["dd"] * 100, M["BTC buy & hold"]["cagr"] * 100), xytext=(-4, 9), textcoords="offset points", fontsize=9, color=INK, ha="right")
ax.set_xlim(0, 85)
ax.set_ylim(0, 100)
ax.set_xlabel("Max drawdown giornaliero (%, valore assoluto)")
ax.set_ylabel("Rendimento annuo composto (CAGR, %)")
ax.grid(color=GRID, lw=0.8)
ax.legend(frameon=False, loc="center right", title="Famiglia")
ax.set_title("Rendimento contro drawdown, 2021–2026: l'angolo in alto a sinistra è vuoto", loc="left", color=INK, fontsize=12, fontweight="bold")
fig.savefig(RES / "rischio_rendimento.png", dpi=160, bbox_inches="tight")
plt.close(fig)
print((RES / "tables.md").read_text())
