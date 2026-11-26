"""Strategia meccanica ricavata dallo stile del canale Telegram (Aldo Qefalia, maggio 2023 – marzo 2024).

Cosa si prende dal trader (dai suoi messaggi, non ottimizzato):
- opera sulle 4 ore, entra su rottura di un livello e successivo retest ("retest positivo del breakout", "reclaim");
- long sulle altcoin solo finché BTC regge ("finché BTC rimarrà sopra i 31k starò long sulle alt"); niente short su BTC in trend
  rialzista; short sul retest negativo di un supporto rotto (il suo "setup preferito") quando il trend è ribassista;
- gestione: chiude metà al primo obiettivo, sposta lo stop a pareggio, lascia correre il resto;
- leva fino a ~10x: qui si dimensiona sul rischio (1% del capitale allo stop), con controvalore massimo 3x per operazione.

Regole fissate prima di guardare i risultati:
- regime: chiusura giornaliera precedente di BTC sopra la sua SMA 50 (long ammessi) o sotto (short ammessi); per le alt anche la
  moneta deve essere sopra (sotto) la sua SMA 50;
- rottura: chiusura a 4 ore sopra il massimo delle 30 candele precedenti (5 giorni) -> livello L;
- retest: entro 18 candele (3 giorni) una candela tocca L (minimo <= L +0,3%) e chiude sopra -> long all'apertura successiva;
- stop: sotto il minimo della candela di retest (o sotto L se piu' basso) meno 0,25 ATR; obiettivo 1 = +1,5 R (meta' posizione,
  stop a pareggio), obiettivo 2 = +3 R; uscita a tempo dopo 7 giorni;
- specchio per gli short; al massimo 4 posizioni aperte; costi 0,08% per lato, funding 0,03% al giorno sui long.
Uscite e stop simulati sulle candele orarie: se nella stessa ora si toccano stop e obiettivo, vale lo stop.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
D1H = ROOT / "data" / "alts_1h"
OUT = ROOT / "results" / "telegram"
OUT.mkdir(parents=True, exist_ok=True)
COST, FUND_D = 0.0008, 0.0003
N_BRK, N_RET, ATR_K, T1, T2, HOLD_D, RISK, MAXN, MAXLEV = 30, 18, 0.25, 1.5, 3.0, 7, 0.01, 4, 3.0
pct = lambda x, d=1: "n/d" if x is None or not np.isfinite(x) else f"{x * 100:+.{d}f}%".replace(".", ",")
num = lambda x, d=2: "n/d" if x is None or not np.isfinite(x) else f"{x:.{d}f}".replace(".", ",")
usd = lambda x: f"{x:,.0f}".replace(",", ".")


def load(sym: str) -> pd.DataFrame:
    d = pd.read_csv(D1H / f"{sym}USDT_1h.csv.gz", index_col=0)
    d.index = pd.to_datetime(d.index, format="mixed")
    return d[~d.index.duplicated()].sort_index()


def bars4h(h: pd.DataFrame) -> pd.DataFrame:
    b = h.resample("4h").agg({"open": "first", "high": "max", "low": "min", "close": "last"}).dropna()
    c = b["close"]
    tr = pd.concat([b["high"] - b["low"], (b["high"] - c.shift()).abs(), (b["low"] - c.shift()).abs()], axis=1).max(axis=1)
    b["atr"] = tr.ewm(alpha=1 / 14, adjust=False).mean()
    return b


def regime(h: pd.DataFrame) -> pd.Series:
    """+1 / -1 secondo la chiusura giornaliera PRECEDENTE rispetto alla SMA 50; riportato sull'orario."""
    d = h["close"].resample("1D").last().dropna()
    r = np.sign(d - d.rolling(50).mean())
    r.index = r.index + pd.Timedelta(days=1)
    return r


