# BTC · analisi tecnica, sentiment e algoritmo long/short

Fondamenti dell'analisi tecnica, lettura tecnica e di sentiment di BTC al 22/11/2026, e un algoritmo long/short costruito
sugli indicatori e testato dal 2018. Data del report: 23/11/2026.

> Ricerca su dati storici, non una raccomandazione d'investimento.

## 1. Sintesi

**BTC è in trend ribassista su tutte le scale e l'algoritmo oggi è fuori dal mercato: né long né short.**

| | |
|---|---|
| Prezzo | 61.271 $, a −51% dal massimo storico di 126.200 $ (06/10/2025) |
| Trend | 15 indicatori su 17 sono short; prezzo sotto le medie a 50 e 200 giorni e a 40 e 200 settimane |
| Momentum | RSI giornaliero 27 (ipervenduto), settimanale 35; MACD sotto il segnale su entrambe le scale |
| Supporti | 60.000, 57.800 (con Fibonacci 61,8%), 56.550; sotto, 49.000 |
| Resistenze | 63.000–69.000 (nodi di volume e massimo del 2021), poi 71.000–72.400 (medie a 200 giorni e 40 settimane) |
| Sentiment | paura estrema (Fear & Greed 11), ma i conti retail sono più long del solito |
| Algoritmo | fuori dal 29/10/2026; il segnale short non è scattato perché manca l'ultimo consenso |

L'algoritmo, in tre righe:

1. **Regola**: voto di 17 indicatori di trend; long con voto ≥ 0,50, short con voto ≤ −0,90, uscita quando il voto rientra.
2. **Risultato dal 2018**: 10.000 $ → 184.406 $, +38,8% annuo, drawdown −49,4%, 30 operazioni, 47% vincenti. Nel periodo di
   verifica 2022–26, mai usato per scegliere i parametri: +17% annuo con drawdown −34%, contro +5% e −67% di BTC tenuto.
3. **Limite principale**: gli short non rendono. I 7 short fatti dal 2018 hanno composto x0,97; tutto il guadagno viene dai
   long. Per restare entro −35% di drawdown su tutto lo storico serve usare metà capitale (0,5x: +21% annuo, −27%).

Rispetto ai tuoi obiettivi: il 70% di operazioni vincenti non è raggiunto (47%), e la leva peggiora il risultato già da 2x.

![BTC settimanale](results/btc/btc_tecnica.png)

## 2. Fondamenti dell'analisi tecnica

**I principi** (teoria di Dow, sistematizzata da Edwards, Magee e Murphy):

| Principio | Significato operativo |
|---|---|
| Il prezzo sconta tutto | si analizza il prezzo, non le notizie |
| I prezzi si muovono in trend | tre scale: primario (mesi-anni), secondario (settimane), minore (giorni) |
| Un trend vale fino a prova contraria | si segue finché non compare un segnale di inversione, non si anticipa |
| Il volume conferma il trend | un movimento senza volume è sospetto |
| Le medie si confermano a vicenda | un segnale conta di più se più indicatori indipendenti concordano |
| Supporti e resistenze | livelli dove in passato domanda o offerta hanno fermato il prezzo; un supporto rotto diventa resistenza |

**Le famiglie di indicatori** e a cosa servono:

| Famiglia | Esempi | Domanda a cui risponde | Debolezza |
|---|---|---|---|
| Trend | medie mobili, Ichimoku, Supertrend, ADX | in che direzione va il mercato? | arriva in ritardo, soffre nei mercati laterali |
| Momentum | MACD, RSI rispetto a 50, variazione a N giorni | il trend accelera o rallenta? | molti falsi segnali sulle scale corte |
| Rottura | canali di Donchian, bande di Bollinger | il prezzo esce da un intervallo? | le false rotture sono frequenti |
| Volume | OBV | i volumi accompagnano il movimento? | i volumi delle borse crypto sono rumorosi |
| Oscillatori contrarian | RSI 30/70, ritorno alle bande | il movimento è eccessivo? | in un trend forte restano "estremi" a lungo |
| Sentiment | Fear & Greed, funding, long/short | la folla è tutta da una parte? | descrive, raramente anticipa |

**Cosa dice la ricerca**:

- Park e Irwin (2007) hanno passato in rassegna 95 studi moderni: 56 trovano risultati positivi per le regole tecniche, 20
  negativi, 19 misti. Segnalano però che molti studi soffrono di selezione a posteriori delle regole.
