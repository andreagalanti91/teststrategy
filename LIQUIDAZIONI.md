# Il prezzo di BTC segue le liquidazioni?

Come verificarlo sui dati, cosa risulta, e come leggere la mappa di Coinglass del 24/11/2026 (prezzo 60.388 $).

> Ricerca su dati storici, non una raccomandazione d'investimento.

## 1. Sintesi

**No: nei dati dal 2022 il prezzo non va verso le liquidazioni più di quanto andrebbe verso un qualsiasi livello alla stessa
distanza. La mappa racconta dove è già passato il prezzo, non dove andrà.**

| Domanda | Come si verifica | Risultato |
|---|---|---|
| Le fasce grandi attirano il prezzo? | Quante volte la fascia più grande viene raggiunta, contro quante volte il prezzo percorre comunque quella distanza | Nessuna differenza: fra −1,6 e +0,1 punti, con segno che cambia fra i periodi |
| Il prezzo va verso il lato più carico? | Rendimento nei giorni successivi per livello di squilibrio | No: correlazione 0,02 con i 7 giorni dopo |
| Cosa misura allora lo squilibrio? | Correlazione con il prezzo dei giorni precedenti | Il passato: −0,62 con i 7 giorni prima |
| Tra due fasce, quale viene toccata? | Giorni in cui il prezzo ne tocca una sola | La più vicina (72% dei casi). Quando la più grande non è la più vicina, viene toccata solo nel 33% dei casi |

Per la mappa di oggi: il 75% delle liquidazioni sopra il prezzo non dice che BTC salirà. È la traccia del −50% dal massimo:
i long sono già stati liquidati scendendo, gli short aperti durante la discesa hanno la liquidazione più in alto. Le fasce
grandi più vicine sono sotto (54.145–50.535 $, a −10/−16%), quelle sopra partono da 76.915 $ (+27%).

Come strategia: le liquidazioni non danno un segnale d'ingresso. Servono a scegliere dove non mettere lo stop e quanta leva
usare. Il tuo radar era arrivato alla stessa conclusione con quattro studi; questa è una replica indipendente con dati
aggiornati.

## 2. Che cos'è una mappa delle liquidazioni

- **È una stima, non un dato.** Le borse non pubblicano i prezzi di liquidazione dei clienti. Coinglass li stima dalle
  posizioni aperte a ogni prezzo e dalle leve più comuni: per ogni aumento di open interest ipotizza nuove posizioni a 10x,
  25x, 50x, 100x e calcola dove verrebbero liquidate.
- **I modelli sono diversi fra loro.** Nella schermata ci sono tre modelli; il radar ne ha uno suo. Il 13/11 la mappa del
  radar e quella di Coinglass davano quadri opposti entro il 5% dal prezzo.
- **Gli unici livelli veri** sono quelli delle borse dove le posizioni sono pubbliche (Hyperliquid, Lighter), che il radar
  registra da novembre 2026.
- **Il totale (61,87 miliardi) somma livelli molto lontani.** Una fascia a 93.000 $ è a +55%: conta nel 75% "sopra", ma non
  dice nulla sui prossimi giorni.

## 3. Come si verifica se il prezzo segue le liquidazioni

Tre trappole rendono l'idea convincente a occhio e vanno tolte dal test:

1. **La distanza.** Un livello vicino viene toccato spesso comunque. Bisogna confrontare con la frequenza con cui il prezzo
   percorre quella distanza in un giorno qualsiasi.
2. **Il passato.** La mappa si svuota dove il prezzo è passato e si riempie dall'altra parte: dopo un calo ci sono sempre più
   short sopra. Lo squilibrio va confrontato con il movimento già avvenuto.
3. **La memoria selettiva.** Si ricordano le volte in cui il prezzo ha "preso" una fascia e non quelle in cui è andato
   dall'altra parte. Servono tutti i giorni, non gli esempi.

Il test: ogni giorno alle 00:00 UTC si ricostruisce la mappa con i soli dati precedenti (open interest orario di Binance
USDT-M, stesso metodo del radar), con memoria di 21 giorni e di 90 giorni, e si misura cosa fa il prezzo dopo.

