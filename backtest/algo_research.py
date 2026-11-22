"""Costruzione dell'algoritmo: tutti i trade 'incrocio MACD settimanale' di ~160 monete con le condizioni presenti
all'ingresso, per vedere quali condizioni separano i trade buoni dai cattivi, in due periodi (2020-23 e 2024-26)."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import macd_rsi as M
import support_study as S
from fetch_alts import ALTS

OUT = S.ROOT / "results" / "algo"
OUT.mkdir(parents=True, exist_ok=True)


def load_any(sym):
    return S.load(sym)


def weekly_features(d: pd.DataFrame) -> pd.DataFrame:
    b = M.bars(d, "W-SUN")
    c = b["close"]
    m, sg = M.macd(c)
    f = pd.DataFrame(index=b.index)
    f["close"] = c
    f["macd_n"] = m / c                                   # MACD in % del prezzo: confrontabile fra monete
    f["hist_n"] = (m - sg) / c
    f["up"] = m > sg
    f["rsi"] = M.rsi(c)
    f["sma40"] = c / c.rolling(40).mean() - 1
    f["sma20"] = c / c.rolling(20).mean() - 1
    f["pos52"] = (c - b["low"].rolling(52).min()) / (b["high"].rolling(52).max() - b["low"].rolling(52).min())
    f["ret12"] = c.pct_change(12)
    f["vol"] = c.pct_change().rolling(26).std()
    return f


def trades(sym: str, d: pd.DataFrame, btcf: pd.DataFrame, stop: float | None = None) -> pd.DataFrame:
    f = weekly_features(d)
    start = d.index[0] + pd.Timedelta(weeks=40)
    if start >= d.index[-1] - pd.Timedelta(weeks=20):
        return pd.DataFrame()
    eq, tr = M.simulate(d, "MACD incrocio", start=str(start.date()), stop=stop)
    rows = []
    for r in tr.itertuples():
        wk = f.index[f.index < r.entra]
        if not len(wk):
            continue
        w = f.loc[wk[-1]]
        bw = btcf.loc[btcf.index <= wk[-1]].iloc[-1] if (btcf.index <= wk[-1]).any() else None
        end = r.esce if pd.notna(r.esce) else d.index[-1]
        days = max((end - r.entra).days, 1)
        net = r.mossa - 2 * M.COST - r.verso * M.FUND_D * days
        rows.append({"sym": sym, "t": r.entra, "side": r.verso, "move": r.mossa, "net": net, "days": days, "exit": r.uscita,
                     **{k: w[k] for k in ("macd_n", "rsi", "sma40", "sma20", "pos52", "ret12", "vol")},
                     "btc_sma40": bw["sma40"] if bw is not None else np.nan, "btc_up": bool(bw["up"]) if bw is not None else np.nan,
                     "btc_rsi": bw["rsi"] if bw is not None else np.nan})
    return pd.DataFrame(rows)


def build(stop=None) -> pd.DataFrame:
    btcf = weekly_features(load_any("BTC"))
    out = []
    for s in sorted(set(ALTS)) + ["BTC"]:
        try:
            d = load_any(s) if s != "TAO" else S.load("TAO")
        except FileNotFoundError:
            continue
        if len(d) < 500:
            continue
        out.append(trades(s, d, btcf, stop))
    x = pd.concat(out, ignore_index=True)
    return x[x["exit"] != "aperto"]


def table(x: pd.DataFrame, name: str, masks: dict) -> None:
    print(f"\n-- {name}")
    print(f"{'condizione':46s} {'n':>5s} {'media':>7s} {'mediana':>8s} {'vinc.':>6s} | {'n 20-23':>7s} {'media':>7s} | {'n 24-26':>7s} {'media':>7s} | senza SOL/TAO")
    for k, m in masks.items():
        y = x[m]
        a, b = y[y.t < "2024-01-01"], y[y.t >= "2024-01-01"]
        z = y[~y.sym.isin(["SOL", "TAO"])]
        if len(y) < 5:
            continue
        print(f"{k:46s} {len(y):5d} {y.net.mean() * 100:+6.1f}% {y.net.median() * 100:+7.1f}% {(y.net > 0).mean() * 100:5.0f}% | "
              f"{len(a):7d} {a.net.mean() * 100:+6.1f}% | {len(b):7d} {b.net.mean() * 100:+6.1f}% | {z.net.mean() * 100:+6.1f}%")


if __name__ == "__main__":
    x = build()
    x.to_csv(OUT / "trade_macd_tutti.csv", index=False)
    print(len(x), "trade su", x.sym.nunique(), "monete")
    L, Sh = x.side > 0, x.side < 0
    table(x, "base", {"tutti": x.side != 0, "long": L, "short": Sh})
    table(x, "territorio del MACD all'incrocio", {
        "long, MACD < 0 (inversione dal basso)": L & (x.macd_n < 0), "long, MACD > 0 (continuazione)": L & (x.macd_n > 0),
        "short, MACD > 0 (inversione dall'alto)": Sh & (x.macd_n > 0), "short, MACD < 0 (continuazione)": Sh & (x.macd_n < 0)})
    table(x, "trend della moneta (prezzo vs SMA 40 settimane)", {
        "long sopra SMA40": L & (x.sma40 > 0), "long sotto SMA40": L & (x.sma40 < 0),
        "short sopra SMA40": Sh & (x.sma40 > 0), "short sotto SMA40": Sh & (x.sma40 < 0)})
    table(x, "trend di BTC (BTC vs SMA 40 settimane)", {
        "long, BTC sopra": L & (x.btc_sma40 > 0), "long, BTC sotto": L & (x.btc_sma40 < 0),
        "short, BTC sopra": Sh & (x.btc_sma40 > 0), "short, BTC sotto": Sh & (x.btc_sma40 < 0)})
    table(x, "MACD di BTC", {"long, MACD BTC su": L & (x.btc_up == True), "long, MACD BTC giu'": L & (x.btc_up == False),
                             "short, MACD BTC su": Sh & (x.btc_up == True), "short, MACD BTC giu'": Sh & (x.btc_up == False)})
    table(x, "RSI settimanale all'ingresso", {
        "long RSI < 45": L & (x.rsi < 45), "long RSI 45-55": L & x.rsi.between(45, 55), "long RSI > 55": L & (x.rsi > 55),
        "short RSI < 45": Sh & (x.rsi < 45), "short RSI 45-55": Sh & x.rsi.between(45, 55), "short RSI > 55": Sh & (x.rsi > 55)})
    table(x, "posizione nell'intervallo a 52 settimane", {
        "long terzo basso": L & (x.pos52 < 1 / 3), "long terzo medio": L & x.pos52.between(1 / 3, 2 / 3), "long terzo alto": L & (x.pos52 > 2 / 3),
        "short terzo basso": Sh & (x.pos52 < 1 / 3), "short terzo medio": Sh & x.pos52.between(1 / 3, 2 / 3), "short terzo alto": Sh & (x.pos52 > 2 / 3)})
    table(x, "combinazioni", {
        "long: BTC sopra SMA40 e moneta sopra SMA40": L & (x.btc_sma40 > 0) & (x.sma40 > 0),
        "long: BTC sopra SMA40 e MACD BTC su": L & (x.btc_sma40 > 0) & (x.btc_up == True),
        "long: BTC sopra SMA40, MACD moneta < 0": L & (x.btc_sma40 > 0) & (x.macd_n < 0),
        "short: BTC sotto SMA40 e moneta sotto SMA40": Sh & (x.btc_sma40 < 0) & (x.sma40 < 0),
        "short: MACD BTC giu' e moneta sotto SMA40": Sh & (x.btc_up == False) & (x.sma40 < 0),
        "short: MACD BTC giu'": Sh & (x.btc_up == False),
        "short: MACD > 0 e MACD BTC giu'": Sh & (x.macd_n > 0) & (x.btc_up == False)})
