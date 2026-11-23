"""Ciclo di studio: verifica su BTC delle regole classiche dell'analisi tecnica, algoritmo v2 a tre schermi, confronto con
quanto gia' fatto, spiegazione di ogni operazione. Scrive results/regole/."""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import btc_ta as B
import btc_v2 as V

OUT = B.ROOT / "results" / "regole"
OUT.mkdir(parents=True, exist_ok=True)
pct = lambda x, d=1: "n/d" if x is None or not np.isfinite(x) else f"{x * 100:+.{d}f}%".replace(".", ",")
usd = lambda x: f"{x:,.0f}".replace(",", ".")
num = lambda x, d=2: f"{x:.{d}f}".replace(".", ",")
T = []
d = B.load()
c, w = d["close"], B.weekly(d)
f = V.features(d)
A0, A1 = B.IS0, B.IS1
dd = d.loc[A0:]

# ------------------------------------------------------------------ R1: verifiche delle regole
fw = {h: c.shift(-h) / c - 1 for h in (5, 20, 90)}


def ev(mask: pd.Series, h: int, first: bool = True):
    m = mask.reindex(dd.index).fillna(False).astype(bool)
    if first:
        m = m & ~m.shift(1, fill_value=False)
    out = []
    for a, b in ((A0, A1), (A1, None)):
        x = fw[h].reindex(m[m].index).loc[a:b].dropna()
        x = x[x.index < (pd.Timestamp(b) if b else x.index.max() + pd.Timedelta(days=1))]
        out.append((len(x), x.mean() if len(x) else np.nan, (x > 0).mean() if len(x) else np.nan))
    return out


def base(h):
    return [(fw[h].loc[a:b].dropna().mean(), (fw[h].loc[a:b].dropna() > 0).mean()) for a, b in ((A0, A1), (A1, None))]


def row(label, mask, h, first=True):
    e = ev(mask, h, first)
    return f"| {label} | {h} g | {e[0][0]} | {pct(e[0][1])} / {e[0][2] * 100:.0f}% | {e[1][0]} | {pct(e[1][1])} / {e[1][2] * 100:.0f}% |" if e[0][0] and e[1][0] else \
        f"| {label} | {h} g | {e[0][0]} | {pct(e[0][1])} | {e[1][0]} | {pct(e[1][1])} |"


def brow(h):
    b = base(h)
    return f"| *Tutti i giorni (riferimento)* | {h} g | – | {pct(b[0][0])} / {b[0][1] * 100:.0f}% | – | {pct(b[1][0])} / {b[1][1] * 100:.0f}% |"


HDR = "| Condizione | Orizzonte | Casi 2018–21 | Rendimento medio / positivi | Casi 2022–26 | Rendimento medio / positivi |\n|---|---|---|---|---|---|"
s200, s50 = B.sma(c, 200), B.sma(c, 50)
up, dn = c > s200, c < s200
rsi = B.rsi(c)
vol20 = d["volume"].rolling(20).mean()
hh55, ll55 = d["high"].rolling(55).max().shift(1), d["low"].rolling(55).min().shift(1)
o, h_, l_ = d["open"], d["high"], d["low"]
body = (c - o).abs()
rng = (h_ - l_).replace(0, np.nan)
m_d, sg_d = B.macd(c)
macd_up = (m_d > sg_d) & ~(m_d > sg_d).shift(1, fill_value=False)
tide_up = (f["wclose"] > f["sma40"])

T.append("## R1 trend\n")
T.append(HDR)
T.append(brow(20))
T.append(row("Prezzo sopra la SMA 200 giorni (tutti i giorni)", up, 20, first=False))
T.append(row("Prezzo sotto la SMA 200 giorni (tutti i giorni)", dn, 20, first=False))
for st in ("rialzista", "mista", "ribassista"):
    T.append(row(f"Struttura settimanale {st} (massimi e minimi di swing)", f["struttura"] == st, 20, first=False))
