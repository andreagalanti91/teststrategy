"""Report BTC: censimento degli indicatori, algoritmo composito long/short, sentiment, fotografia tecnica attuale, grafici."""
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

OUT = B.ROOT / "results" / "btc"
pct = lambda x, d=1: "n/d" if x is None or not np.isfinite(x) else f"{x * 100:+.{d}f}%".replace(".", ",")
usd = lambda x: f"{x:,.0f}".replace(",", ".")
num = lambda x, d=2: f"{x:.{d}f}".replace(".", ",")
T = []
d = B.load()
sig = B.signals(d)
sc = B.score(sig)
w = B.weekly(d)
c = d["close"]

# ------------------------------------------------------------------ B1 censimento
T.append("## B1 censimento\n")
T.append("| Indicatore | Famiglia | Long/short 2018–21 | DD | Long/short 2022–26 | DD | Solo long 2018–21 | Solo long 2022–26 | Trade | Vincenti | Regge in entrambi? |")
T.append("|---|---|---|---|---|---|---|---|---|---|---|")
cen = []
for k in sig.columns:
    r, rl = B.run(d, sig[k]), B.run(d, sig[k], allow_short=False)
    a, b, f = B.stats(r, B.IS0, B.IS1), B.stats(r, B.IS1, None), B.stats(r)
    al, bl = B.stats(rl, B.IS0, B.IS1), B.stats(rl, B.IS1, None)
    ok = "sì" if a["cagr"] > 0.10 and b["cagr"] > 0.10 else "solo long" if al["cagr"] > 0.10 and bl["cagr"] > 0.10 else "no"
    cen.append({"indicatore": k, "famiglia": B.FAMILY[k], "ls_is": a["cagr"], "ls_is_dd": a["dd"], "ls_oos": b["cagr"], "ls_oos_dd": b["dd"],
                "l_is": al["cagr"], "l_oos": bl["cagr"], "n": f["n"], "wr": f["wr"], "regge": ok})
    T.append(f"| {k} | {B.FAMILY[k]} | {pct(a['cagr'], 0)} | {pct(a['dd'], 0)} | {pct(b['cagr'], 0)} | {pct(b['dd'], 0)} | {pct(al['cagr'], 0)} | {pct(bl['cagr'], 0)} | "
             f"{f['n']} | {f['wr'] * 100:.0f}% | {ok} |")
pd.DataFrame(cen).to_csv(OUT / "censimento_indicatori.csv", index=False)
hold = B.run(d, pd.Series(1.0, d.index))
ha, hb = B.stats(hold, B.IS0, B.IS1), B.stats(hold, B.IS1, None)
T.append(f"| *BTC comprato e tenuto (spot)* | – | {pct(ha['cagr'], 0)} | {pct(ha['dd'], 0)} | {pct(hb['cagr'], 0)} | {pct(hb['dd'], 0)} | – | – | – | – | – |")

# ------------------------------------------------------------------ B2 algoritmo: scelta in IS
rows = []
for wk, tl, ts, ex in itertools.product([True, False], [0.25, 0.5, 0.75, 0.9], [0.25, 0.5, 0.75, 0.9, 9], [-0.25, 0.0, 0.25]):
    if ex >= tl or (ts < 9 and ex >= ts):
        continue
    r = B.run(d, B.composite(d, sc, tl, ts, ex, wk))
    a, b, f = B.stats(r, B.IS0, B.IS1), B.stats(r, B.IS1, None), B.stats(r)
    rows.append(dict(settimanale=wk, th_long=tl, th_short=ts, uscita=ex, is_cagr=a["cagr"], is_dd=a["dd"], is_mar=a["mar"], is_sharpe=a["sharpe"],
                     oos_cagr=b["cagr"], oos_dd=b["dd"], oos_sharpe=b["sharpe"], n=f["n"], wr=f["wr"]))
