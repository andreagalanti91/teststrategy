# Opzioni su BTC con i segnali di W3.2: guida da zero, strategia, backtest

Per chi non ha mai usato un'opzione. Cosa sono, come usarle con i segnali del radar, cosa dicono i dati, da dove si opera.
Dati fino al 23/11/2026; quotazioni OKX del 24/11/2026.

> Ricerca su dati storici, non una raccomandazione d'investimento.

## 1. Sintesi

**La strategia è semplice: a ogni segnale di W3.2 si compra una sola opzione a circa 30 giorni (call se long, put se short)
spendendo il 5% del capitale. Rifatta con i prezzi veri delle opzioni dal 2018, rende quanto W3.2 a metà dimensione: non di
più. Quello che cambia è che la perdita per operazione è fissata al 5% in partenza, senza stop e senza leva. Si opera da
OKX, che usi già.**

| Domanda | Risposta |
|---|---|
| Cos'è | Un contratto che dà il diritto di comprare (call) o vendere (put) BTC a un prezzo fissato, entro una data. Si paga un premio. Se va male si perde il premio e basta |
| La strategia | Segnale di W3.2 → una call o una put a circa 30 giorni, al prezzo corrente, con il 5% del capitale. Si vende quando W3.2 esce, o si incassa a scadenza |
| Si può backtestare? | Sì, e con prezzi veri: l'archivio pubblico di Deribit ha gli scambi di tutte le opzioni scadute. Ho rifatto le 23 operazioni di W3.2 dal 2018 con i contratti realmente scambiati quel giorno |
| Risultato con prezzi veri, dal 2018 | 10.000 $ → 55.000 $. W3.2 a metà dimensione: 53.000 $. W3.2 intera: 209.000 $ |
| Cosa cambia rispetto a W3.2 a metà | Perdita peggiore per operazione −5% invece di −12,5%; serie peggiore di perdite −8% invece di −14%. Ma operazioni in guadagno 65% invece di 78% |
| E con il 10%? | 228.000 $ contro 209.000 $ di W3.2 intera, perdita peggiore −10% invece di −25%, serie peggiore −16% invece di −27% |
| Quanto è solido | 23 operazioni, e le tre migliori fanno metà del risultato. La singola operazione dipende molto dalla scadenza disponibile quel giorno. Se i segnali di W3.2 peggiorano (metà delle operazioni in guadagno) il risultato a tre anni scende a +32% e una volta su sei si perde |
| Il modello era giusto? | Sì: la volatilità vera all'ingresso è stata in mediana 1,02 volte quella del modello. La differenza di risultato viene dalle scadenze: nella realtà esistono solo i venerdì, fra 25 e 46 giorni |
| Da dove si opera | OKX Europe offre opzioni su BTC ai clienti al dettaglio: contratto minimo 0,01 BTC (circa 35 $ di premio), premio e incasso in dollari. Bitget non ha opzioni |
| Come partire | Prima sulla carta: annotare il prezzo vero a ogni segnale. Poi con un contratto. Il 5% solo dopo aver visto almeno 3–4 operazioni |

Una verifica indipendente ha riprodotto i calcoli del backtest a modello e ne ha ridimensionato le conclusioni; il backtest
con i prezzi veri, fatto dopo, conferma il quadro: equivale a W3.2 a metà dimensione, con un profilo di perdita diverso.

## 2. Le opzioni in una pagina

