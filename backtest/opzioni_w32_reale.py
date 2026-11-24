"""W3.2 con opzioni comprate, rifatta con gli scambi VERI di Deribit (archivio storico pubblico, history.deribit.com).

Per ogni operazione di W3.2:
- ingresso (lunedi' 00:00 UTC): fra le opzioni scambiate nelle 12 ore prima e dopo, si sceglie la scadenza piu' vicina a 30 giorni
  (fra 20 e 50) e il prezzo d'esercizio piu' vicino al prezzo di BTC; la volatilita' implicita e' la mediana di quegli scambi;
- uscita: volatilita' mediana degli scambi dello stesso contratto intorno al momento in cui W3.2 esce; se l'opzione scade prima,
  valore intrinseco al prezzo di regolamento (media Binance 07:30-08:00 UTC del giorno di scadenza);
- il prezzo dell'opzione e' ricalcolato con la formula di Black alla volatilita' VERA scambiata e al prezzo di BTC di W3.2
  (gli scambi non avvengono nell'istante esatto dell'ingresso); in piu' una versione "grezza" che usa direttamente il primo
  scambio dopo l'ingresso e quello piu' vicino all'uscita (anche dopo).
Uscite: results/opzioni_w32/tables_reale.md, operazioni_reale.csv; cache degli scambi in data/opzioni/deribit/.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import btc_ta as B
import intraday as I
import ricerca_nuova as R

ROOT = B.ROOT
OUT = ROOT / "results" / "opzioni_w32"
CACHE = ROOT / "data" / "opzioni" / "deribit"
CACHE.mkdir(parents=True, exist_ok=True)
API = "https://history.deribit.com/api/v2/public/"
pct = lambda x, d=1: "n/d" if x is None or not np.isfinite(x) else f"{x * 100:+.{d}f}%".replace(".", ",")
num = lambda x, d=2: "n/d" if x is None or not np.isfinite(x) else f"{x:.{d}f}".replace(".", ",")
usd = lambda x: f"{x:,.0f}".replace(",", ".")
H = pd.Timedelta(hours=1)
FEE, FEE_CAP, EX_FEE, SPREAD = 0.0003, 0.125, 0.00015, 0.03       # commissioni Deribit; differenziale 3% del premio per lato come nel modello
MON = {m: i + 1 for i, m in enumerate("JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split())}


def call(path: str) -> dict:
    for k in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(API + path, headers={"User-Agent": "research-client"}), timeout=40) as r:
                return json.load(r).get("result", {})
        except Exception:
            time.sleep(1.5 * (k + 1))
    return {}


def trades(path: str, t0: pd.Timestamp, t1: pd.Timestamp, key: str, max_pages: int = 40) -> pd.DataFrame:
    f = CACHE / f"{key}.csv.gz"
    if f.exists():
        return pd.read_csv(f)
    rows, start = [], int(t0.timestamp() * 1000)
    for _ in range(max_pages):
        r = call(f"{path}&start_timestamp={start}&end_timestamp={int(t1.timestamp() * 1000)}&count=1000&sorting=asc")
        x = r.get("trades", [])
        rows += [(z["instrument_name"], z["timestamp"], z["price"], z.get("iv"), z["index_price"], z["amount"], z.get("mark_price")) for z in x]
        if not r.get("has_more") or not x:
            break
        start = x[-1]["timestamp"] + 1
        time.sleep(0.15)
    d = pd.DataFrame(rows, columns=["instrument", "ts", "price", "iv", "index", "amount", "mark"])
    d.to_csv(f, index=False)
    return d


def parse(name: str) -> tuple:
    _, dt, k, cp = name.split("-")
    day, mon, yr = int(dt[:-5]), MON[dt[-5:-2]], 2000 + int(dt[-2:])
    return pd.Timestamp(yr, mon, day, 8), float(k), 1 if cp == "C" else -1


def basis(a: pd.DataFrame, K: float, cp: int, exp: pd.Timestamp) -> float:
    """Rapporto prezzo a termine / indice implicito negli scambi: Deribit calcola la volatilita' sul future della scadenza e quota
    in BTC = Black(F) / F. Per ogni scambio si cerca l'F che riproduce il prezzo; si prende la mediana di F / indice."""
    out = []
    for z in a.itertuples():
        tau = (exp - pd.Timestamp(z.ts, unit="ms")).total_seconds() / 86400 / 365
        if tau <= 0 or not np.isfinite(z.iv) or z.iv <= 0:
            continue
        f = lambda F: R.bs(F, K, tau, z.iv / 100, cp) / F - z.price
        lo, hi = 0.85 * z.index_, 1.25 * z.index_
        if f(lo) * f(hi) > 0:
            continue
        for _ in range(50):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if f(lo) * f(mid) > 0 else (lo, mid)
        out.append(0.5 * (lo + hi) / z.index_)
    return float(np.median(out)) if out else 1.0


