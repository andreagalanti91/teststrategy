# Opzioni su BTC con i segnali di W3.2: guida da zero, strategia, backtest

Per chi non ha mai usato un'opzione. Cosa sono, come usarle con i segnali del radar, cosa dicono i dati, da dove si opera.
Dati fino al 23/11/2026; quotazioni OKX del 24/11/2026.

> Ricerca su dati storici, non una raccomandazione d'investimento.

## 1. Sintesi

**La strategia è semplice: a ogni segnale di W3.2 si compra una sola opzione a 30 giorni (call se long, put se short) spendendo
il 5% del capitale. Nel backtest rende circa metà di W3.2 con meno della metà del drawdown, e la perdita per operazione non
può superare il 5%. Non rende di più: fa rendere in modo più controllato. Si opera da OKX, che usi già.**

| Domanda | Risposta |
|---|---|
| Cos'è | Un contratto che dà il diritto di comprare (call) o vendere (put) BTC a un prezzo fissato, entro una data. Si paga un premio. Se va male si perde il premio e basta |
| La strategia | Segnale di W3.2 → una call o una put a 30 giorni, al prezzo corrente, con il 5% del capitale. Si vende quando W3.2 esce, o si incassa a scadenza |
| Risultato dal 2019 | 10.000 $ → 55.000 $ (+24% annuo), drawdown −14%, peggiore operazione −5%. W3.2 originale: 236.000 $ (+49%), drawdown −37%, peggiore −18% |
| Si può backtestare? | Sì, ma con prezzi delle opzioni calcolati da una formula: lo storico vero dei contratti scaduti non è gratuito. Dove esistono prezzi veri (OKX, ottobre–novembre 2026) il modello sbaglia dell'1% in mediana |
| Quanto è solido | 20 operazioni. Regge a opzioni più care del 20% (+18% annuo) e a costi doppi (+23%). Non regge se i segnali di W3.2 peggiorano: con metà delle operazioni in guadagno il risultato a tre anni è +31% e la probabilità di perdere è del 16% |
| Da dove si opera | OKX Europe offre opzioni su BTC ai clienti al dettaglio: contratto minimo 0,01 BTC (circa 35 $ di premio), premio e incasso in dollari. Bitget non ha opzioni |
| Come partire | Prima sulla carta: annotare il prezzo vero a ogni segnale. Poi con un contratto. Il 5% solo dopo aver visto almeno 3–4 operazioni |

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

W3.2 guadagna soprattutto nelle prime settimane dopo il segnale: per questo un'opzione breve ne cattura una buona parte.

## 4. La strategia

1. **Segnale**: quello di W3.2 del radar, senza modifiche. Si entra il lunedì.
2. **Cosa comprare**: una call se il segnale è long, una put se è short.
3. **Scadenza**: quella più vicina a 30 giorni (fra 25 e 40). Su OKX le scadenze sono il venerdì.
4. **Prezzo d'esercizio**: il più vicino al prezzo di BTC in quel momento.
5. **Quanto**: il 5% del capitale in premio, commissioni incluse. Il resto del capitale resta fermo, in dollari.
6. **Uscita**: quando W3.2 esce, si vende l'opzione. Se l'opzione scade prima, l'incasso è automatico e si resta fuori fino al
   prossimo segnale.
7. **Mai**: rinnovare l'opzione scaduta, aumentare la quota dopo una perdita, vendere opzioni.
8. **Ordini**: sempre con prezzo limite, a metà fra denaro e lettera.

Le scelte sono poche e fissate prima: una opzione per segnale, perdita massima nota all'ingresso.

## 5. Il backtest

Prezzi delle opzioni calcolati con la formula di Black e la volatilità implicita stimata delle opzioni alla pari. Il valore
è ricalcolato ogni giorno. "Una sola" = regola 6; "con rinnovo" = alla scadenza se ne compra un'altra finché W3.2 resta in
posizione.

{{P1}}

- **Una sola opzione batte il rinnovo.** Rinnovare ogni mese costa: nelle operazioni lunghe e lente (2022–2023, 2025) si
  spende il 25–35% del capitale in premi per un movimento piccolo. È il motivo della regola 7.