Dati orari Binance USDT-M dal 2021-11-30 al 2026-11-07 (43267 ore con open interest).

## 4. Risultati con memoria di 21 giorni

### 4.1 La mappa descrive il passato

Mappa con memoria di 21 giorni, 1782 giorni dal 2021-12-22. Correlazione fra lo squilibrio (short sopra − long sotto, entro ±15%) e il rendimento passato del prezzo: a 1 giorno -0,18, a 7 giorni -0,62, a 30 giorni -0,44. Correlazione con il rendimento dei 7 giorni successivi: 0,02.

Lo squilibrio è alto (più short sopra) dopo che il prezzo è sceso, e viceversa. Con il futuro non ha relazione.

### 4.2 Il lato più carico non indica la direzione

| Squilibrio entro ±15% | Giorni | Rendimento medio a 1 giorno | a 3 giorni | a 7 giorni | a 14 giorni | Positivi a 7 giorni | 7 giorni, 2022–23 | 7 giorni, 2024–26 |
|---|---|---|---|---|---|---|---|---|
| Short sopra dominanti (oltre +30%) | 54 | -0,14% | +0,71% | +1,90% | +1,51% | 59% | +5,11% | -0,14% |
| Equilibrio (fra −30% e +30%) | 1457 | +0,05% | +0,12% | +0,25% | +0,84% | 50% | -0,33% | +0,65% |
| Long sotto dominanti (sotto −30%) | 271 | +0,14% | +0,37% | +1,04% | +0,97% | 54% | +1,95% | +0,33% |
| Short sopra oltre +60% | 6 | -0,34% | +1,83% | +3,26% | +4,52% | 50% | +5,21% | -0,65% |
| Long sotto oltre −60% | 20 | +0,85% | +1,48% | +4,35% | +6,48% | 65% | +4,10% | +5,12% |
| *Tutti i giorni* | 1782 | +0,06% | +0,18% | +0,42% | +0,88% | 51% | +0,19% | +0,58% |

Tolto l'effetto del rendimento dei 7 giorni precedenti, la correlazione fra squilibrio e rendimento a 7 giorni è 0,02. Nei giorni in cui lo squilibrio è opposto al movimento dei 7 giorni precedenti (302 casi con squilibrio oltre 30%), il prezzo a 7 giorni va nel verso dello squilibrio nel 48% dei casi.

- Con gli short dominanti sopra il prezzo sale un po' più della media, ma solo nel 2022–23 (+5,1% a 7 giorni); dal 2024 è
  −0,1%.
- Anche con i long dominanti sotto il prezzo sale più della media. I due estremi danno lo stesso risultato: non è la
  direzione dello squilibrio a contare, sono giorni che seguono movimenti forti.

### 4.3 Le fasce grandi non attirano il prezzo

| Livello | Orizzonte | Giorni | Raggiunto | Atteso a pari distanza | Differenza | Differenza 2022–23 | Differenza 2024–26 |
|---|---|---|---|---|---|---|---|
| Fascia più grande di short sopra (entro 10%) | 1 g | 1778 | 9,6% | 10,5% | -0,9 punti | +0,2 | -1,7 |
| Fascia più grande di short sopra (entro 10%) | 3 g | 1776 | 22,2% | 23,8% | -1,6 punti | +0,0 | -2,8 |
| Fascia più grande di short sopra (entro 10%) | 7 g | 1772 | 39,3% | 39,2% | +0,1 punti | +1,0 | -0,5 |
| Fascia più grande di long sotto (entro 10%) | 1 g | 1778 | 8,4% | 9,2% | -0,7 punti | -0,8 | -0,7 |
| Fascia più grande di long sotto (entro 10%) | 3 g | 1776 | 20,6% | 21,6% | -1,1 punti | -0,8 | -1,3 |
| Fascia più grande di long sotto (entro 10%) | 7 g | 1772 | 35,3% | 35,6% | -0,3 punti | +1,6 | -1,7 |

Distanza mediana della fascia più grande: sopra +5,7%, sotto -5,9%.

Le differenze fra "raggiunto" e "atteso" stanno tutte entro due punti e cambiano segno fra i due periodi.

