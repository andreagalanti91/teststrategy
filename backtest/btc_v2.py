"""Algoritmo v2 "tre schermi" su BTC: ogni operazione nasce da tre controlli in sequenza, e il motivo viene registrato.

Schermo 1 - MAREA (settimanale, noto alla chiusura della domenica):
  struttura di Dow dai massimi e minimi di swing settimanali (un punto e' di swing se e' l'estremo delle K settimane prima e
  dopo; confermato K settimane dopo): rialzista se gli ultimi due massimi e gli ultimi due minimi sono crescenti, ribassista
  se sono entrambi decrescenti, altrimenti mista.
  RIALZISTA = chiusura settimanale sopra la SMA 40 settimane e struttura non ribassista.
  RIBASSISTA = chiusura sotto la SMA 40, SMA 40 in calo su 4 settimane e struttura ribassista (versione severa) oppure solo
  chiusura sotto la SMA 40 e struttura non rialzista (versione simmetrica).
Schermo 2 - ONDA (giornaliero): nella direzione della marea si aspetta un ritracciamento (RSI 14 sceso sotto `rsi_pb` negli
  ultimi 10 giorni; per gli short salito sopra 100 - rsi_pb) oppure una rottura (chiusura oltre il massimo/minimo a 55 giorni).
Schermo 3 - INGRESSO: dopo il ritracciamento, chiusura sopra il massimo del giorno prima (short: sotto il minimo).
USCITA: chandelier, cioe' chiusura sotto la chiusura piu' alta dall'ingresso meno k ATR(22) (short: specchiato); oppure,
  se `regime_exit`, quando la marea non e' piu' a favore.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import btc_ta as B

K = 3


def structure(w: pd.DataFrame, k: int = K) -> pd.DataFrame:
    """Per ogni settimana chiusa: ultimi due massimi e minimi di swing CONFERMATI e stato della struttura."""
    hi, lo = w["high"].to_numpy(), w["low"].to_numpy()
    highs, lows, rows = [], [], []
    for i in range(len(w)):
        j = i - k                                              # il punto j si conferma alla settimana i
        if j >= k:
            if hi[j] == hi[j - k:j + k + 1].max():
                highs.append((w.index[j], float(hi[j])))
            if lo[j] == lo[j - k:j + k + 1].min():
                lows.append((w.index[j], float(lo[j])))
        st = "mista"
        if len(highs) >= 2 and len(lows) >= 2:
            up_h, up_l = highs[-1][1] > highs[-2][1], lows[-1][1] > lows[-2][1]
            st = "rialzista" if up_h and up_l else "ribassista" if (not up_h and not up_l) else "mista"
        rows.append((st, highs[-1][1] if highs else np.nan, highs[-2][1] if len(highs) > 1 else np.nan,
                     lows[-1][1] if lows else np.nan, lows[-2][1] if len(lows) > 1 else np.nan))
    return pd.DataFrame(rows, index=w.index, columns=["struttura", "max1", "max0", "min1", "min0"])


def features(d: pd.DataFrame) -> pd.DataFrame:
    w = B.weekly(d)
    s = structure(w)
    wk = pd.DataFrame({"wclose": w["close"], "sma40": B.sma(w["close"], 40)})
    wk["sma40_giu"] = wk["sma40"] < wk["sma40"].shift(4)
    wk = wk.join(s)
    f = wk.reindex(d.index, method="ffill")
    c = d["close"]
    f["close"], f["rsi"], f["atr"] = c, B.rsi(c), B.atr(d, 22)
    f["prev_high"], f["prev_low"] = d["high"].shift(1), d["low"].shift(1)
    f["hh55"], f["ll55"] = d["high"].rolling(55).max().shift(1), d["low"].rolling(55).min().shift(1)
    f["rsi_min10"], f["rsi_max10"] = f["rsi"].rolling(10).min(), f["rsi"].rolling(10).max()
    return f


def tide(r, short_mode: str) -> int:
    up = r.wclose > r.sma40 and r.struttura != "ribassista"
    if short_mode == "severa":
        dn = r.wclose < r.sma40 and r.sma40_giu and r.struttura == "ribassista"
    elif short_mode == "simmetrica":
        dn = r.wclose < r.sma40 and r.struttura != "rialzista"
    else:
        dn = False
    return 1 if up else -1 if dn else 0


def run(d: pd.DataFrame, f: pd.DataFrame | None = None, mode: str = "entrambi", k_atr: float = 4.0, rsi_pb: float = 45.0, regime_exit: bool = True,
        short_mode: str = "severa", start: str = B.IS0):
    """Ritorna (posizione giornaliera, registro delle operazioni con i motivi)."""
    f = features(d) if f is None else f
    usd = lambda x: f"{x:,.0f}".replace(",", ".")
    pos, log = np.zeros(len(f)), []
    cur, best, entry, t0, why = 0, None, None, None, None
    idx = f.index
    for i, r in enumerate(f.itertuples()):
        if idx[i] < pd.Timestamp(start) or not np.isfinite(r.sma40) or not np.isfinite(r.atr):
            continue
        td = tide(r, short_mode)
        if cur != 0:
            best = max(best, r.close) if cur > 0 else min(best, r.close)
            stop = best - cur * k_atr * r.atr
            out = None
            if (cur > 0 and r.close < stop) or (cur < 0 and r.close > stop):
                out = f"chandelier: chiusura {usd(r.close)} oltre lo stop {usd(stop)} ({k_atr:g} ATR dalla miglior chiusura {usd(best)})"
            elif regime_exit and td != cur:
                out = f"marea non più a favore: chiusura settimanale {usd(r.wclose)} vs SMA 40 {usd(r.sma40)}, struttura {r.struttura}"
            if out:
                log.append({"verso": "long" if cur > 0 else "short", "entra": t0, "esce": idx[i], "prezzo_in": entry, "prezzo_out": r.close,
                            "mossa": cur * (r.close / entry - 1), "perche_entra": why, "perche_esce": out})
                cur = 0
        if cur == 0 and td != 0:
            tide_txt = (f"marea {'rialzista' if td > 0 else 'ribassista'}: chiusura settimanale {usd(r.wclose)} {'sopra' if td > 0 else 'sotto'} la SMA 40 ({usd(r.sma40)}), "
                        f"struttura {r.struttura} (massimi {usd(r.max0)}→{usd(r.max1)}, minimi {usd(r.min0)}→{usd(r.min1)})")
            trig = None
            if td > 0:
                if mode in ("ritracciamento", "entrambi") and r.rsi_min10 < rsi_pb and r.close > r.prev_high:
                    trig = f"ritracciamento finito: RSI sceso a {r.rsi_min10:.0f} negli ultimi 10 giorni, poi chiusura {usd(r.close)} sopra il massimo del giorno prima ({usd(r.prev_high)})"
                elif mode in ("rottura", "entrambi") and r.close > r.hh55:
                    trig = f"rottura: chiusura {usd(r.close)} sopra il massimo a 55 giorni ({usd(r.hh55)})"
            else:
                if mode in ("ritracciamento", "entrambi") and r.rsi_max10 > 100 - rsi_pb and r.close < r.prev_low:
                    trig = f"rimbalzo finito: RSI salito a {r.rsi_max10:.0f} negli ultimi 10 giorni, poi chiusura {usd(r.close)} sotto il minimo del giorno prima ({usd(r.prev_low)})"
                elif mode in ("rottura", "entrambi") and r.close < r.ll55:
                    trig = f"rottura: chiusura {usd(r.close)} sotto il minimo a 55 giorni ({usd(r.ll55)})"
            if trig:
                cur, best, entry, t0 = td, r.close, r.close, idx[i]
                why = f"{tide_txt}; {trig}; stop iniziale {usd(r.close - td * k_atr * r.atr)}"
        pos[i] = cur
    if cur != 0:
        log.append({"verso": "long" if cur > 0 else "short", "entra": t0, "esce": pd.NaT, "prezzo_in": entry, "prezzo_out": f["close"].iloc[-1],
                    "mossa": cur * (f["close"].iloc[-1] / entry - 1), "perche_entra": why, "perche_esce": "aperta"})
    return pd.Series(pos, idx), pd.DataFrame(log)