def signals(sym: str, h: pd.DataFrame, btc_reg: pd.Series, shorts: bool) -> list[dict]:
    b = bars4h(h)
    reg_a = regime(h).reindex(b.index, method="ffill")
    reg_b = btc_reg.reindex(b.index, method="ffill")
    hi, lo, cl, atr = b["high"].to_numpy(), b["low"].to_numpy(), b["close"].to_numpy(), b["atr"].to_numpy()
    out, arm = [], []                                          # arm: rotture in attesa di retest (verso, livello, indice)
    hh = b["high"].rolling(N_BRK).max().shift().to_numpy()
    ll = b["low"].rolling(N_BRK).min().shift().to_numpy()
    for i in range(N_BRK + 1, len(b) - 1):
        ok_l = reg_b.iat[i] > 0 and (sym == "BTC" or reg_a.iat[i] > 0)
        ok_s = shorts and reg_b.iat[i] < 0 and (sym == "BTC" or reg_a.iat[i] < 0)
        arm = [a for a in arm if i - a[2] <= N_RET]
        fired = None
        for a in arm:
            side, L, j = a
            if i == j:
                continue
            if side > 0 and ok_l and lo[i] <= L * 1.003 and cl[i] > L:
                stop = min(lo[i], L) - ATR_K * atr[i]
                fired = (1, stop)
            elif side < 0 and ok_s and hi[i] >= L * 0.997 and cl[i] < L:
                stop = max(hi[i], L) + ATR_K * atr[i]
                fired = (-1, stop)
            if fired:
                out.append({"asset": sym, "t": b.index[i + 1], "verso": fired[0], "stop": fired[1], "livello": L})
                arm = [x for x in arm if x is not a]
                break
        if np.isfinite(hh[i]) and cl[i] > hh[i] and cl[i - 1] <= hh[i - 1]:
            arm.append((1, hh[i], i))
        if np.isfinite(ll[i]) and cl[i] < ll[i] and cl[i - 1] >= ll[i - 1]:
            arm.append((-1, ll[i], i))
    return out


def manage(h: pd.DataFrame, s: dict) -> dict | None:
    """Simula una operazione sulle candele orarie dall'apertura delle 4 ore successive al segnale."""
    seg = h.loc[s["t"]:s["t"] + pd.Timedelta(days=HOLD_D)]
    if len(seg) < 2:
        return None
    sg, entry, stop = s["verso"], float(seg["open"].iat[0]), s["stop"]
    risk = sg * (entry - stop) / entry
    if not (0.002 < risk < 0.15):
        return None
    t1, t2 = entry * (1 + sg * T1 * risk), entry * (1 + sg * T2 * risk)
    half, st, ret, path, t_exit, why = False, stop, 0.0, [], None, "tempo"
    for t, r in seg.iterrows():
        hit_stop = (r["low"] <= st) if sg > 0 else (r["high"] >= st)
        hit1 = (r["high"] >= t1) if sg > 0 else (r["low"] <= t1)
        hit2 = (r["high"] >= t2) if sg > 0 else (r["low"] <= t2)
        if hit_stop:
            px = min(r["open"], st) if sg > 0 else max(r["open"], st)
            ret += (0.5 if half else 1.0) * sg * (px / entry - 1)
            t_exit, why = t, "pareggio" if half else "stop"
            break
        if not half and hit1:
            ret += 0.5 * sg * (t1 / entry - 1)
            half, st = True, entry
        if half and hit2:
            ret += 0.5 * sg * (t2 / entry - 1)
            t_exit, why = t, "obiettivo 2"
            break
        path.append((t, ret + (0.5 if half else 1.0) * sg * (r["close"] / entry - 1)))
    if t_exit is None:
        t_exit = seg.index[-1]
        ret += (0.5 if half else 1.0) * sg * (float(seg["close"].iat[-1]) / entry - 1)
    days = (t_exit - s["t"]).total_seconds() / 86400
    ret -= 2 * COST + (FUND_D * days if sg > 0 else 0.0)
    return s | {"entrata": entry, "rischio": risk, "uscita_t": t_exit, "motivo": why, "rend": ret, "R": ret / risk, "giorni": days,
                "obiettivo1": half, "path": path}


