"""Le tre regole del post di Eliz (24/11/2026) tradotte in regole meccaniche e verificate su BTC dal 2018 (candele a 15 minuti).

A · short sulla deviazione sopra il massimo del range: nelle ultime 48 ore il prezzo e' salito sopra il massimo del range
    (massimo delle N giornate precedenti, escluse le ultime 48 ore); una chiusura oraria torna dentro il range -> short.
    Stop poco sopra il massimo della deviazione, obiettivo il centro del range.
B · long scalp al 75% di ritracciamento: dopo una salita (minimo seguito da massimo, almeno +8%, entro N giorni), il prezzo
    torna al 75% della salita; una candela da 15 minuti scende sotto il livello e chiude sopra (conferma) -> long.
    Stop stretto sotto il minimo di quella candela, obiettivo il 50% della salita.
C · long sulla deviazione sotto il minimo del range: specchio di A (il post chiede anche un ritest: qui si entra al rientro).
Regole fissate prima di guardare i risultati: N = 7 giorni; variante N = 14 come controllo. Costi OKX dal motore intraday.
Controllo: stesse operazioni (verso, stop e obiettivo in %) aperte in momenti casuali dello stesso periodo.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import intraday as I

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "results" / "eliz"
OUT.mkdir(parents=True, exist_ok=True)
pct = lambda x, d=1: "n/d" if x is None or not np.isfinite(x) else f"{x * 100:+.{d}f}%".replace(".", ",")
num = lambda x, d=2: "n/d" if x is None or not np.isfinite(x) else f"{x:.{d}f}".replace(".", ",")
T = []
START, SPLIT = "2018-03-01", "2022-01-01"


def sig_dev(h: pd.DataFrame, n_days: int, side: int) -> pd.DataFrame:
    """A (side=-1) e C (side=+1). Indice = ora di chiusura della candela oraria."""
    N, W = 24 * n_days, 48
    hi = h["high"].shift(W).rolling(N).max()            # range: N giorni che finiscono 48 ore fa
    lo = h["low"].shift(W).rolling(N).min()
    mid = (hi + lo) / 2
    c = h["close"]
    if side < 0:
        ext = h["high"].rolling(W).max()                 # estremo della deviazione nelle ultime 48 ore
        trig = (ext > hi) & (c < hi) & (c.shift() >= hi.shift())
        sl = ext * 1.001 - c
        tp = c - mid
    else:
        ext = h["low"].rolling(W).min()
        trig = (ext < lo) & (c > lo) & (c.shift() <= lo.shift())
        sl = c - ext * 0.999
        tp = mid - c
    width = (hi - lo) / lo
    ok = trig & (sl > 0) & (tp > 0) & width.between(0.04, 0.35)
    s = pd.DataFrame({"side": side, "tp": tp, "sl": sl, "hold": 24 * 7}, index=h.index)[ok]
    return s


def sig_fib(b: pd.DataFrame, h: pd.DataFrame, n_days: int, level: float = 0.75, target: float = 0.5, min_move: float = 0.08) -> pd.DataFrame:
    """B. Lo swing si calcola sulle ore gia' chiuse; il segnale e' la chiusura della candela da 15 minuti di conferma."""
    N = 24 * n_days
    L, H = h["low"].to_numpy(), h["high"].to_numpy()
    rows, used = [], set()
    m15 = b[["low", "close"]]
    for i in range(N, len(h) - 1):
        w0 = i - N + 1
        jl = w0 + int(np.argmin(L[w0:i + 1]))
        if i - jl < 12:
            continue
        jh = jl + int(np.argmax(H[jl:i + 1]))
        lo_, hi_ = L[jl], H[jh]
        if hi_ / lo_ - 1 < min_move or jh <= jl or jh == i:
            continue
        lev = hi_ - level * (hi_ - lo_)
        key = (round(lo_), round(hi_))
        if key in used or h["close"].iat[i] <= lev or L[jh:i + 1].min() <= lev:   # il livello non deve essere gia' stato toccato
            continue
        t0 = h.index[i]                                      # ora appena chiusa; si guardano i 15 minuti dell'ora successiva
        seg = m15.loc[t0:t0 + pd.Timedelta(minutes=45)]
        hit = seg[(seg["low"] <= lev)]
        if hit.empty:
            continue
        used.add(key)
        k = hit.index[0]
        if hit["close"].iat[0] < lev:                       # niente conferma sulla candela che tocca: scenario annullato
            continue
        stop = hit["low"].iat[0] * 0.999
        tgt = hi_ - target * (hi_ - lo_)
        rows.append((k + pd.Timedelta(minutes=15), 1, tgt - hit["close"].iat[0], hit["close"].iat[0] - stop, 72))
    s = pd.DataFrame(rows, columns=["t", "side", "tp", "sl", "hold"]).set_index("t")
    return s[(s.tp > 0) & (s.sl > 0)]


def rmult(t: I.Trades, sig: pd.DataFrame) -> np.ndarray:
    """Risultato di ogni operazione in multipli del rischio (R = distanza dello stop all'ingresso)."""
    d = t.df
    risk = (sig.reindex(d.entry_time - pd.Timedelta(0))["sl"].to_numpy() if False else None)
    return d.ret.to_numpy() / (d["sl_pct"].to_numpy())


def run(b, sig, label):
    t = I.backtest(b, sig)
    d = t.df.copy()
    sl_pct = []
    for r in d.itertuples():
        k = sig.index[sig.index.searchsorted(r.entry_time, side="right") - 1] if len(sig) else None
        sl_pct.append(float(sig.loc[k, "sl"]) / r.entry if k is not None else np.nan)
    d["R"] = d.ret / np.array(sl_pct)
    return d


def placebo(b, sig, rng, reps=200):
    """Stesse operazioni (verso, stop e obiettivo in % del prezzo, durata) aperte a ore casuali dello stesso periodo."""
    h_idx = b.index[(b.index.minute == 0) & (b.index >= START)]
    c = b["close"]
    out = []
    pct_tp = (sig.tp / c.reindex(sig.index, method="ffill")).to_numpy()
    pct_sl = (sig.sl / c.reindex(sig.index, method="ffill")).to_numpy()
    for _ in range(reps):
        tt = pd.DatetimeIndex(np.sort(rng.choice(h_idx[:-200], size=len(sig), replace=False)))
        cc = c.reindex(tt).to_numpy()
        s = pd.DataFrame({"side": sig.side.to_numpy(), "tp": pct_tp * cc, "sl": pct_sl * cc, "hold": sig.hold.to_numpy()}, index=tt)
        out.append(I.backtest(b, s).df.ret.mean())
    return np.array(out)


def main():
    b = I.load("binance")
    h = I.hourly(b)
    rng = np.random.default_rng(11)
    T.append("## E1 regole\n")
    T.append("| Regola (dal post) | N giorni del range | Operazioni | Per anno | In guadagno | Rendimento medio per operazione (netto) | Risultato medio in R | Obiettivo raggiunto | Stop | 2018–2021: media | 2022–2026: media | Controllo casuale: media | Quante volte il caso fa meglio |")
    T.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    rows, keep = [], {}
    for n_days in (7, 14):
        for lab, sig in (("A · short sulla deviazione sopra il range", sig_dev(h, n_days, -1)), ("B · long al 75% con conferma a 15 minuti", sig_fib(b, h, n_days)),
                         ("C · long sulla deviazione sotto il range", sig_dev(h, n_days, 1))):
            sig = sig[sig.index >= START]
            d = run(b, sig, lab)
            if d.empty:
                continue
            yrs = (d.entry_time.iloc[-1] - pd.Timestamp(START)).days / 365.25
            a, z = d[d.entry_time < SPLIT], d[d.entry_time >= SPLIT]
            pl = placebo(b, sig.loc[d.entry_time.min():], rng, 100)
            keep[(lab, n_days)] = d
            T.append(f"| {lab} | {n_days} | {len(d)} | {num(len(d) / yrs, 1)} | {(d.ret > 0).mean() * 100:.0f}% | {pct(d.ret.mean(), 2)} | {num(d.R.mean())} | {(d.reason == 'target').mean() * 100:.0f}% | "
                     f"{(d.reason == 'stop').mean() * 100:.0f}% | {pct(a.ret.mean(), 2)} ({len(a)}) | {pct(z.ret.mean(), 2)} ({len(z)}) | {pct(float(np.mean(pl)), 2)} | {(pl >= d.ret.mean()).mean() * 100:.0f}% |")
    T.append("\nRendimenti sul controvalore della singola operazione, al netto di commissioni (0,05% a mercato, 0,02% limite), slittamento e funding. "
             "R = rischio pianificato (distanza dello stop). 'Quante volte il caso fa meglio': quota delle 100 serie casuali con media pari o superiore.")
    # capitale con rischio fisso dell'1% per operazione (versione N = 7)
    T.append("\n## E2 capitale\n")
    T.append("| Regola, N = 7 | 10.000 $ con rischio 1% per operazione | Drawdown massimo (sulle chiusure) | Serie peggiore di stop di fila |")
    T.append("|---|---|---|---|")
    for (lab, n_days), d in keep.items():
        if n_days != 7:
            continue
        e = np.cumprod(1 + 0.01 * d.R.clip(-3, None).to_numpy())
        dd = float((e / np.maximum.accumulate(e) - 1).min())
        lossrun = int((d.ret <= 0).astype(int).groupby((d.ret > 0).cumsum()).sum().max())
        T.append(f"| {lab} | {f'{10000 * e[-1]:,.0f}'.replace(',', '.')} $ | {pct(dd)} | {lossrun} |")
    for (lab, n_days), d in keep.items():
        d.assign(regola=lab, n_giorni=n_days).to_csv(OUT / f"operazioni_{lab[0]}_{n_days}.csv", index=False)
    (OUT / "tables.md").write_text("\n".join(T) + "\n")
    print("\n".join(T))


if __name__ == "__main__":
    main()
