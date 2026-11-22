"""Studio "compra sul supporto testato, quando vendere": definizione algoritmica dell'evento e confronto delle uscite.

EVENTO (stesso calcolo per ogni moneta, solo con dati disponibili in quel giorno):
- minimo di swing = minimo settimanale piu' basso delle 6 settimane prima e dopo (confermato 6 settimane dopo);
- il minimo "conta" se dopo di esso il prezzo e' salito di almeno il 60%;
- zona di supporto = l'ultimo minimo che conta piu' i minimi precedenti (ultimi 3 anni) entro +/-20% da esso;
  riferimento = mediana dei minimi della zona; tocco n. = minimi nella zona + 1;
- INGRESSO: ordine limite a riferimento x 1,05 quando il prezzo ci torna dall'alto;
- STOP: chiusura giornaliera sotto il minimo piu' basso della zona x 0,88 (per TAO: zona 143-168 -> stop a ~126);
- un solo evento per visita: il successivo richiede che il prezzo sia risalito di almeno il 40% dall'ingresso
  (o che si formi una zona nuova dopo uno stop).
USCITE confrontate sullo stesso insieme di ingressi, tutte con lo stesso stop. Costi 0,1% per lato + 0,1% di slippage sugli stop.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
K, RALLY, BAND, LOOK_Y = 6, 0.60, 0.20, 3
ENTRY_K, STOP_K, REARM = 1.05, 0.88, 0.40
FEE, SLIP, HORIZON = 0.001, 0.001, 730


def load(sym: str) -> pd.DataFrame:
    if sym == "TAO":
        d = pd.read_csv(ROOT / "data" / "tao" / "bitget_TAOUSDT_spot_1d.csv")
    else:
        d = pd.read_csv(ROOT / "data" / "alts" / f"{sym}.csv.gz")
    d["ts"] = pd.to_datetime(d["ts"], format="mixed").astype("datetime64[ns]")
    d = d.set_index("ts").sort_index()
    d = d[~d.index.duplicated()]
    return d[(d.close > 0) & (d.high >= d.low)]


def swing_lows(d: pd.DataFrame) -> list[tuple]:
    """(data del minimo, prezzo, data di conferma, data in cui il rialzo del 60% e' raggiunto o NaT)."""
    w = d.resample("W-SUN").agg({"high": "max", "low": "min"}).dropna()
    lo = w["low"].to_numpy()
    out = []
    for i in range(K, len(w) - K):
        if lo[i] == lo[i - K:i + K + 1].min():
            day = d.loc[w.index[i] - pd.Timedelta(days=6):w.index[i], "low"].idxmin()
            after = d.loc[day:, "high"]
            hit = after[after >= lo[i] * (1 + RALLY)]
            out.append((day, float(lo[i]), w.index[i + K] + pd.Timedelta(days=1), hit.index[0] if len(hit) else pd.NaT))
    return out


def events(sym: str, d: pd.DataFrame) -> list[dict]:
    sl = swing_lows(d)
    ev, blocked_until_px, dead_zone = [], None, None
    C, L, O = d["close"].to_numpy(), d["low"].to_numpy(), d["open"].to_numpy()
    idx = d.index
    for i in range(1, len(d)):
        t = idx[i]
        ok = [s for s in sl if s[2] <= t and pd.notna(s[3]) and s[3] <= t and s[0] >= t - pd.Timedelta(days=365 * LOOK_Y)]
        if not ok:
            continue
        last = ok[-1]
        zone = [s for s in ok if last[1] / (1 + BAND) <= s[1] <= last[1] * (1 + BAND)]
        ref, zmin = float(np.median([s[1] for s in zone])), min(s[1] for s in zone)
        if blocked_until_px is not None:
            if C[i] >= blocked_until_px:
                blocked_until_px = None
            else:
                continue
        if dead_zone is not None and last[0] == dead_zone:
            continue
        px = ref * ENTRY_K
        if L[i] <= px and C[i - 1] > px:
            entry = min(O[i], px)
            stop = zmin * STOP_K
            if entry <= stop:
                continue
            prev_peak = float(d.loc[last[0]:t, "high"].max())
            ev.append({"sym": sym, "t": t, "i": i, "entry": entry, "stop": stop, "touch": len(zone) + 1, "ref": ref,
                       "prev_peak": prev_peak, "last_low_date": last[0]})
            blocked_until_px = entry * (1 + REARM)
            dead_zone_candidate = last[0]
            # se lo stop scatta, la stessa zona non genera altri eventi
            fut = C[i:i + HORIZON]
            if (fut < stop).any() and not (d["high"].to_numpy()[i + 1:i + 1 + int(np.argmax(fut < stop))] >= blocked_until_px).any():
                dead_zone, blocked_until_px = dead_zone_candidate, None
    return ev


def _ind(d: pd.DataFrame) -> pd.DataFrame:
    x = pd.DataFrame(index=d.index)
    c = d["close"]
    tr = pd.concat([d["high"] - d["low"], (d["high"] - c.shift()).abs(), (d["low"] - c.shift()).abs()], axis=1).max(axis=1)
    x["atr"] = tr.ewm(alpha=1 / 22, adjust=False).mean()
    x["sma50"], x["sma140"] = c.rolling(50).mean(), c.rolling(140).mean()       # 140 giorni ~ 20 settimane
    dl = c.diff()
    up, dn = dl.clip(lower=0).ewm(alpha=1 / 14, adjust=False).mean(), (-dl.clip(upper=0)).ewm(alpha=1 / 14, adjust=False).mean()
    x["rsi"] = 100 - 100 / (1 + up / dn)
    wc = c.resample("W-SUN").last()
    wd = wc.diff()
    wu, wn = wd.clip(lower=0).ewm(alpha=1 / 14, adjust=False).mean(), (-wd.clip(upper=0)).ewm(alpha=1 / 14, adjust=False).mean()
    x["rsiw"] = (100 - 100 / (1 + wu / wn)).shift(1).reindex(d.index, method="ffill")   # ultima settimana chiusa
    return x


EXITS = ["target +30%", "target +50%", "target +75%", "target +100%", "target +150%", "target +200%",
         "70% del massimo precedente", "trailing 25% (dal +30%)", "trailing 35% (dal +30%)", "chandelier 3 ATR (dal +30%)",
         "chiusura sotto SMA50 (dal +30%)", "RSI settimanale > 70", "RSI giornaliero > 80",
         "meta' a +50%, meta' trailing 30%", "meta' a +50%, meta' a +100%", "terzi a +30/+60/+100%",
         "uscita a 90 giorni", "uscita a 180 giorni", "solo stop (tenere 2 anni)"]


def apply_exits(d: pd.DataFrame, x: pd.DataFrame, e: dict) -> dict:
    """Per ogni regola: rendimento netto, giorni, motivo. Lo stop (chiusura sotto il livello) vale per tutte."""
    i0 = e["i"]
    sl = slice(i0, min(i0 + HORIZON, len(d)))
    H, Lw, C = d["high"].to_numpy()[sl], d["low"].to_numpy()[sl], d["close"].to_numpy()[sl]
    A, S50, RSI, RW = (x[k].to_numpy()[sl] for k in ("atr", "sma50", "rsi", "rsiw"))
    entry, stop, n = e["entry"], e["stop"], len(C)
    stop_i = int(np.argmax(C < stop)) if (C < stop).any() else n
    net = lambda px, slip=0.0: px * (1 - slip) / entry * (1 - FEE) ** 2 - 1

    def target(mult_px):
        hit = H[1:] >= mult_px                       # il target non conta nel giorno d'ingresso
        return (int(np.argmax(hit)) + 1) if hit.any() else n

    def finish(j_exit, px_exit, why):
        """j_exit = giorno dell'uscita di regola (n se mai); confronta con lo stop."""
        if stop_i <= j_exit and stop_i < n:
            return net(C[stop_i], SLIP), stop_i, "stop"
        if j_exit < n:
            return net(px_exit), j_exit, why
        return net(C[-1]), n - 1, "fine dati/2 anni"

    def trail(kind, arm=0.30):
        armed, peak = False, entry
        for j in range(1, n):
            if j >= stop_i:
                return n, None
            peak = max(peak, C[j])
            if not armed and C[j] >= entry * (1 + arm):
                armed = True
            if armed:
                if kind == "t25" and C[j] <= peak * 0.75: return j, C[j]
                if kind == "t30" and C[j] <= peak * 0.70: return j, C[j]
                if kind == "t35" and C[j] <= peak * 0.65: return j, C[j]
                if kind == "chand" and C[j] <= peak - 3 * A[j]: return j, C[j]
                if kind == "sma50" and C[j] < S50[j]: return j, C[j]
        return n, None

    def first(cond):
        c = cond.copy(); c[0] = False
        return (int(np.argmax(c)), None) if c.any() else (n, None)

    out = {}
    for name, m in (("target +30%", 1.3), ("target +50%", 1.5), ("target +75%", 1.75), ("target +100%", 2.0), ("target +150%", 2.5), ("target +200%", 3.0)):
        j = target(entry * m)
        out[name] = finish(j, entry * m, "target")
    px = max(0.7 * e["prev_peak"], entry * 1.1)
    out["70% del massimo precedente"] = finish(target(px), px, "target")
    for name, kind in (("trailing 25% (dal +30%)", "t25"), ("trailing 35% (dal +30%)", "t35"), ("chandelier 3 ATR (dal +30%)", "chand"),
                       ("chiusura sotto SMA50 (dal +30%)", "sma50")):
        j, p = trail(kind)
        out[name] = finish(j, p if p else 0, "regola")
    j, _ = first(RW > 70)
    out["RSI settimanale > 70"] = finish(j, C[j] if j < n else 0, "regola")
    j, _ = first(RSI > 80)
    out["RSI giornaliero > 80"] = finish(j, C[j] if j < n else 0, "regola")

    def combo(legs):
        r = sum(wt * leg[0] for wt, leg in legs)
        dd = sum(wt * leg[1] for wt, leg in legs)
        return r, dd, "misto"
    jt, pt = trail("t30")
    out["meta' a +50%, meta' trailing 30%"] = combo([(0.5, out["target +50%"]), (0.5, finish(jt, pt if pt else 0, "regola"))])
    out["meta' a +50%, meta' a +100%"] = combo([(0.5, out["target +50%"]), (0.5, out["target +100%"])])
    j60 = target(entry * 1.6)
    out["terzi a +30/+60/+100%"] = combo([(1 / 3, out["target +30%"]), (1 / 3, finish(j60, entry * 1.6, "target")), (1 / 3, out["target +100%"])])
    for name, days in (("uscita a 90 giorni", 90), ("uscita a 180 giorni", 180)):
        out[name] = finish(min(days, n) if days < n else n, C[days] if days < n else 0, "tempo")
    out["solo stop (tenere 2 anni)"] = finish(n, 0, "")
    # percorso: massimo e minimo toccati prima dello stop
    upto = min(stop_i + 1, n)
    e2 = dict(e, mfe=float(H[1:upto].max() / entry - 1) if upto > 1 else 0.0, mae=float(Lw[:upto].min() / entry - 1),
              stopped=stop_i < n, days_to_stop=stop_i if stop_i < n else np.nan, complete=(i0 + HORIZON <= len(d)))
    for k, (r, dd, why) in out.items():
        e2[f"r|{k}"], e2[f"d|{k}"] = r, dd
    return e2


def run(symbols: list[str]) -> pd.DataFrame:
    rows = []
    for s in symbols:
        try:
            d = load(s)
        except FileNotFoundError:
            continue
        if len(d) < 400:
            continue
        x = _ind(d)
        for e in events(s, d):
            rows.append(apply_exits(d, x, e))
    return pd.DataFrame(rows)


if __name__ == "__main__":
    from fetch_alts import ALTS
    df = run(sorted(set(ALTS)))
    out = ROOT / "results" / "tao"
    out.mkdir(parents=True, exist_ok=True)
    df.drop(columns=["i"]).to_csv(out / "eventi_alt.csv", index=False)
    print(len(df), "eventi su", df.sym.nunique(), "monete;", "TAO:", (df.sym == "TAO").sum())
    print(df[df.sym == "TAO"][["t", "entry", "stop", "touch", "prev_peak", "mfe", "mae", "stopped"]].round(2).to_string())
