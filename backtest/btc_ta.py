"""Laboratorio di analisi tecnica su BTC: dati, indicatori, motore long/short, censimento degli indicatori."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
IS0, IS1, END = "2018-01-01", "2022-01-01", "2026-11-22"
COST = 0.0010                    # OKX: 0,05-0,08% commissione + slippage, per lato
FUND_DEFAULT = 0.0003            # 0,01% ogni 8 ore, usato dove manca lo storico (prima del 2020)


# ------------------------------------------------------------------ dati
def load() -> pd.DataFrame:
    """Giornaliero BTC: Bitstamp 2014-08/2017 (solo per scaldare gli indicatori) + Binance spot dalle candele a 15 minuti."""
    b = pd.read_csv(ROOT / "data" / "intraday" / "binance_spot_BTCUSDT_15m.csv.gz")
    b["ts"] = pd.to_datetime(b["ts"], format="mixed").astype("datetime64[ns]")
    b = b.set_index("ts").sort_index()
    d = b.resample("1D").agg({"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}).dropna()
    d = d[d.index >= "2017-08-18"]
    old = pd.read_csv(ROOT / "data" / "intraday" / "bitstamp_btcusd_1d_2014_2017.csv", parse_dates=[0], index_col=0)
    old.index = old.index.astype("datetime64[ns]")
    d = pd.concat([old[old.index < d.index[0]][["open", "high", "low", "close", "volume"]], d])
    d = d[d.index <= END]
    f = pd.read_csv(ROOT / "data" / "btc" / "funding.csv", parse_dates=[0], index_col=0)["funding"]
    d["funding"] = f.reindex(d.index).fillna(FUND_DEFAULT)
    g = pd.read_csv(ROOT / "data" / "btc" / "fng.csv", parse_dates=[0], index_col=0)["fng"]
    d["fng"] = g.reindex(d.index).ffill(limit=3)
    return d


def weekly(d: pd.DataFrame) -> pd.DataFrame:
    w = d.resample("W-SUN").agg({"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}).dropna()
    return w[w.index <= d.index[-1]]                      # solo settimane chiuse


def to_daily(s: pd.Series, d: pd.DataFrame) -> pd.Series:
    """Valore settimanale (noto alla chiusura della domenica) riportato sui giorni: vale da quella domenica in poi."""
    return s.reindex(d.index, method="ffill")


# ------------------------------------------------------------------ indicatori
def sma(s, n): return s.rolling(n).mean()
def ema(s, n): return s.ewm(span=n, adjust=False).mean()


def rsi(c, n=14):
    x = c.diff()
    up, dn = x.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean(), (-x.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / dn)


def macd(c, f=12, s=26, g=9):
    m = ema(c, f) - ema(c, s)
    return m, ema(m, g)


def atr(d, n=14):
    c = d["close"]
    tr = pd.concat([d["high"] - d["low"], (d["high"] - c.shift()).abs(), (d["low"] - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def adx(d, n=14):
    up, dn = d["high"].diff(), -d["low"].diff()
    plus = pd.Series(np.where((up > dn) & (up > 0), up, 0.0), d.index)
    minus = pd.Series(np.where((dn > up) & (dn > 0), dn, 0.0), d.index)
    a = atr(d, n)
    pdi, mdi = 100 * plus.ewm(alpha=1 / n, adjust=False).mean() / a, 100 * minus.ewm(alpha=1 / n, adjust=False).mean() / a
    dx = 100 * (pdi - mdi).abs() / (pdi + mdi)
    return dx.ewm(alpha=1 / n, adjust=False).mean(), pdi, mdi


def obv(d):
    return (np.sign(d["close"].diff()).fillna(0) * d["volume"]).cumsum()


def bollinger(c, n=20, k=2.0):
    m, s = sma(c, n), c.rolling(n).std()
    return m, m + k * s, m - k * s


def donchian_state(d, n):
    """+1 dall'ultima chiusura sopra il massimo delle n barre precedenti, -1 dall'ultima sotto il minimo."""
    hi, lo = d["high"].rolling(n).max().shift(), d["low"].rolling(n).min().shift()
    s = pd.Series(np.where(d["close"] > hi, 1.0, np.where(d["close"] < lo, -1.0, np.nan)), d.index)
    return s.ffill().fillna(0.0)


def supertrend(d, n=10, k=3.0):
    a = atr(d, n)
    mid = (d["high"] + d["low"]) / 2
    ub, lb = (mid + k * a).to_numpy().copy(), (mid - k * a).to_numpy().copy()
    c = d["close"].to_numpy()
    st, dirn = np.zeros(len(c)), np.ones(len(c))
    for i in range(1, len(c)):
        if not np.isfinite(ub[i - 1]):
            continue
        ub[i] = min(ub[i], ub[i - 1]) if c[i - 1] <= ub[i - 1] else ub[i]
        lb[i] = max(lb[i], lb[i - 1]) if c[i - 1] >= lb[i - 1] else lb[i]
        dirn[i] = 1 if c[i] > ub[i - 1] else -1 if c[i] < lb[i - 1] else dirn[i - 1]
    return pd.Series(dirn, d.index)


def ichimoku_state(d):
    h, l, c = d["high"], d["low"], d["close"]
    ten, kij = (h.rolling(9).max() + l.rolling(9).min()) / 2, (h.rolling(26).max() + l.rolling(26).min()) / 2
    sa, sb = ((ten + kij) / 2).shift(26), ((h.rolling(52).max() + l.rolling(52).min()) / 2).shift(26)
    top, bot = pd.concat([sa, sb], axis=1).max(axis=1), pd.concat([sa, sb], axis=1).min(axis=1)
    return pd.Series(np.where(c > top, 1.0, np.where(c < bot, -1.0, 0.0)), d.index)


def hyst(x: pd.Series, up: float, dn: float) -> pd.Series:
    """+1 sopra `up`, -1 sotto `dn`, altrimenti mantiene lo stato."""
    out, cur = [], 0.0
    for v in x.to_numpy():
        cur = 1.0 if v > up else -1.0 if v < dn else cur
        out.append(cur)
    return pd.Series(out, x.index)


def signals(d: pd.DataFrame) -> pd.DataFrame:
    """Posizione suggerita da ogni indicatore preso da solo: +1 long, -1 short, 0 fuori. Dato noto alla chiusura del giorno."""
    c, w = d["close"], weekly(d)
    wc = w["close"]
    s = pd.DataFrame(index=d.index)
    sgn = lambda x: pd.Series(np.sign(x), x.index).fillna(0.0)
    # trend
    s["Prezzo vs SMA 200 giorni"] = sgn(c - sma(c, 200))
    s["SMA 50 vs SMA 200 (golden/death cross)"] = sgn(sma(c, 50) - sma(c, 200))
    s["EMA 20 vs EMA 50"] = sgn(ema(c, 20) - ema(c, 50))
    s["Prezzo vs SMA 40 settimane"] = to_daily(sgn(wc - sma(wc, 40)), d)
    s["Supertrend (10, 3)"] = supertrend(d)
    s["Ichimoku: sopra/sotto la nuvola"] = ichimoku_state(d)
    a, pdi, mdi = adx(d)
    s["ADX > 25 con +DI/−DI"] = np.where(a > 25, np.sign(pdi - mdi), 0.0)
    # momentum
    m, sg = macd(c)
    s["MACD giornaliero vs segnale"] = sgn(m - sg)
    mw, sgw = macd(wc)
    s["MACD settimanale vs segnale"] = to_daily(sgn(mw - sgw), d)
    s["RSI giornaliero vs 50"] = sgn(rsi(c) - 50)
    s["RSI settimanale vs 50"] = to_daily(sgn(rsi(wc) - 50), d)
    s["Momentum a 90 giorni"] = sgn(c.pct_change(90))
    # rotture
    s["Donchian 20 giorni"] = donchian_state(d, 20)
    s["Donchian 55 giorni"] = donchian_state(d, 55)
    s["Donchian 20 settimane"] = to_daily(donchian_state(w, 20), d)
    mid, ub, lb = bollinger(c)
    s["Bollinger: rottura delle bande"] = pd.Series(np.where(c > ub, 1.0, np.where(c < lb, -1.0, np.nan)), d.index).ffill().fillna(0.0)
    # volume
    o = obv(d)
    s["OBV vs sua SMA 100"] = sgn(o - sma(o, 100))
    # ritorno alla media (contrarian)
    s["RSI 30/70 contrarian"] = -hyst(rsi(c), 70, 30)
    s["Bollinger contrarian"] = -pd.Series(np.where(c > ub, 1.0, np.where(c < lb, -1.0, np.nan)), d.index).ffill().fillna(0.0)
    # sentiment
    s["Fear & Greed contrarian (<25 long, >75 short)"] = -hyst(d["fng"].fillna(50), 75, 25)
    return s


FAMILY = {"Prezzo vs SMA 200 giorni": "trend", "SMA 50 vs SMA 200 (golden/death cross)": "trend", "EMA 20 vs EMA 50": "trend",
          "Prezzo vs SMA 40 settimane": "trend", "Supertrend (10, 3)": "trend", "Ichimoku: sopra/sotto la nuvola": "trend",
          "ADX > 25 con +DI/−DI": "trend", "MACD giornaliero vs segnale": "momentum", "MACD settimanale vs segnale": "momentum",
          "RSI giornaliero vs 50": "momentum", "RSI settimanale vs 50": "momentum", "Momentum a 90 giorni": "momentum",
          "Donchian 20 giorni": "rottura", "Donchian 55 giorni": "rottura", "Donchian 20 settimane": "rottura",
          "Bollinger: rottura delle bande": "rottura", "OBV vs sua SMA 100": "volume", "RSI 30/70 contrarian": "contrarian",
          "Bollinger contrarian": "contrarian", "Fear & Greed contrarian (<25 long, >75 short)": "sentiment"}


# ------------------------------------------------------------------ motore
def run(d: pd.DataFrame, pos: pd.Series, lev: float = 1.0, start: str = IS0, end: str = END, allow_short: bool = True) -> dict:
    """pos[t] decisa alla chiusura di t, attiva dal giorno dopo. Long fino a 1x in spot (senza funding), la parte oltre 1x e
    gli short in perp con funding reale (gli short lo incassano quando e' positivo e lo pagano quando e' negativo)."""
    p = pos.shift(1).fillna(0.0)
    if not allow_short:
        p = p.clip(lower=0)
    p = p.loc[start:end] * lev
    r = d["close"].pct_change().reindex(p.index).fillna(0.0)
    turn = p.diff().abs().fillna(p.abs())
    perp = p - p.clip(lower=0, upper=1)                       # quota in perp: short e leva oltre 1x
    ret = (p * r - turn * COST - perp * d["funding"].reindex(p.index)).clip(lower=-1.0)
    eq = (1 + ret).cumprod()
    # trade: sequenze con posizione dello stesso segno
    sg = np.sign(p)
    grp = (sg != sg.shift()).cumsum()
    tr = []
    for _, g in ret.groupby(grp):
        s0 = sg.loc[g.index[0]]
        if s0 != 0:
            tr.append((g.index[0], g.index[-1], s0, float((1 + g).prod() - 1), len(g)))
    return {"equity": eq, "ret": ret, "pos": p, "trades": pd.DataFrame(tr, columns=["da", "a", "verso", "ret", "giorni"])}


def stats(r: dict, a: str | None = None, b: str | None = None) -> dict:
    e = r["equity"].loc[a:b]
    e = e / e.iloc[0]
    yrs = (e.index[-1] - e.index[0]).days / 365.25
    x = e.pct_change().dropna()
    t = r["trades"]
    t = t[(t.da >= e.index[0]) & (t.da <= e.index[-1])]
    yr = e.groupby(e.index.year).last()
    yr = (yr / yr.shift(1).fillna(1.0) - 1).to_dict()
    dd = float((e / e.cummax() - 1).min())
    cagr = float(e.iloc[-1] ** (1 / yrs) - 1) if e.iloc[-1] > 0 else -1.0
    return {"final": float(e.iloc[-1]), "cagr": cagr, "dd": dd, "mar": cagr / abs(dd) if dd < 0 else np.nan,
            "sharpe": float(x.mean() / x.std() * np.sqrt(365)) if x.std() > 0 else np.nan, "n": len(t),
            "wr": float((t.ret > 0).mean()) if len(t) else np.nan, "per_year": len(t) / yrs,
            "time": float((r["pos"].loc[a:b] != 0).mean()), "years": yr, "worst_year": min(yr.values()) if yr else np.nan,
            "avg_win": float(t.ret[t.ret > 0].mean()) if (t.ret > 0).any() else np.nan,
            "avg_loss": float(t.ret[t.ret <= 0].mean()) if (t.ret <= 0).any() else np.nan}


TREND_SET = [k for k, v in FAMILY.items() if v in ("trend", "momentum", "rottura", "volume")]


def score(sig: pd.DataFrame, cols: list[str] | None = None) -> pd.Series:
    """Voto medio degli indicatori che seguono il trend: da -1 (tutti short) a +1 (tutti long)."""
    return sig[cols or TREND_SET].mean(axis=1)


def composite(d: pd.DataFrame, sc: pd.Series, th_long: float = 0.5, th_short: float = 0.5, exit_at: float = 0.0, weekly_decision: bool = True,
              fng_block: float | None = None) -> pd.Series:
    """Long quando il voto supera th_long, short quando scende sotto -th_short; si esce quando il voto torna oltre exit_at
    (long: sotto +exit_at; short: sopra -exit_at). weekly_decision: si decide solo alla chiusura della domenica.
    fng_block: non si aprono nuovi short con Fear & Greed sotto la soglia (paura estrema)."""
    x = sc.to_numpy()
    f = d["fng"].reindex(sc.index).to_numpy()
    dow = sc.index.dayofweek
    out, cur = np.zeros(len(x)), 0.0
    for i in range(len(x)):
        if (not weekly_decision or dow[i] == 6) and np.isfinite(x[i]):
            if cur > 0 and x[i] < exit_at:
                cur = 0.0
            if cur < 0 and x[i] > -exit_at:
                cur = 0.0
            if cur == 0:
                if x[i] >= th_long:
                    cur = 1.0
                elif x[i] <= -th_short and not (fng_block is not None and np.isfinite(f[i]) and f[i] < fng_block):
                    cur = -1.0
        out[i] = cur
    return pd.Series(out, sc.index)
