"""Dati giornalieri per estendere W3.2 ad altre monete: spot e perp USD-M Binance (con volume aggressivo in acquisto) e funding.
Archivio pubblico data.binance.vision. Uscita: data/w32_estesa/{SYM}_spot.csv.gz, {SYM}_perp.csv.gz, {SYM}_funding.csv.gz"""
import io
import sys
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "data" / "w32_estesa"
OUT.mkdir(parents=True, exist_ok=True)
BASE = "https://data.binance.vision/data/"


def get_zip(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "research-client"}), timeout=60) as r:
            z = zipfile.ZipFile(io.BytesIO(r.read()))
        return z.open(z.namelist()[0])
    except Exception:
        return None


def klines(path_tpl, months):
    parts = []
    for m in months:
        f = get_zip(path_tpl.format(m=m))
        if f is None:
            continue
        x = pd.read_csv(f, header=None)
        if not str(x.iloc[0, 0]).isdigit():
            x = x.iloc[1:]
        x = x.iloc[:, :11].astype(float)
        x.columns = ["ts", "open", "high", "low", "close", "volume", "close_ts", "quote_volume", "trades", "taker_buy_volume", "taker_buy_quote"]
        ts = x["ts"].astype("int64")
        x["date"] = pd.to_datetime(ts // 1000 if ts.iloc[0] > 1e14 else ts, unit="ms").dt.normalize()
        parts.append(x.set_index("date")[["open", "high", "low", "close", "volume", "taker_buy_volume"]])
    return pd.concat(parts).sort_index().pipe(lambda d: d[~d.index.duplicated()]) if parts else pd.DataFrame()


def funding(sym, months):
    parts = []
    for m in months:
        f = get_zip(f"{BASE}futures/um/monthly/fundingRate/{sym}/{sym}-fundingRate-{m}.zip")
        if f is None:
            continue
        x = pd.read_csv(f)
        c = [k for k in x.columns if "time" in k.lower()][0]
        r = [k for k in x.columns if "rate" in k.lower() and "funding" in k.lower()][0]
        x["date"] = pd.to_datetime(x[c], unit="ms").dt.normalize()
        parts.append(x.groupby("date")[r].sum().rename("funding"))
    return pd.concat(parts).sort_index() if parts else pd.Series(dtype=float)


if __name__ == "__main__":
    a, b, *syms = sys.argv[1:]
    months = [p.strftime("%Y-%m") for p in pd.period_range(a, b, freq="M")]
    for s in syms:
        sp = klines(BASE + f"spot/monthly/klines/{s}/1d/{s}-1d-{{m}}.zip", months)
        pp = klines(BASE + f"futures/um/monthly/klines/{s}/1d/{s}-1d-{{m}}.zip", months)
        fu = funding(s, months)
        sp.to_csv(OUT / f"{s}_spot.csv.gz"); pp.to_csv(OUT / f"{s}_perp.csv.gz"); fu.to_csv(OUT / f"{s}_funding.csv.gz")
        print(s, "spot", len(sp), sp.index.min() if len(sp) else "-", "| perp", len(pp), pp.index.min() if len(pp) else "-", "| funding", len(fu))
