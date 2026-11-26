"""Confronto finale nel periodo del canale (12/05/2023 – 18/03/2024): W3.2, strategia AE, Aldo (prezzi suoi) e chi lo copiava.

Rendimenti sul capitale, mese per mese.
- W3.2: curva giornaliera del radar (BTC, rischio 25% allo stop).
- AE: portafoglio BTC, ETH, SOL, TAO, rischio 1% e 2% per operazione (backtest/strategia_ae.py).
- Aldo e copytrading: ogni operazione ricostruita (results/telegram/), dimensionata con rischio fisso dell'1% o del 2% del capitale
  allo stop dichiarato (2% del prezzo se manca), leva massima 10x; il risultato si contabilizza alla chiusura dell'operazione.
  Il drawdown e' misurato sulle chiusure: dentro le operazioni puo' essere piu' profondo.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import strategia_ae as AE

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "results" / "confronto_finale"
OUT.mkdir(parents=True, exist_ok=True)
A0, A1 = pd.Timestamp("2023-05-12"), pd.Timestamp("2024-03-18")
pct = lambda x, d=1: "–" if x is None or not np.isfinite(x) else f"{x * 100:+.{d}f}%".replace(".", ",")
num = lambda x, d=1: "–" if x is None or not np.isfinite(x) else f"{x:.{d}f}".replace(".", ",")
MESI = ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]


def aldo_equity(path: Path, risk: float) -> tuple[pd.Series, pd.DataFrame]:
    t = pd.read_csv(path, parse_dates=["apertura", "chiusura"])
    rk = t.rischio_pct.where(t.rischio_pct.between(0.002, 0.2), 0.02)
    t["sul_capitale"] = t.rendimento * np.minimum(risk / rk, 10.0)
    t = t.sort_values("chiusura")
    idx = pd.date_range(A0, A1, freq="D")
    daily = t.groupby(t.chiusura.dt.normalize())["sul_capitale"].apply(lambda x: float(np.prod(1 + x)) - 1)
    eq = (1 + daily.reindex(idx).fillna(0.0)).cumprod()
    return eq, t


def ae_equity(risk: float) -> tuple[pd.Series, list]:
    assets = ["BTC", "ETH", "SOL", "TAO"]
    H = {a: AE.load(a) for a in assets}
    br = AE.btc_regime(H["BTC"])
    tr = [t for a in assets for t in AE.run_asset(a, H[a], br)]
    eq, done = AE.portfolio(tr, str(A0.date()), str(A1.date()), risk)
    return eq / eq.iloc[0], done


def stats(eq: pd.Series) -> dict:
    yrs = (eq.index[-1] - eq.index[0]).days / 365.25
    m = eq.resample("ME").last()
    mr = m / m.shift(1).fillna(1.0) - 1
    return {"tot": float(eq.iloc[-1] - 1), "cagr": float(eq.iloc[-1] ** (1 / yrs) - 1), "dd": float((eq / eq.cummax() - 1).min()),
            "mesi_pos": float((mr > 0).mean()), "best": float(mr.max()), "worst": float(mr.min()), "mr": mr}


def main():
    w = pd.read_csv(ROOT / "results" / "w32" / "equity.csv", index_col=0, parse_dates=True)
    S, info = {}, {}
    e = w["W3.2 radar (rischio 25%)"].loc[A0:A1]
    S["W3.2 (BTC, radar)"] = e / e.iloc[0]
    tr32 = pd.read_csv(ROOT / "results" / "w32" / "movimenti_w32.csv")
    tr32 = tr32[(tr32.entra >= str(A0.date())) & (tr32.entra < str(A1.date()))]
    info["W3.2 (BTC, radar)"] = {"n": len(tr32), "win": float((tr32.sul_capitale > 0).mean()), "ore": None, "tipo": "settimanale, 1 controllo a settimana"}
    for risk in (0.01, 0.02):
        eq, done = ae_equity(risk)
        k = f"Strategia AE, rischio {int(risk * 100)}%"
        S[k] = eq
        info[k] = {"n": len(done), "win": float(np.mean([d["rend"] > 0 for d in done])), "ore": float(np.median([d["giorni"] for d in done]) * 24), "tipo": "oraria, swing di giorni"}
    for f, nm in (("operazioni_trader.csv", "Aldo, prezzi delle sue schermate"), ("operazioni_follower_limite.csv", "Copytrading Aldo con ordini limite"),
                  ("operazioni_follower.csv", "Copytrading Aldo a mercato")):
        for risk in (0.01, 0.02):
            eq, t = aldo_equity(ROOT / "results" / "telegram" / f, risk)
            k = f"{nm}, rischio {int(risk * 100)}%"
            S[k] = eq
            info[k] = {"n": len(t), "win": float((t.rendimento > 0).mean()), "ore": float(t.giorni.median() * 24), "tipo": "intraday / pochi giorni"}
    for nm in ("Copytrading Aldo con ordini limite, rischio 2%",):
        r1, r2 = S["W3.2 (BTC, radar)"].pct_change().fillna(0), S[nm].pct_change().fillna(0)
        k = "50% W3.2 + 50% copytrading con ordini limite (2%)"
        S[k] = (1 + 0.5 * r1 + 0.5 * r2.reindex(r1.index).fillna(0)).cumprod()
        info[k] = {"n": info[nm]["n"] + info["W3.2 (BTC, radar)"]["n"], "win": np.nan, "ore": None, "tipo": "misto"}
    b = w["BTC comprato e tenuto"].loc[A0:A1]
    S["BTC comprato e tenuto"] = b / b.iloc[0]
    info["BTC comprato e tenuto"] = {"n": 0, "win": np.nan, "ore": None, "tipo": "nessuna operazione"}

    T = ["## F1 riepilogo\n", "Periodo del canale, 12/05/2023 – 18/03/2024 (10 mesi). Rendimenti sul capitale, dopo i costi.\n",
         "| Strategia | Rendimento totale | Annualizzato | Max DD | Mesi positivi | Mese migliore | Mese peggiore | Operazioni | In guadagno | Durata mediana |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    ST = {k: stats(v) for k, v in S.items()}
    for k, s in ST.items():
        i = info[k]
        dur = "–" if i["ore"] is None else (f"{num(i['ore'], 0)} ore" if i["ore"] < 48 else f"{num(i['ore'] / 24, 0)} giorni")
        T.append(f"| {k} | {pct(s['tot'], 0)} | {pct(s['cagr'], 0)} | {pct(s['dd'])} | {s['mesi_pos'] * 100:.0f}% | {pct(s['best'])} | {pct(s['worst'])} | "
                 f"{i['n'] if i['n'] else '–'} | {pct(i['win'], 0).lstrip('+') if np.isfinite(i['win']) else '–'} | {dur} |")
    T.append("\nPer Aldo e il copytrading il drawdown è misurato sulle chiusure delle operazioni: dentro le operazioni può essere più profondo.")

    T.append("\n## F2 mesi\n")
    keys = ["W3.2 (BTC, radar)", "Strategia AE, rischio 1%", "Aldo, prezzi delle sue schermate, rischio 2%", "Copytrading Aldo con ordini limite, rischio 2%",
            "Copytrading Aldo a mercato, rischio 2%", "BTC comprato e tenuto"]
    short = {"W3.2 (BTC, radar)": "W3.2", "Strategia AE, rischio 1%": "AE 1%", "Aldo, prezzi delle sue schermate, rischio 2%": "Aldo 2%",
             "Copytrading Aldo con ordini limite, rischio 2%": "Copia limite 2%", "Copytrading Aldo a mercato, rischio 2%": "Copia mercato 2%", "BTC comprato e tenuto": "BTC"}
    T.append("| Mese | " + " | ".join(short[k] for k in keys) + " |")
    T.append("|---|" + "---|" * len(keys))
    months = ST[keys[0]]["mr"].index
    for m in months:
        T.append(f"| {MESI[m.month - 1]} {m.year % 100:02d} | " + " | ".join(pct(float(ST[k]["mr"].get(m, np.nan))) for k in keys) + " |")
    T.append("| **Totale** | " + " | ".join(f"**{pct(ST[k]['tot'], 0)}**" for k in keys) + " |")
    T.append("\nMaggio 2023 parte dal 12; marzo 2024 finisce il 18.")

    pd.DataFrame({k: v for k, v in S.items()}).to_csv(OUT / "equity.csv")
    (OUT / "tables.md").write_text("\n".join(T) + "\n")
    print("\n".join(T))


if __name__ == "__main__":
    main()
