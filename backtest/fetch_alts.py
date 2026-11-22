"""Scarica: (1) TAO da Bitget (spot e perp giornalieri, funding del perp, parametri del contratto);
(2) candele giornaliere spot <SYM>USDT di ~170 altcoin dall'archivio Binance, comprese monete poi crollate o delistate
(LUNA, FTT, SRM, ANC, MIR, ...) per ridurre la distorsione da sopravvivenza. Uso: python backtest/fetch_alts.py [tao|alts]"""
from __future__ import annotations

import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_intraday import _binance_zip, _get

ROOT = Path(__file__).resolve().parent.parent
ALTS = """ETH BNB SOL XRP ADA DOGE TRX LINK AVAX DOT LTC BCH MATIC UNI ATOM NEAR ETC XLM FIL ICP APT ARB OP INJ SUI SEI TIA RNDR FET
AGIX OCEAN GRT AAVE MKR SNX CRV COMP SUSHI YFI 1INCH LDO RUNE FTM ALGO VET HBAR EGLD THETA AXS SAND MANA GALA ENJ CHZ FLOW EOS XTZ
NEO ZEC DASH XMR WAVES KSM ZIL ONE CELO KAVA IOTA QTUM OMG BAT ZRX ENS APE GMT DYDX IMX STX MINA ROSE AR TAO WLD PYTH JUP JTO ORDI
PENDLE STRK ENA ONDO WIF PEPE SHIB FLOKI BONK LUNA LUNC FTT SRM ANC MIR BTT HNT XEM BTS REN KNC STORJ ANKR COTI CELR SKL AUDIO LRC
ICX ONT IOST HOT DENT WIN SXP ALPHA BAND RSR OGN NKN CTSI TRB UMA BAL PERP C98 ALICE TLM SLP ILV YGG JASMY PEOPLE MAGIC GMX SSV
BLUR ID EDU ARKM CYBER AI ALT MANTA DYM PIXEL PORTAL AEVO ETHFI SAGA W OMNI REZ BB NOT IO ZK ZRO LISTA""".split()


def bitget_candles(path: str, extra: str, gran: str) -> pd.DataFrame:
    rows, end = [], int(time.time() * 1000)
    while True:
        j = json.loads(_get(f"https://api.bitget.com{path}?symbol=TAOUSDT{extra}&granularity={gran}&endTime={end}&limit=200"))
        d = j.get("data") or []
        d = [r for r in d if int(r[0]) < end]
        if not d:
            break
        rows += [r[:6] for r in d]
        end = min(int(r[0]) for r in d)
        time.sleep(0.12)
    o = pd.DataFrame(rows, columns=["ts", "open", "high", "low", "close", "volume"]).astype(float)
    o["ts"] = pd.to_datetime(o["ts"].astype("int64"), unit="ms")
    return o.drop_duplicates("ts").sort_values("ts")


def tao() -> None:
    out = ROOT / "data" / "tao"
    s = bitget_candles("/api/v2/spot/market/history-candles", "", "1Dutc")
    s.to_csv(out / "bitget_TAOUSDT_spot_1d.csv", index=False)
    print("spot", len(s), s.ts.iloc[0], s.ts.iloc[-1])
    p = bitget_candles("/api/v2/mix/market/history-candles", "&productType=USDT-FUTURES", "1Dutc")
    p.to_csv(out / "bitget_TAOUSDT_perp_1d.csv", index=False)
    print("perp", len(p), p.ts.iloc[0], p.ts.iloc[-1])
    rows, page = [], 1
    while True:
        j = json.loads(_get(f"https://api.bitget.com/api/v2/mix/market/history-fund-rate?symbol=TAOUSDT&productType=USDT-FUTURES&pageSize=100&pageNo={page}"))
        d = j.get("data") or []
        if not d:
            break
        rows += [(int(r["fundingTime"]), float(r["fundingRate"])) for r in d]
        page += 1
        time.sleep(0.12)
    f = pd.DataFrame(rows, columns=["ts", "rate"]).drop_duplicates("ts").sort_values("ts")
    f["ts"] = pd.to_datetime(f["ts"], unit="ms")
    f.to_csv(out / "bitget_TAOUSDT_funding.csv", index=False)
    print("funding", len(f), f.ts.iloc[0], f.ts.iloc[-1])
    c = json.loads(_get("https://api.bitget.com/api/v2/mix/market/contracts?productType=USDT-FUTURES&symbol=TAOUSDT"))["data"][0]
    (out / "bitget_TAOUSDT_contract.json").write_text(json.dumps(c, indent=1))
    print({k: c.get(k) for k in ("makerFeeRate", "takerFeeRate", "minLever", "maxLever", "fundInterval", "maintainTime")})


def one(sym: str) -> tuple[str, int]:
    parts = []
    for m in pd.period_range("2019-01", "2026-10", freq="M"):
        raw = _get(f"https://data.binance.vision/data/spot/monthly/klines/{sym}USDT/1d/{sym}USDT-1d-{m}.zip")
        if raw is not None:
            parts.append(_binance_zip(raw))
    for day in pd.date_range("2026-11-01", pd.Timestamp.now("UTC").tz_localize(None).normalize() - pd.Timedelta(days=1), freq="D"):
        raw = _get(f"https://data.binance.vision/data/spot/daily/klines/{sym}USDT/1d/{sym}USDT-1d-{day.date()}.zip") if parts else None
        if raw is not None:                                  # mese in corso: file giornalieri
            parts.append(_binance_zip(raw))
    if not parts:
        return sym, 0
    d = pd.concat(parts).drop_duplicates("ts").sort_values("ts")
    d.to_csv(ROOT / "data" / "alts" / f"{sym}.csv.gz", index=False)
    return sym, len(d)


def alts() -> None:
    with ThreadPoolExecutor(16) as ex:
        res = list(ex.map(one, ALTS + ["BTC"]))
    print("alt scaricate:", sum(1 for _, n in res if n), "di", len(res), "| senza dati:", [s for s, n in res if not n])


if __name__ == "__main__":
    for what in (sys.argv[1:] or ["tao", "alts"]):
        {"tao": tao, "alts": alts}[what]()
