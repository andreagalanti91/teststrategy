"""W3.2: quando entra, quando esce, e controlli con ingressi e uscite a scaglioni (DCA).
Motore: vendor/radar_iu_engine.py (copia del motore a scaglioni del radar, rischio 25%), che a configurazione predefinita
riproduce W3.2 (78.474 $ dal 2021 con dati al 15/11/2026; 25.142 $ nel 2018-20). Scrive results/w32_inout/."""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "vendor"))
import radar_iu_engine as E  # noqa: E402

OUT = ROOT / "results" / "w32_inout"
OUT.mkdir(parents=True, exist_ok=True)
pct = lambda x, d=1: "n/d" if x is None or not np.isfinite(x) else f"{x * 100:+.{d}f}%".replace(".", ",")
usd = lambda x: f"{x:,.0f}".replace(",", ".")
num = lambda x, d=2: f"{x:.{d}f}".replace(".", ",")
REASON = {"trail": "trailing", "stop": "stop iniziale", "ema": "EMA 21", "dist": "distribuzione", "open": "aperta", "end": "fine periodo"}
rd = lambda n: pd.read_csv(ROOT / "data" / "btc" / n, index_col=0, parse_dates=True)
F, FL = rd("f_radar_live.csv.gz"), rd("f_long_radar.csv.gz")
FL = FL[FL.index <= "2020-12-31"]
PER = {"ALL": (F, "2021-01-01", None), "IS": (F, "2021-01-01", "2023-12-31"), "OOS": (F, "2024-01-01", None), "L": (FL, "2018-01-01", "2020-12-31")}


def run(cfg, per):
    x, s, e = PER[per]
    return E.simulate(x, cfg, start=s, end=e)


def tl(r):
    return list(r["trades"]) + ([dict(r["open"], pnl=r["open"].get("pnl_close", r["open"]["pnl"]), exit=None, reason="open")] if r["open"] else [])


def met(r):
    e = r["equity"] / r["equity"].iloc[0]
    yrs = (e.index[-1] - e.index[0]).days / 365.25
    dd = float((e / e.cummax() - 1).min())
    pn = np.array([t["pnl"] for t in tl(r)])
    cagr = float(e.iloc[-1] ** (1 / yrs) - 1)
    return dict(final=10000 * float(e.iloc[-1]), cagr=cagr, dd=dd, cdd=cagr / abs(dd), n=len(pn), wr=float((pn > 0).mean()), worst=float(pn.min()))


T = []
# ------------------------------------------------------------------ anatomia delle operazioni
rows = []
for per, x in (("2018–20", "L"), ("2021+", "ALL")):
    r = run({}, x)
    f, w = PER[x][0], r["weekly"]
    H, L, C = f["high"], f["low"], f["close"]
    for t in tl(r):
        sg = 1 if t["side"] == "long" else -1
        ws = w.loc[pd.Timestamp(t["signal"])]
        d0 = pd.Timestamp(t["entry"])
        d1 = pd.Timestamp(t["exit"]) if t.get("exit") else f.index[-1]
        px = t["entry_px"]
        adv = lambda a, b: float(((L if sg > 0 else H).loc[a:b] / px - 1).min() * sg) if sg > 0 else float(-((H.loc[a:b] / px - 1).max()))
        fav = lambda a, b: float(((H.loc[a:b] / px - 1).max())) if sg > 0 else float(-((L.loc[a:b] / px - 1).min()))
        mae14 = adv(d0, min(d0 + pd.Timedelta(days=13), d1))
        mfe = fav(d0, d1)
        mae_all = adv(d0, d1)
        best_close = float(((C.loc[d0:d1] / px - 1) * sg).max())
        # giorni fino al miglior prezzo d'ingresso disponibile nei primi 14 giorni
        seg = (L if sg > 0 else H).loc[d0:min(d0 + pd.Timedelta(days=13), d1)]
        day_best = int((seg.idxmin() if sg > 0 else seg.idxmax() - d0).days) if sg < 0 else int((seg.idxmin() - d0).days)
        post = {}
        if t.get("exit"):
            ex = t["exit_px"]
            for hd in (14, 28):
                seg2 = C.loc[d1:d1 + pd.Timedelta(days=hd)]
                post[hd] = float((seg2.iloc[-1] / ex - 1) * sg) if len(seg2) > 1 else np.nan
        age = int(ws.get("trend_age", np.nan)) if sg > 0 and np.isfinite(ws.get("trend_age", np.nan)) else np.nan
        rows.append({"periodo": per, "verso": t["side"], "segnale": t["signal"], "entra": t["entry"], "esce": t.get("exit"), "prezzo_in": px, "prezzo_out": t.get("exit_px", C.iloc[-1]),
                     "espo": t["expo"], "dist_ema21": float(ws["close"] / ws["ema21"] - 1), "dist_sma40": float(ws["close"] / ws["sma"] - 1), "flusso": float(ws["flow"]),
                     "fund7": float(ws["fund7"]), "eta_trend": age, "stop_dist": float(abs(t["stop0"] / t["sig_close"] - 1)),
                     "mae14": mae14, "giorno_miglior_prezzo": day_best, "mae": mae_all, "mfe": mfe, "miglior_chiusura": best_close, "mossa": t["move"], "pnl": t["pnl"],
                     "restituito": best_close - t["move"], "uscita": REASON.get(t.get("reason"), t.get("reason")), "giorni": (d1 - d0).days,
                     "dopo14": post.get(14, np.nan), "dopo28": post.get(28, np.nan)})
