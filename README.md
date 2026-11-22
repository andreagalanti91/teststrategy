# teststrategy

Confronto di strategie di trading con backtest dal 01/01/2021, a partire dall'analisi del repo
[`andreagalanti91/radar`](https://github.com/andreagalanti91/radar).

**Report: [`STRATEGIE.md`](STRATEGIE.md)** — sintesi, confronto, robustezza, proposta e domande aperte.

```bash
pip install pandas numpy matplotlib
```

```bash
python backtest/run_all.py
```

```bash
python backtest/build_report.py
```

`run_all.py` riscrive `results/` (tabelle, CSV, grafici); `build_report.py` ricompone `STRATEGIE.md` da
`backtest/report_template.md` e dalle tabelle generate. I dati in `data/` sono copie congelate dei dataset del repo radar
(commit `da61c5a`); `vendor/radar_weekly.py` è una copia non modificata di `radar/weekly.py`.

Ricerca su dati storici, non una raccomandazione d'investimento.
