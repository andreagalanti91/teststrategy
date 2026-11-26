"""W3.2 estesa ad altre monete: stesse regole e stesso codice del radar (vendor/radar_weekly_w32.py), dati della moneta.

Per ogni moneta si costruisce lo stesso dataframe giornaliero che il radar usa per BTC:
- prezzi spot Binance (open, high, low, close);
- flusso perp pf14z = z-score a 180 giorni del rapporto (acquisti aggressivi − vendite aggressive) / volume sul perp USD-M,
  somma mobile di 14 giorni (definizione di radar/features.py);
- funding giornaliero del perp (somma delle tre rate).
Controllo: su BTC il risultato deve essere vicino a quello del radar (che usa le sue serie, non gli archivi pubblici).
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data" / "w32_estesa"
OUT = ROOT / "results" / "w32_estesa"
OUT.mkdir(parents=True, exist_ok=True)
sp = importlib.util.spec_from_file_location("w32", ROOT / "vendor" / "radar_weekly_w32.py")
W = importlib.util.module_from_spec(sp)
sys.modules["w32"] = W
sp.loader.exec_module(W)
pct = lambda x, d=1: "n/d" if x is None or not np.isfinite(x) else f"{x * 100:+.{d}f}%".replace(".", ",")
num = lambda x, d=2: "n/d" if x is None or not np.isfinite(x) else f"{x:.{d}f}".replace(".", ",")
usd = lambda x: f"{x:,.0f}".replace(",", ".")
CH0, CH1 = "2023-05-12", "2024-03-18"


def frame(sym: str) -> pd.DataFrame:
    rd = lambda k: pd.read_csv(D / f"{sym}USDT_{k}.csv.gz", index_col=0, parse_dates=True)
    s, p, fu = rd("spot"), rd("perp"), rd("funding")
    f = s[["open", "high", "low", "close"]].copy()
    delta = 2 * p["taker_buy_volume"] - p["volume"]
    flow14 = delta.rolling(14).sum() / p["volume"].rolling(14).sum()
    z = (flow14 - flow14.rolling(180, min_periods=90).mean()) / flow14.rolling(180, min_periods=90).std()
    f["pf14z"] = z.reindex(f.index)
    f["funding"] = fu["funding"].reindex(f.index) if "funding" in fu else np.nan
    return f.loc[:"2026-10-31"]


def run(f: pd.DataFrame, start: str) -> dict:
    r = W.simulate(f, start=start)
    trades = r["trades"] + ([r["open"] | {"pnl": r["open"]["pnl_close"], "exit": None}] if r["open"] else [])
    return {"eq": r["equity"] / r["equity"].iloc[0], "trades": trades}


def stats(eq: pd.Series, trades: list, a: str | None = None, b: str | None = None) -> dict:
    e = eq.loc[a:b].dropna()
    e = e / e.iloc[0]
    yrs = max((e.index[-1] - e.index[0]).days / 365.25, 0.05)
    t = [x for x in trades if (a is None or x["entry"] >= a) and (b is None or x["entry"] < b)]
    pn = np.array([x["pnl"] for x in t]) if t else np.array([])
    return {"fin": float(e.iloc[-1]), "cagr": float(e.iloc[-1] ** (1 / yrs) - 1), "dd": float((e / e.cummax() - 1).min()), "n": len(t),
            "win": float((pn > 0).mean()) if len(pn) else np.nan, "dal": str(e.index[0].date())}


def main():
    syms = ["BTC", "ETH", "SOL", "TAO", "INJ", "DOGE"]
    T, R = [], {}
    T.append("## X1 monete\n")
    T.append("| Moneta | Backtest dal | Operazioni | In guadagno | 10.000 $ → | CAGR | Max DD | Comprata e tenuta, stesso periodo: CAGR / DD |")
    T.append("|---|---|---|---|---|---|---|---|")
    for s in syms:
        try:
            f = frame(s)
        except FileNotFoundError:
            continue
        ok = f.dropna(subset=["pf14z"])
        start = max(pd.Timestamp("2021-01-01"), ok.index[0] + pd.Timedelta(days=280))      # 40 settimane per la SMA
        r = run(f, str(start.date()))
        R[s] = (f, r)
        st = stats(r["eq"], r["trades"])
        c = f["close"].loc[start:]
        bh = c / c.iloc[0]
        yrs = (bh.index[-1] - bh.index[0]).days / 365.25
        T.append(f"| {s} | {st['dal']} | {st['n']} | {pct(st['win'], 0).lstrip('+')} | {usd(10000 * st['fin'])} | {pct(st['cagr'])} | {pct(st['dd'])} | "
                 f"{pct(float(bh.iloc[-1] ** (1 / yrs) - 1))} / {pct(float((bh / bh.cummax() - 1).min()))} |")
    w = pd.read_csv(ROOT / "results" / "w32" / "equity.csv", index_col=0, parse_dates=True)["W3.2 radar (rischio 25%)"]
    if "BTC" in R:
        e = R["BTC"][1]["eq"]
        a, b = e.index[0], min(e.index[-1], w.index[-1])
        rad = w.loc[a:b] / w.loc[a:b].iloc[0]
        T.append(f"\nControllo su BTC: con gli archivi pubblici W3.2 fa ×{num(float(e.loc[:b].iloc[-1]), 1)} dal {a.date()}; il radar, con le sue serie, ×{num(float(rad.iloc[-1]), 1)}. "
                 f"Correlazione dei rendimenti giornalieri {num(float(e.loc[:b].pct_change().corr(rad.pct_change())))}.")
    # periodo del canale e portafoglio
    T.append("\n## X2 periodi\n")
    T.append("| Moneta | Periodo del canale: 10.000 $ → | DD | 2024–2026: 10.000 $ → | DD |")
    T.append("|---|---|---|---|---|")
    for s, (f, r) in R.items():
        a1 = stats(r["eq"], r["trades"], CH0, CH1) if r["eq"].index[0] <= pd.Timestamp(CH0) else None
        a2 = stats(r["eq"], r["trades"], "2024-01-01", None)
        T.append(f"| {s} | {usd(10000 * a1['fin']) if a1 else 'n/d (dati insufficienti)'} | {pct(a1['dd']) if a1 else '–'} | {usd(10000 * a2['fin'])} | {pct(a2['dd'])} |")
    # portafoglio: capitale diviso in parti uguali fra le monete disponibili, ribilanciato ogni giorno
    T.append("\n## X3 portafoglio\n")
    T.append("| Portafoglio (parti uguali, ribilanciato ogni giorno) | Dal | 10.000 $ → | CAGR | Max DD |")
    T.append("|---|---|---|---|---|")
    for combo in (["BTC"], ["BTC", "ETH"], ["BTC", "ETH", "SOL"], ["BTC", "ETH", "SOL", "TAO"]):
        if not all(c in R for c in combo):
            continue
        rets = pd.concat([R[c][1]["eq"].pct_change() for c in combo], axis=1).dropna()
        e = (1 + rets.mean(axis=1)).cumprod()
        yrs = (e.index[-1] - e.index[0]).days / 365.25
        T.append(f"| {' + '.join(combo)} | {e.index[0].date()} | {usd(10000 * float(e.iloc[-1]))} | {pct(float(e.iloc[-1]) ** (1 / yrs) - 1)} | {pct(float((e / e.cummax() - 1).min()))} |")
    rows = []
    for s, (f, r) in R.items():
        for t in r["trades"]:
            rows.append({"moneta": s, "verso": t["side"], "entra": t["entry"], "esce": t.get("exit"), "prezzo_in": t["entry_px"], "prezzo_out": t.get("exit_px"),
                         "esposizione": t["expo"], "sul_capitale": t["pnl"], "uscita": t.get("reason", "aperta")})
    pd.DataFrame(rows).to_csv(OUT / "operazioni.csv", index=False)
    (OUT / "tables.md").write_text("\n".join(T) + "\n")
    print("\n".join(T))


if __name__ == "__main__":
    main()
