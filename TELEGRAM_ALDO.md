# Canale Telegram "Aldo Qefalia - Trading": strategia ricostruita, risultati veri, versione meccanica

Analisi di tutti i messaggi esportati (11/05/2023 – 18/03/2024), con i grafici e le schermate Bybit allegate. Ogni operazione
è ricostruita sui prezzi reali; poi lo stile del trader è tradotto in una strategia meccanica e verificato dal 2018.

> Ricerca su dati storici, non una raccomandazione d'investimento. L'esportazione ricevuta è incompleta: si ferma al 18/03/2024.

## 1. Sintesi

**Con i prezzi delle sue schermate il trader ha fatto bene: 55 operazioni, 73% in guadagno, +3,4% medio per operazione. Chi
copiava i messaggi in tempo reale ha fatto molto meno: 44% in guadagno e +1,4% medio, con BTC in perdita. In entrambi i casi
meno di chi teneva BTC (×2,5) o seguiva W3.2 (×1,9) nello stesso periodo, a meno di usare leva. La strategia meccanica
costruita sul suo stile non ha vantaggio su otto anni.**

| Domanda | Risposta |
|---|---|
| Che trader è | Discrezionale, su perpetual Bybit a leva 10x (5–14,5x). Operazioni brevi (mediana 19 ore), su 4 ore e 1 ora. BTC long e short, altcoin quasi solo long |
| Che setup usa | Rottura e retest di livelli (orizzontali e diagonali), prese di liquidità sopra i massimi, medie a 200, divergenze RSI, notizie macro. Alt long finché BTC regge |
| Come gestisce | Entra a scalare, chiude metà al primo obiettivo, stop a pareggio molto presto, lascia correre il resto |
| Ha guadagnato? | Sì, con i suoi prezzi: ×5,7 componendo le operazioni con controvalore 1x. Ma 16 operazioni su 55 sono state mostrate solo dopo l'ingresso, quasi tutte già in guadagno (88%) |
| E chi lo seguiva? | ×1,6 con controvalore 1x. Su BTC chi copiava ha perso (33% in guadagno); il risultato viene da poche operazioni su altcoin (DOGE +29%, INJ +11%) |
| Meglio di BTC tenuto? | No: BTC nello stesso periodo ha fatto ×2,5. Con leva 3x chi copiava avrebbe fatto ×3,5, con un rischio molto più alto |
| La sua strategia, resa meccanica, funziona? | No: dal 2018 perde (−5% annuo su BTC e 8 altcoin, −1% solo su BTC), con 42% di operazioni in guadagno e risultato medio di zero volte il rischio. Ingressi casuali con la stessa gestione fanno meglio |

Seconda analisi più approfondita (autenticità delle schermate, chi copiava con ordini limite, strategia scritta come regole,
nuova strategia intraday con Eliz): [`ALDO_ELIZ_INTRADAY.md`](ALDO_ELIZ_INTRADAY.md).

## 2. Il trader, dai suoi messaggi

| Voce | Valore |
|---|---|
| Messaggi letti | 812 (11/05/2023 – 18/03/2024), 458 con grafico o schermata |
| Operazioni a leva ricostruite | 55 (35 su BTC, 20 su altcoin; 34 long, 21 short) |
| Comunicate solo dopo l'ingresso | 16 su 55: chi legge il canale non poteva copiarle |
| Accumuli spot tenuti a parte | 11 (TAO, RNDR, INJ, PYR, 0x0, PAAL, ORAI, ARC, BAI, ETH spot) |
| Piani annunciati prima che il prezzo arrivasse | 142: 47 eseguiti, 71 no, 24 senza esito dichiarato |
| Leva nelle schermate Bybit | da 5,0x a 14,5x, mediana 10x |
| Durata mediana di un'operazione | 19 ore |

### Come lavora

- **Analisi dall'alto in basso**: livelli sul giornaliero e sul settimanale (supporti, resistenze, media a 200 settimanale),
  ingresso sulle 4 ore o sull'ora.
- **Setup preferito**: rottura di un supporto diagonale seguita da un retest negativo, poi short. Lo dice lui stesso
  ("con questo semplice setup almeno 4-5 ottimi short").
