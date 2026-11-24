# Nuovo ciclo di ricerca: cosa manca, e la matematica che serve

Quattro cose che nei cicli precedenti non avevamo guardato: quanto sono affidabili i risultati, quanta leva usare, la
volatilità come fonte di rendimento, le opzioni come strumento. Dati fino al 23/11/2026.

> Ricerca su dati storici, non una raccomandazione d'investimento.

## 1. Sintesi

**W3.2 resta la strategia principale e la sua leva giusta è 1x. La sola aggiunta che esce da questo ciclo è vendere
volatilità con il delta coperto, in piccola quota: rende per un motivo diverso dal trend e perde in momenti diversi. Vendere
opzioni senza copertura, invece, su BTC ha perso quasi tutto.**

| Domanda | Risultato | Cosa farne |
|---|---|---|
| I risultati di W3.2 possono essere fortuna? | Lo Sharpe (1,2) è certamente sopra zero se W3.2 fosse l'unica idea provata. Se si contano i tentativi, regge fino a una decina; con cento varianti provate la probabilità scende al 41–49% | Non aggiungere altre regole a W3.2. Ogni variante in più abbassa la fiducia in tutte |
| Quanta leva su W3.2? | La formula di Kelly dice 4x, ma a 2x la probabilità di un drawdown oltre −35% in tre anni è del 75%. A 1x è del 10% | 1x. Mai oltre 1,5x |
| La volatilità implicita di BTC è troppo cara? | Sì: è stata sopra quella poi realizzata nel 67% dei giorni, in media di 6 punti | È un premio, come quello di un'assicurazione: chi vende opzioni lo incassa |
| Basta vendere opzioni per incassarlo? | No. Straddle e strangle venduti senza copertura: da 10.000 $ a 1.400–2.200 $, drawdown −87/−93% | Mai opzioni vendute nude su BTC |
| E coprendo il delta ogni giorno? | Sì: +13% annuo dal 2019 con drawdown −25%, al netto di costi e funding (+23% e +11% nei due periodi con dati DVOL). Correlazione −0,27 con W3.2. Regge all'esame statistico solo sul periodo con dati buoni | Unica candidata nuova. Quota piccola (20% o meno), dopo una prova con importi minimi |
| Opzioni comprate al posto del perp per W3.2? | La perdita per operazione è limitata, ma il rendimento scende a meno di metà. A parità di rischio rende come W3.1 | Non conviene. Lo stop di W3.2 fa già quel lavoro senza pagare un premio |
| I dati delle opzioni anticipano il prezzo? | No: inclinazione, volumi put/call e livello della volatilità non prevedono BTC a 4 settimane | Nessun segnale d'ingresso da qui |

## 2. Cosa manca: la mappa

Cosa abbiamo già verificato in questo repo, e cosa no.

| Area | Stato | Esito | Dove |
|---|---|---|---|
| Trend settimanale con flussi e funding (W3.2) | Verificato | Funziona: è il riferimento | `CONFRONTO_W32.md`, `W32_INGRESSI_USCITE.md` |
| Analisi tecnica giornaliera (voto di indicatori, tre schermi) | Verificato | Più debole di W3.2 | `ANALISI_BTC.md`, `REGOLE_AT.md` |
| Altcoin con MACD a regime | Verificato | Positivo, molto volatile | `ALGORITMO.md`, `SWING.md` |
| Intraday su BTC | Verificato | Nessun vantaggio dopo i costi | `INTRADAY.md` |
| DCA in ingresso e in uscita, acquisti sul supporto | Verificato | Non migliorano | `W32_INGRESSI_USCITE.md`, `SWING.md` |
| Sentiment, liquidazioni, supporti e resistenze | Verificato | Nessun segnale d'ingresso | `ANALISI_BTC.md`, `LIQUIDAZIONI.md`, `LIVELLI_BTC.md` |
| Carry sul funding | Verificato | Regolare, ma rende il 7% annuo | `STRATEGIE.md` |
| **Affidabilità statistica dei risultati** | **Questo ciclo** | W3.2 regge a pochi tentativi, non a centinaia | § 3 |
| **Leva e dimensione della posizione** | **Questo ciclo** | 1x | § 4 |
| **Volatilità come fonte di rendimento** | **Questo ciclo** | Premio reale; incassabile solo con copertura | § 5–7 |
| **Opzioni come strumento** | **Questo ciclo** | Comprate non convengono; vendute solo coperte | § 6, § 8 |
| **Segnali dal mercato delle opzioni** | **Questo ciclo** | Nessuno sul prezzo | § 9 |
| Superficie di volatilità reale (prezzi per strike e scadenza) | Manca | Serve per confermare § 6 | Dati Deribit storici, a pagamento |
| Base dei futures a scadenza (cash-and-carry) | Manca | Parente del carry sul funding | Storico futures trimestrali OKX/Deribit |
| Flussi on-chain e degli ETF | Manca | Il radar ha già i flussi dei perp | Fornitori esterni |
| Libro ordini e microstruttura | Manca | Rilevante solo per l'intraday, già scartato | Dati tick |
| Arbitraggio statistico fra altcoin (coppie) | Manca | Fattibile con i dati che abbiamo | `data/alts/` |

