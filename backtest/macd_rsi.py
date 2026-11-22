"""Regole MACD + RSI long/short su candele settimanali (o giornaliere): riproduzione dei trade su SOL e verifica su altre monete.

Esecuzione: segnale alla chiusura della candela, posizione dalla chiusura stessa (crypto 24/7). Perp a 1x sul capitale.
Costi: 0,06% commissione + 0,05% slippage per lato; funding 0,01% ogni 8 ore pagato dai long e incassato dagli short.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import support_study as S

COST, FUND_D = 0.0011, 0.0003


def bars(d: pd.DataFrame, tf: str) -> pd.DataFrame:
    if tf == "1D":
        return d[["open", "high", "low", "close"]]
    return d.resample(tf).agg({"open": "first", "high": "max", "low": "min", "close": "last"}).dropna().iloc[:-1]   # solo candele chiuse


def macd(c, f=12, s=26, g=9):
    m = c.ewm(span=f, adjust=False).mean() - c.ewm(span=s, adjust=False).mean()
    return m, m.ewm(span=g, adjust=False).mean()


def rsi(c, n=14):
    d = c.diff()
    up, dn = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean(), (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / dn)


def positions(b: pd.DataFrame, rule: str) -> pd.Series:
    """Posizione desiderata (+1 long, -1 short, 0 fuori) dopo ogni candela chiusa."""
    c = b["close"]
    m, sg = macd(c)
    r = rsi(c)
    up, dn = m > sg, m < sg
    if rule == "MACD incrocio":                       # sempre a mercato: long sopra la linea di segnale, short sotto
        p = np.where(up, 1, -1)
    elif rule == "MACD + RSI 50":                     # long solo con RSI > 50, short solo con RSI < 50, altrimenti fuori
        p = np.where(up & (r > 50), 1, np.where(dn & (r < 50), -1, 0))
    elif rule == "MACD + RSI 50, mantiene":           # entra come sopra, esce solo all'incrocio opposto del MACD
        p, cur = [], 0
        for u, d_, rv in zip(up, dn, r):
            if cur == 0 or (cur > 0 and d_) or (cur < 0 and u):
                cur = 1 if (u and rv > 50) else -1 if (d_ and rv < 50) else 0
            p.append(cur)
        p = np.array(p)
    elif rule == "MACD + uscita RSI estremo":         # MACD incrocio; chiude il long con RSI > 75 e lo short con RSI < 30,
        p, cur, blocked = [], 0, 0                    # rientra solo al prossimo incrocio
        prev = 0
        for u, rv in zip(up, r):
            want = 1 if u else -1
            if want != prev:
                blocked = 0
            prev = want
            if (want > 0 and rv > 75) or (want < 0 and rv < 30):
                blocked = 1
            p.append(0 if blocked else want)
        p = np.array(p)
    elif rule == "MACD sopra/sotto zero":             # long se MACD > segnale e > 0; short se < segnale e < 0
        p = np.where(up & (m > 0), 1, np.where(dn & (m < 0), -1, 0))
    elif rule == "RSI 55/45":                         # long quando l'RSI sale sopra 55, short sotto 45 (isteresi)
        p, cur = [], 0
        for rv in r:
            cur = 1 if rv > 55 else -1 if rv < 45 else cur
            p.append(cur)
        p = np.array(p)
    elif rule == "Solo long MACD + RSI 50":
        p = np.where(up & (r > 50), 1, 0)
    else:
        raise ValueError(rule)
    p = pd.Series(p, c.index).astype(float)
    p[(m.isna()) | (np.arange(len(c)) < 35)] = 0.0   # indicatori non ancora stabili
    return p


RULES = ["MACD incrocio", "MACD + RSI 50", "MACD + RSI 50, mantiene", "MACD + uscita RSI estremo", "MACD sopra/sotto zero", "RSI 55/45",
         "Solo long MACD + RSI 50"]


def simulate(d: pd.DataFrame, rule: str, tf: str = "W-SUN", start: str = "2021-01-01", stop: float | None = None):
    """stop: perdita massima dall'ingresso (es. 0,20) su chiusura giornaliera; dopo lo stop si resta fuori fino al segnale successivo."""
    b = bars(d, tf)
    p = positions(b, rule)
    day = d["close"]
    want = p.copy()
    want.index = want.index + pd.Timedelta(days=1)                       # candela chiusa (domenica o giorno t): attiva dal giorno dopo
    want = want.reindex(day.index, method="ffill").fillna(0.0)
    want = want.loc[start:]
    C = day.reindex(want.index).to_numpy()
    prevC = day.shift(1).reindex(want.index).to_numpy()
    W = want.to_numpy()
    eq, e = np.ones(len(W)), 1.0
    cur, entry, stopped_for, tr, t0 = 0.0, None, None, [], None
    idx = want.index
    for i in range(len(W)):
        target = W[i]
        if stopped_for is not None:
            if target == stopped_for:
                target = 0.0
            else:
                stopped_for = None
        if target != cur:                                                # si opera alla chiusura del giorno prima (= apertura di oggi)
            px = prevC[i] if np.isfinite(prevC[i]) else C[i]
            if cur != 0:
                tr.append((t0, idx[i], cur, entry, px, cur * (px / entry - 1), "segnale"))
            e *= 1 - COST * abs(target - cur)
            cur, entry, t0 = target, px, idx[i]
        if cur != 0 and np.isfinite(prevC[i]):
            e *= max(0.0, 1 + cur * (C[i] / prevC[i] - 1) - cur * FUND_D)   # sotto zero = liquidazione
            if stop is not None and cur * (C[i] / entry - 1) <= -stop:   # stop sulla chiusura giornaliera
                tr.append((t0, idx[i], cur, entry, C[i], cur * (C[i] / entry - 1), "stop"))
                e *= 1 - COST * abs(cur)
                stopped_for, cur = W[i], 0.0
        eq[i] = e
    if cur != 0:
        tr.append((t0, None, cur, entry, C[-1], cur * (C[-1] / entry - 1), "aperto"))
    return pd.Series(eq, idx), pd.DataFrame(tr, columns=["entra", "esce", "verso", "prezzo_in", "prezzo_out", "mossa", "uscita"])


def stats(eq: pd.Series, tr: pd.DataFrame) -> dict:
    yrs = (eq.index[-1] - eq.index[0]).days / 365.25
    dd = float((eq / eq.cummax() - 1).min())
    cagr = float(eq.iloc[-1] ** (1 / yrs) - 1) if eq.iloc[-1] > 0 and yrs > 0.5 else np.nan
    return {"final": float(eq.iloc[-1]), "cagr": cagr, "dd": dd, "mar": cagr / abs(dd) if dd < 0 else np.nan, "n": len(tr),
            "wr": float((tr.mossa > 0).mean()) if len(tr) else np.nan, "years": yrs}


if __name__ == "__main__":
    d = S.load("SOL")
    for rule in RULES:
        eq, tr = simulate(d, rule, start="2021-06-01")
        s = stats(eq, tr)
        print(f"\n== {rule}: x{s['final']:.1f} cagr {s['cagr'] * 100:.0f}% dd {s['dd'] * 100:.0f}% trade {s['n']} wr {s['wr'] * 100:.0f}%")
        t = tr.copy()
        t["entra"] = t.entra.dt.date
        t["esce"] = t.esce.apply(lambda x: x.date() if pd.notna(x) else None)
        print(t.round(2).to_string(index=False))
