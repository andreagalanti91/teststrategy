"""Motore comune: dati, simulazione a pesi con costi, metriche.

Convenzioni (uguali per tutte le strategie, per un confronto alla pari):
- capitale iniziale 10.000 $, periodo 01/01/2021 -> 10/11/2026 (ultima data comune a tutti i dataset);
- il segnale si calcola sulla chiusura del giorno t, la posizione vale dal giorno t+1 (crypto: chiusura 00:00 UTC = apertura
  successiva; azioni/ETF: un giorno di ritardo in piu', esecuzione alla chiusura di t+1);
- costi per lato sul controvalore scambiato: crypto spot 0,20% (0,10% commissione + 0,10% slippage, come radar/weekly.py),
  perp 0,15%, ETF/azioni 0,05%;
- la liquidita' non rende (come nel repo radar): scelta prudente;
- nessuna leva salvo dove indicato; il finanziamento della leva costa Fed Funds + 1% annuo.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
START, END = "2021-01-01", "2026-11-10"
SPLIT = "2024-01-01"                    # prima meta' (2021-23) / seconda meta' (2024-26)
CAPITAL = 10_000.0
COST_SPOT, COST_PERP, COST_ETF = 0.0020, 0.0015, 0.0005
COINS = ["BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "DOGE", "LINK", "TRX", "XMR", "ZEC"]
STOCKS = ["AAPL", "AMZN", "AVGO", "BRK-B", "GOOGL", "LLY", "META", "MSFT", "NVDA", "TSLA"]


# ------------------------------------------------------------------ dati
def _csv(path: Path) -> pd.DataFrame:
    d = pd.read_csv(path, parse_dates=[0], index_col=0)
    return d[~d.index.duplicated()].sort_index()


def crypto_close() -> pd.DataFrame:
    """Chiusure giornaliere spot Binance <SYM>USDT; dove lo spot manca (XMR delistato dal 20/02/2024) prezzo del perp."""
    out = {}
    for s in COINS:
        spot, perp = _csv(DATA / "crypto" / f"{s}_spot.csv")["close"], _csv(DATA / "crypto" / f"{s}_perp.csv")["close"]
        out[s] = spot.combine_first(perp)
    return pd.DataFrame(out).loc[:END]


def crypto_perp_close() -> pd.DataFrame:
    return pd.DataFrame({s: _csv(DATA / "crypto" / f"{s}_perp.csv")["close"] for s in COINS}).loc[:END]


def crypto_funding() -> pd.DataFrame:
    """Funding giornaliero (somma delle 3 rate da 8 ore) pagato dai long ai short quando positivo."""
    f = pd.DataFrame({s: _csv(DATA / "crypto" / f"{s}_funding.csv")["funding"] for s in COINS})
    btc = _csv(DATA / "crypto" / "BTC_funding_radar.csv")["funding"]      # copre anche novembre 2026
    f = f.reindex(f.index.union(btc.index))
    f["BTC"] = f["BTC"].combine_first(btc)
    return f.loc[:END]


def equity_close(names: list[str]) -> pd.DataFrame:
    """Chiusure rettificate per dividendi e frazionamenti (Yahoo, congelate nel repo radar)."""
    return pd.DataFrame({s: _csv(DATA / "equity" / f"{s}.csv.gz")["close"] for s in names}).loc[:END]


def fed_funds() -> pd.Series:
    return _csv(DATA / "macro" / "DFF.csv")["DFF"] / 100.0


# ------------------------------------------------------------------ simulazione
def simulate(prices: pd.DataFrame, target: pd.DataFrame, cost: float | pd.Series = COST_SPOT, lag: int = 1,
             carry: pd.DataFrame | None = None, band: float = 0.0, borrow: pd.Series | None = None,
             periods: int = 365) -> pd.DataFrame:
    """Portafoglio a pesi obiettivo. target[t] = pesi decisi sulla chiusura di t, attivi da t+lag.
    I pesi derivano con il prezzo; si ribilancia solo quando l'obiettivo si sposta di piu' di `band` (in peso) dal peso
    effettivo: cosi' i costi non vengono gonfiati da micro-aggiustamenti. carry[t] = rendimento giornaliero aggiuntivo
    per unita' di peso (es. -funding per un long in perp). borrow = tasso annuo pagato sulla parte di esposizione oltre 1.
    Ritorna DataFrame con equity (base 1), esposizione lorda e turnover giornaliero."""
    prices = prices.loc[:END]
    r = prices.pct_change().fillna(0.0)
    tgt = target.reindex(prices.index).shift(lag).fillna(0.0)
    car = carry.reindex(prices.index).fillna(0.0) if carry is not None else None
    cst = np.broadcast_to(np.asarray(cost, float), (prices.shape[1],)) if not np.isscalar(cost) else np.full(prices.shape[1], cost)
    R, T = r.to_numpy(), tgt.to_numpy()
    n, k = R.shape
    w = np.zeros(k)                      # pesi effettivi a inizio giornata (frazione dell'equity)
    eq = np.ones(n)
    gross, turn = np.zeros(n), np.zeros(n)
    bor = borrow.reindex(prices.index).ffill().fillna(0.0).to_numpy() if borrow is not None else np.zeros(n)
    e = 1.0
    for i in range(n):
        # ribilanciamento all'apertura del giorno i verso T[i] (deciso sulla chiusura di i-lag)
        d = T[i] - w
        move = np.abs(d) > band
        move |= ((T[i] == 0) & (w != 0)) | ((T[i] != 0) & (w == 0))   # ingressi da zero e uscite complete si eseguono sempre
        if move.any():
            tc = float((np.abs(d[move]) * cst[move]).sum())
            w = np.where(move, T[i], w)
            e *= 1 - tc
            turn[i] = float(np.abs(d[move]).sum())
        g = float(np.abs(w).sum())
        day = float((w * R[i]).sum())
        if car is not None:
            day += float((w * car.iloc[i].to_numpy()).sum())
        day -= max(0.0, g - 1.0) * bor[i] / periods
        e *= 1 + day
        gross[i], eq[i] = g, e
        w = w * (1 + R[i]) / (1 + day) if day > -1 else np.zeros(k)   # deriva dei pesi
    out = pd.DataFrame({"equity": eq, "gross": gross, "turnover": turn}, index=prices.index)
    return out


# ------------------------------------------------------------------ metriche
def _cagr(e: pd.Series) -> float:
    yrs = (e.index[-1] - e.index[0]).days / 365.25
    return float((e.iloc[-1] / e.iloc[0]) ** (1 / yrs) - 1) if yrs > 0 and e.iloc[-1] > 0 else float("nan")


def _dd(e: pd.Series) -> float:
    return float((e / e.cummax() - 1).min())


def metrics(e: pd.Series, gross: pd.Series | None = None, turnover: pd.Series | None = None, periods: int = 365) -> dict:
    """e = equity giornaliera. Rendimento totale, CAGR, drawdown giornaliero massimo, Sharpe (tasso zero), MAR = CAGR/|DD|,
    anni singoli, due meta'."""
    e = e.loc[START:END].dropna()
    e = e / e.iloc[0]
    r = e.pct_change().dropna()
    r = r[r.index.dayofweek < 5] if periods == 252 else r
    yrs = {}
    prev = 1.0
    for y, v in e.groupby(e.index.year).last().items():
        yrs[int(y)] = v / prev - 1
        prev = v
    a, b = e.loc[:SPLIT], e.loc[SPLIT:]
    dd = _dd(e)
    under = (e / e.cummax() - 1)
    longest = int((under < 0).astype(int).groupby((under == 0).cumsum()).sum().max())
    m = {"final": CAPITAL * float(e.iloc[-1]), "total": float(e.iloc[-1] - 1), "cagr": _cagr(e), "dd": dd,
         "sharpe": float(r.mean() / r.std() * np.sqrt(periods)) if r.std() > 0 else float("nan"),
         "mar": _cagr(e) / abs(dd) if dd < 0 else float("nan"), "vol": float(r.std() * np.sqrt(periods)),
         "worst_year": min(yrs.values()), "years": yrs, "underwater_days": longest,
         "cagr_a": _cagr(a), "dd_a": _dd(a), "cagr_b": _cagr(b), "dd_b": _dd(b)}
    if gross is not None:
        g = gross.loc[START:END]
        m["time_in"] = float((g > 0.01).mean())
        m["avg_gross"] = float(g.mean())
    if turnover is not None:
        t = turnover.loc[START:END]
        m["turnover_yr"] = float(t.sum() / ((e.index[-1] - e.index[0]).days / 365.25))
        m["trades_yr"] = float((t > 0).sum() / ((e.index[-1] - e.index[0]).days / 365.25))
    return m


def lever(e: pd.Series, L: float, borrow: pd.Series, periods: int = 365) -> pd.Series:
    """Stessa strategia con leva L ribilanciata ogni giorno: rendimento giornaliero x L meno il costo del prestito sulla
    parte oltre 1. Approssimazione (ignora i costi del ribilanciamento della leva): ottimistica."""
    e = e.loc[START:END]
    r = e.pct_change().fillna(0.0)
    b = borrow.reindex(r.index).ffill().fillna(0.0)
    rl = (L * r - max(0.0, L - 1.0) * b / periods).clip(lower=-1.0)
    return (1 + rl).cumprod()


def leverage_for(e: pd.Series, target_cagr: float, borrow: pd.Series, periods: int = 365, lmax: float = 20.0):
    """Leva minima (griglia 0,05) che porta il CAGR al target; None se non ci si arriva (la leva oltre l'ottimo di Kelly
    riduce il rendimento composto)."""
    best = None
    for L in np.arange(1.0, lmax + 1e-9, 0.05):
        el = lever(e, float(L), borrow, periods)
        if el.iloc[-1] <= 0:
            break
        c = _cagr(el)
        if c >= target_cagr:
            best = (float(L), c, _dd(el))
            break
    return best
