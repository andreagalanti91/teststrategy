"""W3.2 eseguita con opzioni comprate: a ogni segnale si compra una call (long) o una put (short) alla pari.

Prezzi delle opzioni da modello (Black) con la volatilita' implicita stimata delle opzioni alla pari (vedi ricerca_nuova.iv_series):
non sono prezzi osservati. La parte finale confronta il modello con i prezzi veri di OKX dove esistono.
Uscite: results/opzioni_w32/tables.md, equity.csv, operazioni.csv, opzioni_w32.png
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import btc_ta as B
import ricerca_nuova as R

ROOT = B.ROOT
OUT = ROOT / "results" / "opzioni_w32"
OUT.mkdir(parents=True, exist_ok=True)
pct = lambda x, d=1: "n/d" if x is None or not np.isfinite(x) else f"{x * 100:+.{d}f}%".replace(".", ",")
num = lambda x, d=2: "n/d" if x is None or not np.isfinite(x) else f"{x:.{d}f}".replace(".", ",")
usd = lambda x: f"{x:,.0f}".replace(",", ".")
T = []
DAY = pd.Timedelta(days=1)
# costi OKX (opzioni lineari, listino SEE): taker 0,03% del controvalore con tetto 7% del premio; esercizio 0,02% (stesso tetto)
FEE, FEE_CAP, EX_FEE = 0.0003, 0.07, 0.0002


def simulate(tr: pd.DataFrame, c: pd.Series, iv_in: pd.Series, iv_out: pd.Series, tenor: int, bud: float, roll: bool, spread: float = 0.03,
             moneyness: float = 1.0) -> tuple[pd.Series, pd.DataFrame]:
    """spread = mezzo differenziale denaro-lettera in frazione del premio (si compra a modello x (1+spread), si vende a x (1-spread)).
    roll = se l'opzione scade mentre W3.2 e' ancora in posizione, se ne compra un'altra uguale con la stessa quota del capitale."""
    days = c.loc[iv_in.index[0]:].index
    eq = pd.Series(np.nan, days)
    cap, rows = 1.0, []
    ivq = lambda s, d: float(s.reindex([d], method="ffill").iloc[0])
    for t in tr.itertuples():
        cp = 1 if t.verso == "long" else -1
        cap0, start, s0, spent_tot, n_opt = cap, t.entra, float(t.prezzo_in), 0.0, 0
        eq.loc[eq.index < start] = eq.loc[eq.index < start].fillna(cap)
        while True:
            K = s0 * (moneyness if cp > 0 else 2 - moneyness)
            pm = R.bs(s0, K, tenor / 365, ivq(iv_in, start - DAY), cp)
            unit = pm * (1 + spread) + min(FEE * s0, FEE_CAP * pm)
            spent = bud * cap
            n = spent / unit
            spent_tot += spent
            n_opt += 1
            exp = start + pd.Timedelta(days=tenor)
            end = min(t.esce, exp)
            for d in days[(days >= start) & (days < end)]:                     # valore di realizzo giorno per giorno
                eq[d] = cap - spent + n * R.bs(float(c[d]), K, max(0.0, (exp - d - DAY).days / 365), ivq(iv_out, d), cp) * (1 - spread)
            if t.esce <= exp:                                                 # W3.2 esce prima della scadenza: si rivende l'opzione
                s1 = float(t.prezzo_out) if t.uscita != "aperta" else float(c.loc[:t.esce].iloc[-1])
                tau = max(0.0, (exp - t.esce).days / 365)
                if tau > 0:
                    p1 = R.bs(s1, K, tau, ivq(iv_out, t.esce - DAY), cp)
                    got = n * max(0.0, p1 * (1 - spread) - min(FEE * s1, FEE_CAP * p1))
                else:
                    it = max(0.0, cp * (s1 - K))
                    got = n * (it - min(EX_FEE * s1, FEE_CAP * it))
                cap = cap - spent + got
                break
            s1 = float(c.loc[:exp - DAY].iloc[-1])                            # scadenza: si incassa il valore intrinseco
            it = max(0.0, cp * (s1 - K))
            cap = cap - spent + n * (it - min(EX_FEE * s1, FEE_CAP * it))
            if not roll:
                break
            start, s0 = exp, s1
        rows.append({"verso": t.verso, "entra": t.entra, "esce": t.esce, "aperta": t.uscita == "aperta", "w32": t.sul_capitale, "ris": cap / cap0 - 1, "opzioni": n_opt,
                     "premio": spent_tot / cap0, "prezzo_in": t.prezzo_in, "prezzo_out": t.prezzo_out, "mossa": cp * (float(t.prezzo_out) / float(t.prezzo_in) - 1)})
        eq.loc[(eq.index >= end) & eq.isna()] = np.nan
        eq.loc[eq.index >= min(end, days[-1])] = cap
    return eq.ffill(), pd.DataFrame(rows)