g = pd.DataFrame(rows)
g.to_csv(OUT / "griglia_composito.csv", index=False)
gs = g[g.th_short < 9]
best_ls = gs.sort_values("is_mar", ascending=False).iloc[0]
best_l = g[g.th_short == 9].sort_values("is_mar", ascending=False).iloc[0]
P_LS = dict(th_long=best_ls.th_long, th_short=best_ls.th_short, exit_at=best_ls.uscita, weekly_decision=bool(best_ls.settimanale))
P_L = dict(th_long=best_l.th_long, th_short=9, exit_at=best_l.uscita, weekly_decision=bool(best_l.settimanale))
pos_ls, pos_l = B.composite(d, sc, **P_LS), B.composite(d, sc, **P_L)
R = {"Long/short (scelto sul 2018–21)": B.run(d, pos_ls), "Solo long (scelto sul 2018–21)": B.run(d, pos_l), "BTC comprato e tenuto": hold}
vol = c.pct_change().rolling(30).std() * np.sqrt(365)
scale = (0.50 / vol).clip(upper=1.0).fillna(1.0)
R["Long/short con volatilità obiettivo 50%"] = B.run(d, pos_ls * scale)
R["Long/short, senza nuovi short con Fear & Greed < 20"] = B.run(d, B.composite(d, sc, fng_block=20, **P_LS))
T.append("\n## B2 algoritmo\n")
T.append(f"Parametri scelti sul 2018–21 (miglior rapporto rendimento/drawdown fra {len(g)} combinazioni): long con voto ≥ {num(P_LS['th_long'])}, "
         f"short con voto ≤ −{num(P_LS['th_short'])}, uscita quando il voto torna oltre {num(P_LS['exit_at'])}, decisione "
         f"{'settimanale' if P_LS['weekly_decision'] else 'giornaliera'}. Versione solo long: voto ≥ {num(P_L['th_long'])}, uscita sotto {num(P_L['exit_at'])}, "
         f"decisione {'settimanale' if P_L['weekly_decision'] else 'giornaliera'}.\n")
T.append("| Versione | 10.000 $ → (2018–2026) | CAGR | Max DD | Sharpe | Trade | Vincenti | Vincita / perdita media | 2018–21: CAGR / DD | 2022–26: CAGR / DD | Tempo a mercato |")
T.append("|---|---|---|---|---|---|---|---|---|---|---|")
for k, r in R.items():
    f, a, b = B.stats(r), B.stats(r, B.IS0, B.IS1), B.stats(r, B.IS1, None)
    T.append(f"| {k} | {usd(10000 * f['final'])} | {pct(f['cagr'])} | {pct(f['dd'])} | {num(f['sharpe'])} | {f['n']} | {f['wr'] * 100:.0f}% | {pct(f['avg_win'], 0)} / {pct(f['avg_loss'], 0)} | "
             f"{pct(a['cagr'], 0)} / {pct(a['dd'], 0)} | {pct(b['cagr'], 0)} / {pct(b['dd'], 0)} | {f['time'] * 100:.0f}% |")
T.append(f"\nRobustezza: delle {len(g)} combinazioni di soglie, il {(g.oos_cagr > 0).mean() * 100:.0f}% guadagna nel 2022–26; rendimento mediano 2022–26 "
         f"{pct(g.oos_cagr.median())} annuo con drawdown mediano {pct(g.oos_dd.median())}. Con gli short ammessi a soglia bassa (≤ 0,75) il rendimento mediano 2018–21 è "
         f"{pct(g[g.th_short <= 0.75].is_cagr.median())} annuo; senza short {pct(g[g.th_short == 9].is_cagr.median())}.")

w3s = {}
for k in list(R)[:2]:
    q = B.stats(R[k], "2021-01-01", "2026-11-10")
    w3s[k] = q
T.append("\n## B0 w3\n")
T.append("| Dal 01/2021 al 10/11/2026 | CAGR | Max DD | Trade | Vincenti |")
T.append("|---|---|---|---|---|")
for k, q in w3s.items():
    T.append(f"| {k} | {pct(q['cagr'])} | {pct(q['dd'])} | {q['n']} | {q['wr'] * 100:.0f}% |")
T.append("| W3 del repo radar, rischio 25% | +42,2% | −21,1% | 13 | 92% |")
T.append("| W3.1 del repo radar, rischio 10% | +18,6% | −9,8% | 13 | 92% |")
T.append("\n## B3 anni\n")
ys = list(range(2018, 2027))
T.append("| | " + " | ".join(map(str, ys)) + " |")
T.append("|---|" + "---|" * len(ys))
for k in list(R)[:3]:
    y = B.stats(R[k])["years"]
    T.append(f"| {k} | " + " | ".join(pct(y.get(v), 0) for v in ys) + " |")
