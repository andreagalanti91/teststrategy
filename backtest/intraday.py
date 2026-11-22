"""Motore intraday per BTC: segnali sulle candele orarie chiuse, esecuzione e uscite sulle candele a 15 minuti.

Regole di simulazione (prudenti):
- il segnale nasce alla chiusura di una candela oraria; l'ingresso avviene all'apertura dei 15 minuti successivi, a mercato;
- una sola posizione alla volta; stop e target sono prezzi fissati all'ingresso;
- se nella stessa candela da 15 minuti vengono toccati sia lo stop sia il target, vale lo STOP;
- se il prezzo apre oltre lo stop, lo stop si esegue all'apertura (gap);
- uscita a tempo: alla chiusura della candela in cui scade la durata massima;
- costi OKX, livello base: ingresso e uscite a mercato 0,05% + 0,02% di slippage; target come ordine limite 0,02%;
- funding: 0,01% ogni 8 ore sul controvalore (media storica; pagato dai long, incassato dagli short).
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data" / "intraday"
TAKER, MAKER, SLIP = 0.0005, 0.0002, 0.0002
FUND_8H = 0.0001
BARS_H = 4                               # candele da 15 minuti in un'ora


def load(source: str = "binance") -> pd.DataFrame:
    name = {"binance": "binance_spot_BTCUSDT_15m.csv.gz", "okx": "okx_BTC-USDT-SWAP_15m.csv.gz"}[source]
    d = pd.read_csv(DATA / name)
    d["ts"] = pd.to_datetime(d["ts"], format="mixed").astype("datetime64[ns]")
    d = d.set_index("ts").sort_index()
    d = d[~d.index.duplicated()]
    full = pd.date_range(d.index[0], d.index[-1], freq="15min")
    d = d.reindex(full)                  # buchi dell'exchange (manutenzioni): prezzo fermo, volume zero
    d["close"] = d["close"].ffill()
    for c in ("open", "high", "low"):
        d[c] = d[c].fillna(d["close"])
    d["volume"] = d["volume"].fillna(0.0)
    return d


def hourly(b: pd.DataFrame) -> pd.DataFrame:
    """Candele orarie; l'indice e' l'ORA DI CHIUSURA (quando il dato e' noto)."""
    h = b.resample("1h").agg({"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}).dropna()
    h.index = h.index + pd.Timedelta(hours=1)
    return h


def atr(h: pd.DataFrame, n: int = 14) -> pd.Series:
    c = h["close"]
    tr = pd.concat([h["high"] - h["low"], (h["high"] - c.shift()).abs(), (h["low"] - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def rsi(c: pd.Series, n: int = 14) -> pd.Series:
    d = c.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / dn)


def weekly_regime(b: pd.DataFrame, extra_daily: pd.Series | None = None, sma: int = 40, ema: int = 20) -> pd.Series:
    """Trend settimanale come nel repo radar: +1 se la chiusura settimanale (domenica) e' sopra la SMA 40 e la EMA 20 sale;
    -1 se e' sotto la SMA 40, la SMA 40 scende su 4 settimane e la EMA 20 scende; 0 altrimenti. Noto dal lunedi' 00:00 UTC."""
    d = b["close"].resample("1D").last().dropna()
    if extra_daily is not None:
        d = pd.concat([extra_daily[extra_daily.index < d.index[0]], d])
    w = d.resample("W-SUN").last().dropna()
    w = w[w.index <= d.index[-1]]
    s, e = w.rolling(sma).mean(), w.ewm(span=ema, adjust=False).mean()
    up = (w > s) & (e > e.shift())
    dn = (w < s) & (s < s.shift(4)) & (e < e.shift())
    r = up.astype(int) - dn.astype(int)
    r.index = r.index + pd.Timedelta(days=1)
    return r


def daily_regime(b: pd.DataFrame, n: int) -> pd.Series:
    """+1 se l'ultima chiusura giornaliera COMPLETA (00:00 UTC) e' sopra la sua media a n giorni, -1 se sotto.
    Riportato su ogni ora: di giorno si usa solo il dato del giorno prima."""
    d = b["close"].resample("1D").last().dropna()
    s = np.sign(d - d.rolling(n).mean())
    s.index = s.index + pd.Timedelta(days=1)          # noto dalla mezzanotte successiva
    return s


@dataclass
class Trades:
    df: pd.DataFrame                      # un trade per riga, rendimento netto sul controvalore (ret)
    bars: pd.DataFrame

    def equity(self, lev: float = 1.0, start: str | None = None, end: str | None = None) -> pd.Series:
        """Capitale con leva costante sul controvalore (controvalore = lev x capitale a ogni ingresso), valutato alla
        chiusura di ogni trade e, dentro il trade, al punto peggiore toccato (MAE): cosi' il drawdown non e' sottostimato."""
        t = self.df
        if start:
            t = t[t.entry_time >= start]
        if end:
            t = t[t.entry_time < end]
        e, pts = 1.0, {}
        for r in t.itertuples():
            pts[r.entry_time] = e
            worst = e * (1 + lev * r.mae)
            if worst <= 0:
                pts[r.exit_time] = 0.0
                break
            pts[r.mae_time] = min(pts.get(r.mae_time, np.inf), worst)
            e *= max(0.0, 1 + lev * r.ret)
            pts[r.exit_time] = e
        s = pd.Series(pts).sort_index()
        return s


def backtest(b: pd.DataFrame, sig: pd.DataFrame, cooldown_h: int = 0) -> Trades:
    """sig: indice = ora di chiusura della candela oraria del segnale; colonne side (+1/-1), tp (distanza in prezzo),
    sl (distanza in prezzo), hold (ore massime)."""
    O, H, L, C = (b[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    idx = b.index
    pos = idx.searchsorted(sig.index)
    rows, free = [], 0
    has_lim = "limit" in sig.columns
    for k in range(len(sig)):
        i = int(pos[k])
        if i >= len(idx) - 1 or idx[i] != sig.index[k] or i < free:
            continue
        side, tpd, sld, hold = int(sig["side"].iat[k]), float(sig["tp"].iat[k]), float(sig["sl"].iat[k]), int(sig["hold"].iat[k])
        if side == 0 or not np.isfinite(tpd) or not np.isfinite(sld) or sld <= 0:
            continue
        fee_in, first_tp = TAKER, 0
        if has_lim and np.isfinite(sig["limit"].iat[k]):
            # ordine limite valido `valid` ore: eseguito solo se il prezzo lo ATTRAVERSA (non basta toccarlo); commissione maker
            lim, v1 = float(sig["limit"].iat[k]), min(i + int(sig["valid"].iat[k]) * BARS_H, len(idx))
            thru = (L[i:v1] < lim) if side > 0 else (H[i:v1] > lim)
            if not thru.any():
                continue
            i = i + int(np.argmax(thru))
            px = min(O[i], lim) if side > 0 else max(O[i], lim)
            base, fee_in, first_tp = px, MAKER, 1          # nella candela d'ingresso il target non conta, lo stop si'
        else:
            px, base = O[i] * (1 + SLIP * side), O[i]
        tp, sl = base + side * tpd, base - side * sld
        j1 = min(i + hold * BARS_H, len(idx))
        hi, lo = H[i:j1], L[i:j1]
        hit_sl = (lo <= sl) if side > 0 else (hi >= sl)
        hit_tp = (hi >= tp) if side > 0 else (lo <= tp)
        hit_tp[:first_tp] = False
        a = int(np.argmax(hit_sl)) if hit_sl.any() else 10 ** 9
        c = int(np.argmax(hit_tp)) if hit_tp.any() else 10 ** 9
        if a <= c and a < 10 ** 9:                                   # stop (vince i pareggi)
            j = i + a
            o = O[j]
            raw = (min(o, sl) if side > 0 else max(o, sl)) if j > i else sl
            ex, fee, why = raw * (1 - SLIP * side), TAKER, "stop"
        elif c < 10 ** 9:
            j = i + c
            ex, fee, why = tp, MAKER, "target"
        else:
            j = j1 - 1
            ex, fee, why = C[j] * (1 - SLIP * side), TAKER, "tempo"
        hours = (j - i + 1) / BARS_H
        ret = side * (ex / px - 1) - fee_in - fee - side * FUND_8H * hours / 8
        seg_adv = (L[i:j + 1].min() if side > 0 else H[i:j + 1].max())
        seg_adv = max(seg_adv, sl) if side > 0 else min(seg_adv, sl)   # oltre lo stop non si va (salvo gap, gia' nel ret)
        mae = min(side * (seg_adv / px - 1) - fee_in, ret)
        jm = i + int(np.argmin(L[i:j + 1]) if side > 0 else np.argmax(H[i:j + 1]))
        rows.append((idx[i], idx[j] + pd.Timedelta(minutes=15), side, px, ex, why, hours, ret, mae, idx[jm] + pd.Timedelta(minutes=14)))
        free = j + 1 + cooldown_h * BARS_H
    df = pd.DataFrame(rows, columns=["entry_time", "exit_time", "side", "entry", "exit", "reason", "hours", "ret", "mae", "mae_time"])
    return Trades(df, b)


def stats(t: Trades, lev: float = 1.0, start: str | None = None, end: str | None = None) -> dict:
    d = t.df
    if start:
        d = d[d.entry_time >= start]
    if end:
        d = d[d.entry_time < end]
    if len(d) < 2:
        return {"n": len(d)}
    e = t.equity(lev, start, end)
    t0 = pd.Timestamp(start) if start else d.entry_time.iloc[0]
    t1 = pd.Timestamp(end) if end else d.exit_time.iloc[-1]
    yrs = (t1 - t0).days / 365.25
    w, l = d.ret[d.ret > 0], d.ret[d.ret <= 0]
    fin = float(e.iloc[-1])
    closed = e[e.index.isin(d.exit_time)]
    return {"n": len(d), "per_year": len(d) / yrs, "wr": float((d.ret > 0).mean()), "avg_win": float(w.mean()) if len(w) else 0.0,
            "avg_loss": float(l.mean()) if len(l) else 0.0, "pf": float(w.sum() / -l.sum()) if l.sum() < 0 else np.inf,
            "exp": float(d.ret.mean()), "hours": float(d.hours.mean()), "final": fin,
            "cagr": fin ** (1 / yrs) - 1 if fin > 0 else -1.0, "dd": float((e / e.cummax() - 1).min()),
            "worst": float(d.ret.min()) * lev, "long_share": float((d.side > 0).mean()),
            "max_losses_row": int((d.ret <= 0).astype(int).groupby((d.ret > 0).cumsum()).sum().max()),
            "tstat": float(d.ret.mean() / d.ret.std() * np.sqrt(len(d))) if d.ret.std() > 0 else 0.0,
            "years": {int(y): float(v) for y, v in (closed.groupby(closed.index.year).last() /
                                                    closed.groupby(closed.index.year).last().shift(1).fillna(1.0) - 1).items()}}


def best_leverage(t: Trades, dd_max: float = -0.35, lev_max: float = 5.0, start: str | None = None, end: str | None = None) -> float:
    """Leva piu' alta (passo 0,25, tetto lev_max) con drawdown nel periodo non peggiore di dd_max."""
    best = 0.0
    for lev in np.arange(0.25, lev_max + 1e-9, 0.25):
        e = t.equity(float(lev), start, end)
        if len(e) and e.iloc[-1] > 0 and (e / e.cummax() - 1).min() >= dd_max:
            best = float(lev)
        else:
            break
    return best