### 4.4 Viene toccata la fascia più vicina, non la più grande

| Orizzonte | Giorni in cui il prezzo tocca una sola delle due fasce | Tocca la fascia più grande | Tocca la fascia più vicina | Giorni in cui la più grande NON è la più vicina | In quei giorni tocca la più grande |
|---|---|---|---|---|---|
| 1 g | 310 | 65% | 85% | 103 | 19% |
| 3 g | 712 | 61% | 78% | 272 | 28% |
| 7 g | 1134 | 59% | 72% | 442 | 33% |

È il test più diretto. Se le liquidazioni attirassero il prezzo, la fascia più grande dovrebbe vincere anche quando è più
lontana. Succede una volta su tre a 7 giorni e una su cinque a 1 giorno.

### 4.5 Situazioni simili a oggi

| Situazione simile a oggi | Giorni | Episodi distinti | Rendimento medio a 7 giorni | a 14 giorni | Positivi a 14 giorni | Riferimento: tutti i giorni a 14 giorni |
|---|---|---|---|---|---|---|
| Short sopra oltre +50% e prezzo sceso di oltre il 15% in 30 giorni | 2 | 2 | +2,9% | -0,1% | 50% | +0,9% |
| Short sopra oltre +50% e prezzo sotto la SMA 200 | 5 | 3 | +0,8% | -0,9% | 20% | +0,9% |

Ultima mappa (2026-11-07, prezzo 75.810 $): squilibrio entro ±15% +3%, short sopra 911 M$, long sotto 858 M$ (solo Binance USDT-M, stima).

Gli episodi sono due o tre: non bastano per dire nulla. Questa mappa arriva a ±15% dal prezzo e si ferma al 07/11, quindi
non riproduce il quadro di Coinglass di oggi.

## 5. Con memoria di 90 giorni

Stessa prova con una mappa più "lunga", più vicina a quelle di Coinglass. Le conclusioni non cambiano.

Mappa con memoria di 90 giorni, 1713 giorni dal 2022-03-01. Correlazione fra lo squilibrio (short sopra − long sotto, entro ±15%) e il rendimento passato del prezzo: a 1 giorno -0,12, a 7 giorni -0,56, a 30 giorni -0,47. Correlazione con il rendimento dei 7 giorni successivi: 0,01.

| Squilibrio entro ±15% | Giorni | Rendimento medio a 1 giorno | a 3 giorni | a 7 giorni | a 14 giorni | Positivi a 7 giorni | 7 giorni, 2022–23 | 7 giorni, 2024–26 |
|---|---|---|---|---|---|---|---|---|
| Short sopra dominanti (oltre +30%) | 41 | -0,18% | +0,99% | +2,51% | +2,33% | 61% | +7,19% | -0,18% |
| Equilibrio (fra −30% e +30%) | 1430 | +0,05% | +0,13% | +0,36% | +0,92% | 51% | -0,10% | +0,64% |
| Long sotto dominanti (sotto −30%) | 242 | +0,19% | +0,44% | +0,96% | +1,51% | 52% | +1,78% | +0,33% |
| Short sopra oltre +60% | 2 | -0,98% | -0,67% | -0,82% | -1,75% | 50% | -0,82% | n/d |
| Long sotto oltre −60% | 21 | +0,58% | +1,08% | +3,94% | +6,80% | 62% | +4,37% | +2,57% |
| *Tutti i giorni* | 1713 | +0,07% | +0,20% | +0,49% | +1,04% | 51% | +0,36% | +0,58% |

Tolto l'effetto del rendimento dei 7 giorni precedenti, la correlazione fra squilibrio e rendimento a 7 giorni è 0,02. Nei giorni in cui lo squilibrio è opposto al movimento dei 7 giorni precedenti (257 casi con squilibrio oltre 30%), il prezzo a 7 giorni va nel verso dello squilibrio nel 49% dei casi.

