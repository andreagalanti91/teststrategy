"""Prepara tool/data.json per lo strumento di confronto (tool/index.html): curve di capitale giornaliere e operazioni."""
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
idx = pd.date_range("2018-01-01", "2026-11-22", freq="D")
S, META = {}, {}


def add(name, s, group, note):
    s = s.reindex(s.index.union(idx)).ffill().reindex(idx).where(lambda x: (idx >= s.index[0]) & (idx <= s.index[-1]))
    S[name] = [None if not np.isfinite(v) else round(float(v), 2) for v in s.to_numpy()]
    META[name] = {"gruppo": group, "nota": note, "dal": str(s.first_valid_index().date()), "al": str(s.last_valid_index().date())}


a = pd.read_csv(ROOT / "results" / "w32" / "equity.csv", index_col=0, parse_dates=True)
add("W3.2 radar", a["W3.2 radar (rischio 25%)"], "BTC", "Trend settimanale con flusso del perp, rischio 25%. 2018–20 con flusso stimato.")
add("v1 · voto di 17 indicatori", a["v1 · voto di 17 indicatori"], "BTC", "Long/short dal voto di 17 indicatori tecnici.")
add("v2 · tre schermi", a["v2 · tre schermi"], "BTC", "Marea settimanale, rottura a 55 giorni, chandelier 5 ATR.")
add("50% W3.2 + 50% v1", a["50% W3.2 + 50% v1"], "Combinazioni", "Metà e metà, ribilanciato ogni giorno.")
add("BTC comprato e tenuto", a["BTC comprato e tenuto"], "Riferimenti", "Spot, nessuna operazione.")
b = pd.read_csv(ROOT / "results" / "equity.csv", index_col=0, parse_dates=True)
for col, name, grp, note in (("W3.1 radar (rischio 10%)", "W3.1 radar", "BTC", "Come W3.2 con rischio 10%."),
                             ("Paniere trend 11 crypto", "Paniere trend 11 crypto", "Altcoin", "Ensemble Donchian su 11 monete, solo long."),
                             ("Rotazione momentum crypto", "Rotazione momentum crypto", "Altcoin", "Le 3 monete più forti a 30 giorni; universo scelto a posteriori."),
                             ("Carry funding selettivo", "Carry funding selettivo", "Neutrali", "Long spot + short perp quando il funding è positivo."),
                             ("Dual momentum SPY/QQQ/GLD", "Dual momentum ETF", "ETF", "L'ETF migliore a 12 mesi, se positivo."),
                             ("QQQ 3x sintetico + SMA200", "QQQ 3x + SMA200", "ETF", "Nasdaq a leva 3x sopra la media a 200 giorni (serie sintetica).")):
    add(name, b[col], grp, note)
c = pd.read_csv(ROOT / "results" / "algo" / "equity_finale.csv", index_col=0, parse_dates=True)["equity"]
add("MACD a regime (altcoin)", c, "Altcoin", "MACD settimanale con filtri di trend su moneta e BTC, 30 monete più liquide, solo long.")

T = {}
w = pd.read_csv(ROOT / "results" / "w32" / "movimenti_w32.csv")
T["W3.2 radar"] = [{"verso": r.verso, "entra": r.entra, "esce": r.esce if isinstance(r.esce, str) else None, "in": round(r.prezzo_in), "out": round(r.prezzo_out),
                    "espo": round(r.esposizione, 2), "ris": round(r.sul_capitale * 100, 1), "motivo": r.uscita} for r in w.itertuples()]
v = pd.read_csv(ROOT / "results" / "w32" / "movimenti_v1.csv")
T["v1 · voto di 17 indicatori"] = [{"verso": r.verso, "entra": r.entra, "esce": r.esce if isinstance(r.esce, str) else None, "in": round(r.prezzo_in), "out": round(r.prezzo_out),
                                    "espo": 1.0, "ris": round(r.risultato * 100, 1), "motivo": f"voto {r.voto:.2f} all'ingresso".replace(".", ",")} for r in v.itertuples()]
v2 = pd.read_csv(ROOT / "results" / "w32" / "movimenti_v2.csv")
T["v2 · tre schermi"] = [{"verso": r.verso, "entra": str(r.entra)[:10], "esce": str(r.esce)[:10] if isinstance(r.esce, str) else None, "in": round(r.prezzo_in), "out": round(r.prezzo_out),
                          "espo": 1.0, "ris": round(r.mossa * 100, 1), "motivo": r.perche_esce.split(":")[0]} for r in v2.itertuples()]
out = {"date": [str(d.date()) for d in idx], "serie": S, "meta": META, "operazioni": T, "aggiornato": str(idx[-1].date())}
(ROOT / "tool" / "data.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
print(len(S), "serie,", round((ROOT / "tool" / "data.json").stat().st_size / 1024), "KB")
