"""Candele orarie spot Binance (archivio pubblico data.binance.vision) per una lista di simboli e mesi.
Uso: python backtest/fetch_binance_1h.py 2023-05 2024-04 BTCUSDT INJUSDT ..."""
import io
import sys
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "data" / ("telegram_prezzi" if len(sys.argv) < 2 or sys.argv[1] >= "2023" else "alts_1h")
OUT.mkdir(parents=True, exist_ok=True)


def months(a: str, b: str):
    return [p.strftime("%Y-%m") for p in pd.period_range(a, b, freq="M")]


def fetch(sym: str, a: str, b: str) -> pd.DataFrame:
    parts = []
    for m in months(a, b):
        url = f"https://data.binance.vision/data/spot/monthly/klines/{sym}/1h/{sym}-1h-{m}.zip"
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "research-client"}), timeout=60) as r:
                z = zipfile.ZipFile(io.BytesIO(r.read()))
        except Exception as e:
            print(sym, m, "non disponibile:", e)
            continue
        x = pd.read_csv(z.open(z.namelist()[0]), header=None).iloc[:, :6]
        x.columns = ["ts", "open", "high", "low", "close", "volume"]
        ts = x["ts"].astype("int64")
        x["ts"] = pd.to_datetime(ts // 1000 if ts.iloc[0] > 1e14 else ts, unit="ms")
        parts.append(x)
    d = pd.concat(parts).drop_duplicates("ts").set_index("ts").sort_index() if parts else pd.DataFrame()
    if len(d):
        d.to_csv(OUT / f"{sym}_1h.csv.gz")
    return d


if __name__ == "__main__":
    a, b, *syms = sys.argv[1:]
    for s in syms:
        d = fetch(s, a, b)
        print(s, len(d), d.index.min() if len(d) else "-", d.index.max() if len(d) else "-")