def stats(eq: pd.Series, o: pd.DataFrame) -> dict:
    yrs = (eq.index[-1] - eq.index[0]).days / 365.25
    r = o.ris.to_numpy()
    run = min(np.prod(1 + r[i:j]) - 1 for i in range(len(r)) for j in range(i + 1, len(r) + 1))
    return {"fin": float(eq.iloc[-1]), "cagr": float(eq.iloc[-1] ** (1 / yrs) - 1), "dd": float((eq / eq.cummax() - 1).min()), "win": float((r > 0).mean()), "worst": float(r.min()),
            "best": float(r.max()), "run": float(run), "premio": float(o.premio.mean()), "nopt": float(o.opzioni.mean())}


def main() -> None:
    B.END = "2026-12-31"
    d = B.load()
    c = d["close"]
    iv, ivraw = R.iv_series(d), R.iv_series(d, raw=True)
    tr = pd.read_csv(ROOT / "results" / "w32" / "movimenti_w32.csv")
    tr["entra"] = pd.to_datetime(tr["entra"])
    tr["esce"] = pd.to_datetime(tr["esce"]).fillna(c.index[-1])
    tr = tr[tr.entra >= iv.index[0] + DAY].reset_index(drop=True)
    w = pd.read_csv(ROOT / "results" / "w32" / "equity.csv", index_col=0, parse_dates=True)["W3.2 radar (rischio 25%)"]
    w = w.loc[iv.index[0]:] / w.loc[iv.index[0]:].iloc[0]
    wy = (w.index[-1] - w.index[0]).days / 365.25
    rw = tr.sul_capitale.to_numpy()

    # ---------- P1 griglia
    T.append("## P1 griglia\n")
    T.append(f"Operazioni di W3.2 dal {tr.entra.iloc[0].date()}: {len(tr)} (l'ultima è aperta). Durata mediana: {int((tr.esce - tr.entra).dt.days.median())} giorni. "
             f"Costi: differenziale denaro-lettera 3% del premio per lato, commissione 0,03% del controvalore (tetto 7% del premio), esercizio 0,02%.\n")
    T.append("| Versione | 10.000 $ → | CAGR | Max DD (giornaliero) | Operazioni in guadagno | Operazione peggiore | Migliore | Serie peggiore di perdite | Premio speso per operazione | Opzioni per operazione |")
    T.append("|---|---|---|---|---|---|---|---|---|---|")
    T.append(f"| W3.2 originale (spot e perp, rischio 25% allo stop) | {usd(10000 * float(w.iloc[-1]))} | {pct(float(w.iloc[-1]) ** (1 / wy) - 1)} | {pct(float((w / w.cummax() - 1).min()))} | {(rw > 0).mean() * 100:.0f}% | "
             f"{pct(rw.min())} | {pct(rw.max())} | {pct(min(np.prod(1 + rw[i:j]) - 1 for i in range(len(rw)) for j in range(i + 1, len(rw) + 1)))} | – | – |")
    wd = w.pct_change().fillna(0.0)
    for f_ in (0.5, 0.2):
        e_ = (1 + f_ * wd).cumprod()
        T.append(f"| W3.2 a {'metà' if f_ == 0.5 else 'un quinto della'} dimensione (riferimento a rischio simile) | {usd(10000 * float(e_.iloc[-1]))} | {pct(float(e_.iloc[-1]) ** (1 / wy) - 1)} | {pct(float((e_ / e_.cummax() - 1).min()))} | "
                 f"{(rw > 0).mean() * 100:.0f}% | {pct(f_ * rw.min())} | {pct(f_ * rw.max())} | – | – | – |")
    G, E = {}, {}
    for roll in (False, True):
        for tenor in (30, 60, 90):
            for bud in (0.05, 0.10):
                eq, o = simulate(tr, c, iv, iv, tenor, bud, roll)
                s = stats(eq, o)
                G[(tenor, bud, roll)] = (s, o)
                E[(tenor, bud, roll)] = eq
                T.append(f"| Opzione a {tenor} giorni, {bud * 100:.0f}% del capitale, {'con rinnovo' if roll else 'una sola'} | {usd(10000 * s['fin'])} | {pct(s['cagr'])} | {pct(s['dd'])} | {s['win'] * 100:.0f}% | "
                         f"{pct(s['worst'])} | {pct(s['best'])} | {pct(s['run'])} | {pct(s['premio']).lstrip('+')} | {num(s['nopt'], 1)} |")

    BASE = (30, 0.05, False)                   # una sola opzione per segnale: la perdita massima e' fissata all'ingresso (5% del capitale)
    sb, ob = G[BASE]
    ob.to_csv(OUT / "operazioni.csv", index=False)

    # ---------- P2 dettaglio
    T.append("\n## P2 dettaglio\n")
    T.append("| # | Verso | Entra | Esce | Movimento di BTC a favore | W3.2 originale | Opzioni comprate | Premio speso (sul capitale) | Risultato con opzioni |")
    T.append("|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(ob.itertuples(), 1):
        T.append(f"| {i} | {r.verso} | {r.entra.date()} | {'aperta' if r.aperta else r.esce.date()} | {pct(r.mossa)} | {pct(r.w32)} | {r.opzioni} | {pct(r.premio).lstrip('+')} | {pct(r.ris)} |")

    # ---------- P3 sensibilita'
    T.append("\n## P3 sensibilita\n")
    T.append("| Ipotesi (versione base: 30 giorni, 5% del capitale, una sola opzione) | 10.000 $ → | CAGR | Max DD | Operazioni in guadagno | Operazione peggiore |")
    T.append("|---|---|---|---|---|---|")
    sc = [("Base", dict(iv_in=iv, iv_out=iv)),
          ("Volatilità al livello del DVOL, in acquisto e in vendita", dict(iv_in=ivraw, iv_out=ivraw)),
          ("Si compra al livello del DVOL, si rivende alla volatilità alla pari", dict(iv_in=ivraw, iv_out=iv)),
          ("Volatilità pagata +20%", dict(iv_in=iv * 1.2, iv_out=iv)),
          ("Differenziale denaro-lettera doppio (6% per lato)", dict(iv_in=iv, iv_out=iv, spread=0.06)),
          ("Tutto insieme: DVOL in acquisto, alla pari in vendita, differenziale 6%", dict(iv_in=ivraw, iv_out=iv, spread=0.06)),
          ("Opzione 5% fuori dal prezzo (più economica, serve più movimento)", dict(iv_in=iv, iv_out=iv, moneyness=1.05)),
          ("Opzione 5% dentro il prezzo (più cara, perde valore più lentamente)", dict(iv_in=iv, iv_out=iv, moneyness=0.95))]
    for lab, kw in sc:
        eq, o = simulate(tr, c, tenor=BASE[0], bud=BASE[1], roll=BASE[2], **kw)
        s = stats(eq, o)
        T.append(f"| {lab} | {usd(10000 * s['fin'])} | {pct(s['cagr'])} | {pct(s['dd'])} | {s['win'] * 100:.0f}% | {pct(s['worst'])} |")
    for tn in (21, 25, 35, 45):
        eq, o = simulate(tr, c, iv, iv, tn, BASE[1], False)
        s = stats(eq, o)
        T.append(f"| Scadenza a {tn} giorni invece di 30 | {usd(10000 * s['fin'])} | {pct(s['cagr'])} | {pct(s['dd'])} | {s['win'] * 100:.0f}% | {pct(s['worst'])} |")
    # senza le migliori
    r = ob.ris.to_numpy()
    srt = np.sort(r)[::-1]
    yb = (E[BASE].index[-1] - E[BASE].index[0]).days / 365.25
    T.append(f"\nDipendenza dalle operazioni migliori: tutte le {len(r)} operazioni danno ×{num(float(np.prod(1 + r)), 1)}; senza la migliore ×{num(float(np.prod(1 + srt[1:])), 1)}; "
             f"senza le tre migliori ×{num(float(np.prod(1 + srt[3:])), 1)} ({pct(float(np.prod(1 + srt[3:])) ** (1 / yb) - 1)} annuo); senza le cinque migliori ×{num(float(np.prod(1 + srt[5:])), 1)} "
             f"({pct(float(np.prod(1 + srt[5:])) ** (1 / yb) - 1)} annuo). Per W3.2 originale: ×{num(float(np.prod(1 + rw)), 1)}, ×{num(float(np.prod(1 + np.sort(rw)[::-1][1:])), 1)}, "
             f"×{num(float(np.prod(1 + np.sort(rw)[::-1][3:])), 1)}.")

    # ---------- P4 bootstrap sulle operazioni, con il percorso giornaliero dentro ogni operazione
    T.append("\n## P4 bootstrap\n")
    rng = np.random.default_rng(7)
    NS, NT = 5000, 8                            # circa 2,6 operazioni l'anno: 8 in tre anni
    T.append(f"Si estraggono a caso {NT} operazioni (circa tre anni) dalle {len(r)} dello storico, {usd(NS)} volte, ognuna con il suo percorso giornaliero: il drawdown comprende anche le oscillazioni a operazione aperta.\n")
    T.append("| Versione | Risultato mediano a 3 anni | 5° percentile | Probabilità di chiudere in perdita | Drawdown mediano | Probabilità di drawdown oltre −20% | oltre −35% |")
    T.append("|---|---|---|---|---|---|---|")

    def segs(e, trd):                           # percorso giornaliero relativo di ogni operazione (1 = capitale prima dell'ingresso)
        out = []
        for t in trd.itertuples():
            x = e.loc[t.entra - DAY:t.esce].to_numpy()
            out.append(x / x[0])
        return out

    def boot(sg, lab, mod=None):
        fin, dds = np.empty(NS), np.empty(NS)
        for i in range(NS):
            cur, peak, dd = 1.0, 1.0, 0.0
            for j in rng.integers(0, len(sg), NT):
                x = sg[j] if mod is None else mod(sg[j])
                v = cur * x
                pk = np.maximum(peak, np.maximum.accumulate(v))
                dd = min(dd, float((v / pk - 1).min()))
                cur, peak = float(v[-1]), float(pk[-1])
            fin[i], dds[i] = cur, dd
        T.append(f"| {lab} | {pct(float(np.median(fin)) - 1, 0)} | {pct(float(np.percentile(fin, 5)) - 1, 0)} | {(fin < 1).mean() * 100:.0f}% | {pct(float(np.median(dds)), 0)} | {(dds < -0.20).mean() * 100:.0f}% | {(dds < -0.35).mean() * 100:.0f}% |")

    boot(segs(w, tr), "W3.2 originale")
    boot(segs((1 + 0.5 * wd).cumprod(), tr), "W3.2 a metà dimensione")
    for k, lab in (((30, 0.05, False), "Opzioni a 30 giorni, 5%, una sola (base)"), ((30, 0.10, False), "Opzioni a 30 giorni, 10%, una sola"), ((30, 0.10, True), "Opzioni a 30 giorni, 10%, con rinnovo"),
                   ((90, 0.10, False), "Opzioni a 90 giorni, 10%, una sola")):
        boot(segs(E[k], tr), lab)
    # con meno operazioni in guadagno: una parte delle vincenti estratte diventa una perdita piena del premio
    sgb, winshare = segs(E[BASE], tr), float((ob.ris > 0).mean())
    lose = np.array([1.0, 1 - BASE[1]])
    for share, lab in ((0.65, "Base, se le operazioni in guadagno scendono dall'80% al 65%"), (0.5, "Base, se scendono al 50%"), (0.35, "Base, se scendono al 35%")):
        boot(sgb, lab, mod=lambda x, sh=share: lose if (x[-1] > 1 and rng.random() > sh / winshare) else x)

    # ---------- P7 lo stesso dal 2018, con la volatilita' stimata per l'anno che manca
    lr = np.log(c / c.shift(1))
    est = (np.sqrt((lr ** 2).rolling(30).mean() * 365) * 1.1).loc["2018-01-01":iv.index[0] - DAY]
    iv18 = pd.concat([est, iv])
    tr18 = pd.read_csv(ROOT / "results" / "w32" / "movimenti_w32.csv")
    tr18["entra"] = pd.to_datetime(tr18["entra"])
    tr18["esce"] = pd.to_datetime(tr18["esce"]).fillna(c.index[-1])
    w18 = pd.read_csv(ROOT / "results" / "w32" / "equity.csv", index_col=0, parse_dates=True)["W3.2 radar (rischio 25%)"]
    w18 = w18 / w18.iloc[0]
    y18 = (w18.index[-1] - w18.index[0]).days / 365.25
    T.append("\n## P7 dal2018\n")
    T.append(f"Per il 2018 non esistono dati di volatilità implicita: si usa la volatilità realizzata dei 30 giorni precedenti aumentata del 10%. Operazioni: {len(tr18)}.\n")
    T.append("| Dal 2018 | 10.000 $ → | CAGR | Max DD (giornaliero) | Operazioni in guadagno | Operazione peggiore |")
    T.append("|---|---|---|---|---|---|")
    r18 = tr18.sul_capitale.to_numpy()
    for f_, lab in ((1.0, "W3.2 originale"), (0.5, "W3.2 a metà dimensione")):
        e_ = (1 + f_ * w18.pct_change().fillna(0.0)).cumprod()
        T.append(f"| {lab} | {usd(10000 * float(e_.iloc[-1]))} | {pct(float(e_.iloc[-1]) ** (1 / y18) - 1)} | {pct(float((e_ / e_.cummax() - 1).min()))} | {(r18 > 0).mean() * 100:.0f}% | {pct(f_ * r18.min())} |")
    for tn, bd in ((30, 0.05), (30, 0.10), (35, 0.05), (25, 0.05)):
        eq, o = simulate(tr18, c, iv18, iv18, tn, bd, False)
        s = stats(eq, o)
        T.append(f"| Opzioni a {tn} giorni, {bd * 100:.0f}% | {usd(10000 * s['fin'])} | {pct(s['cagr'])} | {pct(s['dd'])} | {s['win'] * 100:.0f}% | {pct(s['worst'])} |")
    o18 = simulate(tr18, c, iv18, iv18, 30, 0.05, False)[1].head(3)
    T.append("\nLe tre operazioni del 2018: " + "; ".join(f"{r_.verso} del {r_.entra.date()}, W3.2 {pct(r_.w32)}, opzione {pct(r_.ris)}" for r_ in o18.itertuples()) + ".")

    # ---------- P5 il modello contro i prezzi veri di OKX (contratti ancora vivi: storia dal giorno di quotazione)
    okx = ROOT / "data" / "opzioni" / "okx"
    snaps = sorted(okx.glob("catena_*.csv.gz"))
    ch = pd.read_csv(snaps[-1], parse_dates=["scadenza", "quotata"])
    snap_day = snaps[-1].name[7:17]
    T.append("\n## P5 reale\n")
    if (okx / "candele_1Dutc.csv.gz").exists():
        k = pd.read_csv(okx / "candele_1Dutc.csv.gz", parse_dates=["data"]).merge(ch[["instId", "stk", "optType", "scadenza", "ctType"]], on="instId")
        k = k[(k.contratti > 0) & (k.data <= iv.index[-1])]
        k["S"] = c.reindex(k.data).to_numpy()
        k["gg"] = (k.scadenza.dt.normalize() - k.data - DAY).dt.days
        k["usd"] = np.where(k.ctType == "inverse", k.close * k.S, k.close)
        k = k[(k.gg >= 7) & ((k.stk / k.S - 1).abs() <= 0.03) & k.S.notna()]
        k["modello"] = [R.bs(r.S, r.stk, r.gg / 365, float(iv.reindex([r.data], method="ffill").iloc[0]), 1 if r.optType == "C" else -1) for r in k.itertuples()]
        k["dvol"] = [R.bs(r.S, r.stk, r.gg / 365, float(ivraw.reindex([r.data], method="ffill").iloc[0]), 1 if r.optType == "C" else -1) for r in k.itertuples()]
        k["rap"], k["rapd"] = k.usd / k.modello, k.usd / k.dvol
        k.to_csv(OUT / "reale_vs_modello.csv", index=False)
        T.append(f"Prezzi di chiusura giornalieri veri su OKX dei contratti oggi ancora quotati, con prezzo d'esercizio entro il 3% dal prezzo di BTC e almeno un contratto scambiato nel giorno "
                 f"(dal {k.data.min().date()} al {k.data.max().date()}), divisi per il prezzo del modello nello stesso giorno. Sopra 1: l'opzione vera costava più del modello.\n")
        T.append("| Giorni alla scadenza | Osservazioni | Prezzo vero / modello (mediana) | Un quarto dei casi sotto | Un quarto sopra | Prezzo vero / modello al livello del DVOL (mediana) |")
        T.append("|---|---|---|---|---|---|")
        for lab, a_, b_ in (("7–20", 7, 20), ("20–45 (la scadenza della strategia)", 20, 45), ("45–90", 45, 90), ("90–180", 90, 180), ("oltre 180", 180, 9999)):
            y = k[(k.gg >= a_) & (k.gg < b_)]
            if len(y) >= 5:
                T.append(f"| {lab} | {len(y)} | {num(float(y.rap.median()))} | {num(float(y.rap.quantile(0.25)))} | {num(float(y.rap.quantile(0.75)))} | {num(float(y.rapd.median()))} |")
    else:
        T.append("Storico OKX non ancora scaricato (python backtest/fetch_okx_options.py --candele).")

    # ---------- P6 esempio con le quotazioni vere di oggi
    for col in ("bidPx", "askPx", "markVol", "delta", "fwdPx", "stk"):
        ch[col] = pd.to_numeric(ch[col], errors="coerce")
    now = pd.to_datetime(pd.to_numeric(ch.ts).max(), unit="ms")
    lin = ch[(ch.ctType == "linear") & (ch.bidPx > 0) & (ch.askPx > 0)].copy()
    lin["gg"] = (lin.scadenza - now).dt.total_seconds() / 86400
    exp = lin.loc[(lin.gg - 30).abs().idxmin(), "scadenza"]
    y = lin[lin.scadenza == exp]
    fwd = float(y.fwdPx.median())
    T.append("\n## P6 oggi\n")
    T.append(f"Quotazioni OKX del {now.strftime('%d/%m/%Y, %H:%M')} UTC, opzioni lineari (premio e regolamento in dollari), scadenza {exp.strftime('%d/%m/%Y')} ({(exp - now).days} giorni). "
             f"Prezzo a termine di BTC: {usd(fwd)} $. Un contratto vale 0,01 BTC.\n")
    T.append("| Opzione | Prezzo d'esercizio | Denaro (vendi a) | Lettera (compri a) | Differenza denaro-lettera | Costo di un contratto (0,01 BTC) | Volatilità implicita | Premio in % del prezzo di BTC |")
    T.append("|---|---|---|---|---|---|---|---|")
    ks = sorted(y.stk.unique(), key=lambda v: abs(v - fwd))
    atm = ks[0]
    for typ, name in (("P", "Put"), ("C", "Call")):
        for kk in sorted(sorted([v for v in ks if v % 1000 == 0], key=lambda v: abs(v - fwd))[:3]):
            r = y[(y.stk == kk) & (y.optType == typ)]
            if len(r):
                r = r.iloc[0]
                T.append(f"| {name} | {usd(kk)} $ | {usd(r.bidPx)} $ | {usd(r.askPx)} $ | {pct((r.askPx - r.bidPx) / ((r.askPx + r.bidPx) / 2)).lstrip('+')} | {num(r.askPx * 0.01, 2)} $ | {r.markVol * 100:.0f}% | {pct(r.askPx / fwd).lstrip('+')} |")
    CAP, BUD = 45000.0, 0.05
    put = y[(y.stk == atm) & (y.optType == "P")].iloc[0]
    fee = min(FEE * fwd, FEE_CAP * put.askPx)
    ncontr = int(CAP * BUD / ((put.askPx + fee) * 0.01))
    qty = ncontr * 0.01
    spent = ncontr * 0.01 * (put.askPx + fee)
    T.append(f"\nEsempio: capitale {usd(CAP)} $, segnale short di W3.2, quota 5% = {usd(CAP * BUD)} $. Put con prezzo d'esercizio {usd(atm)} $ a {usd(put.askPx)} $: si comprano {ncontr} contratti "
             f"({num(qty, 2)} BTC, controvalore {usd(qty * fwd)} $), spesa {usd(spent)} $ commissioni incluse. Cosa succede alla scadenza:\n")
    T.append("| BTC alla scadenza | Variazione | Valore delle put | Guadagno o perdita | Sul capitale | Lo stesso controvalore short sul perp, senza stop |")
    T.append("|---|---|---|---|---|---|")
    pay = []
    be = atm - spent / qty
    for mv in (-0.30, -0.20, -0.10, be / fwd - 1, 0.0, 0.10, 0.20):
        s1 = fwd * (1 + mv)
        val = qty * max(0.0, atm - s1)
        val -= qty * min(EX_FEE * s1, FEE_CAP * max(0.0, atm - s1))
        perp = qty * (fwd - s1)
        pay.append((s1, val - spent, perp))
        sg = lambda v: ("+" if v > 0.5 else "−" if v < -0.5 else "") + usd(abs(v)) + " $"
        T.append(f"| {usd(s1)} $ | {'invariato' if mv == 0 else pct(mv, 0) if abs(round(mv * 100) - mv * 100) < 1e-6 else pct(mv, 1) + ' (pareggio)'} | {usd(val)} $ | {sg(val - spent)} | {pct((val - spent) / CAP)} | {sg(perp)} |")
    T.append(f"\nPareggio a scadenza: BTC a {usd(be)} $ ({pct(be / fwd - 1)}). Perdita massima: {usd(spent)} $ ({pct(-spent / CAP)} del capitale), qualunque cosa faccia BTC.")

    # ---------- grafico
    INK, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED,
                         "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF})
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 8.4), gridspec_kw={"height_ratios": [3, 2], "hspace": 0.32})
    ser = [("W3.2 originale", w, "#2a78d6"), ("Opzioni a 30 giorni, 10% del capitale", E[(30, 0.10, False)], "#eb6834"), ("Opzioni a 30 giorni, 5%", E[BASE], "#1baf7a"),
           ("Opzioni a 90 giorni, 10%", E[(90, 0.10, False)], "#6250d6")]
    ends = []
    for lab, e, col in ser:
        e = e.dropna() * 10000
        a1.plot(e.index, e, color=col, lw=1.8)
        ends.append((float(e.iloc[-1]), lab, col, e.index[-1]))
    yy = []
    for v, lab, col, last in sorted(ends):
        yv = v if not yy else max(v, yy[-1] * 1.3)
        yy.append(yv)
        a1.annotate(f"{lab} · {usd(v)} $", (last, v), xytext=(last + pd.Timedelta(days=40), yv), fontsize=9, color=INK, va="center", arrowprops=dict(arrowstyle="-", color=col, lw=1.0))
    a1.set_yscale("log")
    a1.set_yticks([10000, 20000, 50000, 100000, 200000])
    a1.set_yticklabels(["10k", "20k", "50k", "100k", "200k"])
    a1.minorticks_off()
    a1.grid(axis="y", color=GRID, lw=0.8)
    last = w.index[-1]
    a1.set_xlim(w.index[0], last + pd.Timedelta(days=900))
    a1.set_xticks([pd.Timestamp(f"{yr}-01-01") for yr in range(2020, last.year + 1)])
    a1.set_xticklabels([str(yr) for yr in range(2020, last.year + 1)])
    a1.set_title("W3.2 con opzioni comprate: 10.000 $ dal 2019 (scala logaritmica, prezzi delle opzioni da modello)", loc="left", color=INK, fontsize=12, fontweight="bold")
    xs = np.linspace(fwd * 0.7, fwd * 1.3, 200)
    opt = np.array([qty * max(0.0, atm - x) - spent for x in xs])
    a2.axhline(0, color=MUTED, lw=0.8)
    a2.plot(xs, opt, color="#eb6834", lw=2.0)
    a2.plot(xs, qty * (fwd - xs), color="#2a78d6", lw=1.6, ls=(0, (4, 3)))
    a2.annotate(f"Put comprate: perdita massima {usd(spent)} $", (xs[-1], opt[-1]), xytext=(-6, 10), textcoords="offset points", ha="right", fontsize=9, color=INK)
    a2.annotate("Short sul perp, stesso controvalore, senza stop", (xs[12], qty * (fwd - xs[12])), xytext=(10, 6), textcoords="offset points", ha="left", fontsize=9, color=INK)
    a2.axvline(fwd, color=GRID, lw=1.0)
    a2.annotate(f"BTC oggi {usd(fwd)} $", (fwd, a2.get_ylim()[1]), xytext=(4, -12), textcoords="offset points", fontsize=9, color=MUTED)
    a2.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: usd(v)))
    a2.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: ("+" if v > 0 else "−" if v < 0 else "") + usd(abs(v))))
    a2.grid(axis="y", color=GRID, lw=0.8)
    a2.set_xlabel("Prezzo di BTC alla scadenza ($)")
    a2.set_title(f"Esempio con i prezzi di oggi: guadagno o perdita a scadenza ($), {ncontr} put da 0,01 BTC", loc="left", color=INK, fontsize=12, fontweight="bold")
    fig.savefig(OUT / "opzioni_w32.png", dpi=160, bbox_inches="tight")

    pd.DataFrame({"W3.2 originale": w, "Opzioni 30 giorni, 5%": E[BASE], "Opzioni 30 giorni, 10%": E[(30, 0.10, False)],
                  "Opzioni 30 giorni, 10%, con rinnovo": E[(30, 0.10, True)], "Opzioni 90 giorni, 10%": E[(90, 0.10, False)]}).to_csv(OUT / "equity.csv")
    (OUT / "tables.md").write_text("\n".join(T) + "\n")
    print("\n".join(T))


if __name__ == "__main__":
    main()