- Le regole a medie mobili di Brock, Lakonishok e LeBaron (1992) funzionavano sul Dow Jones fino al 1986; Sullivan, Timmermann
  e White hanno mostrato che nei dieci anni successivi il vantaggio era sparito.
- Su Bitcoin, Detzel e coautori trovano potere predittivo nelle medie mobili da 5 a 100 giorni; uno studio su circa 15.000
  regole riporta rendimenti corretti per il rischio superiori al comprare e tenere, soprattutto per la riduzione dei
  drawdown. Gli studi che correggono per i test multipli trovano risultati più deboli, e gli indicatori contrarian (RSI,
  Bollinger) in genere sotto il comprare e tenere.

In breve: le regole che seguono il trend hanno un fondamento empirico, soprattutto come protezione dai ribassi; gli
oscillatori usati contro il trend no; e qualunque risultato va verificato su dati non usati per sceglierlo. Il censimento
qui sotto conferma tutti e tre i punti su BTC.

## 3. Censimento di 20 indicatori su BTC

Ogni indicatore usato da solo: long quando è rialzista, short quando è ribassista. Long in spot, short in perp con funding
reale, costi 0,10% per lato. Due periodi separati.

{{B1}}

Cosa si impara:

1. **Nessun indicatore da solo è affidabile come long/short.** Solo due (Ichimoku e OBV) guadagnano oltre il 10% annuo in
   entrambi i periodi, con drawdown oltre −50%.
2. **Il lato short è il problema.** Usati solo long, tutti e 17 gli indicatori di trend chiudono in guadagno in entrambi i
   periodi.
3. **I contrarian perdono sempre**: RSI 30/70, ritorno alle bande di Bollinger e Fear & Greed al contrario perdono in
   entrambi i periodi. Comprare l'ipervenduto e vendere l'ipercomprato su BTC non ha funzionato.
4. **I risultati cambiano molto fra i due periodi.** Gli indicatori veloci (Donchian 20 giorni, Bollinger, Supertrend)
   brillano nel 2018–21 e si spengono dopo; quelli lenti (medie a 200 giorni e 40 settimane) fanno il contrario.
5. **Le percentuali di vincenti sono basse** (19–44% per le regole di trend): guadagnano con poche operazioni grandi.

Per questo l'algoritmo non sceglie l'indicatore migliore: usa il voto di tutti.

## 4. BTC oggi: analisi tecnica

{{B7}}

Lettura:

- **Trend primario ribassista.** Il prezzo è sotto tutte le medie principali, compresa quella a 200 settimane (68.176 $), un
  livello raggiunto in passato solo nelle fasi avanzate dei mercati ribassisti (2018–19 e 2022). L'ADX a 49 con −DI molto sopra +DI indica un ribasso forte, non
  un mercato laterale.
- **Ipervenduto di breve.** RSI giornaliero a 27 e −25% in 30 giorni. Nei dati questo non è un segnale d'acquisto (capitolo
  3), ma rende probabile un rimbalzo tecnico verso le resistenze.
- **La media a 50 giorni è ancora sopra quella a 200**: con il prezzo a −20% dalla prima, l'incrocio al ribasso ("death
  cross") è vicino.

Livelli, dal più alto al più basso:

{{B8}}

- **Supporto decisivo: 55.000–58.000 $.** Qui cadono il ritracciamento del 61,8% del ciclo, i minimi di luglio 2026 e di
  maggio 2024 e il minimo del canale a 20 settimane (55.130 $). Una chiusura settimanale sotto apre lo spazio fino a 49.000 $.
- **Prima resistenza: 63.000–69.000 $**, la fascia più scambiata dal 2024, chiusa in alto dal massimo del 2021.
- **Resistenza di trend: 71.000–72.400 $** (medie a 200 giorni e 40 settimane, Fibonacci 50%). Finché il prezzo resta sotto,
  ogni rialzo è un rimbalzo dentro un trend ribassista.

Il voto dei singoli indicatori oggi:

{{B9}}

## 5. Sentiment

{{C1}}