- **Altri setup**: presa di liquidità poco sopra un massimo e poi short; riconquista di un livello e poi long ("reclaim
  pulito dei 25,3k"); retest della media a 200 come resistenza; testa-spalle rovesciato; divergenze RSI; riempimento dei gap del
  future CME.
- **Altcoin**: long su INJ, FET, WOO, DOGE, SOL, ETH quando BTC tiene un livello e la dominance di BTC scende. In più accumuli
  spot sul tema intelligenza artificiale (TAO, RNDR, FET, PAAL, 0x0, ORAI, ARC, BAI), tenuti fuori dai trade.
- **Gestione**: entrata a scalare e medie contro il movimento ("DCA dello short"); chiusura del 50% al primo obiettivo, spesso
  80% poco dopo; stop a pareggio quasi subito; stop spesso condizionali ("sopra i 31,4k sono out").
- **Notizie**: CPI, FOMC, SEC contro Binance e Coinbase, sentenza XRP, ETF su BTC ed ETH. Chiude spesso prima degli eventi.
- **Dal 2024 cambia**: quasi solo long ("non shorto BTC in trend rialzista") e più altcoin.

## 3. Le operazioni ricostruite

Ogni operazione è ricostruita evento per evento (apertura, aumenti, chiusure parziali, stop a pareggio, chiusura) in due
modi:

- **Prezzi del trader**: quelli scritti o visibili nelle sue schermate Bybit.
- **Chi copiava**: ogni evento al primo prezzo disponibile dopo il messaggio (apertura dell'ora successiva). Le operazioni
  comunicate solo dopo l'ingresso restano fuori: non si potevano copiare.

Rendimento sul controvalore di ogni operazione (movimento del prezzo pesato per le quote aperte e chiuse), al netto di 0,16% di costi andata e ritorno. Le colonne con il simbolo × compongono le operazioni in sequenza con controvalore pari a 1 o 3 volte il capitale.

| Gruppo | Operazioni | In guadagno | Medio per operazione | Mediana | Capitale ×, controvalore 1x | Capitale ×, controvalore 3x |
|---|---|---|---|---|---|---|
| Prezzi dichiarati dal trader, tutte | 55 | 73% | +3,35% | +1,42% | ×5,65 | ×108,14 |
| Prezzi del trader, solo annunciate in tempo | 39 | 67% | +2,89% | +0,98% | ×2,84 | ×15,88 |
| Prezzi del trader, comunicate dopo | 16 | 88% | +4,49% | +3,38% | ×1,99 | ×6,81 |
| Chi copiava in tempo reale | 39 | 44% | +1,38% | -0,16% | ×1,63 | ×3,45 |

Sulle 39 operazioni copiabili, il prezzo del trader è stato migliore di quello disponibile a chi leggeva il messaggio di 1,51 punti per operazione in media.

Il punto chiave è la differenza fra le due righe. Il trader entra prima di scrivere, spesso con ordini limite eseguiti nei
minimi, e pubblica la schermata dopo. Chi legge entra più tardi e a un prezzo peggiore: in media 1,5 punti per operazione,
che su operazioni da qualche punto percentuale sono quasi tutto il guadagno.

Le 16 operazioni comunicate dopo sono un problema diverso: si vedono solo quando sono già andate bene (88% in guadagno).
Non è detto che siano scelte apposta, ma chi guarda il canale vede uno storico migliore di quello che poteva seguire.

| Gruppo (trader → chi copiava) | Operazioni | In guadagno | Medio per operazione | Mediana | Capitale ×, controvalore 1x | Capitale ×, controvalore 3x |
|---|---|---|---|---|---|---|
| BTC · trader | 35 | 63% | +1,67% | +1,32% | ×1,75 | ×4,79 |
| BTC · chi copiava | 24 | 33% | -0,21% | -0,16% | ×0,95 | ×0,83 |
| Altcoin · trader | 20 | 90% | +6,30% | +4,62% | ×3,22 | ×22,59 |
| Altcoin · chi copiava | 15 | 60% | +3,93% | +1,34% | ×1,72 | ×4,14 |
| Long · trader | 34 | 79% | +4,84% | +3,03% | ×4,66 | ×62,25 |
| Long · chi copiava | 24 | 50% | +2,31% | +0,21% | ×1,66 | ×3,67 |
| Short · trader | 21 | 62% | +0,94% | +0,41% | ×1,21 | ×1,74 |
| Short · chi copiava | 15 | 33% | -0,10% | -0,31% | ×0,98 | ×0,94 |
| Mag–ago 2023 · trader | 23 | 70% | +1,85% | +1,42% | ×1,51 | ×3,25 |
| Mag–ago 2023 · chi copiava | 15 | 40% | +0,05% | -0,16% | ×1,00 | ×0,99 |
| Set–dic 2023 · trader | 24 | 71% | +3,18% | +1,08% | ×2,02 | ×6,32 |
| Set–dic 2023 · chi copiava | 18 | 33% | +2,06% | -0,16% | ×1,39 | ×2,23 |
| Dic 2023–mar 2024 · trader | 8 | 88% | +8,19% | +5,34% | ×1,85 | ×5,27 |
| Dic 2023–mar 2024 · chi copiava | 6 | 83% | +2,65% | +2,31% | ×1,17 | ×1,56 |

- **BTC**: il trader guadagna l'1,7% medio, chi copiava perde. Il vantaggio su BTC è tutto nel prezzo d'ingresso.
- **Altcoin**: il risultato migliore, per tutti. Ma conta il periodo: da ottobre 2023 a marzo 2024 le altcoin sono salite
  molto, e quasi ogni long ha funzionato.
- **Short**: anche con i prezzi del trader rendono poco (+0,9%); per chi copiava sono in pari.

| Setup citato | Operazioni | In guadagno (trader) | Medio, prezzi del trader | Operazioni copiabili | Medio, chi copiava |
|---|---|---|---|---|---|
| Rottura di supporto/resistenza diagonale e retest | 9 | 67% | +3,57% | 6 | +0,82% |
| Retest o riconquista di un livello orizzontale | 13 | 62% | +2,78% | 11 | +0,48% |
| Presa di liquidità / falsa rottura | 16 | 75% | +6,89% | 10 | +4,89% |
| Media a 200 (EMA o MA) | 3 | 67% | +1,56% | 2 | +1,64% |
| Divergenza RSI | 6 | 67% | +3,34% | 2 | -0,41% |
| Range (massimo/minimo) | 2 | 50% | +0,00% | 2 | -0,52% |
| Gap del future CME | 3 | 0% | -0,28% | 3 | -0,44% |
| Figure (testa-spalle, doppio massimo) | 1 | 0% | -1,58% | 1 | -4,44% |
| Notizie macro (CPI, FOMC, ETF, SEC) | 13 | 62% | +1,75% | 11 | +0,39% |
| Alt long finché BTC regge | 8 | 88% | +3,15% | 4 | +0,57% |

Un'operazione può citare più setup. Classificazione per parole chiave nei messaggi e nei piani collegati.

Nessun setup si distingue con chiarezza: i campioni sono piccoli (2–16 operazioni) e i risultati di chi copiava sono vicini
a zero per quasi tutti.

| # | Asset | Verso | Apertura (UTC) | Ore | Prezzo medio del trader | Trader | Chi copiava | Note |
|---|---|---|---|---|---|---|---|---|
| A01 | BTC | short | 14/05/23 20:04 | 60 | 27.188 | +0,2% | -0,9% |  |
| A02 | BTC | short | 28/05/23 18:24 | 39 | 27.782 | -0,4% | -0,6% |  |
| A03 | BTC | long | 03/06/23 14:03 | 50 | 27.161 | -1,6% | -4,4% |  |
| A05 | BTC | short | 07/06/23 14:04 | 1 | 27.144 | +2,1% | – | comunicata dopo |
| A06 | MATIC | short | 13/06/23 12:56 | 2 | 0,6547 | +2,6% | +1,3% |  |
| A07 | BTC | long | 16/06/23 13:56 | 6 | 25.360 | +3,8% | +3,4% |  |
| A08 | BTC | short | 20/06/23 17:03 | 1 | 27.400 | -1,3% | -0,2% |  |
| A09 | BTC | short | 28/06/23 17:46 | 47 | 30.619 | +2,1% | +1,1% | residuo 0.20 senza chiusura dichiarata |
| A10 | INJ | long | 01/07/23 07:43 | 126 | 8,088 | +5,3% | – | comunicata dopo; residuo 0.20 senza chiusura dichiarata |
| A11 | FET | long | 01/07/23 07:43 | 103 | 0,225 | +4,3% | – | comunicata dopo; residuo 0.20 senza chiusura dichiarata |
| A12 | WOO | long | 01/07/23 07:43 | 126 | 0,2248 | +9,2% | – | comunicata dopo; residuo 0.20 senza chiusura dichiarata |
| A13 | BTC | short | 05/07/23 12:05 | 22 | 31.014 | -0,2% | – | comunicata dopo |
| A15 | BTC | short | 13/07/23 08:40 | 9 | 30.659 | -2,1% | -2,1% |  |
| A17 | INJ | long | 13/07/23 18:05 | 0 | 8,472 | +1,0% | -0,2% |  |
| A16 | WOO | long | 13/07/23 18:05 | 0 | 0,24 | +1,2% | -0,2% |  |
| A18 | INJ | long | 14/07/23 06:16 | 12 | 8,826 | +5,3% | +4,5% |  |
| A19 | WOO | long | 14/07/23 06:16 | 6 | 0,2477 | -1,7% | -3,0% |  |
| A20 | BTC | long | 25/07/23 16:25 | 16 | 29.163 | -0,0% | -0,2% |  |
| A21 | BTC | short | 26/07/23 18:02 | 142 | 29.378 | +1,3% | – | comunicata dopo |
| A22 | BTC | short | 02/08/23 11:41 | 4 | 29.800 | +2,5% | – | comunicata dopo; residuo 1.00 senza chiusura dichiarata |
| A23 | BTC | long | 18/08/23 15:16 | 126 | 26.132 | +1,4% | +0,4% |  |
| A24 | BTC | long | 29/08/23 14:36 | 2 | 26.989 | +3,0% | +1,7% |  |
| A25 | BTC | short | 31/08/23 13:30 | 3 | 27.869 | +4,4% | – | comunicata dopo |
| B01 | INJ | long | 18/09/23 09:50 | 70 | 7,154 | +1,2% | – | comunicata dopo |
| B02 | BNB | short | 21/09/23 08:28 | 26 | 213 | +0,9% | +0,9% |  |
| B03 | BTC | long | 22/09/23 14:31 | 64 | 26.575 | -1,8% | -2,2% |  |
| B04 | BTC | long | 26/09/23 16:41 | 19 | 26.230 | +2,1% | – | comunicata dopo |
| B05 | BTC | short | 28/09/23 16:29 | 3 | 27.248 | +0,4% | -0,3% |  |
| B06 | BTC | long | 02/10/23 06:33 | 1 | 26.912 | +4,4% | – | comunicata dopo |
| B07 | BTC | short | 02/10/23 07:46 | 5 | 28.400 | -0,7% | -1,0% |  |
| B08 | BTC | short | 09/10/23 17:48 | 32 | 27.896 | +2,3% | -0,2% | residuo 1.00 senza chiusura dichiarata |
| B09 | BTC | long | 11/10/23 15:34 | 50 | 26.749 | -0,2% | -0,0% |  |
| B10 | BTC | short | 18/10/23 05:55 | 0 | 28.770 | -0,7% | – | comunicata dopo |
| B11 | BTC | short | 18/10/23 12:34 | 21 | 28.395 | +0,0% | -0,4% |  |
| B12 | BTC | short | 19/10/23 15:37 | 15 | 28.650 | -1,2% | -2,4% |  |
| B13 | INJ | long | 23/10/23 22:50 | 11 | 10,51 | +16,1% | +11,2% |  |
| B14 | DOGE | long | 23/10/23 22:50 | 22 | 0,06431 | +3,1% | -1,6% |  |
| B15 | INJ | long | 27/10/23 09:02 | 124 | 12,36 | +13,9% | – | comunicata dopo |
| B16 | SOL | short | 01/11/23 18:38 | 1 | 46,13 | +6,5% | +4,2% |  |
| B17 | BTC | short | 02/11/23 13:20 | 30 | 35.200 | +1,3% | +0,4% |  |
| B18 | INJ | long | 09/11/23 09:18 | 7 | 17,18 | +0,2% | -0,2% |  |
| B19 | DOGE | long | 09/11/23 10:20 | 863 | 0,07612 | +28,9% | +29,5% |  |
| B20 | ETH | long | 13/11/23 21:17 | 22 | 2.053 | -3,9% | -0,2% |  |
| B21 | BTC | long | 13/11/23 21:29 | 0 | 36.450 | +0,4% | -0,2% |  |
| B22 | BTC | long | 16/11/23 21:17 | 133 | 35.650 | +2,2% | – | comunicata dopo |
| B23 | BTC | short | 28/11/23 23:05 | 9 | 37.950 | -0,5% | -1,5% |  |
| B24 | BTC | long | 11/12/23 20:52 | 29 | 40.600 | +1,3% | +1,0% | residuo 0.50 senza chiusura dichiarata |
| C01 | BTC | long | 20/12/23 14:23 | 0 | 41.882 | +4,2% | – | comunicata dopo |
| C02 | BTC | long | 03/01/24 12:11 | 153 | 40.750 | +10,4% | +2,2% |  |
| C03 | ETH | long | 10/01/24 09:48 | 494 | 2.356 | +5,7% | +2,9% |  |
| C05 | BTC | long | 22/01/24 19:44 | 17 | 39.477 | -0,1% | -0,2% |  |
| C06 | INJ | long | 17/02/24 22:32 | 40 | 36,65 | +5,0% | +2,4% |  |
| C07 | INJ | long | 28/02/24 17:47 | 7 | 36,73 | +21,3% | +7,2% |  |
| C08 | BTC | long | 08/03/24 15:32 | 0 | 59.909 | +15,6% | – | comunicata dopo |
| C11 | BTC | long | 17/03/24 10:13 | 24 | 66.558 | +3,5% | +1,3% |  |

| Nello stesso periodo (12/05/2023 – 18/03/2024) | Capitale × | Max DD |
|---|---|---|
| BTC comprato e tenuto | ×2,52 | -20,0% |
| W3.2 del radar | ×1,94 | -16,8% |
| v1 · voto di 17 indicatori | ×1,90 | -17,6% |

## 4. La strategia meccanica ricavata dal suo stile

Ho tradotto in regole fisse quello che fa più spesso e che si può misurare senza discrezione:

1. **Regime**: long solo se BTC ha chiuso il giorno prima sopra la sua media a 50 giorni (e la moneta sopra la sua); short
   solo nel caso opposto. È il suo "long sulle alt finché BTC regge" e "non shorto BTC in trend rialzista".
2. **Rottura e retest**: sulle 4 ore, chiusura sopra il massimo delle 30 candele precedenti; entro 3 giorni il prezzo torna sul
   livello rotto, lo tocca e chiude sopra → long. Specchio per lo short (il suo "retest negativo").
3. **Stop** sotto la candela del retest, meno un quarto di ATR.
4. **Gestione come la sua**: metà posizione a +1,5 volte il rischio, stop a pareggio, il resto a +3 volte o dopo 7 giorni.
5. **Rischio**: 1% del capitale allo stop, controvalore massimo 3x, al massimo 4 posizioni insieme.
6. **Universo**: BTC e le 8 altcoin che ha tradato di più (ETH, SOL, BNB, DOGE, INJ, FET, MATIC, WOO), dal 2018 dove ci sono i dati.

La rottura diagonale non è nella regola: una linea tracciata a mano non si traduce in modo univoco.

| Periodo | Versione | 10.000 $ → | CAGR | Max DD | Operazioni | In guadagno | Medio in R | Primo obiettivo raggiunto |
|---|---|---|---|---|---|---|---|---|
| Tutto il periodo | solo long, nel verso del trend, BTC + 8 alt | 6.253 | -5,3% | -54,9% | 1407 | 42% | -0,02 | 41% |
| Tutto il periodo | solo long, nel verso del trend, solo BTC | 9.276 | -0,9% | -22,9% | 241 | 43% | -0,02 | 41% |
| Tutto il periodo | long e short, BTC + 8 alt | 5.225 | -7,2% | -68,9% | 2468 | 43% | -0,01 | 42% |
| Tutto il periodo | long e short, solo BTC | 7.020 | -4,0% | -39,6% | 413 | 42% | -0,08 | 40% |
| Tutto il periodo | W3.2 (riferimento) | 276.181 | +46,6% | -37,3% | – | – | – | – |
| Tutto il periodo | BTC comprato e tenuto (riferimento) | 71.753 | +25,5% | -76,6% | – | – | – | – |
| 2018–2021 | solo long, nel verso del trend, BTC + 8 alt | 11.273 | +3,3% | -23,0% | 581 | 42% | 0,03 | 41% |
| 2018–2021 | solo long, nel verso del trend, solo BTC | 10.564 | +1,5% | -12,1% | 121 | 44% | 0,06 | 41% |
| 2018–2021 | long e short, BTC + 8 alt | 12.437 | +5,8% | -30,8% | 871 | 43% | 0,04 | 42% |
| 2018–2021 | long e short, solo BTC | 9.064 | -2,5% | -22,8% | 189 | 41% | -0,04 | 40% |
| 2018–2021 | W3.2 (riferimento) | 64.373 | +62,4% | -37,3% | – | – | – | – |
| 2018–2021 | BTC comprato e tenuto (riferimento) | 43.702 | +46,8% | -72,1% | – | – | – | – |
| 2022–2026 | solo long, nel verso del trend, BTC + 8 alt | 5.547 | -11,5% | -49,6% | 826 | 42% | -0,06 | 41% |
| 2022–2026 | solo long, nel verso del trend, solo BTC | 8.781 | -2,7% | -17,2% | 120 | 42% | -0,10 | 41% |
| 2022–2026 | long e short, BTC + 8 alt | 4.269 | -16,2% | -58,0% | 1597 | 42% | -0,04 | 42% |
| 2022–2026 | long e short, solo BTC | 7.764 | -5,1% | -30,5% | 224 | 42% | -0,11 | 41% |
| 2022–2026 | W3.2 (riferimento) | 42.903 | +35,2% | -21,1% | – | – | – | – |
| 2022–2026 | BTC comprato e tenuto (riferimento) | 16.419 | +10,8% | -66,9% | – | – | – | – |
| Periodo del canale (12/05/2023–18/03/2024) | solo long, nel verso del trend, BTC + 8 alt | 9.780 | -2,6% | -20,1% | 215 | 43% | -0,00 | 42% |
| Periodo del canale (12/05/2023–18/03/2024) | solo long, nel verso del trend, solo BTC | 10.195 | +2,3% | -4,6% | 23 | 43% | 0,09 | 43% |
| Periodo del canale (12/05/2023–18/03/2024) | long e short, BTC + 8 alt | 10.754 | +8,9% | -18,7% | 302 | 45% | 0,03 | 43% |
| Periodo del canale (12/05/2023–18/03/2024) | long e short, solo BTC | 10.398 | +4,8% | -5,6% | 31 | 48% | 0,10 | 45% |
| Periodo del canale (12/05/2023–18/03/2024) | W3.2 (riferimento) | 19.371 | +117,4% | -16,8% | – | – | – | – |
| Periodo del canale (12/05/2023–18/03/2024) | BTC comprato e tenuto (riferimento) | 25.232 | +196,5% | -20,0% | – | – | – | – |

| Asset | Operazioni (long e short) | In guadagno | Medio in R | Medio per operazione |
|---|---|---|---|---|
| BNB | 478 | 42% | -0,01 | +0,07% |
| BTC | 523 | 42% | -0,07 | -0,02% |
| DOGE | 297 | 44% | 0,09 | +0,33% |
| ETH | 486 | 44% | 0,01 | +0,04% |
| FET | 353 | 42% | -0,02 | +0,24% |
| INJ | 326 | 41% | -0,04 | -0,21% |
| MATIC | 234 | 40% | -0,07 | -0,40% |
| SOL | 362 | 42% | 0,01 | +0,09% |
| WOO | 240 | 35% | -0,18 | -0,94% |
| tutti, short | 1394 | 43% | -0,00 | -0,07% |
| tutti, long | 1905 | 41% | -0,04 | -0,02% |

Controllo: stessi stop e stessa gestione, ingressi long spostati a caso di ±10 giorni rispetto ai segnali (1199 prove): medio 0,21 R, contro -0,04 R della regola.

- **Non ha vantaggio**: su otto anni perde, da −1% annuo (solo BTC) a −7% (BTC e altcoin, long e short), con drawdown fino a
  −69%. Il risultato medio è zero volte il rischio: la gestione a metà posizione con stop a pareggio trasforma molte operazioni
  in piccole perdite e lascia pochi guadagni pieni. Peggio dal 2022 che nel 2018–2021.
- **Nel periodo del canale** va da −3% (solo long) a +9% (long e short), contro ×2,5 di BTC e ×1,9 di W3.2.
- **Ingressi casuali con la stessa gestione fanno meglio** della regola (+0,21 contro −0,04 volte il rischio): il segnale
  "rottura e retest" non aggiunge informazione.
- **Per moneta**: nessuna si salva in modo netto; DOGE e FET leggermente positive, WOO e MATIC le peggiori.

## 5. Confronto

Periodo del canale, 12/05/2023 – 18/03/2024. Per il canale: rendimento sul controvalore di ogni operazione, composto, con controvalore pari a 1 volta e a 3 volte il capitale (la leva vista nelle schermate è 5–14,5x, ma non si sa quanta parte del capitale usasse).

| Chi | Operazioni | In guadagno | Medio per operazione | Capitale ×, controvalore 1x | Capitale ×, controvalore 3x |
|---|---|---|---|---|---|
| Canale, prezzi dichiarati dal trader (tutte) | 55 | 73% | +3,35% | ×5,65 | ×108,14 |
| Canale, prezzi del trader, solo operazioni annunciate in tempo | 39 | 67% | +2,89% | ×2,84 | ×15,88 |
| Canale, chi copiava in tempo reale | 39 | 44% | +1,38% | ×1,63 | ×3,45 |
| Strategia meccanica, solo long (tutte le operazioni del periodo; colonna 3x = portafoglio a rischio 1%) | 303 | 41% | +0,17% | ×1,08 | ×0,98 |
| Strategia meccanica, long e short (tutte le operazioni del periodo; colonna 3x = portafoglio a rischio 1%) | 410 | 43% | +0,15% | ×1,10 | ×1,08 |
| W3.2 | – | – | – | ×1,94 | – |
| BTC comprato e tenuto | – | – | – | ×2,52 | – |

Tre letture:

1. **Il valore del trader, se c'è, sta nella discrezione**: quali livelli contano, quando non entrare, quali altcoin. Una
   regola meccanica che ne copia la forma non lo riproduce.
2. **Per chi lo segue conta il ritardo.** Le sue operazioni sono brevi e con obiettivi vicini: entrare un'ora dopo costa quasi
   tutto il vantaggio. Funziona meglio sulle operazioni lunghe (DOGE, 36 giorni) che sugli scalp su BTC.
3. **Nel periodo analizzato la cosa più redditizia era non fare trading**: BTC tenuto ha fatto ×2,5, W3.2 ×1,9 con drawdown −17%.

## 6. Limiti

- **Esportazione incompleta**: si ferma al 18/03/2024. Con lo storico completo fino a oggi le conclusioni possono cambiare,
  soprattutto perché da marzo 2024 il mercato è stato più difficile.
- **Ricostruzione**: alcune chiusure non sono mai annunciate (residui con stop a pareggio): le ho chiuse con una regola
  (stop o primo obiettivo entro 30 giorni). Sono segnate nell'elenco.
- **Dimensione delle posizioni**: non si sa quanta parte del capitale usasse. Per questo i risultati sono sul controvalore e
  composti a 1x e 3x, non in euro guadagnati.
- **Prezzi di chi copiava**: apertura dell'ora successiva al messaggio, senza differenza denaro-lettera. Chi era più veloce
  ha fatto un po' meglio, chi era più lento peggio.
- **Accumuli spot**: TAO, RNDR e le altre altcoin di intelligenza artificiale non sono nel conto (prezzi mancanti per molte).
  Nel periodo sono salite molto.

## 7. Prossimi passi

1. **Esportazione completa**: rifarla aspettando la fine ("Esportazione completata"), poi ripeto l'analisi fino a oggi.
2. **Controllo dal vivo**: con radar si può registrare l'ora e il prezzo di ogni messaggio nuovo del canale e misurare il
   ritardo reale di chi lo segue.

Codice: `backtest/telegram_ricostruzione.py`, `backtest/telegram_report.py`, `backtest/aldo_meccanico.py`. Operazioni
ricostruite: `results/telegram/`. Messaggi e schermate: non nel repository.
