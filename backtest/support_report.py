"""Tabelle dello studio sul supporto: probabilita' di base, per numero di tocchi, per regime di BTC, confronto delle uscite,
placebo, TAO e leva. Scrive results/tao/tables.md."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import support_study as S
from fetch_alts import ALTS

OUT = S.ROOT / "results" / "tao"
CUT = "2025-11-01"          # eventi con almeno un anno di dati dopo l'ingresso
pct = lambda x, d=0: "n/d" if x is None or not np.isfinite(x) else f"{x * 100:+.{d}f}%".replace(".", ",")
p0 = lambda x: f"{x * 100:.0f}%"
T = []

syms = sorted(set(ALTS))
data = {}
for s in syms:
    try:
        d = S.load(s)
        if len(d) >= 400:
            data[s] = d
    except FileNotFoundError:
        pass
df = S.run(list(data))
df.drop(columns=["i"]).to_csv(OUT / "eventi_alt.csv", index=False)
btc = pd.read_csv(S.ROOT / "data" / "crypto" / "BTC_spot.csv", parse_dates=[0], index_col=0)["close"]
reg = (btc > btc.rolling(200).mean()).reindex(pd.date_range(btc.index[0], "2026-11-30")).ffill()
df["btc_up"] = reg.reindex(df.t).to_numpy()
full = df[df.t < CUT].copy()
others = full[full.sym != "TAO"]


def reach(x, m):
    """Quota di eventi in cui il massimo prima dello stop ha raggiunto +m."""
    return float((x.mfe >= m).mean())


def base_row(name, x):
    return (f"| {name} | {len(x)} | {x.sym.nunique()} | {p0(reach(x, .3))} | {p0(reach(x, .5))} | {p0(reach(x, 1.0))} | {p0(reach(x, 2.0))} | "
            f"{p0(x.stopped.mean())} | {p0((x.mfe < .3).mean())} | {pct(x.mfe.median())} | {pct(x.mae.median())} |")


T.append("## S1 base\n")
T.append("| Gruppo | Eventi | Monete | Arriva a +30% | a +50% | a +100% | a +200% | Stop entro 2 anni | Mai +30% | Massimo mediano | Calo mediano prima |")
T.append("|---|---|---|---|---|---|---|---|---|---|---|")
T.append(base_row("Tutte le alt, 2019–10/2025", full))
T.append(base_row("2019–2022", full[full.t < "2023-01-01"]))
T.append(base_row("2023–10/2025", full[full.t >= "2023-01-01"]))
T.append(base_row("BTC sopra la media a 200 giorni", full[full.btc_up == True]))
T.append(base_row("BTC sotto la media a 200 giorni", full[full.btc_up == False]))
for k, lab in ((2, "2° tocco"), (3, "3° tocco"), (4, "4° tocco")):
    T.append(base_row(lab, full[full.touch == k]))
T.append(base_row("5° tocco o oltre", full[full.touch >= 5]))
T.append(base_row("TAO (Bitget, tutti gli eventi)", df[df.sym == "TAO"]))

# ---------------------------------------------------------------- placebo: stessa moneta, giorno a caso, stesso stop e stessa uscita
rng = np.random.default_rng(11)
pl = []
for s, g in full.groupby("sym"):
    d = data[s]
    H, C = d["high"].to_numpy(), d["close"].to_numpy()
    lo, hi = d.index.searchsorted(pd.Timestamp("2019-06-01")), d.index.searchsorted(pd.Timestamp(CUT))
    lo = max(lo, 300)
    if hi - lo < 50:
        continue
    for _, e in g.iterrows():
        dist = e.stop / e.entry
        for _ in range(20):
            i = int(rng.integers(lo, hi))
            entry, stop = C[i], C[i] * dist
            c = C[i:i + S.HORIZON]
            si = int(np.argmax(c < stop)) if (c < stop).any() else len(c)
            mfe = H[i + 1:i + 1 + si].max() / entry - 1 if si > 0 and i + 1 < len(H) else 0.0
            pl.append((mfe, si < len(c)))
pl = pd.DataFrame(pl, columns=["mfe", "stopped"])
T.append(f"| Ingressi casuali, stesse monete e stesso stop | {len(pl)} | {full.sym.nunique()} | {p0((pl.mfe >= .3).mean())} | {p0((pl.mfe >= .5).mean())} | "
         f"{p0((pl.mfe >= 1).mean())} | {p0((pl.mfe >= 2).mean())} | {p0(pl.stopped.mean())} | {p0((pl.mfe < .3).mean())} | {pct(pl.mfe.median())} | – |")

# ---------------------------------------------------------------- uscite
def exits_table(x, title):
    T.append(f"\n{title}\n")
    T.append("| Regola di vendita | Rendimento medio | Mediano | Vincenti | Peggiore | Giorni medi | Rendimento medio per 100 giorni | Media 2019–22 | Media 2023–25 |")
    T.append("|---|---|---|---|---|---|---|---|---|")
    rows = []
    for k in S.EXITS:
        r, dd = x[f"r|{k}"], x[f"d|{k}"].clip(lower=1)
        a, b = x[x.t < "2023-01-01"][f"r|{k}"], x[x.t >= "2023-01-01"][f"r|{k}"]
        rows.append((k, r.mean(), r.median(), (r > 0).mean(), r.min(), dd.mean(), r.sum() / dd.sum() * 100, a.mean(), b.mean()))
    for k, m, md, w, mn, dd, eff, a, b in sorted(rows, key=lambda z: -z[6]):
        T.append(f"| {k} | {pct(m, 1)} | {pct(md, 1)} | {p0(w)} | {pct(mn)} | {dd:.0f} | {pct(eff, 1)} | {pct(a, 1)} | {pct(b, 1)} |")
    return pd.DataFrame(rows, columns=["regola", "media", "mediana", "wr", "peggiore", "giorni", "per100g", "media_19_22", "media_23_25"])


T.append("\n## S2 uscite")
ex_all = exits_table(full, "**Tutte le alt, eventi 2019–10/2025** (ordinate per rendimento per 100 giorni di capitale impegnato)")
ex_all.to_csv(OUT / "uscite_alt.csv", index=False)
T.append("\n## S3 uscite tocchi")
exits_table(full[full.touch >= 3], "**Solo dal 3° tocco in poi** (la situazione di TAO oggi)")
T.append("\n## S4 uscite TAO")
tao = df[(df.sym == "TAO") & (df.t < "2026-10-01")]
T.append("| Ingresso | Prezzo | Stop | Tocco | Massimo dopo | " + " | ".join(["+50%", "+100%", "70% max prec.", "trailing 25%", "metà +50% / metà trailing", "terzi +30/+60/+100"]) + " |")
T.append("|---|---|---|---|---|---|---|---|---|---|---|")
cols = ["target +50%", "target +100%", "70% del massimo precedente", "trailing 25% (dal +30%)", "meta' a +50%, meta' trailing 30%", "terzi a +30/+60/+100%"]
for _, e in tao.iterrows():
    T.append(f"| {e.t.date()} | {e.entry:.0f} | {e.stop:.0f} | {e.touch} | {pct(e.mfe)} | " + " | ".join(pct(e[f'r|{c}']) for c in cols) + " |")
T.append(f"| **Media** | | | | {pct(tao.mfe.mean())} | " + " | ".join(pct(tao[f'r|{c}'].mean()) for c in cols) + " |")

# ---------------------------------------------------------------- rimbalzi decrescenti: il massimo del rimbalzo rispetto al precedente
T.append("\n## S5 rimbalzi\n")
rb = []
for s, g in full.groupby("sym"):
    g = g.sort_values("t")
    pk = (g.entry * (1 + g.mfe)).to_numpy()
    for a, b, tch in zip(pk[:-1], pk[1:], g.touch.to_numpy()[1:]):
        rb.append((b / a, tch))
rb = pd.DataFrame(rb, columns=["ratio", "touch"])
T.append(f"Su {len(rb)} coppie di visite consecutive alla stessa moneta, il massimo del rimbalzo successivo è stato in mediana il "
         f"{rb.ratio.median() * 100:.0f}% del massimo precedente; nel {p0((rb.ratio < 1).mean())} dei casi è stato più basso, "
         f"nel {p0((rb.ratio < 0.7).mean())} sotto il 70%.")

# ---------------------------------------------------------------- leva su TAO (perp Bitget)
T.append("\n## S6 leva\n")
pp = pd.read_csv(S.ROOT / "data" / "tao" / "bitget_TAOUSDT_perp_1d.csv", parse_dates=["ts"]).set_index("ts")
fr = pd.read_csv(S.ROOT / "data" / "tao" / "bitget_TAOUSDT_funding.csv")
fund_y = fr.rate.mean() * 6 * 365
T.append(f"Funding medio del perp TAO su Bitget negli ultimi {len(fr) // 6} giorni: {pct(fund_y, 1)} annuo pagato dai long (storico più lungo non disponibile dall'API).\n")
T.append("| Leva (margine isolato) | Liquidazione a circa | Stop a 126 $ da ingresso 170 $ | Perdita allo stop sul margine | Guadagno a +50% sul margine | A +100% | Regge un calo del 26% (stop)? |")
T.append("|---|---|---|---|---|---|---|")
for lev in (1, 2, 3, 5, 10):
    liq = -(1 / lev) + 0.01 if lev > 1 else -1.0
    sd = 126 / 170 - 1
    T.append(f"| {lev}x | {pct(liq)} | {pct(sd)} | {pct(max(sd * lev, -1))} | {pct(.5 * lev)} | {pct(1.0 * lev)} | {'sì' if liq < sd - 0.03 else 'no: liquidato prima dello stop'} |")
T.append("\nCrollo lampo del 10/10/2025 sul perp Bitget: da " + f"{pp.loc['2025-10-10', 'open']:.0f} a {pp.loc['2025-10-10', 'low']:.0f} $ in giornata "
         f"({pct(pp.loc['2025-10-10', 'low'] / pp.loc['2025-10-10', 'open'] - 1)}), chiusura {pp.loc['2025-10-10', 'close']:.0f} $.")
T.append("\n| Ingresso long sul perp | Prezzo | Minimo toccato dopo (prima di +50%) | Calo massimo | Liquidato a 2x? | a 3x? | a 5x? |")
T.append("|---|---|---|---|---|---|---|")
for _, e in df[(df.sym == "TAO") & (df.t >= "2024-05-01")].iterrows():
    seg = pp.loc[e.t:]
    hit = seg[seg.high >= e.entry * 1.5]
    seg = seg.loc[:hit.index[0]] if len(hit) else seg
    mae = seg.low.min() / e.entry - 1
    T.append(f"| {e.t.date()} | {e.entry:.0f} | {seg.low.min():.0f} | {pct(mae)} | " + " | ".join("sì" if mae <= -(1 / l) + 0.01 else "no" for l in (2, 3, 5)) + " |")
(OUT / "tables.md").write_text("\n".join(T) + "\n")
print("\n".join(T))
