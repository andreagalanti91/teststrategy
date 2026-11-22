"""Compone STRATEGIE.md: testo di report_template.md + tabelle generate da run_all.py (results/tables.md)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
parts = re.split(r"^## (T\d) .*$", (ROOT / "results" / "tables.md").read_text(), flags=re.M)
tabs = {parts[i]: parts[i + 1].strip() for i in range(1, len(parts), 2)}
txt = (ROOT / "backtest" / "report_template.md").read_text()
for k, v in tabs.items():
    txt = txt.replace("{{" + k + "}}", v)
assert "{{" not in txt, "segnaposto non sostituito"
(ROOT / "STRATEGIE.md").write_text(txt)
print(len(txt.splitlines()), "righe")
