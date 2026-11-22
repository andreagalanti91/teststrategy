"""Strategie a confronto. Parametri fissati PRIMA di guardare i risultati, presi dalla letteratura o dai valori piu' comuni
(nessuna ottimizzazione); la sensibilita' ai parametri e' in robustness.py. Ogni funzione ritorna il DataFrame di
common.simulate (equity base 1, esposizione lorda, turnover)."""
from __future__ import annotations

import importlib.util
import sys

import numpy as np
import pandas as pd

from common import (COINS, COST_ETF, COST_PERP, COST_SPOT, DATA, END, ROOT, START, STOCKS, crypto_close, crypto_funding,
                    crypto_perp_close, equity_close, fed_funds, simulate)

DONCHIAN = [5, 10, 20, 30, 60, 90, 150, 250, 360]     # Zarattini, Pagani, Barbon (2025), "Catching Crypto Trends"


# ------------------------------------------------------------------ segnali
def donchian_pos(close: pd.Series, n: int) -> pd.Series:
    """Long quando la chiusura e' il massimo a n giorni; stop a cricchetto sul punto medio del canale; uscita sotto lo stop."""
    hi, lo = close.rolling(n).max(), close.rolling(n).min()
    mid = ((hi + lo) / 2).to_numpy()
    c, h = close.to_numpy(), hi.to_numpy()
    pos, stop, inpos = np.zeros(len(c)), np.nan, False
    for i in range(len(c)):
        if np.isnan(h[i]):
            continue
        if inpos:
            stop = max(stop, mid[i])
            if c[i] < stop:
                inpos = False
        elif c[i] >= h[i]:
            inpos, stop = True, mid[i]
        pos[i] = 1.0 if inpos else 0.0
    return pd.Series(pos, close.index)


def ensemble_pos(close: pd.Series, lookbacks: list[int] = DONCHIAN) -> pd.Series:
    """Media dei modelli Donchian sui diversi orizzonti: esposizione fra 0 e 1."""
    return pd.concat([donchian_pos(close, n) for n in lookbacks], axis=1).mean(axis=1)