| Livello | Orizzonte | Giorni | Raggiunto | Atteso a pari distanza | Differenza | Differenza 2022–23 | Differenza 2024–26 |
|---|---|---|---|---|---|---|---|
| Fascia più grande di short sopra (entro 10%) | 1 g | 1709 | 9,4% | 10,1% | -0,7 punti | -0,0 | -1,1 |
| Fascia più grande di short sopra (entro 10%) | 3 g | 1707 | 22,0% | 23,2% | -1,1 punti | +0,5 | -2,2 |
| Fascia più grande di short sopra (entro 10%) | 7 g | 1703 | 39,4% | 38,5% | +0,9 punti | +2,4 | -0,1 |
| Fascia più grande di long sotto (entro 10%) | 1 g | 1709 | 7,4% | 8,2% | -0,8 punti | -0,5 | -1,0 |
| Fascia più grande di long sotto (entro 10%) | 3 g | 1707 | 17,8% | 19,7% | -1,9 punti | -1,3 | -2,3 |
| Fascia più grande di long sotto (entro 10%) | 7 g | 1703 | 31,4% | 33,0% | -1,6 punti | -0,3 | -2,5 |

Distanza mediana della fascia più grande: sopra +5,8%, sotto -6,3%.

| Orizzonte | Giorni in cui il prezzo tocca una sola delle due fasce | Tocca la fascia più grande | Tocca la fascia più vicina | Giorni in cui la più grande NON è la più vicina | In quei giorni tocca la più grande |
|---|---|---|---|---|---|
| 1 g | 282 | 67% | 84% | 79 | 19% |
| 3 g | 641 | 61% | 77% | 219 | 26% |
| 7 g | 1033 | 59% | 72% | 360 | 31% |

| Situazione simile a oggi | Giorni | Episodi distinti | Rendimento medio a 7 giorni | a 14 giorni | Positivi a 14 giorni | Riferimento: tutti i giorni a 14 giorni |
|---|---|---|---|---|---|---|
| Short sopra oltre +50% e prezzo sceso di oltre il 15% in 30 giorni | 1 | 1 | +13,3% | +1,5% | 100% | +1,0% |
| Short sopra oltre +50% e prezzo sotto la SMA 200 | 4 | 2 | +2,8% | -0,7% | 25% | +1,0% |

Ultima mappa (2026-11-07, prezzo 75.810 $): squilibrio entro ±15% -18%, short sopra 921 M$, long sotto 1.323 M$ (solo Binance USDT-M, stima).

## 6. Cosa aveva già trovato il radar

| Studio del radar | Domanda | Esito |
|---|---|---|
| Liquidazioni vicine e S/R (lezione 81) | Le fasce attirano il prezzo? Lo squilibrio indica la direzione? | Calamita: no (0 test su 6). Direzione: un effetto a 12–24 ore, in gran parte momentum di breve, sparito a 3–7 giorni |
| Mappa v2 con flusso taker | Una mappa più raffinata localizza meglio le liquidazioni vere? | No: nessuna variante batte il caso sulle liquidazioni reali di Binance |
| Fasce come zone d'ingresso (lezione 92) | Entrare con un limite sulla fascia migliora W3? | No: 59.000 $ contro 78.000 $. Le fasce dicono dove è passata la cascata, non dove entrare |
| Squeeze da squilibrio (lezione 93) | Comprare quando i long sono stati puliti e sopra ci sono short? | No: tutte le regole perdono dopo i costi, indistinguibili dal caso |

Il solo effetto trovato dal radar (lato più carico toccato per primo entro un giorno) è compatibile con quanto misurato qui:
il lato più carico è spesso anche il più vicino.

## 7. Come leggere la mappa di oggi

| | Valore nella schermata | Lettura |
|---|---|---|
| Prezzo | 60.388 $ | – |
| Short sopra (totale) | 46,30 miliardi, 75% | traccia della discesa da 126.000 $: gli short aperti scendendo hanno la liquidazione più in alto |
| Long sotto (totale) | 15,57 miliardi, 25% | i long più vicini sono già stati liquidati |
| Fasce grandi sopra | 76.915 $ (+27%), poi 91.076–93.853 $ (+51/+55%) | lontane: non rilevanti nel breve |
| Fasce grandi sotto | 54.145 e 53.312 $ (−10/−12%), 51.368 $ (−15%, la più grande: 1,18 miliardi), 50.535 $ (−16%) | sono le più vicine |
| Liquidati in 24 ore | 352 milioni, circa metà long e metà short | nessuna cascata in corso |

