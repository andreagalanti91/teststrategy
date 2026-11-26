# Aldo + Eliz: seconda analisi del trader e nuova strategia intraday su BTC, ETH, SOL, TAO

Seguito di `TELEGRAM_ALDO.md` e `ELIZ_24NOV.md`. Tre domande: cosa sfuggiva nella prima analisi del canale; qual è la
strategia di Aldo scritta come regole; se unendo le sue idee a quelle di Eliz si ottiene una strategia intraday che funziona su
BTC, ETH, SOL e TAO.

> Ricerca su dati storici, non una raccomandazione d'investimento. Canale: messaggi dall'11/05/2023 al 18/03/2024 (l'esportazione
> completa non è ancora arrivata).

## 1. Sintesi

**Aldo è un trader vero e bravo: le sue schermate sono autentiche e il suo vantaggio è reale. Ma sta nell'esecuzione
discrezionale (ordini su livelli decisi prima, uscite rapide), non in un setup che si possa scrivere come regola. Nessuna delle
96 versioni meccaniche intraday ispirate a lui e a Eliz guadagna su BTC, ETH, SOL o TAO dopo i costi, e nessuna fa meglio di
ingressi casuali con la stessa gestione. Su questi asset la strategia che funziona meglio resta W3.2, e usare i suoi ingressi
"furbi" su W3.2 la peggiora.**

| Domanda | Risposta |
|---|---|
| Le schermate sono vere? | Sì. Tutti i 124 prezzi dichiarati sono stati toccati davvero dal mercato prima del messaggio; il ROI delle card corrisponde sempre a una leva standard di Bybit |
| Quando entra rispetto al messaggio? | Mediana 25 minuti prima; un quarto delle volte più di 4 ore e mezza prima |
| Cosa sfuggiva? | Chi lo seguiva con **ordini limite sui livelli che annunciava prima** faceva molto meglio che entrando a mercato: 58% in guadagno invece di 44%, ×2,3 invece di ×1,6 |
| Quanto rende con rischio fisso? | Con il 2% del capitale per operazione e i suoi stop: lui 10.000 $ → 50.700 $ in 10 mesi; chi copiava con ordini limite 18.400 $; a mercato 15.700 $. BTC tenuto: 25.200 $ |
| La sua strategia, come regole? | Scritta al § 3. Il nucleo: livelli decisi prima, ingresso con ordine limite, metà al primo obiettivo, stop a pareggio, long sulle alt finché BTC regge |
| Aldo + Eliz intraday funziona? | No: 0 combinazioni positive su 96 nel periodo di verifica 2024–2026, R medio −0,20. Anche nel periodo di prova tutte negative |
| E i loro ingressi applicati a W3.2? | Peggio: 132.000 $ (Eliz) e 105.000 $ (Aldo) contro 203.000 $ di W3.2 con l'ingresso del lunedì. Aspettare un prezzo migliore fa perdere le partenze forti |

## 2. Cosa sfuggiva nella prima analisi

### Le schermate sono autentiche

| Prezzi dichiarati nelle schermate | Quanti | Toccati davvero dal mercato nelle 72 ore prima del messaggio | Ritardo mediano fra l'ultima volta che il mercato era a quel prezzo e il messaggio | Un quarto oltre |
|---|---|---|---|---|
| Ingressi e aumenti | 58 | 100% | 0,4 ore | 4,5 ore |
| Uscite | 66 | 100% | -0,2 ore | 0,5 ore |

Il mercato ha toccato ogni prezzo dichiarato, sia in ingresso sia in uscita. Le uscite coincidono quasi sempre con il momento
del messaggio; gli ingressi no: spesso entra prima e scrive dopo, con l'ordine già eseguito.