T.append(brow(90))
T.append(row("Golden cross: SMA 50 incrocia sopra la SMA 200", s50 > s200, 90))
T.append(row("Death cross: SMA 50 incrocia sotto la SMA 200", s50 < s200, 90))

T.append("\n## R2 rotture\n")
T.append(HDR)
T.append(brow(20))
brk = c > hh55
T.append(row("Chiusura sopra il massimo a 55 giorni", brk, 20))
T.append(row("… con volume oltre 1,5 volte la media a 20 giorni", brk & (d["volume"] > 1.5 * vol20), 20))
T.append(row("… con volume normale o basso", brk & (d["volume"] <= 1.5 * vol20), 20))
T.append(row("… con prezzo sopra la SMA 200", brk & up, 20))
T.append(row("Chiusura sotto il minimo a 55 giorni", c < ll55, 20))

T.append("\n## R3 oscillatori\n")
T.append(HDR)
T.append(brow(20))
T.append(row("RSI giornaliero scende sotto 30", rsi < 30, 20))
T.append(row("… con prezzo sopra la SMA 200", (rsi < 30) & up, 20))
T.append(row("… con prezzo sotto la SMA 200", (rsi < 30) & dn, 20))
T.append(row("RSI giornaliero sale sopra 70", rsi > 70, 20))
T.append(row("… con prezzo sopra la SMA 200", (rsi > 70) & up, 20))
pull = (rsi.rolling(10).min() < 45) & (c > h_.shift(1)) & up
T.append(row("Ritracciamento in trend rialzista: RSI sotto 45, poi chiusura sopra il massimo del giorno prima", pull, 20))

T.append("\n## R4 scale\n")
T.append(HDR)
T.append(brow(20))
T.append(row("MACD giornaliero incrocia al rialzo, tutti i casi", macd_up, 20, first=False))
T.append(row("… con chiusura settimanale sopra la SMA 40 settimane", macd_up & tide_up, 20, first=False))
T.append(row("… con chiusura settimanale sotto la SMA 40 settimane", macd_up & ~tide_up, 20, first=False))

T.append("\n## R5 candele\n")
T.append(HDR)
T.append(brow(5))
bull_eng = (c > o) & (c.shift() < o.shift()) & (c >= o.shift()) & (o <= c.shift()) & (body > body.shift())
bear_eng = (c < o) & (c.shift() > o.shift()) & (c <= o.shift()) & (o >= c.shift()) & (body > body.shift())
hammer = ((pd.concat([o, c], axis=1).min(axis=1) - l_) > 2 * body) & ((h_ - pd.concat([o, c], axis=1).max(axis=1)) < 0.3 * body.clip(lower=1e-9) + 0.1 * rng) & (c.pct_change(5) < 0)
star = ((h_ - pd.concat([o, c], axis=1).max(axis=1)) > 2 * body) & ((pd.concat([o, c], axis=1).min(axis=1) - l_) < 0.3 * body.clip(lower=1e-9) + 0.1 * rng) & (c.pct_change(5) > 0)
doji = (body < 0.1 * rng)
T.append(row("Engulfing rialzista", bull_eng, 5, first=False))
T.append(row("Engulfing ribassista", bear_eng, 5, first=False))
T.append(row("Hammer dopo un calo", hammer, 5, first=False))
T.append(row("Shooting star dopo un rialzo", star, 5, first=False))
T.append(row("Doji", doji, 5, first=False))

# ------------------------------------------------------------------ v2: scelta in IS
rows = []
for mode, k, rp, re, sm in itertools.product(["ritracciamento", "rottura", "entrambi"], [3.0, 4.0, 5.0], [40, 45, 50], [True, False], ["no", "severa", "simmetrica"]):
    if mode == "rottura" and rp != 45:
        continue                                              # con le sole rotture la soglia RSI non entra in gioco
    p, log = V.run(d, f, mode, k, rp, re, sm)
    r = B.run(d, p)
    a, b, t = B.stats(r, A0, A1), B.stats(r, A1, None), B.stats(r)
    rows.append(dict(modo=mode, k_atr=k, rsi=rp, uscita_marea=re, short=sm, n_short=int((log.verso == "short").sum()) if len(log) else 0,
                     is_cagr=a["cagr"], is_dd=a["dd"], is_mar=a["mar"], is_sharpe=a["sharpe"], oos_cagr=b["cagr"], oos_dd=b["dd"], oos_sharpe=b["sharpe"],
                     n=t["n"], wr=t["wr"], cagr=t["cagr"], dd=t["dd"]))