def portfolio(trades: list[dict], start: str, end: str, cap0: float = 10000.0) -> tuple[pd.Series, list[dict]]:
    """Rischio 1% del capitale (realizzato) per operazione, controvalore massimo 3x, al massimo 4 posizioni aperte insieme."""
    tr = sorted([t for t in trades if start <= str(t["t"]) < end], key=lambda x: x["t"])
    cap, open_, done = cap0, [], []
    for t in tr:
        open_ = [o for o in open_ if o["uscita_t"] > t["t"]]
        if len(open_) >= MAXN or any(o["asset"] == t["asset"] for o in open_):
            continue
        realized = cap0 + sum(o["pnl"] for o in done if o["uscita_t"] <= t["t"])
        notional = min(realized * RISK / t["rischio"], MAXLEV * realized)
        t = t | {"notional": notional, "pnl": notional * t["rend"]}
        done.append(t)
        open_.append(t)
    idx = pd.date_range(start, min(pd.Timestamp(end), max([d["uscita_t"] for d in done] + [pd.Timestamp(start)])) , freq="D")
    eq = pd.Series(cap0, idx, dtype=float)
    for d in done:                                            # valore giornaliero: guadagno latente dentro l'operazione, poi realizzato
        p = pd.Series({k: v for k, v in d["path"]}) if d["path"] else pd.Series(dtype=float)
        if len(p):
            daily = p.resample("1D").last().reindex(idx, method=None)
            daily = daily[(daily.index >= d["t"].normalize()) & (daily.index < d["uscita_t"].normalize())]
            eq.loc[daily.index] += d["notional"] * daily.fillna(0).to_numpy()
        eq.loc[idx >= d["uscita_t"].normalize()] += d["pnl"]
    return eq, done


def stats(eq: pd.Series, done: list[dict]) -> dict:
    e = eq / eq.iloc[0]
    yrs = max((e.index[-1] - e.index[0]).days / 365.25, 1e-9)
    r = np.array([d["R"] for d in done]) if done else np.array([np.nan])
    return {"fin": float(e.iloc[-1]), "cagr": float(e.iloc[-1] ** (1 / yrs) - 1), "dd": float((e / e.cummax() - 1).min()), "n": len(done),
            "win": float(np.mean([d["rend"] > 0 for d in done])) if done else np.nan, "R": float(np.nanmean(r)),
            "t1": float(np.mean([d["obiettivo1"] for d in done])) if done else np.nan}


