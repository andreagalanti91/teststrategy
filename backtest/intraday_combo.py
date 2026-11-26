"""Nuova strategia intraday da Aldo (canale Telegram) + Eliz (post del 24/11): BTC, ETH, SOL, TAO su candele da 15 minuti.

Cosa si prende da ciascuno:
- Eliz: il livello e' l'estremo di un range; si entra dopo la deviazione oltre l'estremo e il rientro confermato a 15 minuti,
  con stop oltre l'estremo della deviazione ("no trigger, no trade").
- Aldo: si opera nel verso del trend; le "prese di liquidita'" sopra/sotto i massimi/minimi sono il suo setup che ha reso di piu';
  ingresso con ordine limite su un livello deciso prima; gestione con meta' al primo obiettivo e stop a pareggio.

Famiglie provate (griglia piccola, scelta SOLO sul periodo di prova di BTC/ETH/SOL, TAO mai usato per scegliere):
  S · "sweep & reclaim": il prezzo scende sotto il minimo delle N ore precedenti (almeno 0,1%) e una candela da 15 minuti chiude
      di nuovo sopra entro un'ora -> long all'apertura successiva; stop sotto il minimo della deviazione. Specchio per gli short.
  L · "limite sul livello": ordine limite al minimo delle N ore precedenti (Aldo), stop 1 ATR orario sotto.
  Filtro di trend: nessuno, oppure chiusura giornaliera precedente sopra/sotto la EMA 50 giornaliera (solo long/solo short).
  Gestione: "aldo" (meta' a +1 R, stop a pareggio, resto a +2,5 R) oppure "fissa" (tutto a +2 R). Uscita a tempo dopo 48 ore.
Costi: 0,05% a mercato + 0,02% di slittamento per lato; obiettivi come ordini limite 0,02%. Se nella stessa candela si toccano
stop e obiettivo, vale lo stop. Periodo di prova 2020–2023, verifica 2024–2026 (TAO: solo verifica, da aprile 2024).
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "results" / "intraday_combo"
OUT.mkdir(parents=True, exist_ok=True)
TAKER, SLIP, MAKER = 0.0005, 0.0002, 0.0002
IS0, IS1, OOS1 = "2020-09-01", "2024-01-01", "2026-11-01"
pct = lambda x, d=1: "n/d" if x is None or not np.isfinite(x) else f"{x * 100:+.{d}f}%".replace(".", ",")
num = lambda x, d=2: "n/d" if x is None or not np.isfinite(x) else f"{x:.{d}f}".replace(".", ",")
T = []


def load(sym: str) -> pd.DataFrame:
    if sym == "BTC":
        d = pd.read_csv(ROOT / "data" / "intraday" / "binance_spot_BTCUSDT_15m.csv.gz")
        d["ts"] = pd.to_datetime(d["ts"], format="mixed").astype("datetime64[ns]")
        d = d.set_index("ts")
    else:
        d = pd.read_csv(ROOT / "data" / "intraday15" / f"{sym}USDT_15m.csv.gz", index_col=0)
        d.index = pd.to_datetime(d.index, format="mixed")
    d = d[~d.index.duplicated()].sort_index()[["open", "high", "low", "close"]].astype(float)
    return d.loc[IS0:OOS1]


def trend(d: pd.DataFrame) -> np.ndarray:
    day = d["close"].resample("1D").last().dropna()
    s = np.sign(day - day.ewm(span=50, adjust=False).mean())
    s.index = s.index + pd.Timedelta(days=1)                        # noto dalla mezzanotte successiva
    return s.reindex(d.index, method="ffill").fillna(0).to_numpy()


def atr_1h(d: pd.DataFrame) -> np.ndarray:
    h = d.resample("1h").agg({"high": "max", "low": "min", "close": "last"}).dropna()
    c = h["close"]
    tr = pd.concat([h["high"] - h["low"], (h["high"] - c.shift()).abs(), (h["low"] - c.shift()).abs()], axis=1).max(axis=1)
    a = tr.ewm(alpha=1 / 14, adjust=False).mean().shift()           # solo ore chiuse
    return a.reindex(d.index, method="ffill").to_numpy()


def signals(d: pd.DataFrame, fam: str, n_h: int, filt: bool) -> list[tuple]:
    """Ritorna (indice di ingresso, verso, prezzo d'ingresso o None per mercato, stop)."""
    O, H, L, C = (d[k].to_numpy() for k in ("open", "high", "low", "close"))
    n = n_h * 4
    lo = pd.Series(L).shift(4).rolling(n - 4).min().to_numpy()     # minimo delle N ore che finiscono un'ora fa
    hi = pd.Series(H).shift(4).rolling(n - 4).max().to_numpy()
    tr = trend(d) if filt else np.zeros(len(d))
    at = atr_1h(d)
    out = []
    i = n
    while i < len(d) - 6:
        okL, okS = (tr[i] >= 0) if filt else True, (tr[i] <= 0) if filt else True
        if filt:
            okL, okS = tr[i] > 0, tr[i] < 0
        if fam == "S":
            if okL and np.isfinite(lo[i]) and L[i] < lo[i] * 0.999:
                for k in range(i, i + 4):
                    if C[k] > lo[i]:
                        out.append((k + 1, 1, None, min(L[i:k + 1]) * 0.999, lo[i], hi[i]))
                        i = k + 1
                        break
                else:
                    i += 4
                continue
            if okS and np.isfinite(hi[i]) and H[i] > hi[i] * 1.001:
                for k in range(i, i + 4):
                    if C[k] < hi[i]:
                        out.append((k + 1, -1, None, max(H[i:k + 1]) * 1.001, lo[i], hi[i]))
                        i = k + 1
                        break
                else:
                    i += 4
                continue
        else:                                                        # L: limite sul livello
            if okL and np.isfinite(lo[i]) and L[i] <= lo[i] and np.isfinite(at[i]):
                out.append((i, 1, min(O[i], lo[i]), lo[i] - at[i], lo[i], hi[i]))
                i += 4
                continue
            if okS and np.isfinite(hi[i]) and H[i] >= hi[i] and np.isfinite(at[i]):
                out.append((i, -1, max(O[i], hi[i]), hi[i] + at[i], lo[i], hi[i]))
                i += 4
                continue
        i += 1
    return out


def simulate(d: pd.DataFrame, sig: list[tuple], mgmt: str, hold_h: int = 48) -> pd.DataFrame:
    O, H, L, C = (d[k].to_numpy() for k in ("open", "high", "low", "close"))
    idx = d.index
    rows, free = [], 0
    for i, sg, px_lim, stop, lo, hi in sig:
        if i < free or i >= len(d) - 1:
            continue
        limit = px_lim is not None
        entry = px_lim if limit else O[i] * (1 + sg * SLIP)
        base = px_lim if limit else O[i]
        risk = sg * (base - stop) / base
        if not (0.0015 < risk < 0.08):
            continue
        fee_in = MAKER if limit else TAKER
        t1, t2 = base * (1 + sg * risk), base * (1 + sg * (2.5 if mgmt == "aldo" else 2.0) * risk)
        st, half, ret, j_end, why = stop, False, 0.0, None, "tempo"
        j1 = min(i + hold_h * 4, len(d) - 1)
        for j in range(i, j1 + 1):
            first = (j == i)
            hit_s = (L[j] <= st) if sg > 0 else (H[j] >= st)
            if hit_s:
                px = (min(O[j], st) if sg > 0 else max(O[j], st)) if not first else st
                ret += (0.5 if half else 1.0) * (sg * (px * (1 - sg * SLIP) / entry - 1) - TAKER)
                j_end, why = j, "pareggio" if half else "stop"
                break
            if first and limit:
                continue                                             # nella candela dell'ordine limite non si contano gli obiettivi
            if mgmt == "aldo" and not half and ((H[j] >= t1) if sg > 0 else (L[j] <= t1)):
                ret += 0.5 * (sg * (t1 / entry - 1) - MAKER)
                half, st = True, base
            if (H[j] >= t2) if sg > 0 else (L[j] <= t2):
                ret += (0.5 if half else 1.0) * (sg * (t2 / entry - 1) - MAKER)
                j_end, why = j, "obiettivo"
                break
        if j_end is None:
            j_end = j1
            ret += (0.5 if half else 1.0) * (sg * (C[j1] * (1 - sg * SLIP) / entry - 1) - TAKER)
        ret -= fee_in
        rows.append((idx[i], sg, risk, ret, ret / risk, why, (j_end - i) / 4))
        free = j_end + 1
    return pd.DataFrame(rows, columns=["t", "verso", "rischio", "ret", "R", "uscita", "ore"])


def summary(t: pd.DataFrame, a: str, b: str) -> dict:
    x = t[(t.t >= a) & (t.t < b)]
    if len(x) < 5:
        return {"n": len(x)}
    yrs = max((pd.Timestamp(min(b, str(x.t.max()))) - pd.Timestamp(max(a, str(x.t.min())))).days / 365.25, 0.1)
    eq = np.cumprod(1 + 0.01 * x.R.clip(lower=-3).to_numpy())       # rischio 1% del capitale per operazione
    return {"n": len(x), "anno": len(x) / yrs, "win": float((x.ret > 0).mean()), "R": float(x.R.mean()), "fin": float(eq[-1]),
            "dd": float((eq / np.maximum.accumulate(eq) - 1).min()), "t": float(x.R.mean() / x.R.std() * np.sqrt(len(x))) if x.R.std() > 0 else 0.0}


def placebo(d: pd.DataFrame, t: pd.DataFrame, mgmt: str, rng, reps: int = 30) -> float:
    """Stessi versi e stessi stop (in %), ingressi a caso nello stesso periodo, stessa gestione: R medio."""
    if t.empty:
        return np.nan
    O = d["open"].to_numpy()
    pos = d.index.searchsorted(t.t)
    lo, hi = int(pos.min()), int(pos.max())
    out = []
    for _ in range(reps):
        ii = np.sort(rng.integers(lo, hi, size=len(t)))
        sig = [(int(i), int(s), None, O[i] * (1 - s * r), np.nan, np.nan) for i, s, r in zip(ii, t.verso, t.rischio)]
        out.append(simulate(d, sig, mgmt).R.mean())
    return float(np.mean(out))


def main():
    assets = ["BTC", "ETH", "SOL", "TAO"]
    D = {a: load(a) for a in assets}
    grid = list(itertools.product(("S", "L"), (24, 48, 96), (False, True), ("aldo", "fissa")))
    res, keep = [], {}
    for fam, n_h, filt, mgmt in grid:
        for a in assets:
            t = simulate(D[a], signals(D[a], fam, n_h, filt), mgmt)
            keep[(fam, n_h, filt, mgmt, a)] = t
            res.append({"fam": fam, "n_h": n_h, "filt": filt, "mgmt": mgmt, "asset": a, **{f"is_{k}": v for k, v in summary(t, IS0, IS1).items()},
                        **{f"oos_{k}": v for k, v in summary(t, IS1, OOS1).items()}})
    g = pd.DataFrame(res)
    g.to_csv(OUT / "griglia.csv", index=False)
    # scelta: R medio sul periodo di prova di BTC, ETH, SOL (TAO escluso), con almeno 2 asset su 3 positivi
    sel = g[g.asset != "TAO"].groupby(["fam", "n_h", "filt", "mgmt"]).agg(R_is=("is_R", "mean"), pos_is=("is_R", lambda x: (x > 0).sum()), n_is=("is_n", "sum")).reset_index()
    sel = sel.sort_values(["R_is"], ascending=False)
    best = sel.iloc[0]
    T.append("## I1 griglia\n")
    T.append(f"{len(grid)} varianti × 4 asset. Scelta sul solo periodo di prova (set 2020 – dic 2023) di BTC, ETH e SOL, per R medio; TAO non entra nella scelta.\n")
    T.append("| Famiglia | Ore del range | Filtro di trend | Gestione | R medio in prova (BTC, ETH, SOL) | Asset positivi in prova | Operazioni in prova |")
    T.append("|---|---|---|---|---|---|---|")
    FN = {"S": "sweep & reclaim (Eliz + Aldo)", "L": "limite sul livello (Aldo)"}
    for r in sel.head(8).itertuples():
        T.append(f"| {FN[r.fam]} | {r.n_h} | {'EMA 50 giornaliera' if r.filt else 'nessuno'} | {'metà a 1 R + pareggio' if r.mgmt == 'aldo' else 'tutto a 2 R'} | {num(r.R_is)} | {r.pos_is}/3 | {int(r.n_is)} |")
    T.append(f"| … ultime: {FN[sel.iloc[-1].fam]}, {sel.iloc[-1].n_h} ore | | | | {num(sel.iloc[-1].R_is)} | | |")

    rng = np.random.default_rng(3)
    T.append("\n## I2 verifica\n")
    T.append(f"Variante scelta: {FN[best.fam]}, range di {best.n_h} ore, filtro {'EMA 50 giornaliera' if best.filt else 'nessuno'}, gestione "
             f"{'metà a +1 R e stop a pareggio, resto a +2,5 R' if best.mgmt == 'aldo' else 'tutto a +2 R'}. Rischio 1% del capitale per operazione.\n")
    T.append("| Asset | Periodo | Operazioni | Per anno | In guadagno | R medio | t-stat | 10.000 $ → | Max DD | Ingressi casuali, stessa gestione: R medio |")
    T.append("|---|---|---|---|---|---|---|---|---|---|")
    for a in assets:
        t = keep[(best.fam, best.n_h, best.filt, best.mgmt, a)]
        for lab, x0, x1 in (("prova 2020–2023", IS0, IS1), ("verifica 2024–2026", IS1, OOS1)):
            s = summary(t, x0, x1)
            if s["n"] < 5:
                continue
            pb = placebo(D[a], t[(t.t >= x0) & (t.t < x1)], best.mgmt, rng)
            T.append(f"| {a} | {lab} | {s['n']} | {num(s['anno'], 0)} | {s['win'] * 100:.0f}% | {num(s['R'])} | {num(s['t'], 1)} | {f'{10000 * s[chr(102) + chr(105) + chr(110)]:,.0f}'.replace(',', '.')} | {pct(s['dd'])} | {num(pb)} |")
    # le migliori su ciascun asset in verifica (solo per trasparenza: scelta a posteriori)
    T.append("\n## I3 posteriori\n")
    T.append("| Asset | Migliore variante in verifica (scelta guardando i risultati) | R medio in verifica | Operazioni | Stessa variante in prova |")
    T.append("|---|---|---|---|---|")
    for a in assets:
        x = g[(g.asset == a) & (g.oos_n >= 30)].sort_values("oos_R", ascending=False)
        if len(x):
            r = x.iloc[0]
            T.append(f"| {a} | {FN[r.fam]}, {r.n_h} ore, {'EMA 50' if r.filt else 'senza filtro'}, {'metà a 1 R' if r.mgmt == 'aldo' else '2 R'} | {num(r.oos_R)} | {int(r.oos_n)} | "
                     f"{num(r.is_R) if np.isfinite(r.is_R) else 'n/d'} |")
    pos = (g.oos_R > 0).mean()
    T.append(f"\nVarianti con R medio positivo in verifica: {pos * 100:.0f}% delle {int(g.oos_R.notna().sum())} combinazioni variante × asset; "
             f"R medio di tutte: {num(float(g.oos_R.mean()))}.")
    (OUT / "tables.md").write_text("\n".join(T) + "\n")
    print("\n".join(T))


if __name__ == "__main__":
    main()