tl = R["Long/short (scelto sul 2018–21)"]["trades"]
for side, lab in ((1, "Solo i trade long del long/short"), (-1, "Solo i trade short del long/short")):
    x = tl[tl.verso == side]
    T.append(f"| {lab} | " + " | ".join(pct(float(np.prod(1 + x[x.da.dt.year == v].ret) - 1), 0) if len(x[x.da.dt.year == v]) else "–" for v in ys) + " |")
tl.assign(da=tl.da.dt.date, a=tl.a.dt.date).to_csv(OUT / "trade_long_short.csv", index=False)

T.append("\n## B4 trade\n")
T.append("| Verso | Dal | Al | Giorni | Risultato |")
T.append("|---|---|---|---|---|")
for q in tl.itertuples():
    T.append(f"| {'Long' if q.verso > 0 else 'Short'} | {q.da.date()} | {q.a.date()} | {q.giorni} | {pct(q.ret)} |")
sh = tl[tl.verso < 0]
lg = tl[tl.verso > 0]
T.append(f"\nLong: {len(lg)} trade, {(lg.ret > 0).mean() * 100:.0f}% vincenti, composto x{float(np.prod(1 + lg.ret)):.1f}. ".replace(".", ",", 1) +
         f"Short: {len(sh)} trade, {(sh.ret > 0).mean() * 100:.0f}% vincenti, composto x{float(np.prod(1 + sh.ret)):.2f}.".replace(".", ",", 1))

T.append("\n## B5 leva\n")
T.append("| Leva | 10.000 $ → | CAGR | Max DD | 2018–21: CAGR / DD | 2022–26: CAGR / DD | Anno peggiore | DD entro −35%? |")
T.append("|---|---|---|---|---|---|---|---|")
for lev in (0.5, 0.75, 1, 1.5, 2, 3, 5):
    r = B.run(d, pos_ls, lev=lev)
    f, a, b = B.stats(r), B.stats(r, B.IS0, B.IS1), B.stats(r, B.IS1, None)
    T.append(f"| {num(lev, 2).rstrip('0').rstrip(',')}x | {usd(10000 * f['final'])} | {pct(f['cagr'])} | {pct(f['dd'])} | {pct(a['cagr'], 0)} / {pct(a['dd'], 0)} | "
             f"{pct(b['cagr'], 0)} / {pct(b['dd'], 0)} | {pct(f['worst_year'], 0)} | {'sì' if f['dd'] >= -0.35 else 'no'} |")

# ------------------------------------------------------------------ B6 sentiment: studio a eventi
T.append("\n## B6 sentiment\n")
fng = d["fng"].loc["2018-02-01":]
fwd = {h: c.shift(-h) / c - 1 for h in (7, 30, 90)}
def ev(mask, lab):
    first = mask & ~mask.shift(1, fill_value=False)                      # primo giorno di ogni episodio
    idx = first[first].index
    cells = []
    for h in (7, 30, 90):
        x = fwd[h].reindex(idx).dropna()
        cells.append(f"{pct(x.mean(), 0)} / {pct(x.median(), 0)} / {(x > 0).mean() * 100:.0f}%" if len(x) else "n/d")
    T.append(f"| {lab} | {len(idx)} | " + " | ".join(cells) + " |")
T.append("| Condizione (primo giorno dell'episodio) | Episodi | Dopo 7 giorni: media / mediana / positivi | Dopo 30 giorni | Dopo 90 giorni |")
T.append("|---|---|---|---|---|")
allm = pd.Series(True, fng.index)
cells = []
for h in (7, 30, 90):
    x = fwd[h].reindex(fng.index).dropna()
    cells.append(f"{pct(x.mean(), 0)} / {pct(x.median(), 0)} / {(x > 0).mean() * 100:.0f}%")