## 3. Quanto ci si può fidare di un backtest

### La matematica

Lo **Sharpe** misura il rendimento medio per unità di oscillazione: `Sharpe = media / deviazione standard`, portato su base
annua moltiplicando per √52 se i rendimenti sono settimanali.

Uno Sharpe misurato su pochi anni è una stima con un errore. Il **Probabilistic Sharpe Ratio** (Bailey e López de Prado) dà
la probabilità che lo Sharpe vero superi una soglia `S*`:

```
PSR = Φ( (S − S*) · √(n − 1) / √(1 − γ3·S + (γ4 − 1)/4 · S²) )
```

`n` è il numero di osservazioni, `γ3` l'asimmetria, `γ4` la curtosi, `Φ` la distribuzione normale. Rendimenti con code
pesanti o asimmetria negativa allargano l'errore.

Il problema vero è un altro. Se provo 100 varianti e tengo la migliore, quella avrà uno Sharpe alto anche se nessuna
funziona. Lo **Sharpe deflazionato** usa come soglia `S*` lo Sharpe che il migliore di `N` tentativi senza abilità raggiunge
per caso:

```
S* = σ_S · [ (1 − γ)·Φ⁻¹(1 − 1/N) + γ·Φ⁻¹(1 − 1/(N·e)) ]        γ = 0,5772
```

`σ_S` è quanto variano gli Sharpe fra i tentativi. Nelle nostre griglie è 0,31–0,37; per prudenza uso 0,5.

### I risultati

{{A1}}

Come leggere:

- **W3.2** ha uno Sharpe di 1,2. Preso da solo è sopra zero con certezza. Contro 10 tentativi regge (90%). Contro 100 scende
  sotto il 50%: uno Sharpe di 1,27 esce per caso dal migliore di cento tentativi.
- Quanti tentativi contare per W3.2? È la versione 3.2 di un sistema che ha avuto più revisioni, tarata sul 2021–2026. Non
  sono mille, ma nemmeno uno. La cifra onesta è "decine". Il 2018–2020, che non è stato usato per tararla, dà uno Sharpe
  simile: è l'argomento migliore a suo favore.
- **v1 e v2** (analisi tecnica) non reggono: v1 nel periodo di sola verifica ha Sharpe 0,64, cioè 37% contro 10 tentativi.
  Ne avevamo provati 104 e 126.
- **Il carry sul funding** è l'unico che passa qualunque soglia. Ha uno Sharpe di 2,8 perché oscilla pochissimo, ma rende il
  7% annuo: è affidabile, non ricco.
- **BTC comprato e tenuto**: Sharpe 0,56. Servono quasi nove anni di dati solo per dire che è sopra zero.

Conseguenza pratica: ogni nuova regola provata su W3.2 è un tentativo in più. Il modo per aumentare la fiducia non è
cercare altre varianti, è lasciare passare tempo con le regole ferme.

## 4. Quanta leva: crescita composta e Kelly

### La matematica

Il capitale cresce per moltiplicazione, non per somma. Perdere il 50% e poi guadagnare il 50% lascia al 75%. Per questo la
crescita composta è più bassa del rendimento medio, e la differenza cresce con il quadrato dell'oscillazione:

```
crescita ≈ μ − σ²/2                     (μ = rendimento medio annuo, σ = volatilità annua)
con leva L:  crescita ≈ L·μ − L²·σ²/2
```

Il rendimento sale in proporzione alla leva, il costo dell'oscillazione con il quadrato. Esiste quindi una leva che
massimizza la crescita, quella di **Kelly**: `L* = μ / σ²`. Oltre, la crescita scende; a `2·L*` è zero; più in là si perde
tutto anche con una strategia che in media guadagna.

Tre motivi per stare molto sotto Kelly:

1. `μ` è una stima. Se il vantaggio vero è metà di quello misurato, la leva di Kelly "misurata" è il doppio di quella giusta,
   cioè il punto in cui la crescita è zero.
2. Kelly massimizza la crescita, non limita il drawdown. A Kelly pieno un drawdown del 50% è normale.
3. La formula assume rendimenti regolari. BTC ha giorni da −40%.

### I risultati

{{B1}}

{{B2}}

La seconda tabella rimescola a blocchi di 8 settimane i rendimenti settimanali di W3.2 e simula 4.000 percorsi di tre anni.

- Kelly dice 4x. Nello storico la leva migliore è 3,25–3,75x, e al doppio di quella si azzera il capitale.
- Con il vantaggio dimezzato la leva migliore scende a 1,5x.
- Con il tuo limite di drawdown a −35%: a 1x la probabilità di superarlo in tre anni è del 10%, a 1,5x del 44%, a 2x del 75%.
- A 0,5x la probabilità è zero e la crescita mediana è il 21% annuo.

**La leva giusta per W3.2 è 1x.** Il rischio del 25% allo stop è già una scelta aggressiva: la versione a 10% (W3.1)
corrisponde a circa 0,4x. La leva fino a 5x che avevi indicato come massimo non serve: fra 1x e 2x il rendimento mediano
sale da +44% a +80%, ma la probabilità di uscire dai tuoi limiti passa dal 10% al 75%.

Nota: il drawdown qui è misurato su chiusure settimanali. Dentro la settimana è più profondo.

## 5. Il premio di volatilità

### La matematica

Il prezzo di un'opzione dipende da quanto il mercato si aspetta che BTC oscilli fino alla scadenza: la **volatilità
implicita**. Su Deribit l'indice DVOL la misura a 30 giorni. La **volatilità realizzata** è quella che poi c'è stata davvero.

Se l'implicita è stabilmente più alta della realizzata, chi vende opzioni incassa più di quanto paga: è il **premio di
volatilità**. Esiste su azioni, valute e materie prime per lo stesso motivo per cui un'assicurazione costa più del danno
medio: chi compra protezione accetta di pagarla cara.

### I risultati

{{C1}}

![Volatilità implicita e realizzata; strategie con opzioni](results/ricerca/opzioni.png)

- Il premio c'è: 6 punti di volatilità in media, positivo due giorni su tre.
- Si è ridotto: 12 punti nel 2021–2023, 5 nel 2024–2026. Con più venditori (ETF con covered call, prodotti strutturati) il
  premio scende.
- Non è gratis: il giorno peggiore la realizzata ha superato l'implicita di 157 punti (marzo 2020).
- Il premio è alto quando BTC si muove poco e negativo quando si muove molto (correlazione −0,37 con l'ampiezza del
  movimento). Non dipende dalla direzione (0,06).

Uno studio di CryptoQuant trova lo stesso su quattro anni: implicita sopra la realizzata nel 73,6% dei giorni.

## 6. Vendere opzioni: nude contro coperte

### La matematica

- **Straddle venduto**: vendo una call e una put allo stesso prezzo d'esercizio, quello attuale. Incasso due premi. Guadagno
  se BTC resta vicino, perdo se si allontana in una direzione qualsiasi.
- **Strangle venduto**: come lo straddle ma con prezzi d'esercizio lontani (±15%). Premio più piccolo, perdita che parte più
  tardi.