- **Per sola distanza**, la fascia sotto è la più probabile. Dal 2018, partendo da un giorno qualsiasi, BTC ha toccato −10%
  prima di +27% nel 62% dei casi entro 90 giorni, e +27% prima nel 32%. Le liquidazioni non aggiungono informazione a questo.
- **Coincide con l'analisi tecnica**: 54.000–55.000 $ è appena sotto il supporto a 55.000–58.000 $ indicato in
  `ANALISI_BTC.md`. Se quel supporto cede, lì sotto ci sono stop e liquidazioni di long: il movimento può accelerare fino a
  50.000–51.000 $.
- **Per W3.2**, che è short da 65.286 $ con trailing a 75.764 $: la prima fascia di short è a 76.915 $, appena sopra lo stop.
  È una coincidenza utile da conoscere, non un motivo per spostarlo.

## 8. Come usarle in una strategia

Quello che i dati sostengono:

1. **Non come segnale d'ingresso.** Né "compra perché sopra ci sono short da liquidare" né ordini limite sulle fasce.
2. **Per lo stop.** Una fascia densa è un punto dove il prezzo, se arriva, accelera. Meglio uno stop prima della fascia o
   ben oltre, non in mezzo.
3. **Per la leva.** Il 10/10/2025 una cascata ha portato TAO a −62% in giornata. Le cascate sono il motivo per cui la leva
   alta viene liquidata prima che lo stop serva.
4. **Come contesto dopo una cascata.** Una fascia appena attraversata non c'è più: il carburante in quella direzione è
   finito. Non è un segnale di inversione, i test del radar sul rimbalzo dopo le cascate sono negativi.

Cosa varrebbe la pena testare, con dati che oggi mancano: le liquidazioni reali (non stimate) di Hyperliquid e Lighter, che
il radar raccoglie da poche settimane. Servono alcuni mesi di storia.

## 9. Limiti

- **La mappa testata è una stima** fatta con il metodo del radar su una sola borsa (Binance USDT-M), entro ±15% dal prezzo.
  Non è la mappa di Coinglass, di cui non esiste uno storico pubblico da testare.
- **Dati dal 12/2021 al 07/11/2026**: un solo ciclo e mezzo.
- **Scala giornaliera**: effetti di poche ore (il radar ne ha trovato uno a 12–24 ore, spiegato in gran parte dal momentum)
  non sono misurati qui.
- **Situazioni come quella di oggi sono rarissime nello storico** (2–3 episodi).
- Le fonti divulgative sulle heatmap descrivono l'effetto "calamita" come regola pratica; non ho trovato studi che lo
  dimostrino.

## 10. Riproducibilità

```bash
python backtest/liq_study.py
```

```bash
python backtest/build_report.py
```

`vendor/radar_liqmap.py` è `radar/liqmap.py` del repo radar (commit `2ec2afd`). Le mappe giornaliere sono in
`results/liq/mappe_21g.csv` e `mappe_90g.csv`.

## Fonti

- [Coinglass — come usare la mappa delle liquidazioni](https://coinglass.com/learn/how-to-use-liqmap-to-assist-trading-en) · [documentazione API della heatmap](https://docs.coinglass.com/v3.0/reference/liquidation-heatmap)
- [Cryptoticker — cosa mostra la heatmap di Coinglass e dove sono i suoi limiti](https://cryptoticker.io/en/coinglass-liquidation-heatmap-explained/) · [Cryptorank — i dati di liquidazione di Coinglass](https://cryptorank.io/news/feed/bf393-what-is-coinglass-crypto-liquidation-data-explained)
- [DexTools — come leggere le mappe di liquidazione](https://www.dextools.io/tutorials/how-to-read-liquidation-maps-in-crypto-guide-2026) · [Cryptonomist — guida alla liquidation heatmap](https://en.cryptonomist.ch/2025/12/17/liquidation-heatmap-trading-guide/)
- Studi del repo radar: `research/liquidazioni`, `research/liqmap_v2`, `research/liq_fasce`, `research/liq_squeeze`.