g = pd.DataFrame(rows)
g.to_csv(OUT / "griglia_v2.csv", index=False)
gs = g[g.short != "no"].sort_values(["is_mar", "n_short"], ascending=False)
best = gs.iloc[0]
PV = dict(mode=best.modo, k_atr=float(best.k_atr), rsi_pb=float(best.rsi), regime_exit=bool(best.uscita_marea), short_mode=best.short)
pos2, log2 = V.run(d, f, **PV)
log2.to_csv(OUT / "operazioni_v2.csv", index=False)

# v1 (voto di 17 indicatori), parametri gia' fissati in ANALISI_BTC.md
sig = B.signals(d)
sc = B.score(sig)
pos1 = B.composite(d, sc, 0.5, 0.9, 0.25, False)
pos1l = B.composite(d, sc, 0.5, 9, 0.25, False)
RUNS = {"v1 · voto di 17 indicatori, long/short": B.run(d, pos1), "v1 · voto, solo long": B.run(d, pos1l),
        "v2 · tre schermi (nuovo)": B.run(d, pos2), "50% v1 + 50% v2": B.run(d, 0.5 * pos1 + 0.5 * pos2),
        "Prezzo vs SMA 40 settimane, solo long": B.run(d, sig["Prezzo vs SMA 40 settimane"], allow_short=False),
        "BTC comprato e tenuto": B.run(d, pd.Series(1.0, d.index))}
T.append("\n## V1 scelta\n")
T.append(f"Griglia di {len(g)} combinazioni valutata sul 2018–21. Scelta (miglior rapporto rendimento/drawdown fra quelle con gli short ammessi): ingresso per "
         f"**{PV['mode']}**, chandelier a **{PV['k_atr']:g} ATR**, uscita sul cambio di marea **{'sì' if PV['regime_exit'] else 'no'}**, short in versione **{PV['short_mode']}**.\n")
T.append("| Scelta di progetto | Rendimento annuo mediano 2018–21 | DD mediano | Rendimento annuo mediano 2022–26 | DD mediano | Vincenti | Operazioni |")
T.append("|---|---|---|---|---|---|---|")
for col, lab in (("modo", "Ingresso"), ("short", "Short"), ("uscita_marea", "Uscita sul cambio di marea"), ("k_atr", "Chandelier, ATR")):
    for v, x in g.groupby(col):
        vv = {True: "sì", False: "no"}.get(v, v) if not isinstance(v, float) else f"{v:g}"
        T.append(f"| {lab}: {vv} | {pct(x.is_cagr.median(), 0)} | {pct(x.is_dd.median(), 0)} | {pct(x.oos_cagr.median(), 0)} | {pct(x.oos_dd.median(), 0)} | {x.wr.median() * 100:.0f}% | {x.n.median():.0f} |")
T.append(f"\nCorrelazione fra il risultato 2018–21 e quello 2022–26 delle {len(g)} combinazioni (indice di Sharpe): {num(g.is_sharpe.corr(g.oos_sharpe))}. "
         f"Combinazioni in guadagno nel 2022–26: {(g.oos_cagr > 0).mean() * 100:.0f}%.")

