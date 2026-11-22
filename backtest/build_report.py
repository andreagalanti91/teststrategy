"""Compone STRATEGIE.md e INTRADAY.md: testo dei template + tabelle generate (results/tables.md, results/intraday/tables.md)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for tables, template, out in (("results/tables.md", "backtest/report_template.md", "STRATEGIE.md"),
                              ("results/intraday/tables.md", "backtest/intraday_template.md", "INTRADAY.md")):
    parts = re.split(r"^## ([TI]\d) .*$", (ROOT / tables).read_text(), flags=re.M)
    tabs = {parts[i]: parts[i + 1].strip() for i in range(1, len(parts), 2)}
    txt = (ROOT / template).read_text()
    for k, v in tabs.items():
        txt = txt.replace("{{" + k + "}}", v)
    assert "{{" not in txt, f"segnaposto non sostituito in {template}"
    (ROOT / out).write_text(txt)
    print(out, len(txt.splitlines()), "righe")
