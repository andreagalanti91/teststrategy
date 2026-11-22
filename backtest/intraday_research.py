"""Ricerca intraday su BTC: tre famiglie di regole, griglia valutata SOLO su 2018-2021 (IS), poi verifica 2022-2026 (OOS)."""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from intraday import DATA, atr, backtest, daily_regime, hourly, load, rsi, stats, weekly_regime

IS0, IS1, OOS1 = "2018-03-01", "2022-01-01", "2026-11-22"


def features(b: pd.DataFrame) -> pd.DataFrame:
    h = hourly(b)
    h["atr"] = atr(h)
    h["rsi"] = rsi(h["close"])
    for n in (50, 100, 200):
        h[f"reg{n}"] = daily_regime(b, n).reindex(h.index, method="ffill")
    old = pd.read_csv(DATA / "bitstamp_btcusd_1d_2014_2017.csv", parse_dates=[0], index_col=0)["close"]
    h["regw"] = weekly_regime(b, old).reindex(h.index, method="ffill")
    h4 = b.resample("4h").agg({"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}).dropna()
    h4.index = h4.index + pd.Timedelta(hours=4)
    h["rsi4"], h["atr4"] = rsi(h4["close"]).reindex(h.index), atr(h4).reindex(h.index)      # valori solo alle chiusure 4h
    for n in (24, 48, 72):
        h[f"hh{n}"] = h["high"].rolling(n).max().shift()
        h[f"ll{n}"] = h["low"].rolling(n).min().shift()
    return h


def sig_pullback(h, reg=200, thr=30, k_tp=1.0, k_sl=3.0, hold=24, sides="both"):
    """Ritracciamento nel verso del trend: long quando l'RSI orario scende sotto thr con trend giornaliero rialzista;
    short quando sale sopra 100-thr con trend ribassista."""
    r, p, g = h["rsi"], h["rsi"].shift(), h[f"reg{reg}"]
    side = ((g > 0) & (r < thr) & (p >= thr)).astype(int) - ((g < 0) & (r > 100 - thr) & (p <= 100 - thr)).astype(int)
    if sides == "long":
        side = side.clip(lower=0)
    if sides == "short":
        side = side.clip(upper=0)
    s = pd.DataFrame({"side": side, "tp": k_tp * h["atr"], "sl": k_sl * h["atr"], "hold": hold})
    return s[s.side != 0]


def sig_breakout(h, reg=200, n=48, k_tp=1.0, k_sl=3.0, hold=24, sides="both"):
    """Rottura nel verso del trend: long quando la chiusura oraria supera il massimo delle n ore precedenti con trend
    giornaliero rialzista; short specchiato."""
    c, g = h["close"], h[f"reg{reg}"]
    up = (c > h[f"hh{n}"]) & (c.shift() <= h[f"hh{n}"].shift())
    dn = (c < h[f"ll{n}"]) & (c.shift() >= h[f"ll{n}"].shift())
    side = ((g > 0) & up).astype(int) - ((g < 0) & dn).astype(int)
    if sides == "long":
        side = side.clip(lower=0)
    if sides == "short":
        side = side.clip(upper=0)
    s = pd.DataFrame({"side": side, "tp": k_tp * h["atr"], "sl": k_sl * h["atr"], "hold": hold})
    return s[s.side != 0]


def sig_hour(h, reg=200, hour=21, hold=2, k_sl=3.0):
    """Stagionalita' oraria: long alle `hour` UTC per `hold` ore, solo con trend giornaliero rialzista."""
    side = ((h.index.hour == hour) & (h[f"reg{reg}"] > 0)).astype(int)
    s = pd.DataFrame({"side": side, "tp": 50 * h["atr"], "sl": k_sl * h["atr"], "hold": hold}, index=h.index)
    return s[s.side != 0]


def sig_limit(h, reg="w", k_in=1.5, k_tp=1.0, k_sl=3.0, hold=24, sides="both"):
    """Ordine limite contro il movimento, nel verso del trend: a ogni chiusura oraria con trend rialzista si mette un
    acquisto limite a k_in ATR sotto la chiusura, valido un'ora (specchiato per gli short con trend ribassista)."""
    g = h[f"reg{reg}"]
    side = (g > 0).astype(int) - (g < 0).astype(int)
    if sides == "long":
        side = side.clip(lower=0)
    if sides == "short":
        side = side.clip(upper=0)
    s = pd.DataFrame({"side": side, "limit": h["close"] - side * k_in * h["atr"], "valid": 1, "tp": k_tp * h["atr"],
                      "sl": k_sl * h["atr"], "hold": hold})
    return s[(s.side != 0) & s.limit.notna()]


def sig_pull4h(h, reg="w", thr=35, k_tp=1.0, k_sl=3.0, hold=48, sides="both"):
    """Ritracciamento a 4 ore nel verso del trend: long quando l'RSI a 4 ore chiude sotto thr con trend rialzista; short
    quando chiude sopra 100-thr con trend ribassista. Stop e target in ATR a 4 ore."""
    g, r = h[f"reg{reg}"], h["rsi4"]
    side = ((g > 0) & (r < thr)).astype(int) - ((g < 0) & (r > 100 - thr)).astype(int)
    if sides == "long":
        side = side.clip(lower=0)
    if sides == "short":
        side = side.clip(upper=0)
    s = pd.DataFrame({"side": side, "tp": k_tp * h["atr4"], "sl": k_sl * h["atr4"], "hold": hold})
    return s[s.side != 0]


def sig_placebo(h, like: pd.DataFrame, reg: int, rng) -> pd.DataFrame:
    """Stesso numero di ingressi, stessi stop/target/durata e stesso verso del trend, ma in ore scelte a caso."""
    g = h[f"reg{reg}"]
    ok = h.index[(g != 0) & g.notna() & h["atr"].notna() & (h.index >= like.index[0]) & (h.index <= like.index[-1])]
    pick = np.sort(rng.choice(len(ok), size=min(len(like), len(ok)), replace=False))
    t = ok[pick]
    k_tp, k_sl = float((like["tp"] / h["atr"].reindex(like.index)).median()), float((like["sl"] / h["atr"].reindex(like.index)).median())
    return pd.DataFrame({"side": g.reindex(t).astype(int), "tp": k_tp * h["atr"].reindex(t), "sl": k_sl * h["atr"].reindex(t),
                         "hold": int(like["hold"].iloc[0])}, index=t)


GRIDS = {
    "pullback": (sig_pullback, {"reg": [50, 100, 200], "thr": [25, 30, 35], "k_tp": [0.75, 1.0, 1.5, 2.0], "k_sl": [2.0, 3.0, 4.0], "hold": [24, 48]}),
    "breakout": (sig_breakout, {"reg": [50, 100, 200], "n": [24, 48, 72], "k_tp": [0.75, 1.0, 1.5, 2.0], "k_sl": [2.0, 3.0, 4.0], "hold": [24, 48]}),
    "limite": (sig_limit, {"reg": ["w", 50, 200], "k_in": [1.0, 1.5, 2.0, 2.5], "k_tp": [0.5, 1.0, 1.5], "k_sl": [2.0, 3.0, 4.0], "hold": [12, 24, 48]}),
    "pull4h": (sig_pull4h, {"reg": ["w", 50, 200], "thr": [30, 35, 40], "k_tp": [0.75, 1.0, 1.5, 2.0], "k_sl": [2.0, 3.0, 4.0], "hold": [24, 48, 72]}),
    "ora": (sig_hour, {"reg": [50, 100, 200], "hour": list(range(24)), "hold": [2, 4], "k_sl": [3.0]}),
}


def run_grid(b, h, fam: str) -> pd.DataFrame:
    fn, grid = GRIDS[fam]
    rows = []
    for vals in itertools.product(*grid.values()):
        p = dict(zip(grid.keys(), vals))
        t = backtest(b, fn(h, **p))
        a, o = stats(t, 1.0, IS0, IS1), stats(t, 1.0, IS1, OOS1)
        rows.append({"famiglia": fam, **{f"p_{k}": v for k, v in p.items()},
                     **{f"is_{k}": a.get(k) for k in ("n", "wr", "exp", "pf", "cagr", "dd", "tstat")},
                     **{f"oos_{k}": o.get(k) for k in ("n", "wr", "exp", "pf", "cagr", "dd", "tstat")}})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    b = load("binance")
    h = features(b)
    out = Path(__file__).resolve().parent.parent / "results" / "intraday"
    out.mkdir(parents=True, exist_ok=True)
    for fam in (sys.argv[1:] or GRIDS):
        g = run_grid(b, h, fam)
        g.to_csv(out / f"griglia_{fam}.csv", index=False)
        ok = g[(g.is_wr >= 0.65) & (g.is_n >= 100)] if fam != "ora" else g
        print(f"\n== {fam}: {len(g)} configurazioni; IS con WR>=65%: {len(ok)}; IS exp>0: {(g.is_exp > 0).sum()}; "
              f"IS exp>0 e OOS exp>0: {((g.is_exp > 0) & (g.oos_exp > 0)).sum()}; corr(IS exp, OOS exp) = {g.is_exp.corr(g.oos_exp):.2f}")
        print(ok.sort_values("is_tstat", ascending=False).head(8).round(4).to_string())