T.append(f"| Tutti i giorni dal 02/2018 | {len(fng)} | " + " | ".join(cells) + " |")
ev(fng <= 25, "Fear & Greed ≤ 25 (paura estrema)")
ev(fng <= 15, "Fear & Greed ≤ 15")
ev(fng <= 10, "Fear & Greed ≤ 10")
below = c < B.sma(c, 200)
ev((fng <= 15) & below.reindex(fng.index), "Fear & Greed ≤ 15 con prezzo sotto la SMA 200")
ev((fng <= 15) & ~below.reindex(fng.index), "Fear & Greed ≤ 15 con prezzo sopra la SMA 200")
ev(fng >= 75, "Fear & Greed ≥ 75 (avidità estrema)")
ev(fng >= 90, "Fear & Greed ≥ 90")
f7 = d["funding"].rolling(7).mean().loc["2020-01-01":]
ev((f7 < 0).reindex(fng.index, fill_value=False), "Funding medio a 7 giorni negativo (dal 2020)")

# ------------------------------------------------------------------ B7 fotografia tecnica
T.append("\n## B7 oggi\n")
last, px = d.index[-1], float(c.iloc[-1])
ath, ath_d = float(d["high"].max()), d["high"].idxmax()
wc = w["close"]
m_d, s_d = B.macd(c)
m_w, s_w = B.macd(wc)
a_, pdi, mdi = B.adx(d)
mid, ub, lb = B.bollinger(c)
at = B.atr(d)
rows7 = [("Prezzo (chiusura del " + str(last.date()) + ")", f"{usd(px)} $", ""),
         ("Massimo storico", f"{usd(ath)} $ il {ath_d.date()}", f"prezzo a {pct(px / ath - 1, 0)} dal massimo"),
         ("SMA 50 giorni", f"{usd(B.sma(c, 50).iloc[-1])} $", "prezzo " + pct(px / B.sma(c, 50).iloc[-1] - 1, 0)),
         ("SMA 200 giorni", f"{usd(B.sma(c, 200).iloc[-1])} $", "prezzo " + pct(px / B.sma(c, 200).iloc[-1] - 1, 0) + "; SMA 50 " + ("sopra" if B.sma(c, 50).iloc[-1] > B.sma(c, 200).iloc[-1] else "sotto") + " la SMA 200"),
         ("SMA 40 settimane", f"{usd(B.sma(wc, 40).iloc[-1])} $", "chiusura settimanale " + pct(wc.iloc[-1] / B.sma(wc, 40).iloc[-1] - 1, 0)),
         ("SMA 200 settimane", f"{usd(B.sma(wc, 200).iloc[-1])} $", "prezzo " + pct(px / B.sma(wc, 200).iloc[-1] - 1, 0)),
         ("RSI 14 giornaliero / settimanale", f"{B.rsi(c).iloc[-1]:.0f} / {B.rsi(wc).iloc[-1]:.0f}", "sotto 30 = ipervenduto"),
         ("MACD giornaliero / settimanale", ("sopra" if m_d.iloc[-1] > s_d.iloc[-1] else "sotto") + " / " + ("sopra" if m_w.iloc[-1] > s_w.iloc[-1] else "sotto") + " il segnale",
          "MACD settimanale " + ("positivo" if m_w.iloc[-1] > 0 else "negativo")),
         ("ADX 14 con +DI / −DI", f"{a_.iloc[-1]:.0f} ({pdi.iloc[-1]:.0f} / {mdi.iloc[-1]:.0f})", "sopra 25 = trend forte; −DI sopra +DI = ribassista"),
         ("ATR 14 giornaliero", f"{usd(at.iloc[-1])} $", f"{at.iloc[-1] / px * 100:.1f}% del prezzo".replace(".", ",")),
         ("Bande di Bollinger (20, 2)", f"{usd(lb.iloc[-1])} – {usd(ub.iloc[-1])} $", "prezzo " + ("sotto la banda inferiore" if px < lb.iloc[-1] else "dentro le bande" if px < ub.iloc[-1] else "sopra la banda superiore")),
         ("Canale di Donchian a 20 settimane", f"{usd(w['low'].iloc[-20:].min())} – {usd(w['high'].iloc[-20:].max())} $", ""),
         ("Variazione a 7 / 30 / 90 giorni", f"{pct(c.pct_change(7).iloc[-1], 0)} / {pct(c.pct_change(30).iloc[-1], 0)} / {pct(c.pct_change(90).iloc[-1], 0)}", "")]