Schermate Bybit con prezzo d'ingresso, prezzo d'uscita e ROI leggibili: 18. Dividendo il ROI per il movimento del prezzo si ottiene la leva implicita: in 100% dei casi è una leva standard di Bybit (5x, 10x, 13x, 14,5x… entro l'8%), mediana 10,0x. Le schermate sono coerenti con operazioni reali.

### Chi lo seguiva con ordini limite

La prima analisi faceva entrare chi copiava a mercato, un'ora dopo il messaggio. Ma Aldo annuncia spesso il livello prima
("ordine long al limite a 25.300", "in attesa di un retest a 27,4k"). Chi metteva un ordine limite su quel livello entrava al
suo stesso prezzo.

Operazioni con un livello d'ingresso annunciato prima: 36; ordine limite eseguito in tempo: 20 (di cui 4 fra quelle che il trader ha comunicato solo dopo).

| Chi | Operazioni | In guadagno | Medio per operazione | Capitale ×, controvalore 1x |
|---|---|---|---|---|
| Trader, prezzi delle schermate | 55 | 73% | +3,35% | ×5,65 |
| Chi copiava con ordini limite sui livelli annunciati | 43 | 58% | +2,15% | ×2,33 |
| · di cui entrate con ordine limite | 20 | 60% | +2,05% | ×1,46 |
| · di cui entrate a mercato dopo il messaggio | 23 | 57% | +2,23% | ×1,59 |
| Chi copiava solo a mercato (prima analisi) | 39 | 44% | +1,38% | ×1,63 |

Il miglioramento è grande: da ×1,6 a ×2,3, e la quota di operazioni in guadagno sale dal 44% al 58%. Resta sotto il trader per
due motivi: metà delle operazioni non aveva un livello annunciato prima, e le uscite parziali che decide al momento si possono
copiare solo dopo il messaggio.

### Con il rischio fisso e i suoi stop

| Chi | Rischio per operazione | Capitale finale da 10.000 $ | Peggiore operazione sul capitale |
|---|---|---|---|
| Trader, prezzi delle schermate | 1% | 23.092 $ | -1,9% |
| Trader, prezzi delle schermate | 2% | 50.710 $ | -3,9% |
| Chi copiava con ordini limite | 1% | 13.718 $ | -2,2% |
| Chi copiava con ordini limite | 2% | 18.357 $ | -4,4% |
| Chi copiava a mercato | 1% | 12.685 $ | -2,2% |
| Chi copiava a mercato | 2% | 15.714 $ | -4,4% |

Con i suoi stop e il 2% di rischio per operazione, il suo risultato è notevole: ×5 in dieci mesi con la perdita peggiore
sotto il 4%. Per chi lo seguiva il risultato è positivo ma inferiore a BTC tenuto nello stesso periodo (×2,5), che però aveva
un drawdown del 20%.

## 3. La strategia di Aldo, scritta come regole

Ricostruita dai 812 messaggi e dalle 55 operazioni a leva.

**Contesto**
1. Analisi dall'alto: settimanale e giornaliero per i livelli (supporti, resistenze, media a 200 settimanale, chiusure
   settimanali e mensili), 4 ore e 1 ora per l'ingresso.
2. BTC decide tutto. Long sulle altcoin solo finché BTC tiene il livello indicato e la dominance di BTC scende; niente short su
   BTC in trend rialzista.
3. Calendario: prima di CPI, FOMC, scadenze di opzioni e notizie grosse chiude o riduce.

**Ingresso** (sempre su un livello deciso prima, quasi sempre con ordine limite)
4. Long sul retest positivo di un livello rotto al rialzo, o sulla riconquista di un supporto perso ("reclaim").
5. Short sul retest negativo di un supporto rotto, soprattutto diagonale (il suo setup preferito), o dopo una presa di
   liquidità poco sopra un massimo.
6. Entra a scalare: metà al primo livello, il resto più in alto (short) o più in basso (long), entro un'invalidazione decisa
   prima.

**Gestione**
7. Leva 10x tipica; stop spesso condizionale ("rottura pulita di X e sono fuori").
8. Metà posizione al primo obiettivo (spesso il minimo o massimo di giornata, o il livello successivo), stop a pareggio
   subito dopo.
9. Il resto a un secondo obiettivo, oppure chiuso all'80–100% appena qualcosa non lo convince (divergenze, notizie, weekend).
10. Operazioni brevi: mediana 19 ore. Le eccezioni lunghe (DOGE 36 giorni) sono quelle che rendono di più.

**Perché funziona per lui e non come regola**: i punti 4–5 dipendono da quali livelli sceglie e quali scarta, e i punti 8–9
da decisioni prese guardando il grafico in quel momento. Nella prima analisi la versione meccanica di questo schema (rottura e
retest nel verso del trend, gestione a metà) perdeva dal 2018 (−1/−7% annuo).

## 4. La nuova strategia: Aldo + Eliz, intraday

Ho preso da ciascuno quello che si può scrivere come regola:

- **Eliz**: il livello è l'estremo di un range; si entra dopo una deviazione oltre l'estremo e il rientro confermato a 15 minuti,
  con lo stop oltre l'estremo della deviazione.
- **Aldo**: nel verso del trend; le prese di liquidità sono il suo setup che ha reso di più nel canale (+6,9% medio con i suoi
  prezzi); ordine limite su un livello deciso prima; gestione con metà al primo obiettivo e stop a pareggio.