**Call**: il diritto di comprare BTC a un prezzo fissato (prezzo d'esercizio) entro una data (scadenza). Guadagna se BTC sale.

**Put**: il diritto di vendere BTC a un prezzo fissato entro una data. Guadagna se BTC scende.

**Premio**: quanto costa quel diritto. Si paga subito. È tutto quello che si può perdere.

Cosa succede alla scadenza di una call con prezzo d'esercizio 60.000 $:

- BTC a 70.000 $: l'opzione vale 10.000 $ (la differenza). Su OKX non si riceve BTC: si incassa la differenza in dollari.
- BTC a 60.000 $ o meno: l'opzione vale zero. Si è perso il premio.

Per la put è lo specchio: vale la differenza se BTC è sotto il prezzo d'esercizio, zero se è sopra.

Tre cose da sapere prima di tutto:

1. **Il tempo lavora contro chi compra.** Ogni giorno che passa senza movimento l'opzione vale un po' meno. A 30 giorni dalla
   scadenza un'opzione al prezzo corrente perde circa l'1,7% del suo valore al giorno, e sempre più in fretta verso la fine.
2. **Il prezzo dipende dalla volatilità attesa.** Quando il mercato è nervoso le opzioni costano di più. La misura si chiama
   volatilità implicita: oggi è il 50% annuo, e un'opzione a 30 giorni al prezzo corrente costa il 5,6–5,9% del prezzo di BTC.
3. **Comprare e vendere non sono simmetrici.** Chi compra rischia solo il premio. Chi vende incassa il premio e rischia
   perdite senza limite: lo studio precedente (`RICERCA_NUOVA.md`) mostra che su BTC vendere è finito male. Qui si compra soltanto.

Le parole che si incontrano sulla piattaforma:

| Termine | Significato |
|---|---|
| Strike | Prezzo d'esercizio |
| Expiry | Scadenza |
| ATM (at the money) | Opzione con prezzo d'esercizio uguale al prezzo corrente: "alla pari" |
| OTM / ITM | Fuori dal prezzo (più economica, serve più movimento) / dentro il prezzo (più cara, vale già qualcosa) |
| Bid / Ask | Denaro (prezzo a cui si vende) / lettera (prezzo a cui si compra) |
| IV | Volatilità implicita |
| Delta | Di quanto cambia il prezzo dell'opzione se BTC si muove di 1 $. Alla pari è circa 0,5 |
| Theta | Quanto valore perde l'opzione in un giorno |
| Mark price | Prezzo teorico calcolato dalla piattaforma: serve da riferimento per mettere l'ordine |

### Un esempio con i prezzi veri di oggi

{{P6}}

![Capitale nel tempo e guadagno a scadenza](results/opzioni_w32/opzioni_w32.png)

Il grafico in basso mostra la differenza con il perp. Se BTC scende molto, la put guadagna quasi quanto lo short (meno il
premio). Se BTC sale, lo short perde senza limite finché non scatta lo stop; la put si ferma al premio. Il prezzo di questa
protezione è la fascia centrale: se BTC si muove poco, il perp chiude in pari e la put perde.

## 3. Perché usarle con W3.2

W3.2 oggi apre una posizione spot o perp con uno stop a 2,5 ATR settimanali, dimensionata per perdere il 25% del capitale se
lo stop scatta. Con l'opzione cambia il modo di prendere lo stesso rischio:

| | W3.2 su spot o perp | W3.2 con opzione comprata |
|---|---|---|
| Perdita massima per operazione | Circa 25% allo stop; di più se il prezzo salta lo stop | Il premio pagato: 5% |
| Stop | Necessario, può essere saltato o preso da un movimento breve | Non serve |
| Liquidazione | Possibile con la leva | Impossibile |
| Se BTC resta fermo | Pari | Perdita del premio |
| Se BTC si muove piano nella direzione giusta | Guadagno | Poco o niente: il tempo consuma il premio |
| Se BTC si muove in fretta nella direzione giusta | Guadagno | Guadagno, amplificato |
| Durata | Finché W3.2 non esce | Al massimo 30 giorni |

W3.2 guadagna spesso nelle prime settimane dopo il segnale: per questo un'opzione breve ne cattura una buona parte. Quando
invece il movimento arriva dopo il primo mese, l'opzione è già scaduta.

## 4. La strategia

1. **Segnale**: quello di W3.2 del radar, senza modifiche. Si entra il lunedì.
2. **Cosa comprare**: una call se il segnale è long, una put se è short.
3. **Scadenza**: il venerdì più vicino a 30 giorni fra quelli disponibili (nella pratica fra 25 e 46 giorni).
4. **Prezzo d'esercizio**: il più vicino al prezzo di BTC in quel momento.
5. **Quanto**: il 5% del capitale in premio, commissioni incluse. Il resto del capitale resta fermo, in dollari.
6. **Uscita**: quando W3.2 esce, si vende l'opzione. Se l'opzione scade prima, l'incasso è automatico e si resta fuori fino al
   prossimo segnale.
7. **Mai**: rinnovare l'opzione scaduta, aumentare la quota dopo una perdita, vendere opzioni.
8. **Ordini**: sempre con prezzo limite, a metà fra denaro e lettera.

Le scelte sono poche e fissate prima: una opzione per segnale, perdita massima nota all'ingresso.

## 5. Il backtest a modello

Serve a provare molte varianti in fretta; § 7 lo rifà con i prezzi veri. Prezzi delle opzioni calcolati con la formula di Black e la volatilità implicita stimata delle opzioni alla pari. Il valore
è ricalcolato ogni giorno. "Una sola" = regola 6; "con rinnovo" = alla scadenza se ne compra un'altra finché W3.2 resta in
posizione.

{{P1}}

- **Il confronto giusto è con W3.2 a metà dimensione**, non con W3.2 intera: l'opzione al 5% rende lo stesso (+24% annuo) con
  drawdown −14% invece di −20%. Al 10% rende quanto W3.2 intera con drawdown −26% invece di −37%. Vedi però § 6: includendo
  il 2018 la differenza di drawdown sparisce.
- **Il rinnovo peggiora il drawdown, sempre.** Rinnovare ogni mese costa: nelle operazioni lunghe e lente (2022–2023, 2025) si
  spende il 25–35% del capitale in premi per un movimento piccolo. È il motivo della regola 7.
- **Scadenza breve o lunga: è soprattutto leva.** A parità di spesa l'opzione a 30 giorni muove più controvalore di quella a
  90. Fra 21 e 45 giorni il rendimento non cambia in modo distinguibile (§ 6).
- **5% contro 10%.** Il 5% è una scelta prudente, non un calcolo: dà un drawdown di −14/−20%. Il tuo limite di −35% si
  raggiunge verso il 9–10% (−26% dal 2019, −37% dal 2018). Il 5% corrisponde anche ai 2–3.000 $ che già destini alla leva.

Operazione per operazione, versione base:

{{P2}}

Dove l'opzione fa peggio: operazioni lunghe in cui BTC si muove dopo il primo mese (n. 1, 4, 12, 15, 17). Dove fa meglio: quando
W3.2 sbaglia (n. 3: −5% invece di −18%) e quando il movimento è subito forte (n. 5, 6, 14). In tre casi (n. 10, 18, 19) l'opzione
guadagna più di W3.2, che chiude in pari o in perdita, perché il movimento giusto c'è stato nel primo mese e poi è rientrato.

## 6. Quanto è solido

### Prezzo dell'opzione, costi, scadenza

{{P3}}

- **Prezzo dell'opzione.** Pagare la volatilità il 20% in più toglie un terzo del capitale finale (da 55.000 a 37.000 $):
  circa 3 punti di rendimento annuo ogni 10% di prezzo. Il risultato resta positivo, ma non è indifferente.
- **Costi.** Raddoppiare la differenza denaro-lettera costa meno di 2 punti annui.
- **Giorno di scadenza.** Fra 21 e 45 giorni il rendimento sta fra +22% e +26%: nessuna scadenza è chiaramente migliore. Ma
  il drawdown va da −10% a −17% e le operazioni in guadagno dal 65% all'80%: l'80% della versione a 30 giorni è il valore più
  alto della griglia. Su OKX le scadenze sono solo il venerdì, quindi il giorno esatto non si sceglie.
- **Poche operazioni contano molto.** Senza le tre migliori il rendimento scende a +12% annuo, senza le cinque migliori a +7%.

### Il 2018, con la volatilità stimata e la scadenza a 30 giorni esatti

{{P7}}

Con il 2018 dentro, l'opzione al 5% e W3.2 a metà dimensione sono uguali: +19–20% annuo, drawdown −20%. In questa prova le
tre operazioni del 2018 perdono tutte con l'opzione, compresa quella che W3.2 chiude a +16,7%: lo short di ottobre scade il
giorno prima del crollo di novembre. Con i contratti veri (§ 7) quel giorno la scadenza disponibile era a 74 giorni, e la
stessa operazione chiude a +14%. È la misura di quanto pesa il caso sulla singola operazione.

### Se i segnali peggiorano

{{P4}}

- Nei percorsi simulati l'opzione al 5% e W3.2 a metà dimensione sono vicine: rendimento mediano a tre anni +95% e +98%,
  drawdown mediano −9% e −11%.
- **La strategia vale quanto i segnali di W3.2.** Dal 2019 l'80% delle operazioni ha chiuso in guadagno. Se quella quota
  scende al 50%, a tre anni il risultato mediano è +32% e una volta su sei si chiude in perdita. Se scende al 35% non si
  guadagna più. La perdita resta lenta: 5% per volta.
- Gli altri punti deboli sono quelli visti sopra: prezzi da modello, poche operazioni decisive, il caso sulla scadenza.

## 7. Il backtest con i prezzi veri

Deribit è il mercato dove si scambia la maggior parte delle opzioni su BTC, e pubblica tutti gli scambi dei contratti
scaduti. Per ogni operazione di W3.2:

- all'ingresso si prende, fra le opzioni davvero scambiate nelle 12 ore intorno, la scadenza più vicina a 30 giorni e il
  prezzo d'esercizio più vicino al prezzo di BTC;
- il prezzo pagato è calcolato con la volatilità implicita di quegli scambi;
- all'uscita si usa la volatilità degli scambi dello stesso contratto in quel momento; se l'opzione scade prima, il valore
  alla scadenza.

{{Q1}}

{{Q2}}

- **Dal 2018, con prezzi veri, l'opzione al 5% e W3.2 a metà dimensione finiscono pari**: 55.000 $ e 53.000 $.
- **Il profilo è diverso.** L'opzione perde più spesso (35% delle operazioni contro 22%) ma poco per volta: mai più del 5%, e
  la serie peggiore di perdite è −8% contro −14%. Nel 2018 W3.2 apre con −25% alla prima operazione; l'opzione con −4,9%.
- **Al 10%** il risultato supera W3.2 intera (228.000 $ contro 209.000 $) con perdite più contenute. Sono però gli stessi
  segnali con più leva: vale tutto quello che dice § 6 sulla dipendenza da poche operazioni.
- **Il modello era centrato.** Volatilità vera in media 65%, modello 64%. Il risultato a modello (55.000 $ dal 2019) e quello
  vero (53.000 $) sono vicini.
- **La scadenza non si sceglie.** I contratti veri avevano fra 18 e 74 giorni di vita: fino al 2019 esistevano poche scadenze.
  Dal 2020 in poi si resta fra 25 e 46 giorni.
- **Usando direttamente il primo scambio dopo l'ingresso** invece della volatilità mediana, il risultato dal 2019 è 46.000 $:
  il momento esatto dell'ordine conta.

Limiti di questo backtest: i prezzi sono ricostruiti dalla volatilità scambiata, non sono il book del momento; la
differenza denaro-lettera è una stima (3% per lato; oggi è circa 0,5%); nel 2018–2019 gli scambi erano pochi.

### Controllo sui prezzi di OKX

{{P5}}

Sulla scadenza della strategia (20–45 giorni) i prezzi veri di OKX fra ottobre e novembre 2026 costavano l'1% in più del
modello. Al livello del DVOL il modello sarebbe stato troppo caro del 5%: la volatilità giusta è quella delle opzioni alla
pari. OKX conserva lo storico solo dei contratti ancora vivi, per questo il confronto copre poche settimane. La differenza
denaro-lettera vera oggi è l'1% del premio in totale; il backtest usa il 3% per lato.

## 8. Da dove si opera

| Sede | Cliente al dettaglio in Italia | Contratto minimo | Commissioni | Note |
|---|---|---|---|---|
| **OKX Europe** (Malta, licenza MiFID) | Sì, con test di appropriatezza | 0,01 BTC | 0,03% del controvalore, tetto 7% del premio; esercizio 0,02% | Opzioni lineari: premio e incasso in USD/USDC. Documento informativo (KID) in italiano |
| Deribit | Incerto | 0,1 BTC (0,01 sulle lineari) | 0,03%, tetto 12,5% del premio | Il mercato più liquido, ma senza licenza UE: base giuridica dubbia |
| Kraken Pro | Incerto | n.d. | n.d. | Opzioni nel SEE da ottobre 2026, solo su richiesta di quotazione |
| Interactive Brokers | Sì | 100 quote dell'ETF | Da broker | Opzioni sull'ETF IBIT: mercato USA, orari di borsa, non 24 ore |
| Bitget, Bybit EU, Binance | No | – | – | Bitget non risulta avere licenza UE né opzioni per l'Italia |

La scelta pratica è OKX: è l'exchange che usi, ha la licenza europea e il contratto più piccolo. Da verificare nell'app se
la sezione opzioni è già attiva sul tuo conto: i documenti la prevedono, ma non ho trovato un annuncio di lancio per l'Italia.

Come si fa, passo per passo:

1. Nell'app o sul sito: Trade → Options. Al primo accesso viene chiesto un questionario di conoscenza.
2. Scegliere BTC e la scadenza (il venerdì più vicino a 30 giorni).
3. Nella tabella dei prezzi d'esercizio scegliere la riga più vicina al prezzo di BTC: colonna Call a sinistra, Put a destra.
4. Buy, ordine Limit, prezzo a metà fra Bid e Ask, quantità in contratti (1 contratto = 0,01 BTC).
5. Per chiudere prima della scadenza: Sell sulla stessa opzione, di nuovo con ordine limite.
6. Alla scadenza (08:00 UTC del venerdì) non serve fare nulla: se l'opzione vale qualcosa l'importo viene accreditato.

Fisco, solo un cenno e da verificare con un commercialista: le plusvalenze su cripto-attività sono tassate al 33% dal 2026;
i derivati su cripto secondo i commentatori restano al 26% come redditi diversi. Con un exchange estero la dichiarazione è a
carico tuo (quadri RT e RW).

## 9. Cosa può andare storto

- **Segnali peggiori che in passato.** È il rischio principale (§ 6).
- **Campione piccolo.** 23 operazioni in nove anni.
- **Il caso sulla scadenza.** La singola operazione può passare da perdita piena a guadagno per uno o due giorni di differenza.
- **Prezzi ricostruiti.** § 7 usa la volatilità degli scambi veri, non il prezzo esatto a cui avresti comprato tu.
- **Un'operazione tagliata.** La n. 6 è chiusa il 31/12/2020 per un cambio di dati nel backtest di W3.2, non per un segnale.
- **Liquidità delle opzioni lineari.** Su OKX le quotazioni ci sono, con una differenza denaro-lettera dell'1%, ma gli scambi
  sono pochi: per importi sopra qualche BTC il prezzo può peggiorare. Per 0,5–1 BTC non è un problema.
- **Capitale fermo.** Il 95% resta in dollari senza rendere. È una scelta: è il motivo per cui il drawdown è basso.
- **Tentazione di raddoppiare.** Dopo due o tre premi persi viene voglia di alzare la quota. La regola 7 esiste per questo.

## 10. Come partire

1. **Sulla carta, da subito.** A ogni segnale di W3.2 annotare: data, prezzo di BTC, opzione scelta, prezzo lettera. All'uscita:
   prezzo denaro. Costa zero e dopo qualche operazione dice se il modello è realistico.
2. **Registrare i prezzi.** `python backtest/fetch_okx_options.py` salva la catena completa di OKX: lanciato ogni giorno
   costruisce lo storico vero che oggi manca.
3. **Un contratto.** Alla prima operazione reale, un solo contratto (circa 35 $): serve a imparare la piattaforma.
4. **La quota piena** (5%) solo dopo 3–4 operazioni seguite dall'inizio alla fine.

## 11. Fonti

- OKX Europe, condizioni di servizio e documenti informativi (KID) —
  [termini](https://www.okx.com/en-eu/help/okx-europe-market-ltd-oem-terms-of-service),
  [KID](https://www.okx.com/en-eu/help/oem-key-information-documents-kids),
  [commissioni SEE](https://www.okx.com/en-eu/help/trading-fee-rules-faq-eea)
- Deribit, giurisdizioni escluse — [pagina](https://support.deribit.com/hc/en-us/articles/25944487427741-Restricted-Jurisdictions)
- Kraken, opzioni nel SEE — [annuncio](https://blog.kraken.com/product/kraken-derivatives/options-now-available-in-the-eea)
- Interactive Brokers, opzioni su ETF USA per clienti UE — [nota](https://www.interactivebrokers.com/support/faq/content/40360001)
- Fisco 2026 — [Agenda Digitale](https://www.agendadigitale.eu/documenti/tassazione-cripto-attivita-2026-cosa-cambia-su-plusvalenze-permute-e-isee/)
- Scambi storici delle opzioni: archivio pubblico Deribit, `history.deribit.com` (`data/opzioni/deribit/`).
- Quotazioni: API pubblica OKX (`data/opzioni/okx/`). Volatilità storica: indice DVOL e scambi Deribit (`data/opzioni/`).

Codice: `backtest/opzioni_w32.py`, `backtest/opzioni_w32_reale.py`, `backtest/fetch_okx_options.py`. Tabelle: `results/opzioni_w32/tables.md`.
Studio precedente sulle opzioni vendute e sulla leva: [`RICERCA_NUOVA.md`](RICERCA_NUOVA.md).
