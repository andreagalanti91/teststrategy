"""Scarica le candele a 15 minuti di BTC: Binance spot BTCUSDT (archivio pubblico data.binance.vision, dal 08/2017) e
perp OKX BTC-USDT-SWAP (API pubblica history-candles), piu' lo storico del funding OKX disponibile.
Uso: python backtest/fetch_intraday.py [binance|okx|funding]"""
from __future__ import annotations

import io
import json
import sys
import time
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "data" / "intraday"
OUT.mkdir(parents=True, exist_ok=True)
COLS = ["ts", "open", "high", "low", "close", "volume"]


def _get(url: str, tries: int = 5) -> bytes | None:
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "research-client"}), timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(2 * (k + 1))
        except Exception:
            time.sleep(2 * (k + 1))
    raise RuntimeError(f"download fallito: {url}")


def _binance_zip(raw: bytes) -> pd.DataFrame:
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        d = pd.read_csv(z.open(z.namelist()[0]), header=None, usecols=range(6), names=COLS)
    d = d[pd.to_numeric(d["ts"], errors="coerce").notna()].astype(float)
    unit = "us" if d["ts"].iloc[0] > 1e14 else "ms"          # dal 2025 l'archivio spot e' in microsecondi
    d["ts"] = pd.to_datetime(d["ts"].astype("int64"), unit=unit)
    return d


def binance(sym: str = "BTCUSDT", tf: str = "15m") -> None:
    base = f"https://data.binance.vision/data/spot"
    parts = []
    for m in pd.period_range("2017-08", pd.Timestamp.utcnow().strftime("%Y-%m"), freq="M"):
        raw = _get(f"{base}/monthly/klines/{sym}/{tf}/{sym}-{tf}-{m}.zip")
        if raw is not None:
            parts.append(_binance_zip(raw))
            continue
        for d in pd.date_range(m.start_time, min(m.end_time, pd.Timestamp.utcnow().tz_localize(None)), freq="D"):
            raw = _get(f"{base}/daily/klines/{sym}/{tf}/{sym}-{tf}-{d.date()}.zip")
            if raw is not None:
                parts.append(_binance_zip(raw))
    d = pd.concat(parts).drop_duplicates("ts").sort_values("ts")
    d.to_csv(OUT / f"binance_spot_{sym}_{tf}.csv.gz", index=False)
    print("binance", len(d), d.ts.iloc[0], d.ts.iloc[-1])


def okx(inst: str = "BTC-USDT-SWAP", bar: str = "15m") -> None:
    rows, after = [], ""
    while True:
        j = json.loads(_get(f"https://www.okx.com/api/v5/market/history-candles?instId={inst}&bar={bar}&limit=100" + (f"&after={after}" if after else "")))
        data = j.get("data") or []
        if not data:
            break
        rows += [r[:6] for r in data if r[8] == "1"]            # solo candele chiuse; volume in contratti
        after = data[-1][0]
        time.sleep(0.11)
    d = pd.DataFrame(rows, columns=COLS).astype(float)
    d["ts"] = pd.to_datetime(d["ts"].astype("int64"), unit="ms")
    d = d.drop_duplicates("ts").sort_values("ts")
    d.to_csv(OUT / f"okx_{inst}_{bar}.csv.gz", index=False)
    print("okx", len(d), d.ts.iloc[0], d.ts.iloc[-1])


def funding(inst: str = "BTC-USDT-SWAP") -> None:
    rows, after = [], ""
    while True:
        j = json.loads(_get(f"https://www.okx.com/api/v5/public/funding-rate-history?instId={inst}&limit=100" + (f"&after={after}" if after else "")))
        data = j.get("data") or []
        if not data:
            break
        rows += [(r["fundingTime"], r["realizedRate"]) for r in data]
        after = data[-1]["fundingTime"]
        time.sleep(0.25)
    d = pd.DataFrame(rows, columns=["ts", "rate"]).astype(float)
    d["ts"] = pd.to_datetime(d["ts"].astype("int64"), unit="ms")
    d.sort_values("ts").to_csv(OUT / f"okx_{inst}_funding.csv.gz", index=False)
    print("funding", len(d), d.ts.min(), d.ts.max())


if __name__ == "__main__":
    for what in (sys.argv[1:] or ["binance", "okx", "funding"]):
        {"binance": binance, "okx": okx, "funding": funding}[what]()
