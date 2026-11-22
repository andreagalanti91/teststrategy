"""ALGORITMO "MACD a regime" (long/short settimanale su piu' monete).

Regole (candele settimanali chiuse la domenica 00:00 UTC, si opera il lunedi' all'apertura):
- LONG  se il MACD(12,26,9) settimanale della moneta incrocia al rialzo la linea di segnale, la moneta chiude sopra la sua
  SMA a 40 settimane e BTC chiude sopra la sua SMA a 40 settimane;
- SHORT se il MACD incrocia al ribasso, la moneta chiude sotto la SMA 40 e BTC chiude sotto la sua SMA 40;
- USCITA: incrocio opposto del MACD (chiusura settimanale) oppure stop: chiusura giornaliera a -STOP dall'ingresso;
- UNIVERSO: a ogni settimana, le TOP_K monete per controvalore scambiato mediano a 60 giorni (dato noto in quel momento),
  con almeno 40 settimane di storia;
- DIMENSIONE: ogni posizione rischia RISK del capitale allo stop (controvalore = RISK / STOP x capitale); esposizione lorda
  totale non oltre MAX_GROSS; se i segnali superano i posti liberi, entrano le monete piu' liquide.
Costi: long in spot 0,20% per lato, senza funding; short in perp 0,11% per lato, funding non accreditato (prudente).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import macd_rsi as M
import support_study as S
from fetch_alts import ALTS

COST_L, COST_S = 0.0020, 0.0011
P = dict(stop=0.20, risk=0.02, max_gross=1.0, top_k=30, sma=40, mode="incrocio", regime_exit=False, long=True, short=True, btc_filter=True,
         own_filter=True, trail=None, cap=None, only=None, start="2020-06-01", end="2026-11-21")


def load_any(sym):
    return S.load(sym)


def universe(extra: tuple = ("BTC",)) -> dict:
    out = {}
    for s in sorted(set(ALTS)) + list(extra):
        try:
            d = load_any(s)
        except FileNotFoundError:
            continue
        if len(d) >= 400:
            out[s] = d
    return out


def weekly(d: pd.DataFrame, sma: int) -> pd.DataFrame:
    b = M.bars(d, "W-SUN")
    c = b["close"]
    m, sg = M.macd(c)
    w = pd.DataFrame({"up": m > sg, "above": c > c.rolling(sma).mean(), "ok": c.rolling(sma).mean().notna() & (np.arange(len(c)) >= 35)})
    w["cross_up"] = w["up"] & ~w["up"].shift(1, fill_value=False)
    w["cross_dn"] = ~w["up"] & w["up"].shift(1, fill_value=True)
    w.index = w.index + pd.Timedelta(days=1)                 # dato noto e operabile dal lunedi'
    return w


def run(data: dict, **kw) -> dict:
    p = {**P, **kw}
    days = pd.date_range(p["start"], p["end"], freq="D")
    close = pd.DataFrame({s: d["close"] for s, d in data.items()}).reindex(days)
    dvol = pd.DataFrame({s: (d["close"] * d["volume"]).rolling(60, min_periods=30).median() for s, d in data.items()}).reindex(days).shift(1)
    W = {s: weekly(d, p["sma"]) for s, d in data.items()}
    btc = W["BTC"]
    C = close.to_numpy()
    cols = {s: i for i, s in enumerate(close.columns)}
    eq, e = np.ones(len(days)), 1.0
    pos = {}                                                   # sym -> dict(side, entry, qty, t0); contabilita' in valore
    trades, gross_hist = [], np.zeros(len(days))
    fee = lambda side: COST_L if side > 0 else COST_S
    for i, t in enumerate(days):
        # 1) guadagno del giorno sulle posizioni aperte, poi stop sulla chiusura
        for s, q in list(pos.items()):
            c, c0 = C[i, cols[s]], C[i - 1, cols[s]] if i else np.nan
            if np.isfinite(c) and np.isfinite(c0):
                e += q["qty"] * q["side"] * (c - c0)
        for s, q in list(pos.items()):
            c = C[i, cols[s]]
            if not np.isfinite(c):                              # serie finita (moneta delistata): si chiude all'ultimo prezzo noto
                e -= q["qty"] * q["last"] * fee(q["side"])
                trades.append({**q, "sym": s, "t1": t, "exit": q["last"], "why": "delistata", "move": q["side"] * (q["last"] / q["entry"] - 1)})
                del pos[s]
                continue
            q["last"] = c
            q["best"] = max(q["best"], c) if q["side"] > 0 else min(q["best"], c)
            hit_stop = q["side"] * (c / q["entry"] - 1) <= -p["stop"]
            hit_trail = p["trail"] is not None and q["side"] * (c / q["best"] - 1) <= -p["trail"]      # trailing dalla miglior chiusura
            if hit_stop or hit_trail:
                e -= q["qty"] * c * fee(q["side"])
                trades.append({**q, "sym": s, "t1": t, "exit": c, "why": "stop" if hit_stop else "trailing", "move": q["side"] * (c / q["entry"] - 1)})
                del pos[s]
            elif p["cap"] is not None and q["side"] > 0 and e > 0 and q["qty"] * c / e > p["cap"] * 1.33:   # alleggerisce al tetto
                sell = q["qty"] - p["cap"] * e / c
                e -= sell * c * fee(1)
                q["qty"] -= sell
        # 2) lunedi': uscite e ingressi sui segnali della settimana chiusa (prezzo = chiusura di domenica = C[i-1])
        if t.dayofweek == 0 and i > 0 and t in btc.index and e > 0:
            b_above, b_ok = bool(btc.at[t, "above"]), bool(btc.at[t, "ok"])
            for s, q in list(pos.items()):
                w = W[s]
                if t not in w.index:
                    continue
                r = w.loc[t]
                out = (q["side"] > 0 and not r["up"]) or (q["side"] < 0 and r["up"])
                if p["regime_exit"] and p["btc_filter"]:
                    out = out or (q["side"] > 0 and not b_above) or (q["side"] < 0 and b_above)
                if out:
                    px = C[i - 1, cols[s]]
                    e -= q["qty"] * px * fee(q["side"])
                    trades.append({**q, "sym": s, "t1": t, "exit": px, "why": "segnale", "move": q["side"] * (px / q["entry"] - 1)})
                    del pos[s]
            rank = dvol.iloc[i].dropna().sort_values(ascending=False)
            elig = list(rank.index[:p["top_k"]]) if p["top_k"] else list(rank.index)
            cand = []
            for s in elig:
                if s in pos or t not in W[s].index or (p["only"] and s not in p["only"]):
                    continue
                r = W[s].loc[t]
                if not r["ok"] or not b_ok:
                    continue
                trig_up = r["cross_up"] if p["mode"] == "incrocio" else r["up"]
                trig_dn = r["cross_dn"] if p["mode"] == "incrocio" else not r["up"]
                lo = p["long"] and trig_up and (r["above"] or not p["own_filter"]) and (b_above or not p["btc_filter"])
                sh = p["short"] and trig_dn and (not r["above"] or not p["own_filter"]) and (not b_above or not p["btc_filter"])
                if lo or sh:
                    cand.append((s, 1 if lo else -1))
            wpos = p["risk"] / p["stop"]
            for s, side in cand:
                gross = sum(q["qty"] * C[i - 1, cols[x]] for x, q in pos.items()) / e
                if gross + wpos > p["max_gross"] + 1e-9:
                    break
                px = C[i - 1, cols[s]]
                if not np.isfinite(px):
                    continue
                qty = wpos * e / px
                e -= qty * px * fee(side)
                pos[s] = {"side": side, "entry": px, "qty": qty, "t0": t, "best": px, "last": px}
        e = max(e, 0.0)
        eq[i] = e
        gross_hist[i] = sum(q["qty"] * C[i, cols[x]] for x, q in pos.items() if np.isfinite(C[i, cols[x]])) / e if e > 0 else 0.0
    for s, q in pos.items():
        c = C[-1, cols[s]]
        trades.append({**q, "sym": s, "t1": pd.NaT, "exit": c, "why": "aperto", "move": q["side"] * (c / q["entry"] - 1)})
    return {"equity": pd.Series(eq, days), "trades": pd.DataFrame(trades), "gross": pd.Series(gross_hist, days), "params": p}


def stats(r: dict, a: str | None = None, b: str | None = None) -> dict:
    e = r["equity"].loc[a:b]
    e = e / e.iloc[0]
    yrs = (e.index[-1] - e.index[0]).days / 365.25
    t = r["trades"]
    if len(t):
        t = t[(t.t0 >= e.index[0]) & (t.t0 <= e.index[-1])]
    ret = e.pct_change().dropna()
    yr = e.groupby(e.index.year).last()
    yr = (yr / yr.shift(1).fillna(1.0) - 1).to_dict()
    cost = np.where(t.side > 0, 2 * COST_L, 2 * COST_S) if len(t) else np.array([])
    net = t.move - cost if len(t) else pd.Series(dtype=float)
    return {"final": float(e.iloc[-1]), "cagr": float(e.iloc[-1] ** (1 / yrs) - 1), "dd": float((e / e.cummax() - 1).min()),
            "sharpe": float(ret.mean() / ret.std() * np.sqrt(365)) if ret.std() > 0 else np.nan, "n": len(t),
            "wr": float((net > 0).mean()) if len(t) else np.nan, "avg": float(net.mean()) if len(t) else np.nan,
            "med": float(net.median()) if len(t) else np.nan, "n_long": int((t.side > 0).sum()) if len(t) else 0,
            "wr_long": float((net[t.side > 0] > 0).mean()) if len(t) else np.nan, "wr_short": float((net[t.side < 0] > 0).mean()) if len(t) else np.nan,
            "gross": float(r["gross"].loc[a:b].mean()), "years": yr, "worst_year": min(yr.values())}


if __name__ == "__main__":
    data = universe()
    def show(name, r):
        k, a, b = stats(r), stats(r, None, "2023-12-31"), stats(r, "2024-01-01", None)
        print(f"{name:44s} x{k['final']:6.2f} cagr {k['cagr'] * 100:+6.1f}% dd {k['dd'] * 100:6.1f}% sh {k['sharpe']:.2f} n {k['n']:4d} wr {k['wr'] * 100:3.0f}% "
              f"med {k['med'] * 100:+5.1f}% lordo {k['gross']:.2f} | 20-23 {a['cagr'] * 100:+6.1f}%/{a['dd'] * 100:.0f}% "
              f"| 24-26 {b['cagr'] * 100:+6.1f}%/{b['dd'] * 100:.0f}% | " + " ".join(f"{y % 100}:{v * 100:+.0f}" for y, v in k["years"].items()))
    for name, kw in {"base": {}, "trailing 25%": dict(trail=0.25), "trailing 30%": dict(trail=0.30), "trailing 35%": dict(trail=0.35), "trailing 40%": dict(trail=0.40),
                     "tetto 15%": dict(cap=0.15), "tetto 12%": dict(cap=0.12), "trailing 30% + tetto 15%": dict(trail=0.30, cap=0.15),
                     "trailing 35% + tetto 15%": dict(trail=0.35, cap=0.15), "trailing 30% + tetto 15%, top 15": dict(trail=0.30, cap=0.15, top_k=15),
                     "trailing 30% + tetto 15%, top 60": dict(trail=0.30, cap=0.15, top_k=60), "trailing 30% + tetto 15%, solo long": dict(trail=0.30, cap=0.15, short=False),
                     "trailing 30% + tetto 15%, rischio 4% lordo 2x": dict(trail=0.30, cap=0.30, risk=0.04, max_gross=2.0),
                     "trailing 30% + tetto 15%, senza filtri": dict(trail=0.30, cap=0.15, btc_filter=False, own_filter=False)}.items():
        show(name, run(data, **kw))
    names = sorted(k for k in data if k != "BTC")
    for lab, half in (("meta' A delle monete", names[0::2]), ("meta' B delle monete", names[1::2])):
        sub = {k: data[k] for k in half + ["BTC"]}
        show(lab + " base", run(sub))
        show(lab + " trailing 30% + tetto 15%", run(sub, trail=0.30, cap=0.15))
        show(lab + " senza filtri", run(sub, btc_filter=False, own_filter=False))
