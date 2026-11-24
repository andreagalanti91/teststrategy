"""Prepara export/radar-opzioni/: registro iniziale, storico con prezzi veri, esempi dell'uscita di build() e pagina di riferimento."""
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
EXP = ROOT / "export" / "radar-opzioni"
sys.path.insert(0, str(EXP))
import opzioni as O

UTC = timezone.utc
ORA = datetime(2026, 11, 24, 17, 40, tzinfo=UTC)
CAP = 45000.0
cat = O.carica_catena(str(EXP / "catena_2026-11-24.csv.gz"))

# registro iniziale: la posizione short di W3.2 aperta il 16/11. Il contratto della regola quel giorno era la put 65.000 con scadenza 11/12
# (25 giorni); il gemello lineare non ha scambi, quindi il prezzo d'ingresso viene dall'apertura del 16/11 del contratto inverso: 0,0425 BTC x 65.286 $.
px_in = round(0.0425 * 65285.7, 2)
fee = min(O.FEE * 65285.7, O.FEE_CAP * px_in)
n = int(CAP * O.QUOTA / ((px_in + fee) * O.CONTRATTO_BTC))
seed = [{"chiave": "2026-11-15|short", "verso": "short", "segnale": "2026-11-15", "entra": "2026-11-16", "prezzo_btc_in": 65285.7, "capitale": CAP, "quota": O.QUOTA,
         "stato": "aperta", "id": "BTC-USD_UM-261211-65000-P", "tipo": "put", "strike": 65000.0, "scadenza": "2026-12-11", "scadenza_iso": "2026-12-11T08:00:00+00:00",
         "registrata": "2026-11-16T00:00+00:00", "prezzo_in": px_in, "vol_in_pct": None, "contratti": n, "btc": round(n * O.CONTRATTO_BTC, 2),
         "spesa": round(n * O.CONTRATTO_BTC * (px_in + fee), 2),
         "nota": "ricostruita: prezzo d'ingresso dall'apertura del 16/11 del contratto inverso BTC-USD-261211-65000-P su OKX (0,0425 BTC × 65.286 $); capitale d'esempio 45.000 $"}]
(EXP / "registro_iniziale.json").write_text(json.dumps(seed, ensure_ascii=False, indent=1))

# storico: le 23 operazioni di W3.2 rifatte con gli scambi veri di Deribit
o = pd.read_csv(ROOT / "results" / "opzioni_w32" / "operazioni_reale.csv")
sto = [{"n": int(r.n), "verso": r.verso, "entra": r.entra, "esce": r.esce, "contratto": r.contratto, "giorni": int(r.gg), "vol_pct": round(r.iv_vera * 100),
        "w32_pct": round(r.w32 * 100, 1), "opzione_pct": round(0.05 * (r.mult - 1) * 100, 1)} for r in o.itertuples()]
(EXP / "storico_prezzi_veri.json").write_text(json.dumps(sto, ensure_ascii=False, indent=1))
o.to_csv(EXP / "storico_prezzi_veri.csv", index=False)

w3 = {"status": "aperto", "side": "short", "signal_date": "2026-11-15", "entry": "2026-11-16", "entry_px": 65285.7, "price": 60144.0, "capital": CAP}
oggi = O.build(w3, cat, seed, ORA, storico=sto)
(EXP / "esempio_sezione.json").write_text(json.dumps(oggi, ensure_ascii=False, indent=1))
seg = O.build({"status": "segnale", "side": "long", "signal_date": "2026-11-22", "price": 60144.0, "capital": CAP}, cat, [], ORA, storico=sto)
(EXP / "esempio_segnale.json").write_text(json.dumps(seg, ensure_ascii=False, indent=1))
att = O.build({"status": "nessuno", "price": 60144.0, "capital": CAP}, cat, [], ORA)
(EXP / "esempio_attesa.json").write_text(json.dumps(att, ensure_ascii=False, indent=1))

for f in ("OPZIONI_W32.md",):
    shutil.copy(ROOT / f, EXP / f)
shutil.copy(ROOT / "results" / "opzioni_w32" / "opzioni_w32.png", EXP / "opzioni_w32.png")
shutil.copy(ROOT / "backtest" / "fetch_okx_options.py", EXP / "fetch_okx_options.py")

tpl = (ROOT / "backtest" / "export_opzioni_pagina.html").read_text()
(EXP / "riferimento_sezione.html").write_text(tpl.replace("/*DATI*/", "const STATI = " + json.dumps({"oggi": oggi, "segnale": seg}, ensure_ascii=False) + ";"))
p = oggi["posizione"]
print("oggi:", oggi["azione"], p["id"], "in", p["prezzo_in"], "ora", p["prezzo_ora"], "risultato", p["risultato"], p["risultato_pct"], "% · contratti", p["contratti"], "spesa", p["spesa"])
print("segnale:", seg["azione"], seg["proposta"]["contratto"]["id"], seg["proposta"]["quantita"])