- **Put venduta con liquidità a garanzia**: mi impegno a comprare BTC a −10%. Incasso il premio; se BTC scende sotto, compro.
- **Covered call**: tengo BTC e vendo una call a +10%. Incasso il premio, rinuncio al rialzo oltre.
- **Delta**: di quanto cambia il prezzo dell'opzione se BTC si muove di 1 $. Uno straddle appena venduto ha delta circa zero;
  se BTC sale diventa una scommessa al ribasso, se scende una al rialzo.
- **Copertura del delta**: ogni giorno compro o vendo sul perp la quantità che riporta il delta a zero. Così la posizione non
  dipende più da dove va BTC ma solo da quanto oscilla: guadagno se la volatilità realizzata è sotto quella che ho venduto.

In formula, il guadagno giornaliero di uno straddle venduto e coperto è circa
`½ · Γ · S² · (σ²_implicita − σ²_realizzata) · Δt`: è esattamente il premio di volatilità. Senza copertura, a questo si somma
una scommessa sulla direzione che nessuno ha chiesto.

### I risultati

Opzioni a 30 giorni, quattro comparti aperti a una settimana l'uno dall'altro, valore calcolato ogni giorno. Costi: 4% del
premio per lato come differenza denaro-lettera, 0,03% di commissione, 0,05% su ogni ribilanciamento della copertura, funding
storico sul perp usato per coprire.

{{C2}}

- **Nude**: straddle e strangle venduti perdono quasi tutto. Il premio incassato non compensa le perdite di direzione: fra
  ottobre 2020 e aprile 2021 BTC ha fatto ×5 e le call vendute hanno assorbito tutto. Anche a un quarto dell'esposizione il
  risultato resta negativo.
- **Put venduta e covered call**: positive, ma sono BTC comprato con il rialzo tagliato. La put venduta ha un drawdown del
  −39% per un +12% annuo.
- **Con il delta coperto**: lo straddle venduto passa da −22% a **+13% annuo**, con drawdown −25%
  e Sharpe 0,96. È positivo in tutti e tre i periodi: +5%, +23%, +11%. La copertura toglie la scommessa sulla direzione e
  lascia solo il premio.
- **Il funding conta.** Quando BTC sale, lo straddle venduto diventa una posizione al ribasso e la copertura è un long sul
  perp, che paga il funding proprio quando è alto. Costa circa 4 punti l'anno: senza funding il risultato sarebbe +17%
  (riga di controllo). Chi copre con il future della stessa scadenza delle opzioni evita questo costo.
- **Lo strangle coperto rende meno** (+5%): incassa un premio più piccolo a parità di rischio di salto.
- **Filtro "implicita > realizzata passata"**: non migliora (+8%, Sharpe 0,80). È la regola più citata e qui non funziona.

### Quanto costa un giorno brutto

Uno straddle appena venduto, coperto alla chiusura del giorno prima: perdita in un solo giorno, in percentuale del
controvalore, se BTC si muove e la volatilità implicita sale.

{{E1}}

Un mese fermo rende l'11%. Un giorno da −20% con volatilità che sale costa il 13–19%: più di un mese di premio. Un giorno da
−40% come il 12/03/2020 costa il 31%. La copertura giornaliera non protegge dai salti dentro la giornata.

### L'esame dello Sharpe deflazionato

{{E2}}

L'asimmetria è negativa (−2): molti piccoli guadagni e poche perdite grandi, il contrario di W3.2 (+1,6). È il profilo di
chi vende assicurazioni. In questo ciclo ho provato una dozzina di varianti con opzioni: la colonna da guardare è "10
tentativi". Sull'intero periodo lo straddle coperto non passa (52%). Sul solo periodo DVOL passa (81%), ma sono meno di sei
anni. Il giudizio corretto è: promettente, non dimostrato.

## 7. Insieme a W3.2

{{C3}}

Il confronto giusto è con la riga "80% W3.2 + 20% liquidità": stessa esposizione a W3.2, con il 20% fermo. Sostituire
quella liquidità con lo straddle coperto porta il rendimento da +38,3% a +42,1% e lo Sharpe da 1,39 a 1,51, con lo stesso
drawdown (−31%). La correlazione mensile con W3.2 è negativa (−0,27): lo straddle guadagna nei mesi fermi, quando W3.2 è
fuori o perde poco, e perde nei mesi di forte movimento, quando W3.2 guadagna.