def main():
    syms = ["BTC", "ETH", "SOL", "BNB", "DOGE", "INJ", "FET", "MATIC", "WOO"]
    H = {s: load(s) for s in syms if (D1H / f"{s}USDT_1h.csv.gz").exists()}
    btc_reg = regime(H["BTC"])
    T = []
    allt = {}
    for shorts in (False, True):
        tr = []
        for s, h in H.items():
            for sg in signals(s, h, btc_reg, shorts):
                m = manage(h, sg)
                if m:
                    tr.append(m)
        allt[shorts] = tr
    pd.DataFrame([{k: v for k, v in t.items() if k != "path"} for t in allt[True]]).to_csv(OUT / "aldo_meccanico_operazioni.csv", index=False)
    w = pd.read_csv(ROOT / "results" / "w32" / "equity.csv", index_col=0, parse_dates=True)
    btc = H["BTC"]["close"]
    ch = pd.read_csv(OUT / "operazioni_trader.csv", parse_dates=["apertura"]), pd.read_csv(OUT / "operazioni_follower.csv", parse_dates=["apertura"])
    P = [("Tutto il periodo", "2018-03-01", "2026-11-01"), ("2018–2021", "2018-03-01", "2022-01-01"), ("2022–2026", "2022-01-01", "2026-11-01"),
         ("Periodo del canale (12/05/2023–18/03/2024)", "2023-05-12", "2024-03-18")]
    T.append("## M1 meccanica\n")
    T.append("| Periodo | Versione | 10.000 $ → | CAGR | Max DD | Operazioni | In guadagno | Medio in R | Primo obiettivo raggiunto |")
    T.append("|---|---|---|---|---|---|---|---|---|")
    for lab, a, b in P:
        for shorts, vl in ((False, "solo long, nel verso del trend"), (True, "long e short")):
            for uni, vu in ((None, "BTC + 8 alt"), ("BTC", "solo BTC")):
                tr = [t for t in allt[shorts] if uni is None or t["asset"] == uni]
                eq, done = portfolio(tr, a, b)
                s = stats(eq, done)
                T.append(f"| {lab} | {vl}, {vu} | {usd(10000 * s['fin'])} | {pct(s['cagr'])} | {pct(s['dd'])} | {s['n']} | {pct(s['win'], 0).lstrip('+')} | {num(s['R'])} | {pct(s['t1'], 0).lstrip('+')} |")
        x = w.loc[a:b]
        for c, nm in (("W3.2 radar (rischio 25%)", "W3.2"), ("BTC comprato e tenuto", "BTC comprato e tenuto")):
            e = x[c] / x[c].iloc[0]
            yrs = (e.index[-1] - e.index[0]).days / 365.25
            T.append(f"| {lab} | {nm} (riferimento) | {usd(10000 * float(e.iloc[-1]))} | {pct(float(e.iloc[-1]) ** (1 / yrs) - 1)} | {pct(float((e / e.cummax() - 1).min()))} | – | – | – | – |")
    T.append("\n## M2 confronto\n")
    T.append("Periodo del canale, 12/05/2023 – 18/03/2024. Per il canale: rendimento sul controvalore di ogni operazione, composto, con controvalore pari "
             "a 1 volta e a 3 volte il capitale (la leva vista nelle schermate è 5–14,5x, ma non si sa quanta parte del capitale usasse).\n")
    T.append("| Chi | Operazioni | In guadagno | Medio per operazione | Capitale ×, controvalore 1x | Capitale ×, controvalore 3x |")
    T.append("|---|---|---|---|---|---|")
    for df, nm in ((ch[0], "Canale, prezzi dichiarati dal trader (tutte)"), (ch[0][~ch[0].comunicata_dopo], "Canale, prezzi del trader, solo operazioni annunciate in tempo"),
                   (ch[1], "Canale, chi copiava in tempo reale")):
        r = df.rendimento.to_numpy()
        T.append(f"| {nm} | {len(r)} | {np.mean(r > 0) * 100:.0f}% | {pct(r.mean(), 2)} | ×{num(float(np.prod(1 + r)))} | ×{num(float(np.prod(1 + 3 * r)))} |")
    for shorts, vl in ((False, "solo long"), (True, "long e short")):
        tr = [t for t in allt[shorts] if "2023-05-12" <= str(t["t"]) < "2024-03-18"]
        r = np.array([t["rend"] for t in tr])
        eq, done = portfolio(allt[shorts], "2023-05-12", "2024-03-18")
        T.append(f"| Strategia meccanica, {vl} (tutte le operazioni del periodo; colonna 3x = portafoglio a rischio 1%) | {len(r)} | {np.mean(r > 0) * 100:.0f}% | {pct(r.mean(), 2)} | ×{num(float(np.prod(1 + r)))} | ×{num(stats(eq, done)['fin'])} |")
    a0, a1 = pd.Timestamp("2023-05-12 16:00"), pd.Timestamp("2024-03-18 11:00")
    for c, nm in (("W3.2 radar (rischio 25%)", "W3.2"), ("BTC comprato e tenuto", "BTC comprato e tenuto")):
        T.append(f"| {nm} | – | – | – | ×{num(float(w[c].asof(a1) / w[c].asof(a0)))} | – |")
    # per asset sull'intero periodo
    T.append("\n## M3 asset\n")
    T.append("| Asset | Operazioni (long e short) | In guadagno | Medio in R | Medio per operazione |")
    T.append("|---|---|---|---|---|")
    df = pd.DataFrame([{k: v for k, v in t.items() if k != "path"} for t in allt[True]])
    for a, g in df.groupby("asset"):
        T.append(f"| {a} | {len(g)} | {(g.rend > 0).mean() * 100:.0f}% | {num(g.R.mean())} | {pct(g.rend.mean(), 2)} |")
    for v, g in df.groupby("verso"):
        T.append(f"| tutti, {'long' if v > 0 else 'short'} | {len(g)} | {(g.rend > 0).mean() * 100:.0f}% | {num(g.R.mean())} | {pct(g.rend.mean(), 2)} |")
    # controllo casuale: ingressi a caso nello stesso regime con la stessa gestione
    rng = np.random.default_rng(5)
    rr = []
    for _ in range(3):
        for t in rng.choice(np.array(allt[False], dtype=object), size=min(400, len(allt[False])), replace=False):
            h = H[t["asset"]]
            tt = t["t"] + pd.Timedelta(hours=4 * int(rng.integers(-60, 60)))
            if tt not in h.index:
                continue
            e0 = float(h.loc[tt, "open"])
            m = manage(h, {"asset": t["asset"], "t": tt, "verso": 1, "stop": e0 * (1 - t["rischio"])})
            if m:
                rr.append(m["R"])
    T.append(f"\nControllo: stessi stop e stessa gestione, ingressi long spostati a caso di ±10 giorni rispetto ai segnali ({len(rr)} prove): medio {num(float(np.mean(rr)))} R, "
             f"contro {num(float(np.mean([t['R'] for t in allt[False]])))} R della regola.")
    (OUT / "tables_meccanica.md").write_text("\n".join(T) + "\n")
    print("\n".join(T))


if __name__ == "__main__":
    main()
