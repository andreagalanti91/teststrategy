"""Dati d'esempio INVENTATI per i test e per esempio_sezione.json: undici messaggi scritti apposta (non copiati dal canale) e
prezzi orari sintetici di BTC, ETH e SOL costruiti per far succedere le operazioni dei messaggi. Nessun dato reale.

    python esempio.py      # rigenera esempio_sezione.json, esempio_riepilogo.md e i dati dentro riferimento_sezione.html
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

import aldo as A

QUI = Path(__file__).resolve().parent
ADESSO = "2026-11-26T12:00:00Z"

# (asset, [(ora UTC, prezzo), ...]): percorso a tratti, interpolato ora per ora
PERCORSI = {
    "BTC": [("2026-11-07 00:00", 60100), ("2026-11-10 09:00", 60300), ("2026-11-10 15:00", 61250), ("2026-11-11 09:00", 59800),
            ("2026-11-12 12:00", 58600), ("2026-11-14 00:00", 59400), ("2026-11-18 00:00", 60500), ("2026-11-22 00:00", 61300),
            ("2026-11-25 18:00", 62600), ("2026-11-26 12:00", 62150)],
    "ETH": [("2026-11-07 00:00", 2080), ("2026-11-14 10:00", 2100), ("2026-11-14 13:00", 2116), ("2026-11-15 06:00", 2058),
            ("2026-11-15 09:00", 2052), ("2026-11-20 00:00", 2075), ("2026-11-26 08:00", 2046), ("2026-11-26 12:00", 2041)],
    "SOL": [("2026-11-07 00:00", 126), ("2026-11-20 13:00", 131), ("2026-11-20 20:00", 128.3), ("2026-11-21 07:00", 129.5),
            ("2026-11-23 15:00", 134.2), ("2026-11-25 00:00", 132.4), ("2026-11-26 12:00", 133.1)],
}

# messaggi inventati, nello stile del canale (stessa struttura dei messaggi veri: id, data, testo, foto, risposta_a)
MESSAGGI = [
    (101, "2026-11-10T09:12:00Z", "BTC: se torna sui 61,2k cerco short al retest della resistenza. Stop sopra 62.000, target 59,8k e 58.500. Grafico 4h.", "export"),
    (102, "2026-11-10T16:20:00Z", "Short aperto su BTC a 61.150", "export"),
    (103, "2026-11-11T09:40:00Z", "Chiuso metà al primo target, stop a pareggio", "export"),
    (104, "2026-11-12T12:30:00Z", "Chiuso il resto a 58.600, operazione conclusa", "export"),
    (105, "2026-11-13T19:00:00Z", "Settimana con il dato sull'inflazione mercoledì, riduco l'esposizione.", "export"),
    (106, "2026-11-14T10:05:00Z", "Long ETH aperto a 2.105, stop 2.060, target 2.200", "export"),
    (107, "2026-11-15T08:30:00Z", "Stoppato su ETH, fa parte del gioco", "bot"),
    (108, "2026-11-20T13:00:00Z", "Ordine long al limite su SOL a 128,5, stop 124, target 136 e 142", "bot"),
    (109, "2026-11-21T07:10:00Z", "Long SOL eseguito a 128,5", "bot"),
    (110, "2026-11-23T15:00:00Z", "SOL: chiuso un terzo a 134, stop a pareggio", "bot"),
    (111, "2026-11-25T18:30:00Z", "BTC: possibile short se risale a 63,4k. Invalidazione sopra 64.200, obiettivi 61k e 59,5k.", "bot"),
    (112, "2026-11-26T08:00:00Z", "ETH: ordine long al limite a 2.010, stop 1.960", "bot"),
]


def prezzi_finti(fino=ADESSO) -> dict:
    """Candele orarie sintetiche: apertura e chiusura sul percorso, massimo e minimo 0,1% oltre."""
    out = {}
    fine = A._ts(fino).floor("h")
    for asset, pts in PERCORSI.items():
        t = pd.to_datetime([p[0] for p in pts])
        v = np.array([p[1] for p in pts], dtype=float)
        idx = pd.date_range(t[0], fine, freq="h")
        x = idx.asi8.astype(float)
        mid = np.interp(x, t.asi8.astype(float), v)
        o = mid
        c = np.append(mid[1:], mid[-1])
        df = pd.DataFrame({"open": o, "close": c}, index=idx)
        df["high"] = df[["open", "close"]].max(axis=1) * 1.001
        df["low"] = df[["open", "close"]].min(axis=1) * 0.999
        out[asset] = df[["open", "high", "low", "close"]]
    return out


def messaggi_esempio(fino=None) -> list[dict]:
    lim = A._dt(fino) if fino else None
    return [A.messaggio(i, d, t, origine=o) for i, d, t, o in MESSAGGI if lim is None or A._dt(d) <= lim]


def stato_esempio(fino=ADESSO, capitale=10_000.0):
    """Registro, operazioni e uscita di build() con i dati inventati, come al giro delle `fino`."""
    prezzi = A.Prezzi(dati={k: v for k, v in prezzi_finti(fino).items()})
    msgs = messaggi_esempio(fino)
    reg, _ = A.elabora(msgs, A.registro_vuoto(), prezzi, adesso=fino, usa_modello=False, capitale=capitale)
    ops = A.ricostruisci(reg, prezzi, fino, capitale)
    return msgs, reg, ops, A.build(reg, ops, fino, msgs)


if __name__ == "__main__":
    msgs, reg, ops, sez = stato_esempio()
    sez["capitale_esempio"] = True
    (QUI / "esempio_sezione.json").write_text(json.dumps(sez, ensure_ascii=False, indent=1), encoding="utf-8")
    testo, _ = A.riepilogo_settimanale(reg, ops, "2026-11-26", None, msgs)
    (QUI / "esempio_riepilogo.md").write_text(testo, encoding="utf-8")
    vuoto = A.build(A.registro_vuoto(), {}, ADESSO, [])
    html = QUI / "riferimento_sezione.html"
    s = html.read_text(encoding="utf-8")
    dati = json.dumps({"attiva": sez, "vuota": vuoto}, ensure_ascii=False)
    s = re.sub(r"const STATI = .*?;\n", lambda m: f"const STATI = {dati};\n", s, count=1, flags=re.S)
    html.write_text(s, encoding="utf-8")
    print(sez["stato"], sez["titolo"])
    print(json.dumps(sez["statistiche"], ensure_ascii=False))
