"""Confronto fra gli algoritmi di analisi tecnica (v1 voto, v2 tre schermi) e W3.2 del repo radar, con l'elenco di tutte le
operazioni. W3.2 = codice originale radar/weekly.py (vendor/radar_weekly_w32.py, rischio allo stop 25%), sui dati del radar:
2021+ dal frame aggiornato (data/btc/f_radar_live.csv.gz), 2018-20 dal frame lungo del radar (flusso stimato dal CVD spot)."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import btc_ta as B
import btc_v2 as V

ROOT = B.ROOT
OUT = ROOT / "results" / "w32"
OUT.mkdir(parents=True, exist_ok=True)
pct = lambda x, d=1: "n/d" if x is None or not np.isfinite(x) else f"{x * 100:+.{d}f}%".replace(".", ",")
usd = lambda x: f"{x:,.0f}".replace(",", ".")
num = lambda x, d=2: f"{x:.{d}f}".replace(".", ",")
REASON = {"trail": "trailing 2,5 ATR settimanali", "stop": "stop iniziale", "ema": "chiusura settimanale oltre la EMA 21",
          "dist": "distribuzione (funding e flusso)", "open": "aperta", None: "aperta",
          "seam": "chiusa a fine periodo (cambio di dati al 31/12/2020)"}


def radar():
    spec = importlib.util.spec_from_file_location("radar_weekly_w32", ROOT / "vendor" / "radar_weekly_w32.py")
    m = importlib.util.module_from_spec(spec)
    sys.modules["radar_weekly_w32"] = m
    spec.loader.exec_module(m)
    assert m.R_LONG == 0.25 and m.R_SHORT == 0.25, "il file vendor non e' W3.2"
    return m


def w32():
    """Equity giornaliera (base 1) e operazioni di W3.2: 2018-20 sul frame lungo, 2021+ sul frame aggiornato."""
    m = radar()
    rd = lambda n: pd.read_csv(ROOT / "data" / "btc" / n, index_col=0, parse_dates=True)
    fl, f = rd("f_long_radar.csv.gz"), rd("f_radar_live.csv.gz")
    ra = m.simulate(fl[fl.index <= "2020-12-31"], start="2018-01-01")
    rb = m.simulate(f, start="2021-01-01")
    ea, eb = ra["equity"] / ra["equity"].iloc[0], rb["equity"] / rb["equity"].iloc[0]
    eq = pd.concat([ea, eb * ea.iloc[-1]])
    rows = []
    for per, r in (("2018–20", ra), ("2021+", rb)):
        seam = per == "2018–20"                               # la posizione aperta al 31/12/2020 si chiude li' per la contabilita'
        for t in r["trades"] + ([dict(r["open"], pnl=r["open"]["pnl_close"], exit="2020-12-31" if seam else None, exit_px=r["open"]["last"],
                                      reason="seam" if seam else "open")] if r["open"] else []):
            rows.append({"periodo": per, "verso": t["side"], "segnale": t["signal"], "entra": t["entry"], "esce": t.get("exit"), "prezzo_in": t["entry_px"],
                         "prezzo_out": t.get("exit_px"), "esposizione": t["expo"], "mossa": t["move"], "sul_capitale": t["pnl"],
                         "uscita": REASON.get(t.get("reason"), t.get("reason")), "mercato": t["market"]})
    tr = pd.DataFrame(rows)
    expo = pd.Series(0.0, eq.index)
    for t in tr.itertuples():
        expo.loc[t.entra:(t.esce if isinstance(t.esce, str) else eq.index[-1])] = t.esposizione * (1 if t.verso == "long" else -1)
    return eq, tr, expo, (ra, rb)


def st(e: pd.Series, a=None, b=None) -> dict:
    e = e.loc[a:b]
    e = e / e.iloc[0]
    yrs = (e.index[-1] - e.index[0]).days / 365.25
    x = e.pct_change().dropna()
    yr = e.groupby(e.index.year).last()
    return {"final": float(e.iloc[-1]), "cagr": float(e.iloc[-1] ** (1 / yrs) - 1), "dd": float((e / e.cummax() - 1).min()),
            "sharpe": float(x.mean() / x.std() * np.sqrt(365)), "years": (yr / yr.shift(1).fillna(1.0) - 1).to_dict()}


if __name__ == "__main__":
    T = []
    d = B.load()
    c = d["close"]
    sig = B.signals(d)
    sc = B.score(sig)
    pos1 = B.composite(d, sc, 0.5, 0.9, 0.25, False)
    f2 = V.features(d)
    pos2, log2 = V.run(d, f2, mode="rottura", k_atr=5.0, rsi_pb=45.0, regime_exit=False, short_mode="severa")
    r1, r2 = B.run(d, pos1), B.run(d, pos2)
    eqw, trw, expo, raw = w32()
    END = min(eqw.index[-1], r1["equity"].index[-1])
    E = {"W3.2 radar (rischio 25%)": eqw.loc[:END], "v1 · voto di 17 indicatori": (r1["equity"] / r1["equity"].iloc[0]).loc[:END],
         "v2 · tre schermi": (r2["equity"] / r2["equity"].iloc[0]).loc[:END], "BTC comprato e tenuto": (c.loc["2018-01-01":END] / c.loc["2018-01-01"])}
    rw, rv1, rv2 = E["W3.2 radar (rischio 25%)"].pct_change().fillna(0), E["v1 · voto di 17 indicatori"].pct_change().fillna(0), E["v2 · tre schermi"].pct_change().fillna(0)
    E["50% W3.2 + 50% v1"] = (1 + 0.5 * rw + 0.5 * rv1).cumprod()
    E["1/3 W3.2 + 1/3 v1 + 1/3 v2"] = (1 + (rw + rv1 + rv2) / 3).cumprod()
    pd.DataFrame(E).mul(10000).round(2).to_csv(OUT / "equity.csv", index_label="date")

    def ntr(name, a, b):
        if name.startswith("W3.2"):
            x = trw[(trw.entra >= a) & (trw.entra <= b)]
            return len(x), float((x.sul_capitale > 0).mean()) if len(x) else np.nan
        if name.startswith("v1") or name.startswith("v2"):
            t = (r1 if name.startswith("v1") else r2)["trades"]
            x = t[(t.da >= a) & (t.da <= b)]
            return len(x), float((x.ret > 0).mean()) if len(x) else np.nan
        return None, np.nan

    T.append("## W1 confronto\n")
    PER = (("2018–2026", "2018-01-01", None), ("2018–20", "2018-01-01", "2020-12-31"), ("2021–23", "2021-01-01", "2023-12-31"), ("2024–26", "2024-01-01", None), ("Dal 2021", "2021-01-01", None))
    T.append("| Strategia | 10.000 $ → (2018–2026) | CAGR | Max DD | Sharpe | Operazioni | Vincenti | 2018–20: CAGR / DD | 2021–23: CAGR / DD | 2024–26: CAGR / DD | Dal 2021: CAGR / DD |")
    T.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for k, e in E.items():
        s = {p: st(e, a, b) for p, a, b in PER}
        n, wr = ntr(k, "2018-01-01", str(END.date()))
        T.append(f"| {k} | {usd(10000 * s['2018–2026']['final'])} | {pct(s['2018–2026']['cagr'])} | {pct(s['2018–2026']['dd'])} | {num(s['2018–2026']['sharpe'])} | {n if n else '–'} | "
                 f"{f'{wr * 100:.0f}%' if n else '–'} | " + " | ".join(f"{pct(s[p]['cagr'], 0)} / {pct(s[p]['dd'], 0)}" for p in ("2018–20", "2021–23", "2024–26", "Dal 2021")) + " |")
    T.append("\n## W2 anni\n")
    ys = list(range(2018, 2027))
    T.append("| | " + " | ".join(map(str, ys)) + " |")
    T.append("|---|" + "---|" * len(ys))
    for k, e in E.items():
        y = st(e)["years"]
        T.append(f"| {k} | " + " | ".join(pct(y.get(v), 0) for v in ys) + " |")

    # accordo delle posizioni
    T.append("\n## W3 accordo\n")
    p1, p2, pw = np.sign(pos1.loc["2018-01-01":END]), np.sign(pos2.loc["2018-01-01":END]), np.sign(expo.loc["2018-01-01":END])
    T.append("| Posizione di W3.2 | Giorni | v1 long | v1 fuori | v1 short | v2 long | v2 fuori |")
    T.append("|---|---|---|---|---|---|---|")
    for val, lab in ((1, "long"), (0, "fuori"), (-1, "short")):
        m = pw == val
        T.append(f"| {lab} | {int(m.sum())} | " + " | ".join(f"{(p1[m] == v).mean() * 100:.0f}%" for v in (1, 0, -1)) + " | " + " | ".join(f"{(p2[m] == v).mean() * 100:.0f}%" for v in (1, 0)) + " |")
    mm = pd.DataFrame({"w": rw, "v1": rv1, "v2": rv2}).resample("ME").apply(lambda x: (1 + x).prod() - 1).corr()
    T.append(f"\nStessa posizione di W3.2: v1 nel {(p1 == pw).mean() * 100:.0f}% dei giorni, v2 nel {(p2 == pw).mean() * 100:.0f}%. Posizioni opposte (uno long e l'altro short): "
             f"v1 nel {num(((p1 * pw) < 0).mean() * 100, 1)}% dei giorni." + f" Correlazione dei rendimenti mensili con W3.2: v1 {num(mm.loc['w', 'v1'])}, v2 {num(mm.loc['w', 'v2'])}.")

    # movimentazioni
    def at(pos, day):
        v = pos.reindex([pd.Timestamp(day)]).iloc[0] if pd.Timestamp(day) in pos.index else 0
        return "long" if v > 0 else "short" if v < 0 else "fuori"
    T.append("\n## W4 movimenti w32\n")
    T.append("| # | Periodo | Verso | Mercato | Segnale | Entra | Esce | Prezzo | Esposizione | Mossa del prezzo | Sul capitale | Uscita | v1 all'ingresso | v2 all'ingresso |")
    T.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for i, t in enumerate(trw.itertuples(), 1):
        T.append(f"| {i} | {t.periodo} | {t.verso} | {t.mercato} | {t.segnale} | {t.entra} | {t.esce if isinstance(t.esce, str) else 'aperta'} | {usd(t.prezzo_in)} → {usd(t.prezzo_out)} | {num(t.esposizione)}x | "
                 f"{pct(t.mossa)} | {pct(t.sul_capitale)} | {t.uscita} | {at(pos1, t.entra)} | {at(pos2, t.entra)} |")
    for per in ("2018–20", "2021+"):
        x = trw[trw.periodo == per]
        T.append(f"\n{per}: {len(x)} operazioni, {(x.sul_capitale > 0).mean() * 100:.0f}% in guadagno, media {pct(x.sul_capitale.mean())} sul capitale, peggiore {pct(x.sul_capitale.min())}.")
    trw.to_csv(OUT / "movimenti_w32.csv", index=False)

    T.append("\n## W5 movimenti v1\n")
    T.append("| # | Verso | Entra | Esce | Giorni | Prezzo | Risultato | Voto all'ingresso | W3.2 all'ingresso |")
    T.append("|---|---|---|---|---|---|---|---|---|")
    t1 = r1["trades"]
    rows1 = []
    for i, q in enumerate(t1.itertuples(), 1):
        d0 = q.da - pd.Timedelta(days=1)                       # giorno della decisione
        pin, pout = c.loc[d0], c.loc[q.a]
        opened = q.a >= d.index[-1] and pos1.iloc[-1] != 0
        rows1.append({"verso": "long" if q.verso > 0 else "short", "entra": q.da.date(), "esce": None if opened else q.a.date(), "giorni": q.giorni, "prezzo_in": pin,
                      "prezzo_out": pout, "risultato": q.ret, "voto": sc.loc[d0]})
        T.append(f"| {i} | {'long' if q.verso > 0 else 'short'} | {q.da.date()} | {'aperta' if opened else q.a.date()} | {q.giorni} | {usd(pin)} → {usd(pout)} | {pct(q.ret)} | "
                 f"{num(sc.loc[d0])} | {at(expo, q.da)} |")
    pd.DataFrame(rows1).to_csv(OUT / "movimenti_v1.csv", index=False)
    T.append(f"\n{len(t1)} operazioni, {(t1.ret > 0).mean() * 100:.0f}% in guadagno, media {pct(t1.ret.mean())}, peggiore {pct(t1.ret.min())}.")

    T.append("\n## W6 movimenti v2\n")
    T.append("| # | Verso | Entra | Esce | Prezzo | Mossa del prezzo | W3.2 all'ingresso |")
    T.append("|---|---|---|---|---|---|---|")
    for i, q in enumerate(log2.itertuples(), 1):
        T.append(f"| {i} | {q.verso} | {q.entra.date()} | {q.esce.date() if pd.notna(q.esce) else 'aperta'} | {usd(q.prezzo_in)} → {usd(q.prezzo_out)} | {pct(q.mossa)} | {at(expo, q.entra)} |")
    log2.to_csv(OUT / "movimenti_v2.csv", index=False)

    T.append("\n## W7 oggi\n")
    o = raw[1]["open"]
    T.append("| | Posizione oggi | Dettaglio |")
    T.append("|---|---|---|")
    if o:
        T.append(f"| W3.2 radar | **{o['side']}** dal {o['entry']} | ingresso {usd(o['entry_px'])} $, esposizione {num(o['expo'])}x, ultimo prezzo {usd(o['last'])} $, {pct(o['pnl'])} sul capitale, "
                 f"trailing a {usd(o['trail'])} $ |")
    else:
        T.append("| W3.2 radar | **fuori** | |")
    T.append(f"| v1 · voto | **{at(pos1, pos1.index[-1])}** | voto {num(sc.iloc[-1])}: short a −0,90, long a +0,50 |")
    T.append(f"| v2 · tre schermi | **{at(pos2, pos2.index[-1])}** | marea neutra: prezzo sotto la media a 40 settimane, struttura non ancora ribassista |")
    (OUT / "tables.md").write_text("\n".join(T) + "\n")
    print("\n".join(T))

    INK, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED,
                         "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": SURF,
                         "axes.facecolor": SURF, "savefig.facecolor": SURF})
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 7.6), sharex=True, gridspec_kw={"height_ratios": [3, 2], "hspace": 0.12})
    sel = [("W3.2 radar (rischio 25%)", "W3.2 radar", "#2a78d6"), ("v1 · voto di 17 indicatori", "v1 · voto", "#eb6834"), ("v2 · tre schermi", "v2 · tre schermi", "#eda100"),
           ("50% W3.2 + 50% v1", "50% W3.2 + 50% v1", "#6250d6"), ("BTC comprato e tenuto", "BTC tenuto", "#1baf7a")]
    ends = []
    for k, lab, col in sel:
        e = E[k] * 10000
        a1.plot(e.index, e, color=col, lw=2, label=lab)
        a2.plot(e.index, (e / e.cummax() - 1) * 100, color=col, lw=1.3)
        ends.append((float(e.iloc[-1]), lab, col))
    yy = []
    for v, lab, col in sorted(ends):
        y = v if not yy else max(v, yy[-1] * 1.36)
        yy.append(y)
        a1.annotate(f"{lab} · {usd(v)} $", (e.index[-1], v), xytext=(e.index[-1] + pd.Timedelta(days=40), y), fontsize=9, color=INK, va="center",
                    arrowprops=dict(arrowstyle="-", color=col, lw=1.0))
    a1.axvline(pd.Timestamp("2021-01-01"), color=MUTED, lw=1, ls=(0, (4, 3)))
    a1.set_yscale("log")
    a1.set_ylim(top=520000)
    a1.set_yticks([5000, 10000, 20000, 50000, 100000, 200000])
    a1.set_yticklabels(["5k", "10k", "20k", "50k", "100k", "200k"])
    a1.minorticks_off()
    a1.grid(axis="y", color=GRID, lw=0.8)
    a1.legend(frameon=False, loc="lower right", fontsize=9, bbox_to_anchor=(0.76, 0.02))
    a1.set_title("10.000 $ dal 01/2018: prima della linea W3.2 usa un flusso stimato, dopo i dati reali del perp", loc="left", color=INK, fontsize=11, fontweight="bold")
    a2.grid(axis="y", color=GRID, lw=0.8)
    a2.set_title("Drawdown dal massimo (%)", loc="left", color=INK, fontsize=11, fontweight="bold")
    a2.set_xlim(e.index[0], e.index[-1] + pd.Timedelta(days=820))
    a2.set_xticks([pd.Timestamp(f"{y}-01-01") for y in range(2018, 2027)])
    a2.set_xticklabels([str(y) for y in range(2018, 2027)])
    fig.savefig(OUT / "confronto_w32.png", dpi=160, bbox_inches="tight")
