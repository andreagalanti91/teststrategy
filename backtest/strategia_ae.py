"""Strategia "AE" (Aldo + Eliz), costruita sulle lezioni delle prove precedenti: meno operazioni, obiettivi piu' larghi, nel trend.

Lezioni usate:
- l'intraday meccanico perde per i costi (300-400 operazioni l'anno, stop dell'1-2%): qui si sale di scala, livelli di 10 giorni;
- il trend settimanale di BTC funziona (W3.2); Aldo: "long sulle alt finche' BTC regge", "niente short su BTC in trend rialzista";
- Eliz: si entra sul rientro dopo la deviazione oltre l'estremo del range, con stop oltre la deviazione; Aldo: le prese di
  liquidita' sono il suo setup che ha reso di piu'; meta' al primo obiettivo e stop a pareggio; i guadagni grandi vengono dalle
  operazioni lasciate correre (DOGE, 36 giorni).

Regole (fissate prima di guardare i risultati; nessuna ottimizzazione):
- regime di BTC, settimanale: chiusura sopra la SMA 40 settimane ed EMA 20 in salita = long ammessi; sotto la SMA 40, SMA 40 in
  calo su 4 settimane ed EMA 20 in calo = short ammessi; altrimenti niente. Noto dal lunedi'.
- regime della moneta: chiusura giornaliera precedente sopra (long) / sotto (short) la sua EMA 50 giornaliera;
- livello: minimo (massimo) dei 10 giorni che finiscono 24 ore prima;
- presa di liquidita': il prezzo scende sotto il livello di almeno lo 0,2%; rientro: una chiusura oraria torna sopra il livello
  entro 8 ore -> long all'apertura dell'ora successiva. Specchio per gli short;
- stop: minimo della deviazione meno lo 0,3%; meta' posizione a +2 volte il rischio, poi stop a pareggio; il resto esce alla prima
  chiusura giornaliera sotto (long) / sopra (short) la EMA 20 giornaliera; massimo 30 giorni;
- rischio 1% del capitale per operazione (variante 2%), una posizione per moneta, al massimo 4 insieme; costi 0,08% per lato,
  funding 0,03% al giorno sui long.
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "results" / "strategia_ae"
OUT.mkdir(parents=True, exist_ok=True)
COST, FUND_D = 0.0008, 0.0003
pct = lambda x, d=1: "n/d" if x is None or not np.isfinite(x) else f"{x * 100:+.{d}f}%".replace(".", ",")
num = lambda x, d=2: "n/d" if x is None or not np.isfinite(x) else f"{x:.{d}f}".replace(".", ",")
usd = lambda x: f"{x:,.0f}".replace(",", ".")
CH0, CH1 = "2023-05-12", "2024-03-18"


def load(sym: str) -> pd.DataFrame:
    def rd(f):
        d = pd.read_csv(f, index_col=0)
        d.index = pd.to_datetime(d.index, format="mixed")
        return d[["open", "high", "low", "close"]].astype(float)
    if sym == "TAO":
        a = rd(ROOT / "data" / "alts_1h" / "TAOUSDT_bitget_1h_2023.csv.gz")
        b = rd(ROOT / "data" / "intraday15" / "TAOUSDT_15m.csv.gz").resample("1h").agg({"open": "first", "high": "max", "low": "min", "close": "last"}).dropna()
        d = pd.concat([a[a.index < b.index[0]], b])
    else:
        d = rd(ROOT / "data" / "alts_1h" / f"{sym}USDT_1h.csv.gz")
    d = d[~d.index.duplicated()].sort_index()
    return d.loc[:"2026-10-31 23:00"]


def btc_regime(h: pd.DataFrame) -> pd.Series:
    w = h["close"].resample("W-SUN").last().dropna()
    s, e = w.rolling(40).mean(), w.ewm(span=20, adjust=False).mean()
    r = ((w > s) & (e > e.shift())).astype(int) - ((w < s) & (s < s.shift(4)) & (e < e.shift())).astype(int)
    r.index = r.index + pd.Timedelta(days=1)
    return r


def daily_side(h: pd.DataFrame, n: int) -> pd.Series:
    d = h["close"].resample("1D").last().dropna()
    s = np.sign(d - d.ewm(span=n, adjust=False).mean())
    s.index = s.index + pd.Timedelta(days=1)
    return s


def run_asset(sym: str, h: pd.DataFrame, breg: pd.Series, look_d: int = 10, tp1: float = 2.0, shorts: bool = True) -> list[dict]:
    O, H, L, C = (h[k].to_numpy() for k in ("open", "high", "low", "close"))
    idx = h.index
    rb = breg.reindex(idx, method="ffill").fillna(0).to_numpy()
    ra = daily_side(h, 50).reindex(idx, method="ffill").fillna(0).to_numpy()
    d20 = h["close"].resample("1D").last().dropna()
    ema20 = d20.ewm(span=20, adjust=False).mean()
    dclose = d20.reindex(idx, method="ffill").to_numpy()            # ultima chiusura giornaliera nota (00:00 UTC)
    dema = ema20.reindex(idx, method="ffill").to_numpy()
    newday = (idx.hour == 0)
    n = look_d * 24
    lo = pd.Series(L).shift(24).rolling(n).min().to_numpy()
    hi = pd.Series(H).shift(24).rolling(n).max().to_numpy()
    out, i = [], n + 24
    while i < len(h) - 2:
        okL, okS = rb[i] > 0 and ra[i] > 0, shorts and rb[i] < 0 and ra[i] < 0
        sig = None
        if okL and np.isfinite(lo[i]) and L[i] < lo[i] * 0.998:
            for k in range(i, min(i + 8, len(h) - 2)):
                if C[k] > lo[i]:
                    sig = (k + 1, 1, L[i:k + 1].min() * 0.997)
                    break
        elif okS and np.isfinite(hi[i]) and H[i] > hi[i] * 1.002:
            for k in range(i, min(i + 8, len(h) - 2)):
                if C[k] < hi[i]:
                    sig = (k + 1, -1, H[i:k + 1].max() * 1.003)
                    break
        if not sig:
            i += 1
            continue
        j0, sg, stop = sig
        entry = O[j0]
        risk = sg * (entry - stop) / entry
        if not (0.003 < risk < 0.12):
            i = j0
            continue
        t1 = entry * (1 + sg * tp1 * risk)
        st, half, ret, why, path = stop, False, 0.0, "tempo", []
        jmax = min(j0 + 30 * 24, len(h) - 1)
        j = j0
        for j in range(j0, jmax + 1):
            if (L[j] <= st) if sg > 0 else (H[j] >= st):
                px = (min(O[j], st) if sg > 0 else max(O[j], st)) if j > j0 else st
                ret += (0.5 if half else 1.0) * sg * (px / entry - 1)
                why = "pareggio" if half else "stop"
                break
            if not half and ((H[j] >= t1) if sg > 0 else (L[j] <= t1)):
                ret += 0.5 * sg * (t1 / entry - 1)
                half, st = True, entry
            if half and newday[j] and j > j0 and ((dclose[j] < dema[j]) if sg > 0 else (dclose[j] > dema[j])):
                ret += 0.5 * sg * (O[j] / entry - 1)
                why = "EMA 20 giornaliera"
                break
            path.append((idx[j], ret + (0.5 if half else 1.0) * sg * (C[j] / entry - 1)))
        else:
            ret += (0.5 if half else 1.0) * sg * (C[jmax] / entry - 1)
        days = (j - j0) / 24
        ret -= 2 * COST + (FUND_D * days if sg > 0 else 0.0)
        out.append({"asset": sym, "t": idx[j0], "uscita_t": idx[j], "verso": sg, "entrata": entry, "rischio": risk, "rend": ret, "R": ret / risk,
                    "motivo": why, "giorni": days, "obiettivo1": half, "path": path})
        i = j + 1
    return out


def portfolio(trades, start, end, risk=0.01, maxn=4, cap0=10000.0):
    tr = sorted([t for t in trades if start <= str(t["t"]) < end], key=lambda x: x["t"])
    done, open_ = [], []
    for t in tr:
        open_ = [o for o in open_ if o["uscita_t"] > t["t"]]
        if len(open_) >= maxn or any(o["asset"] == t["asset"] for o in open_):
            continue
        realized = cap0 + sum(o["pnl"] for o in done if o["uscita_t"] <= t["t"])
        notional = min(realized * risk / t["rischio"], 3.0 * realized)
        t = t | {"notional": notional, "pnl": notional * t["rend"]}
        done.append(t)
        open_.append(t)
    idx = pd.date_range(start, end, freq="D")
    eq = pd.Series(cap0, idx, dtype=float)
    for d in done:
        if d["path"]:
            p = pd.Series(dict(d["path"])).resample("1D").last()
            p = p[(p.index >= idx[0]) & (p.index <= idx[-1]) & (p.index < d["uscita_t"].normalize())]
            eq.loc[p.index] += d["notional"] * p.to_numpy()
        eq.loc[idx >= d["uscita_t"].normalize()] += d["pnl"]
    return eq, done


def st(eq, done):
    e = eq / eq.iloc[0]
    yrs = max((e.index[-1] - e.index[0]).days / 365.25, 0.05)
    r = np.array([d["R"] for d in done]) if done else np.array([np.nan])
    return {"fin": float(e.iloc[-1]), "cagr": float(e.iloc[-1] ** (1 / yrs) - 1), "dd": float((e / e.cummax() - 1).min()), "n": len(done),
            "win": float(np.mean([d["rend"] > 0 for d in done])) if done else np.nan, "R": float(np.nanmean(r))}


def main():
    assets = ["BTC", "ETH", "SOL", "TAO"]
    H = {a: load(a) for a in assets}
    breg = btc_regime(H["BTC"])
    T = []
    base = {a: run_asset(a, H[a], breg) for a in assets}
    allb = [t for v in base.values() for t in v]
    pd.DataFrame([{k: v for k, v in t.items() if k != "path"} for t in allb]).to_csv(OUT / "operazioni.csv", index=False)
    w = pd.read_csv(ROOT / "results" / "w32" / "equity.csv", index_col=0, parse_dates=True)
    P = [("Periodo del canale (12/05/2023–18/03/2024)", CH0, CH1), ("2020–2022", "2020-01-01", "2023-01-01"), ("2023–2026", "2023-01-01", "2026-11-01"),
         ("Tutto (2020–2026)", "2020-01-01", "2026-11-01")]
    T.append("## S1 risultati\n")
    T.append("| Periodo | Versione | 10.000 $ → | CAGR | Max DD | Operazioni | In guadagno | Medio in R |")
    T.append("|---|---|---|---|---|---|---|---|")
    for lab, a, b in P:
        for risk in (0.01, 0.02):
            for uni, vu in ((assets, "BTC, ETH, SOL, TAO"), (["BTC"], "solo BTC")):
                eq, done = portfolio([t for t in allb if t["asset"] in uni], a, b, risk)
                s = st(eq, done)
                T.append(f"| {lab} | {vu}, rischio {int(risk * 100)}% | {usd(10000 * s['fin'])} | {pct(s['cagr'])} | {pct(s['dd'])} | {s['n']} | {pct(s['win'], 0).lstrip('+')} | {num(s['R'])} |")
        x = w.loc[a:b]
        for c, nm in (("W3.2 radar (rischio 25%)", "W3.2"), ("BTC comprato e tenuto", "BTC comprato e tenuto")):
            e = x[c] / x[c].iloc[0]
            yrs = (e.index[-1] - e.index[0]).days / 365.25
            T.append(f"| {lab} | {nm} (riferimento) | {usd(10000 * float(e.iloc[-1]))} | {pct(float(e.iloc[-1]) ** (1 / yrs) - 1)} | {pct(float((e / e.cummax() - 1).min()))} | – | – | – |")
    T.append("\n## S2 asset\n")
    T.append("| Asset | Dati dal | Operazioni | Per anno | Long / short | In guadagno | Medio in R | Medio per operazione | Nel periodo del canale: operazioni, medio in R |")
    T.append("|---|---|---|---|---|---|---|---|---|")
    for a in assets:
        g = pd.DataFrame([{k: v for k, v in t.items() if k != "path"} for t in base[a]])
        if g.empty:
            continue
        yrs = (H[a].index[-1] - H[a].index[0]).days / 365.25
        c = g[(g.t >= CH0) & (g.t < CH1)]
        T.append(f"| {a} | {H[a].index[0]:%m/%Y} | {len(g)} | {num(len(g) / yrs, 1)} | {(g.verso > 0).sum()} / {(g.verso < 0).sum()} | {(g.rend > 0).mean() * 100:.0f}% | {num(g.R.mean())} | "
                 f"{pct(g.rend.mean(), 2)} | {len(c)}, {num(c.R.mean()) if len(c) else '–'} |")
    # robustezza: vicini dei parametri (non usati per scegliere)
    T.append("\n## S3 vicini\n")
    T.append("| Giorni del livello | Primo obiettivo (volte il rischio) | Operazioni (4 asset, 2020–2026) | Medio in R | 10.000 $ → con rischio 1% (2020–2026) | Periodo del canale: 10.000 $ → |")
    T.append("|---|---|---|---|---|---|")
    for look, tp in itertools.product((5, 10, 20), (1.5, 2.0, 3.0)):
        tr = base_tr = [t for a in assets for t in (base[a] if (look, tp) == (10, 2.0) else run_asset(a, H[a], breg, look, tp))]
        s, s2 = st(*portfolio(tr, "2020-01-01", "2026-11-01")), st(*portfolio(tr, CH0, CH1))
        T.append(f"| {look} | {num(tp, 1)} | {s['n']} | {num(s['R'])} | {usd(10000 * s['fin'])} | {usd(10000 * s2['fin'])} |")
    # controllo casuale: stessi rischi, ingressi a caso nello stesso regime e stessa gestione
    rng = np.random.default_rng(9)
    rr = []
    for a in assets:
        h = H[a]
        O, Lw, Hh = h["open"].to_numpy(), h["low"].to_numpy(), h["high"].to_numpy()
        for t in base[a]:
            for _ in range(3):
                j = h.index.searchsorted(t["t"]) + int(rng.integers(-240, 240))
                if j < 300 or j >= len(h) - 800:
                    continue
                e0 = O[j]
                stop = e0 * (1 - t["verso"] * t["rischio"])
                fake = {"asset": a, "t": h.index[j], "verso": t["verso"]}
                # gestione identica: riuso run_asset su una finestra con segnale forzato
                sub = run_forced(h, j, t["verso"], stop)
                if sub is not None:
                    rr.append(sub)
    T.append(f"\nControllo: stessi stop e stessa gestione, ingressi spostati a caso di ±10 giorni rispetto ai segnali ({len(rr)} prove): medio {num(float(np.mean(rr)))} R, "
             f"contro {num(float(np.mean([t['R'] for t in allb])))} R della regola.")
    (OUT / "tables.md").write_text("\n".join(T) + "\n")
    print("\n".join(T))


def run_forced(h, j0, sg, stop, tp1=2.0):
    O, H, L, C = (h[k].to_numpy() for k in ("open", "high", "low", "close"))
    idx = h.index
    d20 = h["close"].resample("1D").last().dropna()
    ema20 = d20.ewm(span=20, adjust=False).mean()
    dclose = d20.reindex(idx[j0:j0 + 30 * 24 + 1], method="ffill").to_numpy()
    dema = ema20.reindex(idx[j0:j0 + 30 * 24 + 1], method="ffill").to_numpy()
    entry = O[j0]
    risk = sg * (entry - stop) / entry
    if risk <= 0:
        return None
    t1 = entry * (1 + sg * tp1 * risk)
    st_, half, ret = stop, False, 0.0
    jmax = min(j0 + 30 * 24, len(h) - 1)
    j = j0
    for j in range(j0, jmax + 1):
        k = j - j0
        if (L[j] <= st_) if sg > 0 else (H[j] >= st_):
            px = (min(O[j], st_) if sg > 0 else max(O[j], st_)) if j > j0 else st_
            ret += (0.5 if half else 1.0) * sg * (px / entry - 1)
            break
        if not half and ((H[j] >= t1) if sg > 0 else (L[j] <= t1)):
            ret += 0.5 * sg * (t1 / entry - 1)
            half, st_ = True, entry
        if half and idx[j].hour == 0 and j > j0 and ((dclose[k] < dema[k]) if sg > 0 else (dclose[k] > dema[k])):
            ret += 0.5 * sg * (O[j] / entry - 1)
            break
    else:
        ret += (0.5 if half else 1.0) * sg * (C[jmax] / entry - 1)
    ret -= 2 * COST + (FUND_D * (j - j0) / 24 if sg > 0 else 0.0)
    return ret / risk


if __name__ == "__main__":
    main()