Il miglioramento è reale ma piccolo: quattro punti l'anno. W3.2 da sola a 1x rende di più (+48,5%) con un drawdown più alto
(−37%). La scelta è fra più rendimento e meno drawdown, non c'è un pasto gratis.

## 8. W3.2 con opzioni comprate

Idea: invece di aprire spot o perp con lo stop, a ogni segnale di W3.2 comprare un'opzione (call per i long, put per gli
short). La perdita massima è il premio pagato, senza stop e senza liquidazione.

{{D1}}

- Le operazioni in guadagno scendono dall'85% al 70%: l'opzione perde valore ogni giorno, e un'operazione che chiude in
  piccolo guadagno sul perp chiude in perdita con l'opzione.
- Confronto a rischio simile: l'opzione a 90 giorni con il 6% del capitale fa 45.059 $ con perdita peggiore −5,9%; W3.1 fa
  49.142 $ con perdita peggiore −7,2%. Con il 10% l'opzione fa 107.767 $ e perdita peggiore −9,8%. Per unità di rischio i due
  sono equivalenti, entro l'errore del modello.
- Contro W3.2 originale (246.794 $) nessuna versione con opzioni si avvicina.
- Le opzioni a 180 giorni rendono meno: costano di più e W3.2 esce in media dopo due o tre mesi.

Lo stop di W3.2 funziona già come un'opzione che non si paga in anticipo. Le opzioni comprate avrebbero senso solo se gli
stop venissero saltati spesso da movimenti improvvisi, e nello storico non è successo.

{{D2}}

## 9. I dati delle opzioni anticipano il prezzo?

Quattro segnali presi ogni domenica dai dati Deribit dal 2019, contro il rendimento di BTC e il premio di volatilità nelle
quattro settimane dopo.

{{E3}}

- **Sul prezzo: niente.** Nessun segnale ha una correlazione stabile con il rendimento di BTC. Il livello della volatilità
  implicita sembrava funzionare nel 2019–2022 (0,21) e non più dopo (0,05).
- **Sul premio: il livello della volatilità implicita.** Quando l'implicita è alta rispetto al suo ultimo anno, il premio
  incassato dopo è più alto (0,40 e 0,33 nei due periodi). Ho quindi provato una regola: vendere
  lo straddle coperto solo quando l'implicita è sopra la sua mediana dell'ultimo anno. Risultato: +12% annuo, drawdown −12%,
  Sharpe 1,58, positiva nei tre periodi (+16%, +13%, +10%), investita solo un terzo del tempo. **Attenzione: questa regola
  l'ho trovata guardando gli stessi dati su cui la misuro.** È un'ipotesi da verificare su dati futuri, non un risultato.
- L'inclinazione (put più care delle call) e il rapporto put/call non dicono nulla, né sul prezzo né sul premio.

## 10. La candidata: premio di volatilità con delta coperto

Regole usate nel backtest, senza parametri ottimizzati:

1. Ogni settimana vendere uno straddle a 30 giorni al prezzo corrente (una call e una put), per un controvalore pari a un
   quarto della quota destinata. A regime ci sono quattro straddle aperti.
2. Ogni giorno, alla chiusura, calcolare il delta totale e riportarlo a zero con il perp.
3. Tenere fino a scadenza. Nessuno stop, nessun segnale.
4. Quota: non oltre il 20% del capitale. Il resto a W3.2 o in liquidità.

Cosa serve in pratica:

- Un conto con opzioni e perp sullo stesso margine (OKX o Deribit). Su OKX il contratto minimo è 0,01 BTC: con 9.000 $ di
  quota ogni straddle è di circa 0,04 BTC.
- Un controllo al giorno. Non è una strategia a segnali: è un lavoro quotidiano di manutenzione.
- Margine largo. Nel giorno peggiore dello storico la quota destinata ha perso il 13,9% (marzo 2020); con i dati DVOL, l'8,2% in un giorno.

Perché potrebbe non funzionare:

- Il premio si sta riducendo (da 12 a 5 punti).
- Nel 2019–03/2021 ha reso solo il 5% annuo, con il drawdown peggiore. Sono gli anni con i dati meno affidabili, ma anche gli unici con un crollo da −40% in un giorno.
- Un salto di prezzo dentro la giornata non è coperto. Il backtest ha un solo marzo 2020.

Prima di usarla: tre mesi con il minimo (uno straddle da 0,01 BTC a settimana), per confrontare i prezzi reali con quelli
del modello.

## 11. Limiti

- **Prezzi delle opzioni calcolati, non osservati.** Uso la formula di Black-Scholes con la volatilità DVOL uguale per tutti i
  prezzi d'esercizio. Nella realtà le opzioni lontane hanno volatilità diversa (di solito più alta): questo penalizza
  strangle e put vendute nel backtest e pesa poco sullo straddle, che è al prezzo corrente.
- **Prima del 24/03/2021 non c'è il DVOL.** Uso la volatilità implicita media degli scambi della domenica, tenuta ferma fino
  alla domenica dopo. I risultati 2019–03/2021 sono indicativi. Le conclusioni vanno lette sul periodo DVOL.
- **Copertura alla chiusura giornaliera**, una volta al giorno. Chi copre più spesso ha meno rischio di salto e più costi.
- **Funding e base.** Le opzioni coperte sono prezzate sul prezzo a termine, stimato con il funding dei 7 giorni precedenti;
  la base vera dei future può essere diversa. Prima del 2020 il funding non c'è e uso la media storica (11,6% annuo).
- **Lo Sharpe deflazionato dipende da due numeri scelti**: quanti tentativi contare e quanto variano fra loro. Ho mostrato
  tre valori di N apposta.
- **Kelly e bootstrap usano i rendimenti passati di W3.2.** Se il vantaggio futuro è più basso, tutte le leve vanno ridotte.
- **Il bootstrap a blocchi** conserva le sequenze fino a 8 settimane, non i cicli di più anni.

## 12. Prossimo ciclo

In ordine di utilità:

1. **Prova reale minima** dello straddle coperto (tre mesi, importi minimi), per misurare la differenza fra modello e prezzi
   veri. Vale più di qualunque altro backtest.
2. **Superficie di volatilità storica** (strike e scadenze) per rifare § 6 con prezzi osservati.
3. **Base dei futures a scadenza**: stesso principio del carry sul funding, con un rendimento fissato all'ingresso.
4. **Coppie fra altcoin**: l'unica famiglia di strategie non direzionali che i dati già presenti permettono di provare.
5. **Nessuna nuova variante di W3.2**: § 3 spiega perché.

## 13. Fonti

- Bailey, López de Prado, *The Deflated Sharpe Ratio* — [SSRN 2460551](https://papers.ssrn.com/abstract=2460551);
  [voce Wikipedia](https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)
- MacLean, Thorp, Ziemba, *The Kelly Capital Growth Investment Criterion* —
  [capitolo 1](https://www.maths.ed.ac.uk/mckinnon/blackouts/StochOptFinanceAndEnergySpringer/Chap1_KellyZiemba.pdf);
  [Kelly criterion, Wikipedia](https://en.wikipedia.org/wiki/Kelly_criterion)
- *Tackling estimation risk in Kelly investing using options* — [arXiv 2508.18868](https://arxiv.org/pdf/2508.18868)
- Alexander, Imeraj, *The Bitcoin VIX and its Variance Risk Premium* — [Sussex](https://sro.sussex.ac.uk/id/eprint/91094/)
- *Risk Premia in the Bitcoin Market* — [arXiv 2410.15195](https://arxiv.org/html/2410.15195v2)
- CryptoQuant, opzioni su Bitcoin: volatilità prezzata contro realizzata —
  [nota](https://cryptoquant.com/insights/quicktake/6ad17a06a30b2764be042a93-Bitcoin-Options-Priced-More-Volatility-Than-Delivered-on-736-of-Days-Over-Four-Y)
- Dati: indice DVOL e scambi di opzioni Deribit (`data/opzioni/`), copie dal repo radar; prezzi BTC da Binance.

Codice: `backtest/ricerca_nuova.py`. Tabelle: `results/ricerca/tables.md`.
