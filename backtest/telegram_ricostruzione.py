"""Ricostruisce l'esito di ogni operazione annunciata nel canale, sui prezzi reali (candele orarie Binance spot).

Ingresso: telegram/estrazione/eventi_*.json (estratti messaggio per messaggio, con i livelli letti da testo e grafici).
Prezzo di ogni evento: quello scritto dal trader se c'e'; altrimenti l'apertura della candela oraria successiva al messaggio
(cioe' il primo prezzo eseguibile da chi legge il messaggio). Stop a pareggio colpito = prezzo medio d'ingresso.
Quote: apertura graduale e aumenti in frazioni della posizione piena; le chiusure parziali in frazione del rimanente, oppure
cumulative se superano la quota gia' chiusa ("chiuso meta'" poi "chiuso l'80%" = 80% del totale).
Costi: 0,06% per lato (commissione taker) + 0,02% di slittamento. Posizioni ancora aperte a fine export: valutate all'ultimo prezzo.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
EST = ROOT / "telegram" / "estrazione"
PRZ = ROOT / "data" / "telegram_prezzi"
OUT = ROOT / "results" / "telegram"
OUT.mkdir(parents=True, exist_ok=True)
COST = 0.0008
FINE = pd.Timestamp("2024-03-18 11:00")
_P = {}


def prices(asset: str) -> pd.DataFrame | None:
    sym = asset.upper().replace("/", "").replace("USDT", "") + "USDT"
    if sym not in _P:
        f = PRZ / f"{sym}_1h.csv.gz"
        _P[sym] = pd.read_csv(f, index_col=0, parse_dates=True) if f.exists() else None
    return _P[sym]


def px_at(asset: str, t: pd.Timestamp) -> float | None:
    p = prices(asset)
    if p is None:
        return None
    k = p.index.searchsorted(t.floor("h") + pd.Timedelta(hours=1))
    if k >= len(p):
        return float(p["close"].iloc[-1])
    return float(p["open"].iloc[k])


def load_events() -> pd.DataFrame:
    ev = []
    for f in sorted(EST.glob("eventi_*.json")):
        ev += json.load(open(f, encoding="utf-8"))
    e = pd.DataFrame(ev)
    e["utc"] = pd.to_datetime(e["utc"])
    return e.sort_values(["utc", "msg_id"]).reset_index(drop=True)


def rebuild(e: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for tid, g in e.groupby("trade", sort=False):
        g = g.sort_values(["utc", "msg_id"])
        asset, side = g["asset"].iloc[0], g["verso"].iloc[0]
        sg = 1 if str(side).lower() == "long" else -1
        size, closed_cum, maxsize, cost_basis, realized, fees = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        avg, stop0, notes, t_open, t_close, fonte = None, None, [], None, None, set()
        for r in g.itertuples():
            tipo = r.tipo
            if tipo in ("ordine_non_eseguito",):
                continue
            p = r.prezzo if isinstance(r.prezzo, (int, float)) and r.prezzo and np.isfinite(r.prezzo) else None
            src = "trader" if p else "mercato"
            if tipo in ("stop_preso",) and p is None and avg:
                p, src = avg, "pareggio"
            if p is None:
                p = px_at(asset, r.utc)
            if p is None:
                notes.append(f"#{r.msg_id}: prezzo di {asset} non disponibile")
                continue
            fonte.add(src)
            q = r.quota if isinstance(r.quota, (int, float)) and r.quota == r.quota else None
            if tipo in ("apertura", "aumento", "ordine_limite"):
                add = q if q else (1.0 - size if tipo == "aumento" and size < 1 else (1.0 if size == 0 else 0.0))
                if tipo == "aumento" and q and size + q > 1.0001 and q <= 1:
                    add = max(0.0, q - size) if q > size else q            # "full position" = porta a 1
                if add <= 0:
                    continue
                cost_basis += add * p
                size += add
                avg = cost_basis / size
                maxsize = max(maxsize, size)
                fees += add * COST
                t_open = t_open or r.utc
                if stop0 is None and isinstance(r.stop, (int, float)) and r.stop == r.stop:
                    stop0 = r.stop
            elif tipo in ("chiusura_parziale", "chiusura_totale", "stop_preso", "target_preso") and size > 0:
                if tipo == "chiusura_parziale" and q:
                    total = maxsize
                    if q > closed_cum / total + 1e-9 and q < 1:
                        out = max(0.0, q * total - closed_cum)              # quota cumulativa
                    else:
                        out = q * size                                      # quota del rimanente
                else:
                    out = size
                out = min(out, size)
                realized += out * sg * (p - avg) / avg
                fees += out * COST
                closed_cum += out
                size -= out
                cost_basis = avg * size
                t_close = r.utc
            if size <= 1e-9 and t_open is not None and tipo not in ("apertura", "aumento", "ordine_limite"):
                size = 0.0
        aperta = size > 1e-9
        if aperta:
            p = prices(asset)
            last = float(p.loc[:FINE, "close"].iloc[-1]) if p is not None else avg
            realized += size * sg * (last - avg) / avg
            fees += size * COST
            notes.append(f"aperta a fine export: valutata a {last:.4g}")
            t_close = FINE
        if t_open is None or maxsize == 0:
            continue
        ret_pos = (realized - fees) / maxsize                                # rendimento sulla posizione piena
        risk = abs(avg - stop0) / avg if stop0 and avg else None
        rows.append({"trade": tid, "asset": asset, "verso": side, "apertura": t_open, "chiusura": t_close, "giorni": (t_close - t_open).total_seconds() / 86400 if t_close is not None else None,
                     "prezzo_medio": avg, "stop": stop0, "rischio_pct": risk, "dimensione_max": maxsize, "rendimento": ret_pos, "R": ret_pos / risk if risk else None,
                     "aperta_a_fine": aperta, "prezzi": "+".join(sorted(fonte)), "eventi": len(g), "note": "; ".join(notes)})
    return pd.DataFrame(rows).sort_values("apertura").reset_index(drop=True)


if __name__ == "__main__":
    e = load_events()
    print(len(e), "eventi,", e["trade"].nunique(), "trade,", sorted(e["asset"].str.upper().unique()))
    t = rebuild(e)
    t.to_csv(OUT / "operazioni_ricostruite.csv", index=False)
    print(t[["trade", "asset", "verso", "apertura", "giorni", "prezzo_medio", "rendimento", "R", "prezzi", "note"]].to_string())