Dalle notizie degli ultimi giorni: il Fear & Greed è sceso fino a 9 il 20/11 (6 sull'indice di CoinMarketCap il 21/11); il
20/11 sono state liquidate posizioni per circa 1,5 miliardi di dollari; il 19/11 gli ETF spot su Bitcoin hanno registrato
deflussi per 582 milioni di dollari. Anche l'indice di paura sulle azioni (CNN) è a 14.

Lettura:

- **Paura estrema, ma senza capitolazione dei conti retail.** Il rapporto long/short dei conti è a 2,63 contro una media di
  1,66: molti piccoli conti stanno comprando il ribasso a leva. È carburante per altre liquidazioni se il supporto cede.
- **Funding intorno a zero**: non c'è l'eccesso di short che di solito precede un rimbalzo violento.
- **Open interest in calo moderato** (−5% in 30 giorni): la leva si sta riducendo, ma non è stata azzerata.

Che cosa è successo in passato dopo letture simili, dal 2018:

{{B6}}

- **La paura estrema non è un segnale d'acquisto.** Dopo un Fear & Greed sotto 25 i rendimenti a 30 e 90 giorni sono stati
  uguali o peggiori della media. Sotto 10, come oggi, sono nella media: +3% a 30 giorni, positivi nel 55% dei casi.
- **Il sentiment su BTC segue il trend, non lo anticipa**: i rendimenti migliori sono arrivati dopo l'avidità estrema
  (sopra 90), non dopo la paura.
- **Il funding negativo è l'unico segnale contrarian con qualche valore** (+8% medio a 30 giorni, 67% positivi, 31 episodi).
  Oggi è a zero, non negativo.

Conclusione sul sentiment: descrive bene la situazione, ma da solo non giustifica un acquisto. Un filtro che vieta nuovi
short con Fear & Greed sotto 20 migliora l'algoritmo di meno di un punto l'anno: non l'ho incluso.

## 6. L'algoritmo long/short

### 6.1 Regole

| | Regola |
|---|---|
| **Voto** | 17 indicatori di trend, momentum, rottura e volume (tutti quelli del censimento tranne i contrarian e il sentiment). Ognuno vale +1 se rialzista, −1 se ribassista, 0 se neutro. Voto = media, da −1 a +1. |
| **Long** | voto ≥ 0,50: almeno 13 indicatori rialzisti su 17 quando gli altri sono ribassisti. Acquisto spot. |
| **Short** | voto ≤ −0,90: almeno 16 ribassisti su 17 e nessuno rialzista. Vendita sul perp. |
| **Uscita** | long: voto sotto 0,25. Short: voto sopra −0,25. |
| **Frequenza** | controllo alla chiusura giornaliera (00:00 UTC), operazione all'apertura successiva |
| **Dimensione** | 1x del capitale dedicato; nessuna leva |

{{B2}}

- **Tutti e 17 gli indicatori entrano nel voto**: non ho scelto i migliori, per non adattare la regola al passato.
- **La soglia short è molto più severa di quella long**: l'ha scelta il periodo 2018–21, e riflette il censimento.
- **La volatilità obiettivo riduce il drawdown** da −49% a −38% togliendo 7 punti di rendimento annuo.

![Algoritmo](results/btc/btc_algoritmo.png)

### 6.2 Anno per anno

{{B3}}

- Gli short hanno aiutato solo nel 2018 (+28%); nel 2022 il contributo è stato +3% e dal 2025 è negativo.
- Il 2026 è l'anno peggiore (−21%): cinque operazioni, nessuna oltre il +2%, in un mercato senza direzione chiara fino a
  novembre.

### 6.3 Tutte le operazioni

{{B4}}

Tre long (2019, 2020–21, 2023–24) fanno la gran parte del risultato; 16 operazioni su 30 chiudono in perdita, quasi tutte
sotto il 10%.

### 6.4 Leva e drawdown

{{B5}}

- **Il rendimento massimo è intorno a 1,5–2x**; oltre, la leva lo riduce, e a 5x il capitale si azzera.
- **Per restare entro −35% su tutto lo storico serve 0,5x**: +21% annuo con drawdown −27%.

### 6.5 Confronto con W3 del repo radar

{{B0}}

Sullo stesso periodo W3 resta migliore per rendimento, drawdown e percentuale di vincenti. W3 usa un dato in più, il flusso
sul perp, che nei tuoi test è ciò che fa la differenza su BTC. L'algoritmo tecnico ha due vantaggi: si può testare dal 2018 e
usa solo il prezzo.

## 7. Cosa fare adesso secondo l'algoritmo

| Scenario | Condizione | Azione |
|---|---|---|
| Oggi | voto −0,76: 15 short, 2 long | fuori dal mercato |
| Segnale short | voto ≤ −0,90: devono girare anche gli ultimi due indicatori. In pratica una chiusura sotto 55.130 $ (minimo a 20 settimane) insieme all'incrocio al ribasso delle medie a 50 e 200 giorni | short sul perp, 1x |
| Rimbalzo | prezzo verso 63.000–69.000 $ con voto ancora negativo | nessuna azione: è un rimbalzo dentro il trend ribassista |
| Segnale long | voto ≥ 0,50: richiede in pratica il prezzo stabilmente sopra 72.000 $ (medie a 200 giorni e 40 settimane) | acquisto spot |

Questo coincide con W3.1 di radar, che è short dal 16/11, e con l'algoritmo sulle altcoin di `ALGORITMO.md`, che non
ammette acquisti finché BTC è sotto la media a 40 settimane.

## 8. Limiti

- **Parametri scelti su quattro anni** (2018–21) e verificati su cinque: la verifica è reale, ma il periodo è uno solo e il
  rendimento è sceso dal 70% al 17% annuo.
- **30 operazioni in nove anni**: poche per stimare con precisione la percentuale di vincenti o il valore degli short (7).
- **Dati**: prezzi Binance spot; funding reale dal 2020 e fisso (0,01% ogni 8 ore) prima; nessun dato OKX prima del 12/2019.
- **Esecuzione** alla chiusura giornaliera, con slippage fisso: nei movimenti violenti l'esecuzione reale è peggiore.
- **Il sentiment** usa l'indice Fear & Greed, il funding e i rapporti long/short di Binance raccolti dal repo radar; i dati
  sulle notizie degli ultimi giorni vengono da fonti di settore non verificate una per una.
- I livelli di supporto e resistenza sono descrittivi: nel repo radar le strategie costruite sui livelli non hanno funzionato.
- Tasse non considerate.

## 9. Riproducibilità

```bash
python backtest/fetch_intraday.py binance
```

```bash
python backtest/btc_report.py
```

```bash
python backtest/build_report.py
```

Codice: `backtest/btc_ta.py` (dati, indicatori, voto, motore), `backtest/btc_report.py` (tabelle e grafici). Risultati in
`results/btc/`: `censimento_indicatori.csv`, `griglia_composito.csv` (le 104 combinazioni di soglie), `trade_long_short.csv`,
`livelli.csv`.

## Fonti

- [Park, Irwin — What do we know about the profitability of technical analysis? (Journal of Economic Surveys, 2007)](https://econpapers.repec.org/RePEc:bla:jecsur:v:21:y:2007:i:4:p:786-826) · [versione di lavoro](https://farmdoc.illinois.edu/publications/the-profitability-of-technical-analysis-a-review)
- [Park, Irwin — technical trading rules in US futures markets, con correzione per data snooping](https://ageconsearch.umn.edu/record/19039/files/cp05pa01.pdf)
- [Federal Reserve Bank of St. Louis — rassegna sulle regole tecniche (2011)](https://fraser.stlouisfed.org/docs/publications/frbsl_wp/2011-001.pdf)
- [Technical trading in cryptocurrency markets, circa 15.000 regole (Annals of Operations Research)](https://link.springer.com/article/10.1007/s10479-019-03357-1)
- [Technical trading rules' profitability and dynamic risk premiums of cryptocurrency exchange rates](https://emerald.com/insight/content/doi/10.1108/JCMS-10-2021-0030) · [studio su 12 criptovalute con controllo del data snooping](https://eprints.gla.ac.uk/302711/1/302711.pdf)
- [Bitcoin Magazine Pro — How good is the Bitcoin Fear & Greed Index](https://bmpro.substack.com/p/how-good-is-the-bitcoin-fear-and) · [KuCoin — what happens when the index hits extreme fear](https://www.kucoin.com/blog/what-happens-when-the-crypto-fear-greed-index-hits-extreme-fear)
- Notizie del 19–22/11/2026: [KuCoin — Bitcoin falls below $56,000, index at 6](https://www.kucoin.com/news/flash/bitcoin-falls-below-56-000-as-fear-and-greed-index-hits-6) · [Crypto Briefing — index falls to 14](https://cryptobriefing.com/fear-greed-index-falls-to-14-extreme-fear/) · [Bitcoin World — Bitcoin slips under $60,000](https://bitcoinworld.co.in/bitcoin-below-60k-extreme-fear/) · [Bitcoin.com — fear hits extreme levels](https://news.bitcoin.com/market-updates/bitcoin-fear-hits-extreme-levels-analyst-sees-contrarian-signal/) · [TokenPost — price recovers $61,000](https://www.tokenpost.com/news/investing/62408)