A = pd.DataFrame(rows)
A.to_csv(OUT / "anatomia_operazioni.csv", index=False)

T.append("## I1 ingressi\n")
T.append("| # | Verso | Segnale | Entra a | Sopra/sotto EMA 21 | Sopra/sotto SMA 40 | Flusso perp | Stop a | Esposizione | Peggior prezzo nei primi 14 giorni | Giorno del miglior prezzo d'ingresso | Risultato finale |")
T.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
for i, q in enumerate(A.itertuples(), 1):
    T.append(f"| {i} | {q.verso} | {q.segnale} | {usd(q.prezzo_in)} | {pct(q.dist_ema21)} | {pct(q.dist_sma40)} | {num(q.flusso)} | {pct(-q.stop_dist, 0)} | {num(q.espo)}x | "
             f"{pct(q.mae14)} | {q.giorno_miglior_prezzo} | {pct(q.pnl)} |")
T.append("\n## I2 uscite\n")
T.append("| # | Verso | Entra | Esce | Giorni | Motivo | Massimo guadagno toccato | Miglior chiusura | Mossa incassata | Restituito | Prezzo 14 giorni dopo l'uscita | 28 giorni dopo |")
T.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
for i, q in enumerate(A.itertuples(), 1):
    T.append(f"| {i} | {q.verso} | {q.entra} | {q.esce if isinstance(q.esce, str) else 'aperta'} | {q.giorni} | {q.uscita} | {pct(q.mfe)} | {pct(q.miglior_chiusura)} | {pct(q.mossa)} | "
             f"{pct(q.restituito)} | {pct(q.dopo14)} | {pct(q.dopo28)} |")

# coerenza
T.append("\n## I3 coerenza ingressi\n")
cl = A[A.uscita != "aperta"]
T.append("| Gruppo | Operazioni | Distanza mediana dalla EMA 21 | Distanza mediana dalla SMA 40 | Flusso mediano | Stop mediano | Prezzo peggiore nei primi 14 giorni (mediana) | Con almeno −5% nei primi 14 giorni | Miglior prezzo d'ingresso: giorno mediano |")
T.append("|---|---|---|---|---|---|---|---|---|")
for lab, x in (("Tutte", A), ("Long", A[A.verso == "long"]), ("Short", A[A.verso == "short"]), ("In guadagno", A[A.pnl > 0]), ("In perdita", A[A.pnl <= 0]),
               ("Dal 2021", A[A.periodo == "2021+"]), ("2018–20", A[A.periodo == "2018–20"])):
    T.append(f"| {lab} | {len(x)} | {pct(x.dist_ema21.abs().median())} | {pct(x.dist_sma40.abs().median())} | {num(x.flusso.abs().median())} | {pct(-x.stop_dist.median(), 0)} | "
             f"{pct(x.mae14.median())} | {(x.mae14 <= -0.05).mean() * 100:.0f}% | {x.giorno_miglior_prezzo.median():.0f} |")
T.append("\n## I4 coerenza uscite\n")
T.append("| Motivo di uscita | Operazioni | In guadagno | Mossa media incassata | Miglior chiusura media | Restituito in media | Prezzo 14 giorni dopo (media, nel verso del trade) | 28 giorni dopo | Uscite seguite da un movimento a favore oltre +5% a 28 giorni |")
T.append("|---|---|---|---|---|---|---|---|---|")
for lab, x in [(k, v) for k, v in cl.groupby("uscita")] + [("Tutte le chiuse", cl)]:
    T.append(f"| {lab} | {len(x)} | {(x.pnl > 0).mean() * 100:.0f}% | {pct(x.mossa.mean())} | {pct(x.miglior_chiusura.mean())} | {pct(x.restituito.mean())} | {pct(x.dopo14.mean())} | "
             f"{pct(x.dopo28.mean())} | {(x.dopo28 > 0.05).sum()} su {x.dopo28.notna().sum()} |")