T.append("| Misura | Valore | Lettura |")
T.append("|---|---|---|")
for a1, b1, c1 in rows7:
    T.append(f"| {a1} | {b1} | {c1} |")

# livelli: minimi/massimi di swing settimanali, Fibonacci del ciclo, nodi di volume
T.append("\n## B8 livelli\n")
lo_cycle = float(d.loc["2022-06-01":"2023-03-01", "low"].min())
lo_d = d.loc["2022-06-01":"2023-03-01", "low"].idxmin()
lev_rows = [(ath, "massimo storico"), (float(d.loc[:"2022-01-01", "high"].max()), "massimo del ciclo 2021")]
for f_ in (0.382, 0.5, 0.618, 0.786):
    lev_rows.append((ath - f_ * (ath - lo_cycle), f"ritracciamento di Fibonacci {f_ * 100:.1f}% del ciclo".replace(".", ",")))
K = 5
wl, wh = w["low"].to_numpy(), w["high"].to_numpy()
for i in range(len(w) - 160, len(w) - K):
    if wl[i] == wl[i - K:i + K + 1].min():
        lev_rows.append((float(wl[i]), f"minimo di swing settimanale ({w.index[i].date()})"))
    if wh[i] == wh[i - K:i + K + 1].max():
        lev_rows.append((float(wh[i]), f"massimo di swing settimanale ({w.index[i].date()})"))
