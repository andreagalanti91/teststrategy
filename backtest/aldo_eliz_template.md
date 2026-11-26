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

{{V1}}

Il mercato ha toccato ogni prezzo dichiarato, sia in ingresso sia in uscita. Le uscite coincidono quasi sempre con il momento
del messaggio; gli ingressi no: spesso entra prima e scrive dopo, con l'ordine già eseguito.

{{V2}}

### Chi lo seguiva con ordini limite

La prima analisi faceva entrare chi copiava a mercato, un'ora dopo il messaggio. Ma Aldo annuncia spesso il livello prima
("ordine long al limite a 25.300", "in attesa di un retest a 27,4k"). Chi metteva un ordine limite su quel livello entrava al
suo stesso prezzo.

{{V3}}

Il miglioramento è grande: da ×1,6 a ×2,3, e la quota di operazioni in guadagno sale dal 44% al 58%. Resta sotto il trader per
due motivi: metà delle operazioni non aveva un livello annunciato prima, e le uscite parziali che decide al momento si possono
copiare solo dopo il messaggio.

### Con il rischio fisso e i suoi stop

{{V4}}

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

{{I1}}

{{I2}}

{{I3}}

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

{{E1}}

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