T.append(f"\nDurata mediana: {cl.giorni.median():.0f} giorni (in guadagno {cl[cl.pnl > 0].giorni.median():.0f}, in perdita {cl[cl.pnl <= 0].giorni.median():.0f}). "
         f"Somma dei massimi guadagni toccati: {pct(cl.mfe.sum(), 0)}; somma delle mosse incassate: {pct(cl.mossa.sum(), 0)}.")

# ------------------------------------------------------------------ varianti DCA
VAR = {
    "W3.2 (tutto subito, tutto insieme)": {},
    "Ingresso: 1/3 lunedì, mercoledì, venerdì": dict(entry=("E1", (0, 2, 4))),
    "Ingresso: 1/3 ogni lunedì per 3 settimane (senza condizioni)": dict(entry=("E1", (0, 7, 14))),
    "Ingresso: 1/2 subito, 1/2 la settimana dopo se il segnale regge": dict(entry=("E2", 2)),
    "Ingresso: 1/3 a settimana per 3 settimane se il segnale regge": dict(entry=("E2", 3)),
    "Ingresso: 1/2 subito, 1/2 con limite a −0,25 ATR (5 giorni)": dict(entry=("E3", 0.25, 5)),
    "Ingresso: 1/2 subito, 1/2 con limite a −0,5 ATR (5 giorni)": dict(entry=("E3", 0.5, 5)),
    "Ingresso: 1/2 subito, 1/2 con limite a −1 ATR (10 giorni)": dict(entry=("E3", 1.0, 10)),
    "Uscita: 1/2 al primo segnale, 1/2 alla conferma": dict(exit=("U1", 0.5)),
    "Uscita: 1/3 al primo segnale, 2/3 alla conferma": dict(exit=("U1", 1 / 3)),
    "Uscita: due metà con trailing a 2,0 e 3,0 ATR": dict(exit=("U2", 2.0, 3.0)),
    "Uscita: due metà con trailing a 1,5 e 2,5 ATR": dict(exit=("U2", 1.5, 2.5)),
    "Uscita: 1/3 a +2R (target), resto con le regole": dict(tp=dict(levels=(2,), frac=1 / 3)),
    "Uscita: 1/3 a +1R e 1/3 a +2R, resto con le regole": dict(tp=dict(levels=(1, 2), frac=1 / 3)),
    "Uscita: 1/2 a +1R, resto con le regole": dict(tp=dict(levels=(1,), frac=0.5)),
    "Entrambi: ingresso lun/mer/ven + uscita in due metà": dict(entry=("E1", (0, 2, 4)), exit=("U1", 0.5)),
    "Entrambi: ingresso con limite −0,5 ATR + 1/3 a +2R": dict(entry=("E3", 0.5, 5), tp=dict(levels=(2,), frac=1 / 3)),
}
base = {p: run({}, p) for p in PER}
bm = {p: met(base[p]) for p in PER}
bt = {t["signal"]: t["pnl"] for t in tl(base["ALL"])} | {t["signal"]: t["pnl"] for t in tl(base["L"])}
T.append("\n## I5 dca\n")
T.append("| Variante | 10.000 $ → (dal 2021) | CAGR | Max DD | CAGR/DD | Operazioni | Vincenti | Peggiore | 2021–23: finale | 2024–26: finale | 2018–20: finale / DD | Operazioni migliorate / peggiorate | Esito |")
T.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
vres, deltas = [], {}
for nm, cfg in VAR.items():
    rr = {p: run(cfg, p) for p in PER}
    m = {p: met(rr[p]) for p in PER}
    vt = {t["signal"]: t["pnl"] for t in tl(rr["ALL"])} | {t["signal"]: t["pnl"] for t in tl(rr["L"])}
    dl = {k: vt[k] - bt[k] for k in bt if k in vt}
    deltas[nm] = dl
    up, dn = sum(v > 0.002 for v in dl.values()), sum(v < -0.002 for v in dl.values())
    beats = nm.startswith("W3.2") or (m["IS"]["cdd"] > bm["IS"]["cdd"] and m["OOS"]["cdd"] > bm["OOS"]["cdd"] and m["L"]["cdd"] >= bm["L"]["cdd"])
    part = (m["IS"]["cdd"] > bm["IS"]["cdd"]) + (m["OOS"]["cdd"] > bm["OOS"]["cdd"]) + (m["L"]["cdd"] >= bm["L"]["cdd"])
    esito = "riferimento" if nm.startswith("W3.2") else "migliora in tutti e tre i periodi" if beats else f"migliora in {part} periodi su 3"
    vres.append({"variante": nm, **{f"{p}_{k}": v for p in PER for k, v in m[p].items()}, "migliorate": up, "peggiorate": dn, "esito": esito})
    T.append(f"| {nm} | {usd(m['ALL']['final'])} | {pct(m['ALL']['cagr'])} | {pct(m['ALL']['dd'])} | {num(m['ALL']['cdd'])} | {m['ALL']['n']} | {m['ALL']['wr'] * 100:.0f}% | {pct(m['ALL']['worst'])} | "
             f"{usd(m['IS']['final'])} | {usd(m['OOS']['final'])} | {usd(m['L']['final'])} / {pct(m['L']['dd'], 0)} | {'–' if nm.startswith('W3.2') else f'{up} / {dn}'} | {esito} |")