b15 = pd.read_csv(B.ROOT / "data" / "intraday" / "binance_spot_BTCUSDT_15m.csv.gz")
b15["ts"] = pd.to_datetime(b15["ts"], format="mixed")
b15 = b15[b15.ts >= "2024-01-01"]
bins = (b15.close // 2000) * 2000 + 1000
vp = b15.groupby(bins).volume.sum().sort_values(ascending=False)
for lvl in vp.index[:4]:
    lev_rows.append((float(lvl), f"nodo di volume dal 2024 (fascia {usd(lvl - 1000)}–{usd(lvl + 1000)})"))
lev_rows.append((float(B.sma(wc, 200).iloc[-1]), "SMA 200 settimane"))
lev_rows.append((float(B.sma(wc, 40).iloc[-1]), "SMA 40 settimane"))
lev_rows.append((float(B.sma(c, 200).iloc[-1]), "SMA 200 giorni"))
lv = pd.DataFrame(lev_rows, columns=["livello", "cosa"]).sort_values("livello", ascending=False)
lv = lv[(lv.livello > px * 0.6) & (lv.livello < px * 1.45)]
lv.to_csv(OUT / "livelli.csv", index=False)
T.append("| Livello | Distanza dal prezzo | Che cos'è | Ruolo |")
T.append("|---|---|---|---|")
done = False
for q in lv.itertuples():
    if not done and q.livello < px:
        T.append(f"| **{usd(px)} $** | – | **prezzo attuale** | – |")
        done = True
    T.append(f"| {usd(q.livello)} $ | {pct(q.livello / px - 1, 0)} | {q.cosa} | {'resistenza' if q.livello > px else 'supporto'} |")

# voto degli indicatori oggi e stato dell'algoritmo
T.append("\n## B9 voto\n")
T.append("| Indicatore | Famiglia | Oggi |")
T.append("|---|---|---|")
for k in sig.columns:
    v = sig[k].iloc[-1]
    T.append(f"| {k} | {B.FAMILY[k]} | {'long' if v > 0 else 'short' if v < 0 else 'neutro'} |")
nl, ns = int((sig[B.TREND_SET].iloc[-1] > 0).sum()), int((sig[B.TREND_SET].iloc[-1] < 0).sum())
cur = pos_ls.iloc[-1]
since = pos_ls[(pos_ls != cur)].index[-1] + pd.Timedelta(days=1) if (pos_ls != cur).any() else pos_ls.index[0]
T.append(f"\nVoto degli indicatori di trend: {nl} long, {ns} short su {len(B.TREND_SET)}: punteggio {num(sc.iloc[-1])}. "
         f"Posizione dell'algoritmo long/short: **{'long' if cur > 0 else 'short' if cur < 0 else 'fuori'}** dal {since.date()}"
         + (f" (prezzo d'ingresso {usd(c.loc[since - pd.Timedelta(days=1)])} $, risultato in corso {pct(cur * (px / c.loc[since - pd.Timedelta(days=1)] - 1))})." if cur != 0 else ".")
         + f" Versione solo long: **{'long' if pos_l.iloc[-1] > 0 else 'fuori'}**.")

# sentiment oggi
T.append("\n## C1 sentiment oggi\n")
met = pd.read_csv(B.ROOT / "data" / "btc" / "metrics.csv", parse_dates=[0], index_col=0)
fn = d["fng"].dropna()
streak = int((fn[::-1] <= 25).cumprod().sum())
T.append("| Misura | Valore | Lettura |")
T.append("|---|---|---|")
T.append(f"| Fear & Greed (alternative.me) | {fn.iloc[-1]:.0f} | paura estrema; più basso solo nel {num((fn < fn.iloc[-1]).mean() * 100, 1)}% dei giorni dal 2018; sotto 25 da {streak} giorni |")
T.append(f"| Fear & Greed, media a 30 giorni | {fn.iloc[-30:].mean():.0f} | un anno fa {fn.iloc[-395:-365].mean():.0f} |")
fraw = pd.read_csv(B.ROOT / "data" / "btc" / "funding.csv", parse_dates=[0], index_col=0)["funding"].dropna()
f7n, f30n = fraw.iloc[-7:].mean(), fraw.iloc[-30:].mean()
T.append(f"| Funding del perp, media 7 / 30 giorni | {pct(f7n * 365, 1)} / {pct(f30n * 365, 1)} annuo | {'intorno a zero: nessun eccesso da una parte' if abs(f7n * 365) < 0.02 else 'negativo: gli short pagano i long' if f7n < 0 else 'positivo: i long pagano gli short'} |")
T.append(f"| Rapporto long/short dei conti (Binance) | {met['global_ls'].iloc[-1]:.2f} | media a un anno {met['global_ls'].iloc[-365:].mean():.2f}; sopra 1 = più conti long che short |".replace(".", ","))
T.append(f"| Rapporto long/short dei grandi conti, per posizione | {met['top_ls_pos'].iloc[-1]:.2f} | media a un anno {met['top_ls_pos'].iloc[-365:].mean():.2f} |".replace(".", ","))
oi = met["oi"]
T.append(f"| Open interest (BTC, Binance) | {usd(oi.iloc[-1])} | {pct(oi.iloc[-1] / oi.iloc[-31] - 1, 0)} in 30 giorni, {pct(oi.iloc[-1] / oi.iloc[-366] - 1, 0)} in un anno |")
T.append(f"| Volatilità realizzata a 30 giorni | {vol.iloc[-1] * 100:.0f}% annua | media a un anno {vol.iloc[-365:].mean() * 100:.0f}% |")
(OUT / "tables.md").write_text("\n".join(T) + "\n")
print("\n".join(T))

# ------------------------------------------------------------------ grafici
INK, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb"
BLUE, ORANGE, AQUA, YELLOW, RED = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#d03b3b"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED,
                     "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "savefig.facecolor": SURF})
ww = w.loc["2023-01-01":]
fig, ax = plt.subplots(3, 1, figsize=(10, 9), sharex=True, gridspec_kw={"height_ratios": [4, 1.3, 1.3], "hspace": 0.14})
a0 = ax[0]
a0.vlines(ww.index, ww.low, ww.high, color=BLUE, lw=0.8, alpha=0.45)
a0.plot(ww.index, ww.close, color=BLUE, lw=2, label="Chiusura settimanale")
a0.plot(ww.index, B.sma(wc, 40).reindex(ww.index), color=ORANGE, lw=1.6, label="SMA 40 settimane")
a0.plot(ww.index, B.sma(wc, 200).reindex(ww.index), color=AQUA, lw=1.6, label="SMA 200 settimane")
for lvl, lab, dy in ((ath - 0.5 * (ath - lo_cycle), "Fibonacci 50%", 16), (float(d.loc[:"2022-01-01", "high"].max()), "massimo 2021", 2),
                     (ath - 0.618 * (ath - lo_cycle), "Fibonacci 61,8%", -14)):
    a0.axhline(lvl, color=MUTED, lw=0.9, ls=(0, (4, 3)))
    a0.annotate(f"{lab} · {usd(lvl)}", (ww.index[-1], lvl), xytext=(8, dy), textcoords="offset points", fontsize=9, color=INK, va="center")
a0.annotate(f"prezzo · {usd(px)}", (ww.index[-1], px), xytext=(8, -4), textcoords="offset points", fontsize=9, color=INK, va="center", fontweight="bold")
a0.set_title("BTC settimanale: prezzo, medie e livelli", loc="left", color=INK, fontsize=12, fontweight="bold")
a0.legend(frameon=False, loc="upper left", fontsize=9)
a0.grid(axis="y", color=GRID, lw=0.8)
rw = B.rsi(wc).reindex(ww.index)
ax[1].plot(ww.index, rw, color=BLUE, lw=1.6)
for v in (30, 50, 70):
    ax[1].axhline(v, color=MUTED, lw=0.8, ls=(0, (4, 3)))
ax[1].set_ylim(15, 90)
ax[1].set_title("RSI settimanale (14)", loc="left", color=INK, fontsize=10, fontweight="bold")
hist = (m_w - s_w).reindex(ww.index)
ax[2].bar(ww.index, hist, width=5, color=np.where(hist >= 0, BLUE, RED))
ax[2].axhline(0, color=MUTED, lw=0.8)
ax[2].set_title("Istogramma del MACD settimanale (12, 26, 9)", loc="left", color=INK, fontsize=10, fontweight="bold")
ax[2].set_xlim(ww.index[0], ww.index[-1] + pd.Timedelta(days=230))
fig.savefig(OUT / "btc_tecnica.png", dpi=160, bbox_inches="tight")
plt.close(fig)

fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 7.6), sharex=True, gridspec_kw={"height_ratios": [3, 2], "hspace": 0.12})
for (lab, r), col in zip(list(R.items())[:3], (BLUE, ORANGE, AQUA)):
    e = r["equity"] / r["equity"].iloc[0] * 10000
    a1.plot(e.index, e, color=col, lw=2, label=lab)
    a2.plot(e.index, (e / e.cummax() - 1) * 100, color=col, lw=1.3)
