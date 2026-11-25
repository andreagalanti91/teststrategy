# teststrategy

Confronto di strategie di trading con backtest dal 01/01/2021, a partire dall'analisi del repo
[`andreagalanti91/radar`](https://github.com/andreagalanti91/radar).

- **[`STRATEGIE.md`](STRATEGIE.md)** — confronto di 16 strategie e 4 portafogli dal 2021, robustezza, proposta e domande aperte.
- **[`OPZIONI_W32.md`](OPZIONI_W32.md)** — le opzioni da zero, la strategia "una call o una put a ogni segnale di W3.2", backtest, confronto con i prezzi veri di OKX, da dove operare.
- **[`RICERCA_NUOVA.md`](RICERCA_NUOVA.md)** — cosa manca: affidabilità statistica dei risultati (Sharpe deflazionato), leva (Kelly), premio di volatilità, opzioni vendute e comprate.
- **[`LIVELLI_BTC.md`](LIVELLI_BTC.md)** — supporti, resistenze e liquidazioni di BTC oggi; cosa succede quando un supporto cede.
- **[`LIQUIDAZIONI.md`](LIQUIDAZIONI.md)** — il prezzo di BTC segue le liquidazioni? Come verificarlo, risultati, lettura della mappa di Coinglass.
- **[`W32_INGRESSI_USCITE.md`](W32_INGRESSI_USCITE.md)** — W3.2 operazione per operazione: quando entra, quando esce, prove di DCA in ingresso e in uscita.
- **[`CONFRONTO_W32.md`](CONFRONTO_W32.md)** — algoritmi di analisi tecnica contro W3.2 del radar, con l'elenco di tutte le movimentazioni.
- **[`REGOLE_AT.md`](REGOLE_AT.md)** — come funziona l'analisi tecnica, 15 regole classiche verificate su BTC, regole operative, nuovo algoritmo a tre schermi, confronto e motivo di ogni operazione.
- **[`ANALISI_BTC.md`](ANALISI_BTC.md)** — fondamenti dell'analisi tecnica, lettura tecnica e di sentiment di BTC, algoritmo long/short a voto di 17 indicatori con backtest dal 2018.
- **[`ALGORITMO.md`](ALGORITMO.md)** — l'algoritmo "MACD a regime" costruito sui dati: regole, verifiche, rischio e leva, stato attuale.
- **[`SWING.md`](SWING.md)** — TAO sul supporto e SOL con MACD/RSI: le operazioni reali confrontate con le regole, 165 altcoin, quando vendere, leva.
- **[`INTRADAY.md`](INTRADAY.md)** — ricerca di una strategia intraday su BTC per OKX dal 2018: 5 famiglie, 1.224 configurazioni, verifiche.

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


Esportazioni per il repo radar: `export/radar-v1/` (switch W3.2 · v1 · Confronto), `export/radar-opzioni/` (sezione "Opzioni": prompt, modulo, test, dati) e `export/radar-livelli/` (sezione "Livelli").

Strumento di confronto: `tool/index.html` con `tool/data.json` (rigenerabile con `python backtest/build_tool.py`).
