"""Il prezzo di BTC segue le liquidazioni? Replica indipendente con la mappa stimata del radar (vendor/radar_liqmap.py).

Ogni giorno alle 00:00 UTC si costruisce la mappa delle liquidazioni stimate dall'open interest orario di Binance USDT-M
(posizioni nuove = aumento di OI, meta' long e meta' short, leve 10/25/50/100x), con due memorie: 21 giorni (come il radar) e
90 giorni (piu' vicina alle mappe a lungo raggio tipo Coinglass). Poi si misura cosa fa il prezzo dopo. Nessun dato futuro:
la mappa del giorno usa solo le ore precedenti."""
from __future__ import annotations

import importlib.util
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("radar_liqmap", ROOT / "vendor" / "radar_liqmap.py")
LM = importlib.util.module_from_spec(spec)
spec.loader.exec_module(LM)
OUT = ROOT / "results" / "liq"
SPLIT = "2024-01-01"
pct = lambda x, d=1: "n/d" if x is None or not np.isfinite(x) else f"{x * 100:+.{d}f}%".replace(".", ",")
num = lambda x, d=2: f"{x:.{d}f}".replace(".", ",")


def hourly() -> pd.DataFrame:
    k = pd.read_csv(ROOT / "data" / "liq" / "BTCUSDT_1h.csv.gz")
    k["t"] = pd.to_datetime(k["ts"]).dt.tz_localize(None)
    k = k.set_index("t")[["high", "low", "close"]].astype(float)
    m = pd.read_csv(ROOT / "data" / "liq" / "BTCUSDT_metrics_1h.csv.gz")
    m["t"] = pd.to_datetime(m["ts"]).dt.tz_localize(None)
    k["oi_usd"] = m.set_index("t")["oi_value"].reindex(k.index).ffill(limit=3)
    return k.dropna()


def daily_maps(h: pd.DataFrame, look_days: int) -> pd.DataFrame:
    cache = OUT / f"mappe_{look_days}g.csv"
    if cache.exists():
        return pd.read_csv(cache, index_col=0, parse_dates=True)
    rows = []
    for d in pd.date_range(h.index[0].normalize() + pd.Timedelta(days=look_days + 1), h.index[-1].normalize(), freq="D"):
        win = h[(h.index >= d - pd.Timedelta(days=look_days)) & (h.index < d)]
        if len(win) < look_days * 20:
            continue
        p = float(win["close"].iloc[-1])
        w = LM.window(LM.build(win), p, 0.15)
        up, dn = LM.clusters(w, p, "short", rng=0.10), LM.clusters(w, p, "long", rng=0.10)
        bu = max(up, key=lambda c: c["usd"]) if up else None
        bd = max(dn, key=lambda c: c["usd"]) if dn else None
        i5, i15 = LM.imbalance(w, p, 0.05), LM.imbalance(w, p, 0.15)
        rows.append({"date": d, "price": p, "imb5": i5["pct"] / 100, "imb15": i15["pct"] / 100, "short15": i15["short_above"], "long15": i15["long_below"],
                     "up_dist": bu["dist_pct"] / 100 if bu else np.nan, "up_usd": bu["usd"] if bu else np.nan,
                     "dn_dist": -bd["dist_pct"] / 100 if bd else np.nan, "dn_usd": bd["usd"] if bd else np.nan})
    z = pd.DataFrame(rows).set_index("date")
    z.to_csv(cache)
    return z


