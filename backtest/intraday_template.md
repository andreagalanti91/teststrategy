# Strategia intraday su BTC · backtest dal 2018

Richiesta: strategia intraday solo su BTC, su OKX, leva fino a 5x, drawdown fino a −35%, circa il 70% di operazioni vincenti
in un backtest che parta dal 2018. Data del report: 22/11/2026. Seguito di [`STRATEGIE.md`](STRATEGIE.md).

> Ricerca su dati storici, non una raccomandazione d'investimento.

## 1. Sintesi

**Non ho trovato una strategia intraday su BTC che rispetti i vincoli e guadagni. Il consiglio è di non operare intraday con
queste regole.**

- Ho testato 5 famiglie di regole e 1.224 configurazioni dal 03/2018 al 11/2026, con i costi di OKX.
- **Il 70% di operazioni vincenti è facile**: 535 configurazioni lo raggiungono nel 2018–21. Basta un target più vicino dello
  stop. Con ingressi scelti a caso e le stesse uscite si ottiene il 67%.
- **Guadagnare no**: solo 3 configurazioni su 1.224 chiudono in positivo sia nel 2018–21 sia nel 2022–26, tutte con un
  guadagno medio per trade di 0,02–0,03%, indistinguibile da zero.
- Il candidato scelto con i dati 2018–21 (ritracciamento a 4 ore nel trend settimanale) ha il 70% di vincenti, ma nel 2022–26
  perde il 10% l'anno a leva 1x. Dal 2018 a oggi 10.000 $ diventano 9.604 $ con drawdown −49,8%. Con leva 5x il capitale si
  azzera quasi del tutto (−99,4%).
- Il motivo è aritmetico: con il 70% di vincenti la perdita media (−2,6%) è più del doppio della vincita media (+1,2%), e i
  costi di andata e ritorno (0,09–0,14% del controvalore) valgono circa un decimo della vincita media.

L'unica strategia già misurata che rispetta quattro dei cinque vincoli (solo BTC, OKX, leva ≤ 5x, drawdown ≤ −35%) con più
del 70% di vincenti è **W3 del repo radar a leva 2x**: 12 trade vincenti su 13, +82% annuo e drawdown −35,2% dal 2021. Non è
intraday: fa 2–3 operazioni l'anno. Dettagli in [`STRATEGIE.md`](STRATEGIE.md), capitolo 7.1.

## 2. Dati e regole di simulazione

| Aspetto | Scelta |
|---|---|
| Prezzi | Binance spot BTCUSDT a 15 minuti dal 08/2017 (archivio pubblico), serie principale perché parte prima del 2018. Perp OKX BTC-USDT-SWAP a 15 minuti dal 16/12/2019 (API pubblica), usato come verifica: OKX non pubblica storia precedente. |
| Periodi | Scelta dei parametri solo su 03/2018–12/2021; verifica su 01/2022–11/2026, mai usato per scegliere. |
| Segnali | Su candele orarie o a 4 ore chiuse; ingresso all'apertura dei 15 minuti successivi. |
| Uscite | Target e stop fissati all'ingresso, in multipli dell'ATR; uscita a tempo. Se una candela da 15 minuti tocca entrambi, vale lo stop. |
| Costi OKX (livello base) | Mercato 0,05% + 0,02% di slippage; ordine limite 0,02%; funding 0,01% ogni 8 ore. |
| Una posizione alla volta | Sì. Il capitale è valutato anche al punto peggiore dentro ogni trade, per non sottostimare il drawdown. |
| Trend | Giornaliero (chiusura sopra o sotto la media a 50, 100, 200 giorni) oppure settimanale come in radar (SMA 40 ed EMA 20 settimanali). Long solo con trend rialzista, short solo con trend ribassista. |

## 3. Le cinque famiglie

{{I1}}

"Guadagna" = rendimento medio per trade positivo dopo i costi. "Miglior t" è la statistica t del rendimento medio per trade
della configurazione migliore nel 2018–21: sotto 2 non è distinguibile dal caso, e qui è il massimo fra centinaia di prove.

Lettura:

- Le regole sull'ora del giorno e sulle rotture non guadagnano in nessun periodo.
- Gli ordini limite contro il movimento guadagnano nel 2018–21 in 43 configurazioni e nel 2022–26 in nessuna.
- Il ritracciamento a 4 ore è l'unica famiglia con qualche configurazione positiva in entrambi i periodi (3 su 324).

## 4. I due candidati

Scelti con una regola fissata prima: fra le configurazioni con almeno il 65% di vincenti e 100 trade nel 2018–21, quella con
la statistica t più alta in ogni famiglia promettente.

| | A · Ritracciamento a 4 ore (scelto) | B · Ordine limite |
|---|---|---|
| Trend | settimanale, come W3 di radar | chiusura giornaliera sopra o sotto la media a 50 giorni |
| Ingresso long | RSI(14) a 4 ore chiude sotto 35 con trend rialzista: acquisto a mercato | a ogni ora, acquisto limite 1 ATR orario sotto l'ultima chiusura, valido un'ora |
| Ingresso short | RSI(14) a 4 ore chiude sopra 65 con trend ribassista | vendita limite 1 ATR sopra, con trend ribassista |
| Target | 0,75 ATR a 4 ore | 1,5 ATR orari |
| Stop | 4 ATR a 4 ore | 3 ATR orari |
| Durata massima | 24 ore | 48 ore |

{{I2}}

Anno per anno:

{{I3}}

Il candidato A mantiene il 58–82% di vincenti ogni anno, ma dal 2022 chiude in perdita tre anni su cinque e gli altri due sono vicini a zero.