ends = sorted((float(r["equity"].iloc[-1] / r["equity"].iloc[0] * 10000), lab) for lab, r in list(R.items())[:3])
yy = []
for v, lab in ends:
    y = v if not yy else max(v, yy[-1] * 1.22)
    yy.append(y)
    a1.annotate(f"{lab.split(' (')[0]} · {usd(v)} $", (e.index[-1], v), xytext=(e.index[-1] + pd.Timedelta(days=30), y), fontsize=9, color=INK, va="center",
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
a1.axvline(pd.Timestamp(B.IS1), color=MUTED, lw=1, ls=(0, (4, 3)))
a1.annotate("← scelta dei parametri | verifica →", (pd.Timestamp(B.IS1), 1.0), xycoords=("data", "axes fraction"), xytext=(0, -12), textcoords="offset points",
            ha="center", fontsize=9, color=MUTED)
a1.set_yscale("log")
a1.set_yticks([5000, 10000, 20000, 50000, 100000, 200000])
a1.set_yticklabels(["5k", "10k", "20k", "50k", "100k", "200k"])
a1.minorticks_off()
a1.grid(axis="y", color=GRID, lw=0.8)
a1.legend(frameon=False, loc="lower right", fontsize=9, bbox_to_anchor=(0.76, 0.02))
a1.set_title("10.000 $ dal 01/2018 al 22/11/2026 (scala logaritmica, costi inclusi)", loc="left", color=INK, fontsize=12, fontweight="bold")
a2.grid(axis="y", color=GRID, lw=0.8)
a2.set_title("Drawdown dal massimo (%)", loc="left", color=INK, fontsize=11, fontweight="bold")
a2.set_xlim(e.index[0], e.index[-1] + pd.Timedelta(days=820))
a2.set_xticks([pd.Timestamp(f"{y}-01-01") for y in range(2018, 2027)])
a2.set_xticklabels([str(y) for y in range(2018, 2027)])
fig.savefig(OUT / "btc_algoritmo.png", dpi=160, bbox_inches="tight")
