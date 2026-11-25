"""Prepara export/radar-v1/: esempi di evaluate() e confronto(), file di W3.2 2018-2026, pagina di riferimento."""
import json
import math
import shutil
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
EXP = ROOT / "export" / "radar-v1"
sys.path.insert(0, str(EXP))
import v1 as V

d = pd.read_csv(EXP / "btc_giornaliero.csv", index_col=0, parse_dates=True)
eq = pd.read_csv(ROOT / "results" / "w32" / "equity.csv", index_col=0, parse_dates=True)["W3.2 radar (rischio 25%)"]
tw = pd.read_csv(ROOT / "results" / "w32" / "movimenti_w32.csv")
tw["esce"] = tw["esce"].where(tw["esce"].notna(), None)
trades = [{k: (None if (isinstance(v, float) and math.isnan(v)) else v) for k, v in r.items()} for r in tw.to_dict("records")]
pd.DataFrame({"date": eq.index.date, "w32_equity": (eq / eq.iloc[0]).round(6)}).to_csv(EXP / "w32_equity_2018_2026.csv", index=False)
tw.to_csv(EXP / "w32_operazioni_2018_2026.csv", index=False)

clean = lambda o: json.loads(json.dumps(o, default=lambda x: None if isinstance(x, float) and not math.isfinite(x) else str(x)).replace("NaN", "null"))
sim = V.simulate(d)
ev = V.evaluate(d, capital=45000.0)
cf = V.confronto(d, eq, trades, sim=sim)
pd.DataFrame(sim["trades"]).to_csv(EXP / "v1_operazioni_2018_2026.csv", index=False)
(EXP / "esempio_v1.json").write_text(json.dumps(clean(ev), ensure_ascii=False))
(EXP / "esempio_confronto.json").write_text(json.dumps(clean(cf), ensure_ascii=False))
w3 = {"stato": "aperto", "verso": "short", "segnale": "2026-11-15", "entra": "2026-11-16", "prezzo_in": 65285.7, "prezzo": float(d["close"].iloc[-1]),
      "stop": "trailing 2,5 ATR settimanali", "esposizione": 0.972}
for f in ("ANALISI_BTC.md", "CONFRONTO_W32.md"):
    shutil.copy(ROOT / f, EXP / f)
tpl = (ROOT / "backtest" / "export_v1_pagina.html").read_text()
ev_light = {k: v for k, v in ev.items() if k != "storico"} | {"storico": {k: v for k, v in ev["storico"].items() if k not in ("eq", "eq_d")}}
(EXP / "riferimento_sezione.html").write_text(tpl.replace("/*DATI*/", "const V1 = " + json.dumps(clean(ev_light), ensure_ascii=False) + ";\nconst CF = "
                                                          + json.dumps(clean(cf), ensure_ascii=False) + ";\nconst W3 = " + json.dumps(w3) + ";"))
m = cf["metriche"][0]["righe"]
print({k: (v["finale_10k"], round(v["cagr"] * 100, 1), round(v["dd"] * 100, 1)) for k, v in m.items()})
print("accordo:", round(cf["accordo"]["stesso_verso_quota"] * 100), "% giorni stesso verso · corr mensile", round(cf["accordo"]["corr_mensile"], 2))
for s in cf["accordo"]["stati"]:
    print(s)
for k, v in cf["affidabilita"].items():
    print(k, {a: round(b, 3) for a, b in v.items()})
