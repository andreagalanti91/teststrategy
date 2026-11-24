"""Ciclo di ricerca sulle aree non ancora toccate:
A) quanto sono "veri" i risultati: Sharpe probabilistico e deflazionato (Bailey, Lopez de Prado), durata minima del track record;
B) quanta leva: crescita composta al variare della leva (Kelly) e bootstrap a blocchi di W3.2;
C) premio di volatilita' su BTC: volatilita' implicita (Deribit DVOL) contro realizzata, e strategie che vendono opzioni
   prezzate con Black-Scholes;
D) W3.2 espressa con opzioni comprate (perdita massima definita).
Scrive results/ricerca/tables.md e un grafico. Nessun dato futuro: ogni ciclo usa solo la volatilita' implicita del giorno d'ingresso."""
from __future__ import annotations

import math
import sys
from pathlib import Path
from statistics import NormalDist

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import btc_ta as B

ROOT = B.ROOT
OUT = ROOT / "results" / "ricerca"
OUT.mkdir(parents=True, exist_ok=True)
ND = NormalDist()
EULER = 0.5772156649
pct = lambda x, d=1: "n/d" if x is None or not np.isfinite(x) else f"{x * 100:+.{d}f}%".replace(".", ",")
usd = lambda x: f"{x:,.0f}".replace(",", ".")
num = lambda x, d=2: "n/d" if x is None or not np.isfinite(x) else f"{x:.{d}f}".replace(".", ",")
T = []


# ================================================================== A · quanto sono veri i risultati
def weekly_ret(e: pd.Series) -> pd.Series:
    return e.dropna().resample("W-SUN").last().pct_change().dropna()


def psr(r: pd.Series, sr_star: float = 0.0) -> float:
    """Probabilita' che lo Sharpe vero superi sr_star (per periodo), dati asimmetria e code dei rendimenti."""
    sr, n = r.mean() / r.std(), len(r)
    g3, g4 = float(r.skew()), float(r.kurt()) + 3.0
    den = math.sqrt(max(1e-12, 1 - g3 * sr + (g4 - 1) / 4 * sr ** 2))
    return ND.cdf((sr - sr_star) * math.sqrt(n - 1) / den)


def sr0(n_trials: int, sd_sr: float) -> float:
    """Sharpe atteso del migliore fra n_trials tentativi senza abilita', con dispersione sd_sr fra i tentativi."""
    if n_trials <= 1:
        return 0.0
    return sd_sr * ((1 - EULER) * ND.inv_cdf(1 - 1 / n_trials) + EULER * ND.inv_cdf(1 - 1 / (n_trials * math.e)))


def min_trl_years(r: pd.Series, conf: float = 0.95) -> float:
    sr = r.mean() / r.std()
    if sr <= 0:
        return float("inf")
    g3, g4 = float(r.skew()), float(r.kurt()) + 3.0
    return (1 + (1 - g3 * sr + (g4 - 1) / 4 * sr ** 2) * (ND.inv_cdf(conf) / sr) ** 2) / 52


def part_a() -> dict:
    a = pd.read_csv(ROOT / "results" / "w32" / "equity.csv", index_col=0, parse_dates=True)
    al = pd.read_csv(ROOT / "results" / "algo" / "equity_finale.csv", index_col=0, parse_dates=True)["equity"]
    b = pd.read_csv(ROOT / "results" / "equity.csv", index_col=0, parse_dates=True)
    S = {"W3.2 radar, 2018–2026": a["W3.2 radar (rischio 25%)"], "W3.2 radar, dal 2021 (dati reali)": a["W3.2 radar (rischio 25%)"].loc["2021-01-01":],
         "v1 · voto di 17 indicatori, 2018–2026": a["v1 · voto di 17 indicatori"], "v1, solo verifica 2022–2026": a["v1 · voto di 17 indicatori"].loc["2022-01-01":],
         "v2 · tre schermi, 2018–2026": a["v2 · tre schermi"], "MACD a regime (altcoin), dal 2020": al, "Carry funding selettivo, dal 2021": b["Carry funding selettivo"],
         "BTC comprato e tenuto, 2018–2026": a["BTC comprato e tenuto"]}
    g1 = pd.read_csv(ROOT / "results" / "btc" / "griglia_composito.csv")
    g2 = pd.read_csv(ROOT / "results" / "regole" / "griglia_v2.csv")
    sd1, sd2 = float(g1.is_sharpe.std()), float(g2.is_sharpe.std())
    T.append("## A1 sharpe\n")
    T.append(f"Dispersione dello Sharpe annuo fra le varianti provate in questa ricerca: {num(sd1)} fra le {len(g1)} soglie di v1, {num(sd2)} fra le {len(g2)} varianti di v2. "
             f"Per la colonna \"deflazionato\" si assume una dispersione di 0,5 fra i tentativi. Sharpe che il migliore di N tentativi senza abilità raggiunge per caso, "
             f"su base annua: N=10 → {num(sr0(10, 0.5))}; N=100 → {num(sr0(100, 0.5))}; N=1.000 → {num(sr0(1000, 0.5))}.\n")
    T.append("| Strategia | Anni | Sharpe annuo (settimanale) | Asimmetria | Probabilità che lo Sharpe vero sia > 0 | Deflazionato, 10 tentativi | 100 tentativi | 1.000 tentativi | Anni minimi per esserne certi al 95% |")
    T.append("|---|---|---|---|---|---|---|---|---|")
    res = {}
    for k, e in S.items():
        r = weekly_ret(e)
        sr_a = r.mean() / r.std() * math.sqrt(52)
        d = [psr(r, sr0(n, 0.5) / math.sqrt(52)) for n in (10, 100, 1000)]
        res[k] = sr_a
        T.append(f"| {k} | {len(r) / 52:.1f} | {num(sr_a)} | {num(float(r.skew()), 1)} | {psr(r) * 100:.1f}% | {d[0] * 100:.0f}% | {d[1] * 100:.0f}% | {d[2] * 100:.0f}% | {num(min_trl_years(r), 1)} |".replace(".", ",", 1) if False else
                 f"| {k} | {num(len(r) / 52, 1)} | {num(sr_a)} | {num(float(r.skew()), 1)} | {num(psr(r) * 100, 1)}% | {d[0] * 100:.0f}% | {d[1] * 100:.0f}% | {d[2] * 100:.0f}% | {num(min_trl_years(r), 1)} |")
    return {"w32": a["W3.2 radar (rischio 25%)"], "v1": a["v1 · voto di 17 indicatori"], "btc": a["BTC comprato e tenuto"]}