T.append("\n## V2 confronto\n")
T.append("| Strategia | 10.000 $ → (2018–2026) | CAGR | Max DD | Sharpe | Operazioni | Vincenti | Vincita / perdita media | 2018–21: CAGR / DD | 2022–26: CAGR / DD | Dal 2021: CAGR / DD | Tempo a mercato |")
T.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
for k, r in RUNS.items():
    t, a, b, q = B.stats(r), B.stats(r, A0, A1), B.stats(r, A1, None), B.stats(r, "2021-01-01", "2026-11-10")
    T.append(f"| {k} | {usd(10000 * t['final'])} | {pct(t['cagr'])} | {pct(t['dd'])} | {num(t['sharpe'])} | {t['n']} | {t['wr'] * 100:.0f}% | {pct(t['avg_win'], 0)} / {pct(t['avg_loss'], 0)} | "
             f"{pct(a['cagr'], 0)} / {pct(a['dd'], 0)} | {pct(b['cagr'], 0)} / {pct(b['dd'], 0)} | {pct(q['cagr'], 0)} / {pct(q['dd'], 0)} | {t['time'] * 100:.0f}% |")
T.append("| W3 del repo radar, rischio 25% (dati dal 2021) | – | – | – | 1,30 | 13 | 92% | – | – | – | +42% / −21% | 61% |")
r1, r2 = RUNS["v1 · voto di 17 indicatori, long/short"]["ret"], RUNS["v2 · tre schermi (nuovo)"]["ret"]
mc = pd.concat([r1, r2], axis=1).resample("ME").apply(lambda x: (1 + x).prod() - 1).corr().iloc[0, 1]
same = float((np.sign(pos1.loc[A0:]) == np.sign(pos2.loc[A0:])).mean())
T.append(f"\nv1 e v2 hanno la stessa posizione nel {same * 100:.0f}% dei giorni; correlazione dei rendimenti mensili {num(mc)}.")

T.append("\n## V3 anni\n")
ys = list(range(2018, 2027))
T.append("| | " + " | ".join(map(str, ys)) + " |")
T.append("|---|" + "---|" * len(ys))
for k in list(RUNS)[:4] + ["BTC comprato e tenuto"]:
    y = B.stats(RUNS[k])["years"]
    T.append(f"| {k} | " + " | ".join(pct(y.get(v), 0) for v in ys) + " |")

T.append("\n## V4 operazioni\n")
T.append("| # | Verso | Entra | Esce | Prezzo | Risultato | Perché entra | Perché esce |")
T.append("|---|---|---|---|---|---|---|---|")
for i, q in enumerate(log2.itertuples(), 1):
    T.append(f"| {i} | {q.verso} | {q.entra.date()} | {q.esce.date() if pd.notna(q.esce) else 'aperta'} | {usd(q.prezzo_in)} → {usd(q.prezzo_out)} | {pct(q.mossa, 0)} | {q.perche_entra} | {q.perche_esce} |")

# ------------------------------------------------------------------ perche' oggi
T.append("\n## V5 oggi\n")
r = f.iloc[-1]
td = V.tide(r, PV["short_mode"])
chk = lambda ok: "sì" if ok else "no"
T.append("| Schermo | Controllo | Valore oggi | Esito |")
T.append("|---|---|---|---|")
T.append(f"| 1 · Marea | chiusura settimanale rispetto alla SMA 40 settimane | {usd(r.wclose)} contro {usd(r.sma40)} | {'sopra: favorevole ai long' if r.wclose > r.sma40 else 'sotto: long esclusi'} |")
T.append(f"| 1 · Marea | struttura di Dow settimanale | massimi {usd(r.max0)} → {usd(r.max1)}, minimi {usd(r.min0)} → {usd(r.min1)} | {r.struttura} |")
T.append(f"| 1 · Marea | SMA 40 settimane in calo su 4 settimane | {chk(bool(r.sma40_giu))} | {'conferma il ribasso' if r.sma40_giu else 'non ancora in calo'} |")
T.append(f"| 1 · Marea | **verdetto** | | **{'rialzista: solo long' if td > 0 else 'ribassista: solo short' if td < 0 else 'neutra: nessuna operazione'}** |")
T.append(f"| 2 · Onda | rottura del minimo a 55 giorni (per uno short) | chiusura {usd(r.close)} contro minimo {usd(r.ll55)} | {chk(r.close < r.ll55)} |")
T.append(f"| 2 · Onda | rottura del massimo a 55 giorni (per un long) | chiusura {usd(r.close)} contro massimo {usd(r.hh55)} | {chk(r.close > r.hh55)} |")
T.append(f"| 2 · Onda | RSI giornaliero | {r.rsi:.0f} (minimo a 10 giorni {r.rsi_min10:.0f}) | {'ipervenduto' if r.rsi < 30 else 'neutro' if r.rsi < 70 else 'ipercomprato'} |")
T.append(f"| 3 · Rischio | ATR a 22 giorni | {usd(r.atr)} $ ({num(r.atr / r.close * 100, 1)}% del prezzo)" + f" | stop a {PV['k_atr']:g} ATR = {usd(PV['k_atr'] * r.atr)} $ di distanza ({PV['k_atr'] * r.atr / r.close * 100:.0f}%) |")
cur2 = pos2.iloc[-1]
T.append(f"\nPosizione di v2 oggi: **{'long' if cur2 > 0 else 'short' if cur2 < 0 else 'fuori'}**" + (f" — {log2.iloc[-1].perche_entra}." if cur2 != 0 else ".") +
         f" Posizione di v1 oggi: **{'long' if pos1.iloc[-1] > 0 else 'short' if pos1.iloc[-1] < 0 else 'fuori'}** (voto {num(sc.iloc[-1])}).")