pd.DataFrame(vres).to_csv(OUT / "varianti_dca.csv", index=False)

T.append("\n## I6 delta\n")
show = ["Ingresso: 1/3 lunedì, mercoledì, venerdì", "Ingresso: 1/3 a settimana per 3 settimane se il segnale regge", "Ingresso: 1/2 subito, 1/2 con limite a −0,5 ATR (5 giorni)",
        "Uscita: 1/2 al primo segnale, 1/2 alla conferma", "Uscita: due metà con trailing a 2,0 e 3,0 ATR", "Uscita: 1/3 a +2R (target), resto con le regole"]
short = ["DCA lun/mer/ven", "DCA 3 settimane", "Limite −0,5 ATR", "Uscita in due metà", "Trailing 2,0/3,0", "1/3 a +2R"]
T.append("| Segnale | Verso | W3.2 | " + " | ".join(short) + " |")
T.append("|---|---|---|" + "---|" * len(short))
for q in A.itertuples():
    T.append(f"| {q.segnale} | {q.verso} | {pct(q.pnl)} | " + " | ".join(pct(deltas[k].get(q.segnale, np.nan)) for k in show) + " |")
T.append("| **Somma delle differenze** | | | " + " | ".join(pct(sum(deltas[k].values())) for k in show) + " |")
(OUT / "tables.md").write_text("\n".join(T) + "\n")
print("\n".join(T))

# ------------------------------------------------------------------ controllo sull'unica variante promettente: trailing in due meta'
T2 = ["\n## I7 vicini\n"]
T2.append("| Variante | 10.000 $ → (dal 2021) | Max DD | CAGR/DD | Esposizione media in posizione | 2021–23: finale | 2024–26: finale | 2018–20: finale / DD | Peggiore |")
T2.append("|---|---|---|---|---|---|---|---|---|")
NB = {"W3.2: trailing unico a 2,5 ATR": {}, "Due metà 1,5 e 2,5 ATR": dict(exit=("U2", 1.5, 2.5)), "Due metà 1,25 e 2,5": dict(exit=("U2", 1.25, 2.5)),
      "Due metà 1,75 e 2,5": dict(exit=("U2", 1.75, 2.5)), "Due metà 2,0 e 2,5": dict(exit=("U2", 2.0, 2.5)), "Due metà 1,5 e 3,0": dict(exit=("U2", 1.5, 3.0)),
      "Due metà 1,0 e 3,0": dict(exit=("U2", 1.0, 3.0)), "Due metà 2,0 e 3,0": dict(exit=("U2", 2.0, 3.0)),
      "Trailing unico a 2,0 ATR (stessa dimensione di 1,5 e 2,5)": dict(k=2.0), "Trailing unico a 2,25 ATR": dict(k=2.25), "Trailing unico a 1,5 ATR": dict(k=1.5),
      "Trailing unico a 3,0 ATR": dict(k=3.0)}
nb = []
for nm, cfg in NB.items():
    rr = {p: run(cfg, p) for p in PER}
    m = {p: met(rr[p]) for p in PER}
    ex = float(np.mean([t["expo"] for t in tl(rr["ALL"])]))
    nb.append({"variante": nm, "finale": m["ALL"]["final"], "dd": m["ALL"]["dd"], "cdd": m["ALL"]["cdd"], "espo": ex, "is": m["IS"]["final"], "oos": m["OOS"]["final"],
               "l": m["L"]["final"], "l_dd": m["L"]["dd"]})
    T2.append(f"| {nm} | {usd(m['ALL']['final'])} | {pct(m['ALL']['dd'])} | {num(m['ALL']['cdd'])} | {num(ex)}x | {usd(m['IS']['final'])} | {usd(m['OOS']['final'])} | "
              f"{usd(m['L']['final'])} / {pct(m['L']['dd'], 0)} | {pct(m['ALL']['worst'])} |")
pd.DataFrame(nb).to_csv(OUT / "vicini_trailing.csv", index=False)
with open(OUT / "tables.md", "a") as fh:
    fh.write("\n".join(T2) + "\n")
print("\n".join(T2))