## 5. Verifiche

### 5.1 Costi

{{I4}}

Anche a costi zero il candidato A perde nel 2022–26: il problema non sono solo le commissioni. Il candidato B a costi zero è
in pareggio nel 2022–26; ai costi base di OKX perde il 24% l'anno perché fa 456 operazioni l'anno.

### 5.2 Ingressi casuali

Stesse uscite, stesso verso del trend, stesso numero di ingressi, ma in ore scelte a caso (200 estrazioni, 2018–2026):

{{I5}}

Il 67% di vincenti arriva dalla sola struttura delle uscite. Il segnale RSI aggiunge 3 punti di vincenti e circa 0,1% per
trade rispetto al caso: un vantaggio reale ma più piccolo dei costi.

### 5.3 Dati OKX

{{I6}}

Sul perp di OKX i risultati sono gli stessi di Binance spot: la conclusione non dipende dalla fonte dei prezzi.

### 5.4 Leva e drawdown

{{I7}}

Nessun candidato resta entro −35% di drawdown nemmeno a leva 1x. Per rispettare il vincolo servirebbe investire metà del
capitale (A) o un quarto (B), su una strategia che comunque perde.

## 6. Perché succede

1. **Vincenti e guadagno sono due cose diverse.** Un 70% di vincenti con vincita +1,2% e perdita −2,6% rende
   0,7 × 1,2 − 0,3 × 2,6 = +0,06% lordo per trade; bastano 2–3 punti di vincenti in meno per andare in perdita.
2. **I costi pesano in proporzione al movimento cercato.** Su un target di 0,5–1,5% l'andata e ritorno su OKX costa 0,09–0,14%.
   Su un trade settimanale da +20% lo stesso costo è trascurabile.
3. **Il vantaggio intraday su BTC si è ridotto dopo il 2021.** Le stesse regole che guadagnavano nel 2018–21 perdono dopo,
   in tutte le famiglie. È coerente con il repo radar, che ha già scartato l'intraday due volte (lezioni 78 e 82) con dati
   2020–2026 e anche con flussi e open interest.
4. **La leva non crea rendimento.** Moltiplica un rendimento atteso negativo e porta il trade peggiore da −9,5% a −47,7%
   del capitale a 5x.

## 7. Cosa propongo

| Opzione | Rispetta i vincoli? | Risultato misurato |
|---|---|---|
| **W3 di radar a leva 2x su OKX** (long metà spot e metà perp, short in perp) | BTC, OKX, leva 2x, DD −35,2%, 92% di vincenti. Non intraday, backtest dal 2021 | 10.000 → 334.535 $, +82% annuo; attesa realistica 55–65% annuo (stima) |
| W3 a leva 1x, rischio 25% | Come sopra, DD −21,1% | +42% annuo |
| Intraday, candidato A o B | 70% di vincenti sì; drawdown e rendimento no | perde dal 2022 |

Se l'intraday resta un obiettivo, le strade che non ho potuto testare e che hanno qualche probabilità sono:

1. **Intraday solo come esecuzione di W3**: usare le regole intraday per scegliere il prezzo d'ingresso e di uscita dei
   segnali settimanali, non per generare operazioni. Non aumenta il numero di trade, può migliorare i prezzi.
2. **Dati che il prezzo non contiene**: book, liquidazioni e flussi in tempo reale. Radar li raccoglie da poche settimane e
   finora non ha trovato vantaggio; servono mesi di storia.
3. **Costi da market maker**: con commissioni maker a zero o negative il candidato B passa da −3,7% a +17% annuo sul periodo
   intero, ma resta in perdita nel 2022–26 e con drawdown −63%. Non basta.

## 8. Limiti

- 1.224 configurazioni provate: i pochi risultati positivi sono compatibili con il caso.
- Prima del 12/2019 i prezzi sono Binance spot, non OKX; il funding è una media fissa (0,01% ogni 8 ore), non lo storico.
- Slippage fisso; nei movimenti violenti gli stop a mercato si eseguono peggio di quanto simulato.
- Gli ordini limite sono considerati eseguiti solo se il prezzo li attraversa: ipotesi prudente ma non una simulazione della
  coda degli ordini.
- Non ho testato regole basate su flussi, open interest o liquidazioni, già scartate da radar su dati 2020–2026.
- W3 a leva 2x: 13 trade dal 2021, nessun dato prima; vedi i limiti in `STRATEGIE.md`.

## 9. Domande

1. **L'intraday è un requisito o un mezzo?** Se l'obiettivo è il rendimento con il 70% di vincenti, W3 a leva 2x lo ottiene
   con 2–3 operazioni l'anno. Se l'obiettivo è operare ogni giorno, i dati dicono che costa.
2. **Vuoi che testi W3 a leva 2x sui sette giorni di decisione** e con l'esecuzione intraday degli ingressi? È il prossimo
   passo con più valore.
3. **Che livello di commissioni hai su OKX?** Con il livello base l'intraday è escluso; un livello VIP cambia poco.

## 10. Riproducibilità

```bash
python backtest/fetch_intraday.py
```

```bash
python backtest/intraday_research.py
```

```bash
python backtest/intraday_final.py
```

```bash
python backtest/build_report.py
```

Il primo comando richiede accesso a `data.binance.vision` e `www.okx.com`; i dati scaricati sono già in `data/intraday/`.
La griglia completa richiede circa 30 minuti. Risultati in `results/intraday/`: una griglia per famiglia
(`griglia_*.csv`), i trade dei due candidati (`trades_A.csv`, `trades_B.csv`), il placebo e le tabelle di questo report.