def main() -> None:
    B.END = "2026-12-31"
    c = B.load()["close"]
    m15 = I.load("binance")["close"]
    iv_model = R.iv_series(B.load())
    tr = pd.read_csv(ROOT / "results" / "w32" / "movimenti_w32.csv")
    tr["entra"] = pd.to_datetime(tr["entra"])
    tr["esce"] = pd.to_datetime(tr["esce"])
    rows = []
    for n, t in enumerate(tr.itertuples(), 1):
        cp = 1 if t.verso == "long" else -1
        t_in, s0 = t.entra, float(t.prezzo_in)
        a, largo = pd.DataFrame(), ""
        for hrs, g0_, g1_, lab_ in ((12, 20, 50, ""), (36, 20, 50, "scambi entro 36 ore"), (36, 14, 75, "scadenza fuori da 20–50 giorni")):
            a = trades("get_last_trades_by_currency_and_time?currency=BTC&kind=option", t_in - hrs * H, t_in + hrs * H, f"ingresso_{t_in.date()}_{hrs}h")
            if a.empty:
                continue
            p = a.instrument.map(parse)
            a = a.assign(exp=[z[0] for z in p], K=[z[1] for z in p], cp=[z[2] for z in p])
            a["gg"] = (a.exp - t_in).dt.total_seconds() / 86400
            a = a[(a.cp == cp) & a.gg.between(g0_, g1_) & a.iv.notna() & (a.iv > 0) & ((a.K / s0 - 1).abs() < 0.12)]
            if len(a):
                largo = lab_
                break
        if a.empty:
            rows.append({"n": n, "nota": "nessuna opzione vicina al prezzo scambiata entro 36 ore"})
            continue
        exp = a.loc[(a.gg - 30).abs().idxmin(), "exp"]
        a = a[a.exp == exp]
        K = float(a.loc[(a.K / s0 - 1).abs().idxmin(), "K"])
        a = a[a.K == K].sort_values("ts")
        name, tau0 = a.instrument.iloc[0], (exp - t_in).total_seconds() / 86400 / 365
        iv0 = float(a.iv.median()) / 100
        g0b = basis(a.rename(columns={"index": "index_"}), K, cp, exp)
        p0 = R.bs(s0 * g0b, K, tau0, iv0, cp)                                             # premio in dollari sul prezzo a termine (opzioni lineari)
        unit = p0 * (1 + SPREAD) + min(FEE * s0, FEE_CAP * p0)
        # versione grezza: primo scambio dopo l'ingresso (o il piu' vicino), prezzo in BTC x indice
        aft = a[a.ts >= t_in.timestamp() * 1000]
        g0 = (aft.iloc[0] if len(aft) else a.iloc[-1])
        raw_in = float(g0.price * g0["index"])
        open_ = not isinstance(t.uscita, str) or t.uscita == "aperta"
        t_out = t.esce if pd.notna(t.esce) else c.index[-1] + 24 * H
        how, ivm = "", float(iv_model.reindex([t_in - 24 * H], method="ffill").iloc[0]) if t_in - 24 * H >= iv_model.index[0] else np.nan
        if t_out >= exp or (open_ and c.index[-1] + 24 * H >= exp):                       # scade prima che W3.2 esca
            px = m15.loc[exp - 0.5 * H:exp - 0.25 * H]                                    # candele aperte alle 07:30 e 07:45: chiusure 07:45 e 08:00
            s1 = float(px.mean()) if len(px) else float(c.loc[:exp].iloc[-1])
            it = max(0.0, cp * (s1 - K))
            got, raw_out, how, iv1 = it - min(EX_FEE * s1, FEE_CAP * it), it, "scadenza", np.nan
        else:
            s1 = float(t.prezzo_out) if not open_ else float(c.iloc[-1])
            tx = t_out if not open_ else c.index[-1] + 24 * H
            if not open_ and "fine periodo" in str(t.uscita):                             # chiusa alla chiusura del giorno, non all'apertura
                tx = tx + 24 * H
            lo, hi = (tx - 12 * H, tx + 12 * H) if not open_ else (tx - 48 * H, tx)
            if not open_ and "trailing" in str(t.uscita):                                 # stop infrasettimanale: scambi del giorno d'uscita
                lo, hi = tx, tx + 24 * H
                tx = tx + 12 * H
            b = trades(f"get_last_trades_by_instrument_and_time?instrument_name={name}", lo, hi, f"uscita_{name}_{tx.date()}")
            if b.empty:
                b = trades(f"get_last_trades_by_instrument_and_time?instrument_name={name}", lo - 72 * H, hi + 72 * H, f"uscita_largo_{name}_{tx.date()}")
                how = "uscita: scambi entro 4 giorni"
            tau1, g1b = max(0.0, (exp - tx).total_seconds() / 86400 / 365), 1.0
            if b.empty or b.iv[b.iv > 0].dropna().empty:
                iv1 = float(iv_model.reindex([tx - 24 * H], method="ffill").iloc[0])
                how, raw_out = "uscita: nessuno scambio, volatilità del modello", max(0.0, cp * (s1 - K))    # grezzo: solo il valore intrinseco
            else:
                iv1 = float(b.iv[b.iv > 0].median()) / 100
                g1b = basis(b.rename(columns={"index": "index_"}), K, cp, exp)
                how = how or "venduta"
                bb = b.iloc[(b.ts - tx.timestamp() * 1000).abs().argmin()]
                raw_out = float(bb.price * bb["index"])
            p1 = R.bs(s1 * g1b, K, tau1, iv1, cp)
            got = max(0.0, p1 * (1 - SPREAD) - min(FEE * s1, FEE_CAP * p1))
        pm = R.bs(s0, K, tau0, ivm, cp) if np.isfinite(ivm) else np.nan
        base_in = g0b - 1
        rows.append({"n": n, "verso": t.verso, "entra": t_in.date(), "esce": "aperta" if open_ else t.esce.date(), "contratto": name, "gg": (exp - t_in).days, "K_su_S": K / s0 - 1, "iv_vera": iv0,
                     "iv_modello": ivm, "premio": p0 / s0, "premio_modello": pm / s0 if np.isfinite(pm) else np.nan, "scambi": len(a), "base": base_in, "esito": how, "w32": t.sul_capitale,
                     "mult": got / unit, "mult_grezzo": (raw_out * (1 - SPREAD)) / (raw_in * (1 + SPREAD)) if np.isfinite(raw_out) else np.nan, "nota": largo})
        print(n, name, how, round(got / unit, 2), flush=True)
    o = pd.DataFrame(rows)
    o.to_csv(OUT / "operazioni_reale.csv", index=False)

    mod = pd.read_csv(OUT / "operazioni.csv", parse_dates=["entra"])            # backtest a modello (dal 2019), per il confronto
    T = ["## Q1 reale\n"]
    ok = o[o.mult.notna()].copy()
    T.append(f"Operazioni di W3.2: {len(o)}; con un'opzione vera vicina al prezzo scambiata all'ingresso: {len(ok)}. Prezzi ricalcolati alla volatilità implicita degli scambi veri di Deribit; "
             f"costi: differenziale 3% del premio per lato, commissioni Deribit (0,03% del controvalore, tetto 12,5% del premio; regolamento 0,015%).\n")
    T.append("| # | Verso | Entra | Esce | Contratto vero | Giorni alla scadenza | Volatilità vera | Volatilità del modello | Come finisce | W3.2 originale | Opzione, 5% del capitale: prezzi veri | Modello a 30 giorni |")
    T.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in o.itertuples():
        if not isinstance(r.verso, str):
            T.append(f"| {r.n} | – | – | – | {r.nota} | | | | | | | |")
            continue
        mm = mod[mod.entra == pd.Timestamp(r.entra)]
        T.append(f"| {r.n} | {r.verso} | {r.entra} | {r.esce} | {r.contratto}{' (' + r.nota + ')' if isinstance(r.nota, str) and r.nota else ''} | {int(r.gg)} | {r.iv_vera * 100:.0f}% | {'n/d' if not np.isfinite(r.iv_modello) else f'{r.iv_modello * 100:.0f}%'} | {r.esito} | {pct(r.w32)} | "
                 f"{pct(0.05 * (r.mult - 1))} | {pct(float(mm.ris.iloc[0])) if len(mm) else 'n/d'} |")
    T.append("\n## Q2 totali\n")
    T.append("| Periodo e versione | Operazioni | 10.000 $ → | Operazioni in guadagno | Operazione peggiore | Migliore | Serie peggiore di perdite | Senza le tre migliori |")
    T.append("|---|---|---|---|---|---|---|---|")

    def line(lab, r):
        r = np.asarray(r, float)
        run = min(np.prod(1 + r[i:j]) - 1 for i in range(len(r)) for j in range(i + 1, len(r) + 1))
        T.append(f"| {lab} | {len(r)} | {usd(10000 * float(np.prod(1 + r)))} | {(r > 0).mean() * 100:.0f}% | {pct(r.min())} | {pct(r.max())} | {pct(run)} | ×{num(float(np.prod(1 + np.sort(r)[::-1][3:])), 1)} |")

    y19 = ok[pd.to_datetime(ok.entra) >= "2019-01-07"]
    line("Dal 2019 · W3.2 originale", y19.w32)
    line("Dal 2019 · W3.2 a metà dimensione", 0.5 * y19.w32)
    line("Dal 2019 · opzioni 5%, prezzi veri", 0.05 * (y19.mult - 1))
    line("Dal 2019 · opzioni 5%, modello (30 giorni esatti)", mod.ris)
    line("Dal 2019 · opzioni 10%, prezzi veri", 0.10 * (y19.mult - 1))
    g = y19[y19.mult_grezzo.notna()]
    line("Dal 2019 · opzioni 5%, scambi grezzi (primo dopo l'ingresso, più vicino all'uscita)", 0.05 * (g.mult_grezzo - 1))
    line("Dal 2018 · W3.2 originale", ok.w32)
    line("Dal 2018 · W3.2 a metà dimensione", 0.5 * ok.w32)
    line("Dal 2018 · opzioni 5%, prezzi veri", 0.05 * (ok.mult - 1))
    line("Dal 2018 · opzioni 10%, prezzi veri", 0.10 * (ok.mult - 1))
    z = y19[np.isfinite(y19.iv_modello)]
    T.append(f"\nVolatilità all'ingresso, dal 2019: vera {z.iv_vera.mean() * 100:.0f}% in media, modello {z.iv_modello.mean() * 100:.0f}%; rapporto mediano vera / modello {num(float((z.iv_vera / z.iv_modello).median()))} "
             f"(fra {num(float((z.iv_vera / z.iv_modello).min()))} e {num(float((z.iv_vera / z.iv_modello).max()))}). Premio medio pagato: {pct(float(z.premio.mean())).lstrip('+')} del prezzo di BTC "
             f"(modello: {pct(float(z.premio_modello.mean())).lstrip('+')}). Prezzo a termine sopra il prezzo corrente, in mediana: {pct(float(z.base.median()))} (massimo {pct(float(z.base.max()))}). Scadenza media dei contratti veri: {z.gg.mean():.0f} giorni (fra {int(z.gg.min())} e {int(z.gg.max())}).")
    (OUT / "tables_reale.md").write_text("\n".join(T) + "\n")
    print("\n".join(T))


if __name__ == "__main__":
    main()