Due famiglie, 24 varianti, 4 asset:

- **Sweep & reclaim**: il prezzo scende sotto il minimo delle ultime 24, 48 o 96 ore (almeno lo 0,1%) e una candela da 15 minuti
  richiude sopra entro un'ora → long; stop sotto il minimo della deviazione. Specchio per gli short.
- **Limite sul livello**: ordine limite sul minimo (massimo) delle ultime 24, 48 o 96 ore, stop un ATR orario oltre.
- **Filtro**: nessuno, oppure solo long sopra la EMA 50 giornaliera e solo short sotto.
- **Gestione**: metà a +1 volta il rischio con stop a pareggio e resto a +2,5; oppure tutto a +2.
- **Metodo**: scelta sul periodo di prova (settembre 2020 – dicembre 2023) di BTC, ETH e SOL; verifica 2024–2026. TAO non entra
  nella scelta: è solo verifica. Controllo con ingressi casuali e stessa gestione.

24 varianti × 4 asset. Scelta sul solo periodo di prova (set 2020 – dic 2023) di BTC, ETH e SOL, per R medio; TAO non entra nella scelta.

| Famiglia | Ore del range | Filtro di trend | Gestione | R medio in prova (BTC, ETH, SOL) | Asset positivi in prova | Operazioni in prova |
|---|---|---|---|---|---|---|
| sweep & reclaim (Eliz + Aldo) | 96 | nessuno | tutto a 2 R | -0,09 | 0/3 | 3360 |
| sweep & reclaim (Eliz + Aldo) | 96 | EMA 50 giornaliera | tutto a 2 R | -0,11 | 0/3 | 1146 |
| sweep & reclaim (Eliz + Aldo) | 24 | EMA 50 giornaliera | tutto a 2 R | -0,11 | 0/3 | 3588 |
| sweep & reclaim (Eliz + Aldo) | 48 | EMA 50 giornaliera | tutto a 2 R | -0,12 | 0/3 | 2121 |
| sweep & reclaim (Eliz + Aldo) | 96 | nessuno | metà a 1 R + pareggio | -0,13 | 0/3 | 3357 |
| sweep & reclaim (Eliz + Aldo) | 48 | nessuno | tutto a 2 R | -0,13 | 0/3 | 5034 |
| sweep & reclaim (Eliz + Aldo) | 24 | nessuno | tutto a 2 R | -0,13 | 0/3 | 7339 |
| sweep & reclaim (Eliz + Aldo) | 96 | EMA 50 giornaliera | metà a 1 R + pareggio | -0,15 | 0/3 | 1147 |
| … ultime: limite sul livello (Aldo), 48 ore | | | | -0,21 | | |

Variante scelta: sweep & reclaim (Eliz + Aldo), range di 96 ore, filtro nessuno, gestione tutto a +2 R. Rischio 1% del capitale per operazione.

| Asset | Periodo | Operazioni | Per anno | In guadagno | R medio | t-stat | 10.000 $ → | Max DD | Ingressi casuali, stessa gestione: R medio |
|---|---|---|---|---|---|---|---|---|---|
| BTC | prova 2020–2023 | 1058 | 319 | 35% | -0,13 | -2,9 | 2.313 | -80,2% | -0,22 |
| BTC | verifica 2024–2026 | 946 | 334 | 33% | -0,24 | -5,2 | 919 | -91,1% | -0,26 |
| ETH | prova 2020–2023 | 1097 | 332 | 35% | -0,11 | -2,4 | 2.791 | -75,6% | -0,17 |
| ETH | verifica 2024–2026 | 990 | 350 | 32% | -0,25 | -5,5 | 785 | -92,6% | -0,21 |
| SOL | prova 2020–2023 | 1205 | 366 | 36% | -0,05 | -1,1 | 5.061 | -67,8% | -0,13 |
| SOL | verifica 2024–2026 | 1112 | 394 | 32% | -0,20 | -4,6 | 980 | -91,3% | -0,17 |
| TAO | verifica 2024–2026 | 1179 | 466 | 33% | -0,13 | -3,2 | 1.804 | -85,8% | -0,13 |

| Asset | Migliore variante in verifica (scelta guardando i risultati) | R medio in verifica | Operazioni | Stessa variante in prova |
|---|---|---|---|---|
| BTC | limite sul livello (Aldo), 24 ore, senza filtro, metà a 1 R | -0,22 | 2575 | -0,19 |
| ETH | limite sul livello (Aldo), 24 ore, EMA 50, 2 R | -0,19 | 1111 | -0,19 |
| SOL | limite sul livello (Aldo), 24 ore, EMA 50, metà a 1 R | -0,14 | 1334 | -0,11 |
| TAO | limite sul livello (Aldo), 24 ore, EMA 50, metà a 1 R | -0,07 | 1183 | n/d |