(OUT / "tables.md").write_text("\n".join(T) + "\n")
print("\n".join(T))

# grafico
INK, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED,
                     "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "savefig.facecolor": SURF})
fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 7.6), sharex=True, gridspec_kw={"height_ratios": [3, 2], "hspace": 0.12})
sel = [("v1 · voto di 17 indicatori, long/short", "v1 · voto", "#2a78d6"), ("v2 · tre schermi (nuovo)", "v2 · tre schermi", "#eb6834"),
       ("50% v1 + 50% v2", "50% v1 + 50% v2", "#6250d6"), ("BTC comprato e tenuto", "BTC comprato e tenuto", "#1baf7a")]
ends = []
for k, lab, col in sel:
    e = RUNS[k]["equity"] / RUNS[k]["equity"].iloc[0] * 10000
    a1.plot(e.index, e, color=col, lw=2, label=lab)
    a2.plot(e.index, (e / e.cummax() - 1) * 100, color=col, lw=1.3)
    ends.append((float(e.iloc[-1]), lab, col))
yy = []
for v, lab, col in sorted(ends):
    y = v if not yy else max(v, yy[-1] * 1.25)
    yy.append(y)
    a1.annotate(f"{lab} · {usd(v)} $", (e.index[-1], v), xytext=(e.index[-1] + pd.Timedelta(days=40), y), fontsize=9, color=INK, va="center",
                arrowprops=dict(arrowstyle="-", color=col, lw=1.0))
a1.axvline(pd.Timestamp(A1), color=MUTED, lw=1, ls=(0, (4, 3)))
a1.set_yscale("log")
a1.set_yticks([5000, 10000, 20000, 50000, 100000, 200000])
a1.set_yticklabels(["5k", "10k", "20k", "50k", "100k", "200k"])
a1.minorticks_off()
a1.grid(axis="y", color=GRID, lw=0.8)
a1.legend(frameon=False, loc="lower right", fontsize=9, bbox_to_anchor=(0.76, 0.02))
a1.set_title("10.000 $ dal 01/2018 al 22/11/2026: a sinistra della linea la scelta dei parametri, a destra la verifica", loc="left", color=INK, fontsize=11, fontweight="bold")
a2.grid(axis="y", color=GRID, lw=0.8)
a2.set_title("Drawdown dal massimo (%)", loc="left", color=INK, fontsize=11, fontweight="bold")
a2.set_xlim(e.index[0], e.index[-1] + pd.Timedelta(days=820))
a2.set_xticks([pd.Timestamp(f"{y}-01-01") for y in range(2018, 2027)])
a2.set_xticklabels([str(y) for y in range(2018, 2027)])
fig.savefig(OUT / "confronto.png", dpi=160, bbox_inches="tight")