- **La scadenza breve batte la lunga.** A parità di spesa, l'opzione a 30 giorni muove più controvalore.
- **5% contro 10%.** Il 10% rende quanto W3.2 originale (230.000 $) con drawdown −26% invece di −37%. Ma una serie di quattro
  perdite piene fa −34%. Il 5% è la quota coerente con il tuo limite di drawdown e con i 2–3.000 $ che già destini alla leva.
- **Rispetto a W3.2 a metà dimensione** il rendimento è simile: la differenza è il drawdown più basso e la perdita per
  operazione fissata in partenza.

Operazione per operazione, versione base:

{{P2}}

Dove l'opzione fa peggio: operazioni lunghe in cui BTC si muove dopo il primo mese (n. 1, 4, 12, 15, 17). Dove fa meglio: quando
W3.2 sbaglia (n. 3: −5% invece di −18%) e quando il movimento è subito forte (n. 5, 6, 14). In tre casi (n. 10, 18, 19) l'opzione
guadagna più di W3.2, che chiude in pari o in perdita, perché il movimento giusto c'è stato nel primo mese e poi è rientrato.

## 6. Quanto è solido

{{P3}}

- Il risultato non dipende dal prezzo esatto dell'opzione: con volatilità pagata il 20% in più si scende da +24% a +18% annuo.
- Dipende invece dalla scelta del prezzo d'esercizio meno di quanto sembri: fuori dal prezzo rende di più con meno operazioni
  in guadagno, dentro il prezzo il contrario. Alla pari è la scelta di mezzo, non la migliore a posteriori.

{{P4}}

Il punto debole è uno solo: **la strategia vale quanto i segnali di W3.2**. Dal 2019 l'80% delle operazioni ha chiuso in
guadagno. Se quella quota scende al 50%, a tre anni il risultato mediano è +31% e una volta su sei si chiude in perdita. Se
scende al 35% la strategia non guadagna più. La perdita resta comunque lenta: 5% per volta.

## 7. Il modello contro i prezzi veri

{{P5}}

- **Sulla scadenza della strategia il modello è centrato**: 318 prezzi veri fra il 13/10 e il 17/11/2026, mediana 1,01, metà
  dei casi fra 0,96 e 1,07. Le opzioni vere costavano l'1% in più del modello.
- **Al livello del DVOL il modello sarebbe troppo caro del 5%**: conferma che la volatilità giusta è quella delle opzioni alla
  pari, più bassa dell'indice.
- **Sulle scadenze lunghe le opzioni vere costano di più** (fino al 9% oltre i 180 giorni): il modello usa la volatilità a 30
  giorni anche per quelle. È un altro motivo per restare sulle scadenze brevi.
- **Il limite**: OKX conserva lo storico solo dei contratti ancora vivi. Per i 30 giorni il confronto copre cinque settimane
  del 2026, non il 2019–2025. Per coprire tutto servono i prezzi storici di Deribit, che non sono raggiungibili da questo
  ambiente, oppure il tempo: lo script di § 10 costruisce lo storico da oggi in avanti.
- La differenza denaro-lettera vera oggi è l'1% del premio in totale; il backtest usa il 3% per lato, cioè sei volte tanto.

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
- **Campione piccolo e favorevole.** 20 operazioni dal 2019. Il 2018 non c'è perché mancano i dati di volatilità, ed è stato
  l'anno peggiore di W3.2 (due perdite e un guadagno).
- **Scadenza scelta dopo aver visto i risultati.** Fra 30, 60 e 90 giorni la migliore è 30. Con 90 giorni il risultato è
  +18% annuo invece di +24%.
- **Prezzi da modello.** § 7 misura lo scarto solo sul 2026.
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
- Quotazioni: API pubblica OKX (`data/opzioni/okx/`). Volatilità storica: indice DVOL e scambi Deribit (`data/opzioni/`).

Codice: `backtest/opzioni_w32.py`, `backtest/fetch_okx_options.py`. Tabelle: `results/opzioni_w32/tables.md`.
Studio precedente sulle opzioni vendute e sulla leva: [`RICERCA_NUOVA.md`](RICERCA_NUOVA.md).