Varianti con R medio positivo in verifica: 0% delle 96 combinazioni variante × asset; R medio di tutte: -0,20.

- **Nessuna variante funziona**, nemmeno nel periodo di prova, dove sono state scelte: la migliore perde 0,09 volte il rischio
  per operazione. In verifica perdono tutte.
- **La conferma a 15 minuti di Eliz aiuta un poco**: sweep & reclaim fa leggermente meglio degli ingressi casuali (−0,13 contro
  −0,22 volte il rischio su BTC in prova). Non abbastanza per coprire i costi.
- **I costi decidono**: con stop dell'1–2% e 300–400 operazioni l'anno, commissioni e slittamento valgono circa 0,1 volte il
  rischio per operazione. Il segnale non vale altrettanto.
- **TAO**, mai usato per scegliere, va come gli altri.
- Coerente con tutto quello che abbiamo provato sull'intraday (`INTRADAY.md`: 1.224 regole su BTC, nessuna valida).

## 5. L'ultima prova: i loro ingressi applicati a W3.2

Se il vantaggio di Aldo è l'esecuzione, forse serve a entrare meglio nei segnali di W3.2. Stesso segnale settimanale, stessa
uscita; cambia solo come si entra nella prima settimana.

Le 23 operazioni di W3.2 dal 2018, stesso segnale e stessa uscita, tre modi di entrare. Risultato sul capitale = esposizione di W3.2 × movimento.

| Ingresso | Operazioni eseguite | Prezzo d'ingresso migliore del lunedì | Miglioramento medio del prezzo | 10.000 $ → | Operazioni saltate |
|---|---|---|---|---|---|
| Apertura del lunedì (W3.2) | 23 | 0 su 23 | +0,00% | 203.450 | 0 |
| Ordine limite al minimo/massimo delle 48 ore prima (Aldo) | 23 | 14 su 23 | -2,23% | 105.164 | 0 |
| Presa di liquidità e rientro a 15 minuti (Eliz) | 23 | 12 su 23 | -1,28% | 131.924 | 0 |

Peggio in entrambi i casi. Il prezzo d'ingresso migliora in metà delle operazioni, ma nelle operazioni migliori di W3.2
(maggio 2019, dicembre 2020, febbraio 2021, ottobre 2023) il prezzo parte subito e non torna: l'ordine limite si esegue una
settimana dopo, molto più in alto. Per un sistema che segue il trend, aspettare un prezzo migliore costa più di quanto rende.

## 6. Cosa funziona meglio, alla fine

1. **Su BTC: W3.2, come oggi.** Nessuna delle strategie intraday provate fa meglio, nemmeno nello stesso periodo del canale.
2. **Su ETH, SOL e TAO**: nessuna strategia intraday meccanica regge. La strada più promettente è la stessa logica di W3.2
   (trend settimanale con flussi), che radar ha già su ETH: va estesa e verificata su SOL e TAO.
3. **Se vuoi seguire Aldo**, il modo che rende di più è quello misurato al § 2: ordini limite sui livelli che annuncia prima,
   la sua gestione (metà al primo obiettivo, stop a pareggio), rischio fisso piccolo (1–2%), e solo sulle operazioni annunciate
   prima. Da verificare sullo storico completo, quando arriva l'esportazione: fino a marzo 2024 il mercato è stato quasi solo al
   rialzo.

## 7. Limiti

- Canale fermo al 18/03/2024: dieci mesi, quasi tutti di mercato rialzista.
- Ordini limite di chi copiava: eseguiti se il prezzo tocca il livello (tolleranza 0,15%); nella realtà una parte non si
  sarebbe riempita.
- Intraday: dati Binance spot a 15 minuti, nessun funding, slittamento fisso. Con un exchange più caro i risultati sono peggiori.
- Le varianti provate sono 24 per famiglia d'idea, non infinite: un'altra traduzione delle regole di Aldo o Eliz potrebbe dare
  numeri diversi. Ma il risultato è coerente con tutte le prove precedenti.

Codice: `backtest/telegram_verifica.py`, `backtest/intraday_combo.py`, `backtest/w32_esecuzione.py`. Risultati:
`results/telegram/`, `results/intraday_combo/`.
