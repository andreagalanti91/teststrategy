# Il prezzo di BTC segue le liquidazioni?

Come verificarlo sui dati, cosa risulta, e come leggere la mappa di Coinglass del 24/11/2026 (prezzo 60.388 $).

> Ricerca su dati storici, non una raccomandazione d'investimento.

## 1. Sintesi

**No: nei dati dal 2022 non c'è un effetto misurabile delle liquidazioni oltre la semplice distanza dal prezzo. La mappa
racconta dove è già passato il prezzo, non dove andrà.**

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

{{L0}}

## 4. Risultati con memoria di 21 giorni

### 4.1 La mappa descrive il passato

{{L1}}

Lo squilibrio è alto (più short sopra) dopo che il prezzo è sceso, e viceversa. Con il futuro non ha relazione.

### 4.2 Il lato più carico non indica la direzione

{{L2}}

- Con gli short dominanti sopra il prezzo sale un po' più della media, ma solo nel 2022–23 (+5,1% a 7 giorni); dal 2024 è
  −0,1%.
- Anche con i long dominanti sotto il prezzo sale più della media. I due estremi danno lo stesso risultato: non è la
  direzione dello squilibrio a contare, sono giorni che seguono movimenti forti.

### 4.3 Le fasce grandi non attirano il prezzo

{{L3}}

Le differenze fra "raggiunto" e "atteso" stanno tutte entro due punti e cambiano segno fra i due periodi.

### 4.4 Viene toccata la fascia più vicina, non la più grande

{{L4}}

È il test più diretto. Se le liquidazioni attirassero il prezzo, la fascia più grande dovrebbe vincere anche quando è più
lontana. Succede una volta su tre a 7 giorni e una su cinque a 1 giorno.

Controlli aggiuntivi fatti dalla verifica indipendente, a 7 giorni:

- **Fascia più grande almeno doppia dell'altra** (104 giorni): viene toccata nel 66% dei casi, la più vicina nel 75%; quando
  la più grande non è la più vicina, nel 36%. Con rapporto almeno triplo: 26%.
- **Ordine esatto sul percorso orario** (quale fascia viene toccata per prima): stessi numeri, 59% la più grande, 72% la più
  vicina, 33% la più grande quando è più lontana.
- **A parità di distanza** il lato più grande è toccato per primo un po' più spesso (da 1 a 5 punti in quattro gruppi su
  cinque), ma la relazione è debole (correlazione 0,05) e non distinguibile da zero. Quindi: nessun effetto misurabile della
  dimensione, non un effetto nullo dimostrato.

### 4.5 Situazioni simili a oggi

{{L5}}

Gli episodi sono due o tre: non bastano per dire nulla. Questa mappa arriva a ±15% dal prezzo e si ferma al 07/11, quindi
non riproduce il quadro di Coinglass di oggi.

## 5. Con memoria di 90 giorni

Stessa prova con una mappa più "lunga", più vicina a quelle di Coinglass. Le conclusioni non cambiano.

{{L6}}

{{L7}}

{{L8}}

{{L9}}

{{L10}}

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
- **Nessuna misura di incertezza formale**: le finestre a 7 giorni si sovrappongono e le mappe cambiano lentamente, quindi i
  giorni davvero indipendenti sono molti meno di 1.782. Le righe con pochi giorni (squilibri oltre il 60%, situazioni simili a
  oggi) non sostengono alcuna conclusione.
- **"Atteso a pari distanza" è calcolato su tutto il campione**, senza tenere conto della volatilità del momento.
- **Verifica indipendente**: un secondo agente ha ricostruito le mappe a mano su sei date (coincidono), escluso l'uso di dati
  futuri e ricalcolato i test della mappa a 21 giorni (confermati). La mappa a 90 giorni non è stata riverificata.
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