def ann_vol(close: pd.DataFrame | pd.Series, n: int = 60) -> pd.DataFrame | pd.Series:
    return close.pct_change().rolling(n, min_periods=n // 2).std() * np.sqrt(365)


# ------------------------------------------------------------------ BTC
def btc_hold() -> pd.DataFrame:
    px = crypto_close()[["BTC"]]
    tgt = pd.DataFrame(1.0, index=px.index[px.index >= pd.Timestamp(START) - pd.Timedelta(days=1)], columns=["BTC"])
    return simulate(px, tgt, band=10.0)


def btc_sma200() -> pd.DataFrame:
    """Faber (2007) applicato a BTC: long sopra la media a 200 giorni, liquidita' sotto."""
    px = crypto_close()[["BTC"]]
    return simulate(px, (px > px.rolling(200).mean()).astype(float), band=10.0)


def btc_ensemble(lookbacks: list[int] = DONCHIAN, vol_ref: float = 0.60) -> pd.DataFrame:
    """Ensemble Donchian su BTC, esposizione scalata a volatilita' di riferimento 60% (tetto 1x, senza leva)."""
    px = crypto_close()[["BTC"]]
    w = ensemble_pos(px["BTC"], lookbacks) * (vol_ref / ann_vol(px["BTC"])).clip(upper=1.0)
    return simulate(px, w.to_frame("BTC"), band=0.10)


def btc_tsmom_ls(horizons: tuple = (30, 90, 180), vol_target: float = 0.50) -> pd.DataFrame:
    """Time-series momentum long/short su perp: media dei segni dei rendimenti a 30/90/180 giorni, esposizione scalata
    a volatilita' obiettivo 50% (tetto 1x). Funding reale."""
    px = crypto_perp_close()[["BTC"]]
    c = px["BTC"]
    sig = sum(np.sign(c.pct_change(h)) for h in horizons) / len(horizons)
    w = (sig * (vol_target / ann_vol(c)).clip(upper=1.0)).to_frame("BTC")
    return simulate(px, w, cost=COST_PERP, band=0.15, carry=-crypto_funding()[["BTC"]])


def _radar_weekly():
    spec = importlib.util.spec_from_file_location("radar_weekly", ROOT / "vendor" / "radar_weekly.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["radar_weekly"] = mod
    spec.loader.exec_module(mod)
    return mod


def radar_w3(risk: float = 0.10, lev: float = 1.0, end: str = END) -> tuple[pd.DataFrame, list]:
    """W3.1 del repo radar, codice originale (vendor/radar_weekly.py) e feature congelate del repo. risk=0,10 -> W3.1;
    risk=0,25 -> W3. Ritorna equity e lista dei trade."""
    mod = _radar_weekly()
    mod.R_LONG = mod.R_SHORT = risk
    f = pd.read_csv(DATA / "crypto" / "btc_features_radar.csv.gz", parse_dates=[0], index_col=0).loc[:end]
    r = mod.simulate(f, lev=lev)
    e = r["equity"] / r["equity"].iloc[0]
    trades = r["trades"] + ([r["open"]] if r["open"] else [])
    out = pd.DataFrame({"equity": e, "gross": np.nan, "turnover": 0.0})
    expo = pd.Series(0.0, e.index)
    for t in trades:
        expo.loc[t["entry"]:t.get("exit", end)] = t["expo"]
        out.loc[t["entry"], "turnover"] = t["expo"]
    out["gross"] = expo
    return out, trades


# ------------------------------------------------------------------ paniere crypto
def crypto_trend_basket(vol_ref: float = 0.60, lookbacks: list[int] = DONCHIAN, coins: list[str] = COINS) -> pd.DataFrame:
    """Ensemble Donchian su ogni moneta, peso 1/N scalato a rischio uguale (volatilita' di riferimento 60% ~ BTC, tetto 1,5):
    le alt piu' volatili pesano meno. Solo long, spot, senza leva."""
    px = crypto_close()[coins]
    pos = pd.DataFrame({s: ensemble_pos(px[s].dropna(), lookbacks) for s in coins}).reindex(px.index).fillna(0.0)
    w = pos * (vol_ref / ann_vol(px)).clip(upper=1.5).fillna(0.0) / len(coins)
    return simulate(px, w, band=0.02)


def crypto_rotation(lookback: int = 30, top: int = 3, regime: int = 200, coins: list[str] = COINS, dow: int = 6,
                    vol_ref: float | None = None) -> pd.DataFrame:
    """Rotazione momentum settimanale (decisione alla chiusura della domenica, dow=6): le `top` monete con il rendimento a
    `lookback` giorni piu' alto e positivo, pesi uguali; tutto in liquidita' se BTC e' sotto la media a `regime` giorni.
    vol_ref: se indicato, il peso di ogni moneta e' ridotto a min(1, vol_ref / volatilita' a 60 giorni) (rischio controllato)."""
    px = crypto_close()[coins]
    mom = px.pct_change(lookback)
    ok = px["BTC"] > px["BTC"].rolling(regime).mean()
    rank = mom.where(mom > 0).rank(axis=1, ascending=False)
    w = ((rank <= top).astype(float) / top).where(ok, 0.0)
    if vol_ref:
        w = w * (vol_ref / ann_vol(px)).clip(upper=1.0).fillna(0.0)
    w = w[w.index.dayofweek == dow].reindex(px.index).ffill().fillna(0.0)
    return simulate(px, w, band=0.08)


def funding_carry(coins: tuple = ("BTC", "ETH", "SOL"), x: float = 0.8, smart: bool = False,
                  enter: float = 0.0001, exit_: float = 0.0, n: int = 14) -> pd.DataFrame:
    """Cash-and-carry neutrale al prezzo: long spot + short perp dello stesso controvalore (x = 80% del capitale, il 20% resta
    come margine: leva 4x sul solo lato perp, ribilanciata). Incassa il funding quando e' positivo, lo paga quando e' negativo;
    include la variazione della base perp/spot e i costi delle due gambe. smart=True: una moneta e' attiva solo se il funding
    medio a 14 giorni supera 0,0001/giorno (3,65% annuo) e si spegne quando scende sotto zero."""
    coins = list(coins)
    spot, perp, fund = crypto_close()[coins], crypto_perp_close()[coins], crypto_funding()[coins]
    px = pd.concat([spot.add_suffix("_s"), perp.add_suffix("_p")], axis=1).dropna(how="all")
    on = pd.DataFrame(1.0, index=px.index, columns=coins)
    if smart:
        f = fund.rolling(n).mean().reindex(px.index)
        for s in coins:
            state, col = 0.0, []
            for v in f[s].to_numpy():
                if np.isnan(v):
                    state = 0.0
                elif state == 0.0 and v > enter:
                    state = 1.0
                elif state == 1.0 and v < exit_:
                    state = 0.0
                col.append(state)
            on[s] = col
    on = on.where(perp.reindex(px.index).notna() & spot.reindex(px.index).notna(), 0.0)
    w = pd.concat([(on * x / len(coins)).add_suffix("_s"), (-on * x / len(coins)).add_suffix("_p")], axis=1)
    carry = pd.concat([pd.DataFrame(0.0, index=px.index, columns=[c + "_s" for c in coins]),
                       (-fund.reindex(px.index).fillna(0.0)).add_suffix("_p")], axis=1)
    cost = np.array([COST_SPOT] * len(coins) + [COST_PERP] * len(coins))
    return simulate(px, w[px.columns], cost=cost, band=0.03, carry=carry[px.columns])


# ------------------------------------------------------------------ azioni / ETF
def etf_hold(name: str) -> pd.DataFrame:
    px = equity_close([name])
    tgt = pd.DataFrame(1.0, index=px.index[px.index >= pd.Timestamp(START) - pd.Timedelta(days=7)], columns=[name])
    return simulate(px, tgt, cost=COST_ETF, band=10.0, lag=2, periods=252)


def dual_momentum(assets: tuple = ("SPY", "QQQ", "GLD"), months: int = 12) -> pd.DataFrame:
    """Dual momentum alla Antonacci: a fine mese si tiene l'asset con il rendimento a 12 mesi piu' alto, solo se positivo
    (altrimenti liquidita')."""
    px = equity_close(list(assets)).dropna()
    m = px.resample("ME").last()
    mom = m.pct_change(months).dropna()
    best = mom.idxmax(axis=1)
    w = pd.DataFrame(0.0, index=mom.index, columns=px.columns)
    for d in mom.index:
        if mom.loc[d, best[d]] > 0:
            w.loc[d, best[d]] = 1.0
    w.index = [px.loc[:d].index[-1] for d in w.index]              # ultimo giorno di borsa del mese
    return simulate(px, w.reindex(px.index).ffill().fillna(0.0), cost=COST_ETF, band=10.0, lag=2, periods=252)


def synth_3x(name: str = "QQQ") -> pd.Series:
    """ETF a leva 3x giornaliera SINTETICO (tipo TQQQ): 3 x rendimento giornaliero - finanziamento 2 x (Fed Funds + 0,5%)
    - spese 0,9% annuo. Non e' la serie reale del prodotto."""
    c = equity_close([name])[name].dropna()
    ff = fed_funds().reindex(c.index).ffill()
    r = 3 * c.pct_change().fillna(0.0) - (2 * (ff + 0.005) + 0.009) / 252
    return (1 + r).cumprod()


def qqq3x_sma200(sma: int = 200) -> pd.DataFrame:
    """3x Nasdaq-100 sintetico solo quando QQQ chiude sopra la media a 200 giorni, altrimenti liquidita'."""
    q = equity_close(["QQQ"])["QQQ"].dropna()
    px = synth_3x("QQQ").to_frame("QQQ3x")
    w = (q > q.rolling(sma).mean()).astype(float).to_frame("QQQ3x")
    return simulate(px, w, cost=COST_ETF * 2, band=10.0, lag=2, periods=252)


def megacap_rotation(months: int = 6, top: int = 3) -> pd.DataFrame:
    """Momentum mensile sulle 10 azioni del repo radar (le 10 maggiori di OGGI: distorsione da sopravvivenza, limite superiore
    non replicabile): le 3 con il rendimento a 6 mesi piu' alto, solo se SPY e' sopra la media a 200 giorni."""
    px = equity_close(STOCKS).dropna()
    spy = equity_close(["SPY"])["SPY"].reindex(px.index)
    m = px.resample("ME").last()
    rank = m.pct_change(months).rank(axis=1, ascending=False)
    w = (rank <= top).astype(float) / top
    w.index = [px.loc[:d].index[-1] for d in w.index]
    w = w[~w.index.duplicated()].reindex(px.index).ffill().fillna(0.0)
    w = w.where(spy > spy.rolling(200).mean(), 0.0)
    return simulate(px, w, cost=COST_ETF, band=0.10, lag=2, periods=252)


# ------------------------------------------------------------------ portafogli di strategie
def blend(curves: dict[str, pd.Series], weights: dict[str, float], band: float = 0.05) -> pd.DataFrame:
    """Portafoglio di strategie a pesi fissi, ribilanciato quando un peso devia di 5 punti. Le curve azionarie sono
    riportate sui giorni di calendario (sabato e domenica = ultimo valore)."""
    idx = pd.date_range(START, END, freq="D")
    px = pd.DataFrame({k: curves[k].reindex(idx.union(curves[k].index)).ffill().reindex(idx) for k in weights})
    px = px.bfill()
    tgt = pd.DataFrame({k: weights[k] for k in weights}, index=idx)
    first = pd.DataFrame({k: weights[k] for k in weights}, index=[idx[0] - pd.Timedelta(days=1)])
    px = pd.concat([px.iloc[:1].set_axis([idx[0] - pd.Timedelta(days=1)]), px])
    return simulate(px, pd.concat([first, tgt]), cost=0.0, band=band)