# ================================================================== B · quanta leva
def part_b(w32: pd.Series) -> None:
    T.append("\n## B1 kelly\n")
    BORROW = 0.06                                        # costo annuo della parte di esposizione oltre 1x
    T.append("| Campione | Rendimento medio annuo (aritmetico) | Volatilità annua | Leva di Kelly teorica (media / varianza) | Leva che massimizza la crescita nello storico | Crescita annua a 1x | a metà di quella leva | a quella leva | al doppio | Leva oltre cui la crescita diventa negativa |")
    T.append("|---|---|---|---|---|---|---|---|---|---|")
    grid = np.arange(0.25, 12.01, 0.25)

    def growth(r, f):
        x = 1 + f * r - max(0.0, f - 1) * BORROW / 365
        return -1.0 if (x <= 0).any() else float(np.exp(np.log(x).mean() * 365) - 1)

    for lab, e in (("W3.2, 2018–2026", w32), ("W3.2, dal 2021", w32.loc["2021-01-01":]), ("W3.2 dal 2021, con il vantaggio dimezzato", w32.loc["2021-01-01":])):
        r = e.pct_change().dropna().to_numpy()
        if "dimezzato" in lab:
            r = r - r.mean() / 2
        mu, sd = r.mean() * 365, r.std() * math.sqrt(365)
        g = np.array([growth(r, f) for f in grid])
        fs = float(grid[int(np.argmax(g))])
        neg = grid[(g < 0) & (grid > fs)]
        T.append(f"| {lab} | {pct(mu)} | {pct(sd)} | {num(mu / sd ** 2, 1)}x | {num(fs, 2)}x | {pct(growth(r, 1.0))} | {pct(growth(r, fs / 2))} | {pct(growth(r, fs))} | {pct(growth(r, min(2 * fs, 12)))} | "
                 f"{num(float(neg[0]), 2) + 'x' if len(neg) else 'oltre 12x'} |")

    T.append("\n## B2 bootstrap\n")
    rng = np.random.default_rng(42)
    T.append("| Campione | Leva | CAGR mediano a 3 anni | 5° percentile | Probabilità di chiudere in perdita | Drawdown mediano | Probabilità di drawdown oltre −35% | oltre −50% |")
    T.append("|---|---|---|---|---|---|---|---|")
    for lab, e in (("W3.2, 2018–2026", w32), ("W3.2, dal 2021", w32.loc["2021-01-01":])):
        r = weekly_ret(e).to_numpy()
        n, H, BL, NS = len(r), 156, 8, 4000
        starts = rng.integers(0, n - BL, size=(NS, H // BL + 1))
        paths = np.concatenate([r[s:s + BL] for s in starts.ravel()]).reshape(NS, -1)[:, :H]
        for f in (0.5, 1.0, 1.5, 2.0, 3.0):
            x = np.clip(1 + f * paths - max(0.0, f - 1) * BORROW / 52, 0, None)
            eq = np.cumprod(x, axis=1)
            cagr = eq[:, -1] ** (1 / 3) - 1
            dd = (eq / np.maximum.accumulate(np.maximum(eq, 1e-12), axis=1) - 1).min(axis=1)
            T.append(f"| {lab} | {num(f, 1)}x | {pct(float(np.median(cagr)))} | {pct(float(np.percentile(cagr, 5)))} | {(cagr < 0).mean() * 100:.0f}% | {pct(float(np.median(dd)))} | "
                     f"{(dd < -0.35).mean() * 100:.0f}% | {(dd < -0.50).mean() * 100:.0f}% |")


# ================================================================== C · premio di volatilita'
def bs(S: float, K: float, tau: float, sig: float, cp: int, b: float = 0.0) -> float:
    """Black sul prezzo a termine F = S·e^(b·tau), senza sconto (opzioni a margine, come su Deribit). cp = +1 call, -1 put.
    b = costo annuo di portare la posizione (base del future, cioe' funding atteso); b = 0 e' Black-Scholes a tasso zero."""
    if tau <= 0 or sig <= 0:
        return max(0.0, cp * (S - K))
    F = S * math.exp(b * tau)
    v = sig * math.sqrt(tau)
    d1 = (math.log(F / K) + 0.5 * v * v) / v
    call = F * ND.cdf(d1) - K * ND.cdf(d1 - v)
    return call if cp > 0 else call - F + K


def delta(S: float, K: float, tau: float, sig: float, cp: int, b: float = 0.0) -> float:
    """Delta rispetto allo spot (e quindi al perp)."""
    if tau <= 0 or sig <= 0:
        return (1.0 if S > K else 0.0) * cp if cp > 0 else (-1.0 if S < K else 0.0)
    g = math.exp(b * tau)
    d1 = (math.log(S * g / K) + 0.5 * sig * sig * tau) / (sig * math.sqrt(tau))
    return g * ND.cdf(d1) if cp > 0 else g * (ND.cdf(d1) - 1.0)


def iv_series(d: pd.DataFrame) -> pd.Series:
    """Volatilita' implicita annua (frazione): DVOL giornaliero dal 24/03/2021; prima, IV at-the-money dei contratti scambiati
    la domenica su Deribit (settimanale, tenuto fermo fino alla domenica dopo): approssimazione, usata solo per il 2019-2021."""
    dv = pd.read_csv(ROOT / "data" / "opzioni" / "dvol_btc_1d.csv", parse_dates=[0], index_col=0)["close"] / 100
    su = pd.read_csv(ROOT / "data" / "opzioni" / "deribit_opt_sunday.csv", parse_dates=[0], index_col=0)["atm_iv"] / 100
    idx = d.index[(d.index >= su.index[0]) & (d.index <= dv.index[-1])]
    return dv.reindex(idx).combine_first(su.reindex(idx, method="ffill")).ffill()


_FU = {}


def funding_daily(days: pd.DatetimeIndex) -> tuple[np.ndarray, np.ndarray]:
    """Funding giornaliero del perp BTC (somma delle tre rate) e costo annuo atteso di portare la posizione, stimato con la media
    dei 7 giorni gia' passati. Prima del 2020 non c'e' il dato: si usa la media dell'intero storico."""
    key = (days[0], days[-1], len(days))
    if key not in _FU:
        f = pd.read_csv(ROOT / "data" / "btc" / "funding.csv", index_col=0, parse_dates=True)["funding"]
        f = f.reindex(days).fillna(float(f.mean()))
        _FU[key] = (f.to_numpy(), (f.rolling(7, min_periods=1).mean() * 365).to_numpy())
    return _FU[key]


def cycles(c: pd.Series, iv: pd.Series, legs: list, und: float = 0.0, notional: float = 1.0, offset: int = 0, tenor: int = 30, filt=None,
           haircut: float = 0.04, fee: float = 0.0003, hedge: bool = False, hedge_cost: float = 0.0005, carry: bool = False) -> tuple[pd.Series, list]:
    """Un comparto che ogni `tenor` giorni apre le gambe indicate (cp, moneyness, quantita': negativa = venduta) su `notional` volte
    il capitale, le tiene a scadenza e ricomincia. Valore giornaliero a mercato con Black-Scholes e l'IV del giorno.
    Costi: `haircut` del premio (denaro-lettera) e `fee` del sottostante per gamba (tetto 12,5% del premio), come su Deribit."""
    days = iv.index
    S, IV = c.reindex(days).to_numpy(), iv.to_numpy()
    FU, CA = funding_daily(days) if carry else (np.zeros(len(days)), np.zeros(len(days)))
    eq, e, i, out = np.full(len(days), np.nan), 1.0, offset, []
    eq[:offset + 1] = 1.0
    while i + tenor < len(days):
        s0, v0 = S[i], IV[i]
        on = True if filt is None else bool(filt.reindex([days[i]]).iloc[0])
        prem = [bs(s0, m * s0, tenor / 365, v0, cp, CA[i]) for cp, m, q in legs] if on else []
        cost = sum(haircut * p + min(fee * s0, 0.125 * p) for p in prem) if on else 0.0
        # copertura del delta sul perp, aggiustata ogni giorno alla chiusura: h = quantita' di BTC tenuta per annullare il delta
        h = -sum(q * delta(s0, m * s0, tenor / 365, v0, cp, CA[i]) for cp, m, q in legs) if (on and hedge) else 0.0
        hpl = -abs(h) * hedge_cost if hedge else 0.0
        for k in range(1, tenor + 1):
            s, tau = S[i + k], (tenor - k) / 365
            pl = und * (s / s0 - 1)
            if on:
                if hedge:
                    hpl += h * (s - S[i + k - 1]) / s0 - h * FU[i + k] * S[i + k - 1] / s0      # il perp long paga il funding, lo short lo incassa
                    hn = -sum(q * delta(s, m * s0, tau, IV[i + k], cp, CA[i + k]) for cp, m, q in legs) if k < tenor else 0.0
                    hpl -= abs(hn - h) * hedge_cost * s / s0
                    h = hn
                pl += sum(q * (bs(s, m * s0, tau, IV[i + k], cp, CA[i + k]) - p) for (cp, m, q), p in zip(legs, prem)) / s0 - cost / s0 + hpl
            eq[i + k] = max(0.0, e * (1 + notional * pl))
        out.append((days[i], on, eq[i + tenor] / e - 1))
        e = eq[i + tenor]
        i += tenor
    return pd.Series(eq, days).ffill(), out


def portfolio(c, iv, legs, und=0.0, notional=1.0, filt=None, tenor=30, hedge=False, carry=None):
    """Quattro comparti da un quarto del capitale, partiti a 0, 7, 15 e 22 giorni: riduce la dipendenza dal giorno di partenza."""
    parts, cyc = [], []
    for off in (0, 7, 15, 22):
        e, o = cycles(c, iv, legs, und, notional, off, tenor, filt, hedge=hedge, carry=hedge if carry is None else carry)
        parts.append(e)
        cyc += o
    return pd.concat(parts, axis=1).mean(axis=1), cyc


def perf(e: pd.Series, a=None, b=None) -> dict:
    e = e.loc[a:b].dropna()
    e = e / e.iloc[0]
    yrs = (e.index[-1] - e.index[0]).days / 365.25
    r = e.pct_change().dropna()
    m = e.resample("ME").last().pct_change().dropna()
    return {"cagr": float(e.iloc[-1] ** (1 / yrs) - 1) if e.iloc[-1] > 0 else -1.0, "dd": float((e / e.cummax() - 1).min()),
            "sharpe": float(r.mean() / r.std() * math.sqrt(365)) if r.std() > 0 else float("nan"), "worst_m": float(m.min()) if len(m) else float("nan"),
            "final": float(e.iloc[-1])}


def part_c(d: pd.DataFrame, w32: pd.Series) -> dict:
    c = d["close"]
    iv = iv_series(d)
    lr = np.log(c / c.shift(1))
    rv_f = np.sqrt((lr ** 2).rolling(30).mean().shift(-30) * 365)          # realizzata nei 30 giorni DOPO
    rv_p = np.sqrt((lr ** 2).rolling(30).mean() * 365)                     # realizzata nei 30 giorni PRIMA
    x = pd.DataFrame({"iv": iv, "rvf": rv_f.reindex(iv.index), "rvp": rv_p.reindex(iv.index)}).dropna()
    x["vrp"] = x.iv - x.rvf
    x.to_csv(OUT / "iv_rv.csv")
    T.append("\n## C1 premio\n")
    T.append("| Periodo | Giorni | Volatilità implicita media | Realizzata nei 30 giorni dopo | Differenza media | Mediana | Giorni in cui l'implicita è stata più alta | Giorno peggiore (realizzata − implicita) |")
    T.append("|---|---|---|---|---|---|---|---|")
    for lab, a, b in (("2019 – 03/2021 (IV approssimata)", "2019-01-01", "2021-03-23"), ("03/2021 – 2023 (DVOL)", "2021-03-24", "2023-12-31"), ("2024 – 2026 (DVOL)", "2024-01-01", None),
                      ("Tutto", None, None)):
        y = x.loc[a:b]
        T.append(f"| {lab} | {len(y)} | {y.iv.mean() * 100:.0f}% | {y.rvf.mean() * 100:.0f}% | {num(y.vrp.mean() * 100, 1)} punti | {num(y.vrp.median() * 100, 1)} | {(y.vrp > 0).mean() * 100:.0f}% | "
                 f"{num(-y.vrp.min() * 100, 0)} punti il {y.vrp.idxmin().date()} |")
    T.append(f"\nCorrelazione fra il premio (implicita − realizzata dopo) e il rendimento di BTC negli stessi 30 giorni: {num(x.vrp.corr((c.shift(-30) / c - 1).reindex(x.index)))}. "
             f"Con il valore assoluto del rendimento: {num(x.vrp.corr((c.shift(-30) / c - 1).abs().reindex(x.index)))}.")

    sma200 = c > c.rolling(200).mean()
    ivhi = (iv > rv_p.reindex(iv.index)).fillna(False)
    ivrank = (iv.rolling(365, min_periods=180).rank(pct=True) > 0.5).fillna(False)   # solo dati passati
    STR = {
        "Straddle venduto alla pari, 1x": dict(legs=[(1, 1.0, -1), (-1, 1.0, -1)]),
        "Straddle venduto, 0,25x": dict(legs=[(1, 1.0, -1), (-1, 1.0, -1)], notional=0.25),
        "Straddle venduto con copertura giornaliera del delta, 1x": dict(legs=[(1, 1.0, -1), (-1, 1.0, -1)], hedge=True),
        "· controllo: senza funding (copertura con il future della stessa scadenza)": dict(legs=[(1, 1.0, -1), (-1, 1.0, -1)], hedge=True, carry=False),
        "Straddle coperto, solo se implicita > realizzata passata": dict(legs=[(1, 1.0, -1), (-1, 1.0, -1)], hedge=True, filt=ivhi),
        "Straddle coperto, solo se implicita sopra la sua mediana a un anno": dict(legs=[(1, 1.0, -1), (-1, 1.0, -1)], hedge=True, filt=ivrank),
        "Strangle ±15% con copertura giornaliera del delta, 1x": dict(legs=[(1, 1.15, -1), (-1, 0.85, -1)], hedge=True),
        "Strangle venduto ±15%, 1x": dict(legs=[(1, 1.15, -1), (-1, 0.85, -1)]),
        "Strangle ±15%, solo se implicita > realizzata passata": dict(legs=[(1, 1.15, -1), (-1, 0.85, -1)], filt=ivhi),
        "Put venduta −10% con liquidità a garanzia": dict(legs=[(-1, 0.90, -1)]),
        "Put venduta −10%, solo sopra la SMA 200": dict(legs=[(-1, 0.90, -1)], filt=sma200.reindex(iv.index).fillna(False)),
        "BTC + call venduta +10% (covered call)": dict(legs=[(1, 1.10, -1)], und=1.0),
        "BTC comprato e tenuto (riferimento)": dict(legs=[], und=1.0),
    }
    T.append("\n## C2 strategie\n")
    T.append("| Strategia (scadenze a 30 giorni, 4 comparti sfalsati) | 10.000 $ → | CAGR | Max DD | Sharpe | Mese peggiore | Cicli in guadagno | CAGR / DD 2019–03/2021 | CAGR / DD 03/2021–2023 | CAGR / DD 2024–2026 |")
    T.append("|---|---|---|---|---|---|---|---|---|---|")
    E = {}
    for k, kw in STR.items():
        e, cyc = portfolio(c, iv, **kw)
        E[k] = e
        on = [z for z in cyc if z[1]]
        p, pa, pb, pc = perf(e), perf(e, None, "2021-03-23"), perf(e, "2021-03-24", "2023-12-31"), perf(e, "2024-01-01", None)
        T.append(f"| {k} | {usd(10000 * p['final'])} | {pct(p['cagr'])} | {pct(p['dd'])} | {num(p['sharpe'])} | {pct(p['worst_m'])} | "
                 f"{(np.mean([z[2] > 0 for z in on]) * 100 if on else 0):.0f}% di {len(on)} | {pct(pa['cagr'], 0)} / {pct(pa['dd'], 0)} | {pct(pb['cagr'], 0)} / {pct(pb['dd'], 0)} | {pct(pc['cagr'], 0)} / {pct(pc['dd'], 0)} |")
    pd.DataFrame(E).to_csv(OUT / "equity_opzioni.csv")

    # con W3.2
    T.append("\n## C3 insieme\n")
    wr = w32.pct_change().fillna(0.0)
    T.append("| Combinazione (ribilanciata ogni giorno, dal 2019) | CAGR | Max DD | Sharpe | Correlazione mensile con W3.2 |")
    T.append("|---|---|---|---|---|")
    base = (1 + wr.loc[iv.index[0]:iv.index[-1]]).cumprod()
    pb_ = perf(base)
    T.append(f"| W3.2 da sola | {pct(pb_['cagr'])} | {pct(pb_['dd'])} | {num(pb_['sharpe'])} | – |")
    pc_ = perf((1 + 0.8 * wr.loc[iv.index[0]:iv.index[-1]]).cumprod())
    T.append(f"| 80% W3.2 + 20% liquidità (riferimento) | {pct(pc_['cagr'])} | {pct(pc_['dd'])} | {num(pc_['sharpe'])} | – |")
    for k in ("Straddle venduto con copertura giornaliera del delta, 1x", "Put venduta −10% con liquidità a garanzia", "Put venduta −10%, solo sopra la SMA 200"):
        sr_ = E[k].pct_change().fillna(0.0)
        mm = pd.concat([wr, sr_], axis=1).dropna().resample("ME").apply(lambda z: (1 + z).prod() - 1).corr().iloc[0, 1]
        for wgt in (0.2,):
            cmb = (1 + (1 - wgt) * wr.reindex(sr_.index).fillna(0) + wgt * sr_).cumprod()
            pp = perf(cmb)
            T.append(f"| 80% W3.2 + 20% {k.lower()} | {pct(pp['cagr'])} | {pct(pp['dd'])} | {num(pp['sharpe'])} | {num(mm)} |")
    return {"iv": iv, "E": E, "x": x}


# ================================================================== D · W3.2 con opzioni comprate
def part_d(d: pd.DataFrame, iv: pd.Series) -> None:
    c = d["close"]
    tr = pd.read_csv(ROOT / "results" / "w32" / "movimenti_w32.csv")
    tr["entra"] = pd.to_datetime(tr["entra"])
    tr["esce"] = pd.to_datetime(tr["esce"]).fillna(iv.index[-1])
    tr = tr[tr.entra >= iv.index[0]].reset_index(drop=True)
    T.append("\n## D1 opzioni\n")
    T.append(f"Operazioni di W3.2 dal {iv.index[0].date()} (prima non c'è volatilità implicita): {len(tr)}. A ogni ingresso si compra un'opzione alla pari (call per i long, put per gli short) "
             "spendendo una quota fissa del capitale; si rivende quando W3.2 esce, o si incassa il valore a scadenza. Costo denaro-lettera: 4% del premio per lato.\n")
    T.append("| Versione | Capitale finale da 10.000 $ | Operazioni in guadagno | Operazione peggiore | Operazione migliore | Perdita massima per operazione | Capitale composto nelle sole perdenti consecutive peggiori |")
    T.append("|---|---|---|---|---|---|---|")
    base = float(np.prod(1 + tr.sul_capitale))
    worst_run = lambda r: float(min(np.prod(1 + r[i:j]) - 1 for i in range(len(r)) for j in range(i + 1, len(r) + 1)))
    T.append(f"| W3.2 originale (spot e perp) | {usd(10000 * base)} | {(tr.sul_capitale > 0).mean() * 100:.0f}% | {pct(tr.sul_capitale.min())} | {pct(tr.sul_capitale.max())} | fino a −25% (stop) | {pct(worst_run(tr.sul_capitale.to_numpy()))} |")
    # W3.1 (stessi segnali, rischio allo stop 10%): confronto a parita' di perdita pianificata
    import importlib.util
    sp = importlib.util.spec_from_file_location("radar_weekly_w31", ROOT / "vendor" / "radar_weekly.py")
    W1 = importlib.util.module_from_spec(sp)
    sys.modules["radar_weekly_w31"] = W1
    sp.loader.exec_module(W1)
    W1.R_LONG = W1.R_SHORT = 0.10
    rd = lambda n: pd.read_csv(ROOT / "data" / "btc" / n, index_col=0, parse_dates=True)
    fl, fv = rd("f_long_radar.csv.gz"), rd("f_radar_live.csv.gz")
    t1 = []
    for r_ in (W1.simulate(fl[fl.index <= "2020-12-31"], start="2018-01-01"), W1.simulate(fv, start="2021-01-01")):
        t1 += [(x["entry"], x["pnl"]) for x in r_["trades"]] + ([(r_["open"]["entry"], r_["open"]["pnl_close"])] if r_["open"] else [])
    r1 = np.array([p_ for e_, p_ in t1 if pd.Timestamp(e_) >= iv.index[0]])
    T.append(f"| W3.1 (stessi segnali, rischio 10% allo stop) | {usd(10000 * float(np.prod(1 + r1)))} | {(r1 > 0).mean() * 100:.0f}% | {pct(r1.min())} | {pct(r1.max())} | fino a −10% (stop) | {pct(worst_run(r1))} |")
    rows = {}
    for tenor in (90, 180):
        for bud in (0.03, 0.06, 0.10):
            rets = []
            for t in tr.itertuples():
                cp = 1 if t.verso == "long" else -1
                s0, v0 = float(c.loc[t.entra - pd.Timedelta(days=1)]), float(iv.reindex([t.entra - pd.Timedelta(days=1)], method="ffill").iloc[0])
                p0 = bs(s0, s0, tenor / 365, v0, cp) * 1.04
                exp = t.entra + pd.Timedelta(days=tenor)
                te = min(t.esce, exp)
                s1 = float(c.loc[:te - pd.Timedelta(days=1)].iloc[-1])
                tau = max(0.0, (exp - te).days / 365)
                p1 = bs(s1, s0, tau, float(iv.reindex([te - pd.Timedelta(days=1)], method="ffill").iloc[0]), cp) * (0.96 if tau > 0 else 1.0)
                rets.append(bud * (p1 / p0 - 1))
            r = np.array(rets)
            rows[(tenor, bud)] = r
            T.append(f"| Opzione a {tenor} giorni, {bud * 100:.0f}% del capitale per operazione | {usd(10000 * float(np.prod(1 + r)))} | {(r > 0).mean() * 100:.0f}% | {pct(r.min())} | {pct(r.max())} | "
                     f"−{bud * 100:.0f}% | {pct(worst_run(r))} |")
    best = rows[(90, 0.06)]
    T.append("\n## D2 dettaglio\n")
    T.append("| Operazione W3.2 | Verso | Entra | Esce | W3.2 originale | Con opzione a 90 giorni (6% del capitale) |")
    T.append("|---|---|---|---|---|---|")
    for t, r in zip(tr.itertuples(), best):
        T.append(f"| {t.Index + 1} | {t.verso} | {t.entra.date()} | {'aperta' if t.uscita == 'aperta' else t.esce.date()} | {pct(t.sul_capitale)} | {pct(float(r))} |")


# ================================================================== E · prove di sforzo e segnali dal mercato delle opzioni
def part_e(d: pd.DataFrame, iv: pd.Series, E: dict) -> None:
    c = d["close"]
    # E1 · quanto costa un movimento di un giorno a uno straddle venduto appena aperto (30 giorni, alla pari, delta coperto alla chiusura precedente)
    T.append("\n## E1 sforzo\n")
    T.append("| Movimento di BTC in un giorno | Volatilità implicita 50% → 50% | 50% → 80% | 50% → 120% |")
    T.append("|---|---|---|---|")
    S0, tau, v0 = 100.0, 30 / 365, 0.50
    p0 = bs(S0, S0, tau, v0, 1) + bs(S0, S0, tau, v0, -1)
    h = delta(S0, S0, tau, v0, 1) + delta(S0, S0, tau, v0, -1)             # delta dello straddle comprato; chi vende tiene +h di BTC
    for mv in (0.0, 0.05, -0.05, 0.10, -0.10, 0.20, -0.20, -0.30, -0.40):
        row = []
        for v1 in (0.50, 0.80, 1.20):
            S1 = S0 * (1 + mv)
            p1 = bs(S1, S0, tau - 1 / 365, v1, 1) + bs(S1, S0, tau - 1 / 365, v1, -1)
            row.append(pct((p0 - p1 + h * (S1 - S0)) / S0, 1))
        T.append(f"| {pct(mv, 0) if mv else 'fermo'} | " + " | ".join(row) + " |")
    T.append(f"\nPremio incassato all'apertura: {num(p0, 1)}% del controvalore. Guadagno massimo se BTC resta fermo fino a scadenza: lo stesso {num(p0, 1)}%.")

    # E2 · lo straddle coperto passa l'esame dello Sharpe deflazionato?
    T.append("\n## E2 esame\n")
    T.append("| Serie | Anni | Sharpe annuo (settimanale) | Asimmetria | Giorno peggiore | Settimana peggiore | Probabilità che lo Sharpe vero sia > 0 | Deflazionato, 10 tentativi | 100 tentativi |")
    T.append("|---|---|---|---|---|---|---|---|---|")
    k = "Straddle venduto con copertura giornaliera del delta, 1x"
    for lab, a, b in (("Straddle coperto, 2019–2026", None, None), ("Straddle coperto, solo DVOL (dal 24/03/2021)", "2021-03-24", None), ("Straddle coperto, 2024–2026", "2024-01-01", None)):
        e = E[k].loc[a:b]
        r = weekly_ret(e)
        sr = r.mean() / r.std()
        T.append(f"| {lab} | {num(len(r) / 52, 1)} | {num(sr * math.sqrt(52))} | {num(float(r.skew()), 1)} | {pct(float(e.pct_change().min()), 1)} | {pct(float(r.min()), 1)} | {num(psr(r) * 100, 1)}% | "
                 + " | ".join(f"{psr(r, sr0(n, 0.5 / math.sqrt(52))) * 100:.0f}%" for n in (10, 100)) + " |")

    # E3 · i dati delle opzioni anticipano il prezzo o la volatilita'? (dati settimanali Deribit, domenica)
    su = pd.read_csv(ROOT / "data" / "opzioni" / "deribit_opt_sunday.csv", index_col=0, parse_dates=True)
    lr = np.log(c / c.shift(1))
    rvp = np.sqrt((lr ** 2).rolling(30).mean() * 365)
    rvf = np.sqrt((lr ** 2).rolling(28).mean().shift(-28) * 365)
    f = pd.DataFrame({
        "Inclinazione: put lontane − call lontane (punti di volatilità)": su.pw_iv - su.cw_iv,
        "Livello della volatilità implicita (posizione nelle 52 settimane prima)": su.atm_iv.rolling(52).rank(pct=True),
        "Premio atteso: implicita − realizzata dei 30 giorni prima": su.atm_iv / 100 - rvp.reindex(su.index),
        "Volumi: put / call": su.put_btc / su.call_btc,
    })
    fwd = (c.shift(-28) / c - 1).reindex(su.index)
    fvol = (su.atm_iv / 100 - rvf.reindex(su.index))                       # premio poi incassato: implicita − realizzata delle 4 settimane dopo
    T.append("\n## E3 segnali\n")
    T.append("| Segnale la domenica | Settimane | BTC nelle 4 settimane dopo: terzo basso del segnale | terzo medio | terzo alto | Correlazione col rendimento, 2019–2022 | 2023–2026 | Correlazione col premio poi incassato (implicita − realizzata dopo), 2019–2022 | 2023–2026 |")
    T.append("|---|---|---|---|---|---|---|---|---|")
    sp = lambda u, w: float(u.rank().corr(w.rank()))                       # correlazione di rango (Spearman) senza scipy
    for name in f.columns:
        z = pd.DataFrame({"s": f[name], "r": fwd, "v": fvol}).dropna()
        q = pd.qcut(z.s.rank(method="first"), 3, labels=False)
        g = z.r.groupby(q).mean()
        h1, h2 = z.loc[:"2022-12-31"], z.loc["2023-01-01":]
        T.append(f"| {name} | {len(z)} | {pct(g[0], 1)} | {pct(g[1], 1)} | {pct(g[2], 1)} | {num(sp(h1.s, h1.r))} | {num(sp(h2.s, h2.r))} | "
                 f"{num(sp(h1.s, h1.v))} | {num(sp(h2.s, h2.v))} |")
    T.append(f"\nRendimento medio di BTC a 4 settimane su tutte le domeniche: {pct(float(fwd.dropna().mean()), 1)}. Le finestre si sovrappongono (4 settimane su dati settimanali): "
             f"le osservazioni indipendenti sono circa {len(fwd.dropna()) // 4} per l'intero periodo, la metà per ogni sottoperiodo; una correlazione sotto 0,2 in valore assoluto non è distinguibile dal caso.")


def chart(x: pd.DataFrame, E: dict) -> None:
    INK, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED,
                         "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": SURF,
                         "axes.facecolor": SURF, "savefig.facecolor": SURF})
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={"height_ratios": [2, 3], "hspace": 0.28})
    a1.plot(x.index, x.iv * 100, color="#2a78d6", lw=1.6, label="Implicita (attesa dal mercato)")
    a1.plot(x.index, x.rvf * 100, color="#eb6834", lw=1.3, label="Realizzata nei 30 giorni dopo")
    a1.set_title("Volatilità di BTC: implicita contro realizzata (%, annua)", loc="left", color=INK, fontsize=12, fontweight="bold")
    a1.legend(frameon=False, loc="upper right", fontsize=9)
    a1.grid(axis="y", color=GRID, lw=0.8)
    sel = [("Straddle venduto con copertura giornaliera del delta, 1x", "#2a78d6"), ("Put venduta −10% con liquidità a garanzia", "#eb6834"), ("BTC + call venduta +10% (covered call)", "#eda100"),
           ("Straddle venduto alla pari, 1x", "#6250d6"), ("BTC comprato e tenuto (riferimento)", "#1baf7a")]
    ends = []
    for k, col in sel:
        e = E[k].dropna() * 10000
        a2.plot(e.index, e, color=col, lw=1.8)
        ends.append((float(e.iloc[-1]), k.split(" (")[0].split(",")[0].replace("con copertura giornaliera del delta", "con delta coperto"), col, e.index[-1]))
    yy = []
    for v, lab, col, last in sorted(ends):
        y = v if not yy else max(v, yy[-1] * 1.45)
        yy.append(y)
        a2.annotate(f"{lab} · {usd(v)} $", (last, v), xytext=(last + pd.Timedelta(days=40), y), fontsize=9, color=INK, va="center", arrowprops=dict(arrowstyle="-", color=col, lw=1.0))
    a2.set_yscale("log")
    a2.set_yticks([2500, 5000, 10000, 20000, 50000, 100000])
    a2.set_yticklabels(["2,5k", "5k", "10k", "20k", "50k", "100k"])
    a2.minorticks_off()
    a2.grid(axis="y", color=GRID, lw=0.8)
    last = E[sel[0][0]].index[-1]
    a2.set_xlim(E[sel[0][0]].index[0], last + pd.Timedelta(days=900))
    a2.set_xticks([pd.Timestamp(f"{y}-01-01") for y in range(2020, last.year + 1)])
    a2.set_xticklabels([str(y) for y in range(2020, last.year + 1)])
    a2.spines["bottom"].set_bounds(matplotlib.dates.date2num(E[sel[0][0]].index[0]), matplotlib.dates.date2num(last))
    a2.set_title("Vendere opzioni su BTC: 10.000 $ dal 2019 (scala logaritmica, valore giornaliero a mercato)", loc="left", color=INK, fontsize=12, fontweight="bold")
    fig.savefig(OUT / "opzioni.png", dpi=160, bbox_inches="tight")


if __name__ == "__main__":
    B.END = "2026-12-31"
    d = B.load()
    s = part_a()
    part_b(s["w32"])
    r = part_c(d, s["w32"])
    part_d(d, r["iv"])
    part_e(d, r["iv"], r["E"])
    (OUT / "tables.md").write_text("\n".join(T) + "\n")
    print("\n".join(T))
    chart(r["x"], r["E"])