def main():
    h = hourly()
    T = []
    T.append("## L0 dati\n")
    T.append(f"Dati orari Binance USDT-M dal {h.index[0].date()} al {h.index[-1].date()} ({len(h)} ore con open interest).")
    c = h["close"].resample("1D").last()
    hi, lo = h["high"].resample("1D").max(), h["low"].resample("1D").min()
    for look in (21, 90):
        z = daily_maps(h, look)
        z = z[z.index <= c.index[-1]]
        # allineamento: la mappa del giorno D e' delle 00:00, con prezzo p = ultima chiusura oraria di D-1. Tutto si misura da p:
        # "a n giorni" = chiusura del giorno D+n-1; massimi e minimi futuri = giorni da D a D+n-1; passato = fino alla chiusura di D-1.
        p0 = z["price"]
        cz = lambda k: c.shift(k).reindex(z.index)
        fw = {n: cz(-(n - 1)) / p0 - 1 for n in (1, 3, 7, 14)}
        past = {n: cz(1) / cz(1 + n) - 1 for n in (1, 7, 30)}
        fmax = {n: pd.concat([hi.shift(-k) for k in range(n)], axis=1).max(axis=1, skipna=False).reindex(z.index) / p0 - 1 for n in (1, 3, 7)}
        fmin = {n: pd.concat([lo.shift(-k) for k in range(n)], axis=1).min(axis=1, skipna=False).reindex(z.index) / p0 - 1 for n in (1, 3, 7)}
        sma200 = c.rolling(200).mean().shift(1).reindex(z.index)
        per = [("2022–23", z.index < SPLIT), ("2024–26", z.index >= SPLIT)]

        # ---------------- T1: la mappa descrive il passato?
        T.append(f"\n## L{1 if look == 21 else 6} passato {look}\n")
        T.append(f"Mappa con memoria di {look} giorni, {len(z)} giorni dal {z.index[0].date()}. Correlazione fra lo squilibrio (short sopra − long sotto, entro ±15%) e il rendimento "
                 f"passato del prezzo: a 1 giorno {num(z.imb15.corr(past[1]))}, a 7 giorni {num(z.imb15.corr(past[7]))}, a 30 giorni {num(z.imb15.corr(past[30]))}. "
                 f"Correlazione con il rendimento dei 7 giorni successivi: {num(z.imb15.corr(fw[7]))}.")

        # ---------------- T2: direzione
        T.append(f"\n## L{2 if look == 21 else 7} direzione {look}\n")
        T.append("| Squilibrio entro ±15% | Giorni | Rendimento medio a 1 giorno | a 3 giorni | a 7 giorni | a 14 giorni | Positivi a 7 giorni | 7 giorni, 2022–23 | 7 giorni, 2024–26 |")
        T.append("|---|---|---|---|---|---|---|---|---|")
        groups = (("Short sopra dominanti (oltre +30%)", z.imb15 > 0.30), ("Equilibrio (fra −30% e +30%)", z.imb15.abs() <= 0.30), ("Long sotto dominanti (sotto −30%)", z.imb15 < -0.30),
                  ("Short sopra oltre +60%", z.imb15 > 0.60), ("Long sotto oltre −60%", z.imb15 < -0.60), ("*Tutti i giorni*", z.imb15.notna()))
        for lab, m in groups:
            T.append(f"| {lab} | {int(m.sum())} | " + " | ".join(pct(fw[n][m].mean(), 2) for n in (1, 3, 7, 14)) + f" | {(fw[7][m] > 0).mean() * 100:.0f}% | " +
                     " | ".join(pct(fw[7][m & pm].mean(), 2) for _, pm in per) + " |")
        # controllo sul momentum: squilibrio a parita' di rendimento passato
        resid = fw[7] - np.polyval(np.polyfit(past[7].fillna(0), fw[7].fillna(0), 1), past[7].fillna(0))
        T.append(f"\nTolto l'effetto del rendimento dei 7 giorni precedenti, la correlazione fra squilibrio e rendimento a 7 giorni è {num(z.imb15.corr(resid))}. "
                 f"Nei giorni in cui lo squilibrio è opposto al movimento dei 7 giorni precedenti ({int(((np.sign(z.imb15) != np.sign(past[7])) & (z.imb15.abs() > 0.3)).sum())} casi con squilibrio oltre 30%), "
                 f"il prezzo a 7 giorni va nel verso dello squilibrio nel {(np.sign(fw[7]) == np.sign(z.imb15))[(np.sign(z.imb15) != np.sign(past[7])) & (z.imb15.abs() > 0.3)].mean() * 100:.0f}% dei casi.")

        # ---------------- T3: calamita
        T.append(f"\n## L{3 if look == 21 else 8} calamita {look}\n")
        T.append("| Livello | Orizzonte | Giorni | Raggiunto | Atteso a pari distanza | Differenza | Differenza 2022–23 | Differenza 2024–26 |")
        T.append("|---|---|---|---|---|---|---|---|")
        for side, dist, ext in (("Fascia più grande di short sopra (entro 10%)", z.up_dist, fmax), ("Fascia più grande di long sotto (entro 10%)", z.dn_dist, fmin)):
            for n in (1, 3, 7):
                ok = dist.notna() & ext[n].notna()
                reach = (ext[n] >= dist) if "short" in side else (-ext[n] >= dist)
                # atteso: frequenza con cui, in TUTTI i giorni, il prezzo percorre almeno quella distanza in quella direzione nello stesso orizzonte
                allmove = (ext[n] if "short" in side else -ext[n]).dropna().to_numpy()
                exp = dist[ok].apply(lambda dd: float((allmove >= dd).mean()))
                df = float(reach[ok].mean() - exp.mean())
                dper = [float(reach[ok & pm].mean() - exp[pm[ok]].mean()) if (ok & pm).sum() > 20 else np.nan for _, pm in per]
                T.append(f"| {side} | {n} g | {int(ok.sum())} | {reach[ok].mean() * 100:.1f}% | {exp.mean() * 100:.1f}% | {df * 100:+.1f} punti | {dper[0] * 100:+.1f} | {dper[1] * 100:+.1f} |".replace(".", ","))
        T.append(f"\nDistanza mediana della fascia più grande: sopra {pct(z.up_dist.median())}, sotto {pct(-z.dn_dist.median())}.")

        # ---------------- T4: lato piu' pesante toccato per primo
        T.append(f"\n## L{4 if look == 21 else 9} primo {look}\n")
        ok = z.up_dist.notna() & z.dn_dist.notna()
        heavy_up = z.up_usd > z.dn_usd
        rows4 = []
        for n in (1, 3, 7):
            hu = fmax[n] >= z.up_dist
            hd = -fmin[n] >= z.dn_dist
            only_up, only_dn = hu & ~hd, hd & ~hu
            dec = ok & (only_up | only_dn)
            hit = (heavy_up & only_up) | (~heavy_up & only_dn)
            near = (z.up_dist < z.dn_dist)                      # riferimento banale: il lato piu' vicino
            hit_near = (near & only_up) | (~near & only_dn)
            both = heavy_up == near                              # la fascia piu' grande e' anche la piu' vicina
            rows4.append(f"| {n} g | {int(dec.sum())} | {hit[dec].mean() * 100:.0f}% | {hit_near[dec].mean() * 100:.0f}% | {int((dec & ~both).sum())} | "
                         f"{hit[dec & ~both].mean() * 100:.0f}% |")
        T.append("| Orizzonte | Giorni in cui il prezzo tocca una sola delle due fasce | Tocca la fascia più grande | Tocca la fascia più vicina | Giorni in cui la più grande NON è la più vicina | In quei giorni tocca la più grande |")
        T.append("|---|---|---|---|---|---|")
        T += rows4

        # ---------------- T5: situazione di oggi (short sopra dominanti dopo un forte calo)
        T.append(f"\n## L{5 if look == 21 else 10} oggi {look}\n")
        an = (z.imb15 > 0.5) & (past[30] < -0.15)
        an2 = (z.imb15 > 0.5) & (p0 < sma200)
        T.append("| Situazione simile a oggi | Giorni | Episodi distinti | Rendimento medio a 7 giorni | a 14 giorni | Positivi a 14 giorni | Riferimento: tutti i giorni a 14 giorni |")
        T.append("|---|---|---|---|---|---|---|")
        for lab, m in (("Short sopra oltre +50% e prezzo sceso di oltre il 15% in 30 giorni", an), ("Short sopra oltre +50% e prezzo sotto la SMA 200", an2)):
            ep = int((m & ~m.shift(1, fill_value=False)).sum())
            T.append(f"| {lab} | {int(m.sum())} | {ep} | {pct(fw[7][m].mean())} | {pct(fw[14][m].mean())} | {(fw[14][m] > 0).mean() * 100:.0f}% | {pct(fw[14].mean())} |")
        us = lambda v: f"{v:,.0f}".replace(",", ".")
        T.append(f"\nUltima mappa ({z.index[-1].date()}, prezzo {us(z.price.iloc[-1])} $): squilibrio entro ±15% {pct(z.imb15.iloc[-1], 0)}, short sopra {us(z.short15.iloc[-1] / 1e6)} M$, "
                 f"long sotto {us(z.long15.iloc[-1] / 1e6)} M$ (solo Binance USDT-M, stima).")
    (OUT / "tables.md").write_text("\n".join(T) + "\n")
    print("\n".join(T))


if __name__ == "__main__":
    main()
