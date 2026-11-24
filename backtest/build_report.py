"""Compone i report: testo dei template + tabelle generate dagli script."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JOBS = ((["results/tables.md"], "backtest/report_template.md", "STRATEGIE.md"),
        (["results/intraday/tables.md"], "backtest/intraday_template.md", "INTRADAY.md"),
        (["results/tao/tables.md", "results/tao/tables_macd.md"], "backtest/swing_template.md", "SWING.md"),
        (["results/algo/tables.md"], "backtest/algo_template.md", "ALGORITMO.md"),
        (["results/btc/tables.md"], "backtest/btc_template.md", "ANALISI_BTC.md"),
        (["results/regole/tables.md"], "backtest/regole_template.md", "REGOLE_AT.md"),
        (["results/w32/tables.md"], "backtest/w32_template.md", "CONFRONTO_W32.md"),
        (["results/w32_inout/tables.md"], "backtest/w32_inout_template.md", "W32_INGRESSI_USCITE.md"),
        (["results/liq/tables.md"], "backtest/liq_template.md", "LIQUIDAZIONI.md"))
for tables, template, out in JOBS:
    src = "\n".join((ROOT / t).read_text() for t in tables)
    parts = re.split(r"^## ([A-Z]\d+) .*$", src, flags=re.M)
    tabs = {parts[i]: parts[i + 1].strip() for i in range(1, len(parts), 2)}
    txt = (ROOT / template).read_text()
    for k, v in tabs.items():
        txt = txt.replace("{{" + k + "}}", v)
    assert "{{" not in txt, f"segnaposto non sostituito in {template}"
    (ROOT / out).write_text(txt)
    print(out, len(txt.splitlines()), "righe")
