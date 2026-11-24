# Nuovo ciclo di ricerca: cosa manca, e la matematica che serve

Quattro cose che nei cicli precedenti non avevamo guardato: quanto sono affidabili i risultati, quanta leva usare, la
volatilità come fonte di rendimento, le opzioni come strumento. Dati fino al 23/11/2026.

> Ricerca su dati storici, non una raccomandazione d'investimento.

## 1. Sintesi

**Nessuna strategia nuova supera la verifica. W3.2 a leva 1x resta la scelta, e 1x è già il massimo compatibile con il tuo
limite di drawdown. Vendere volatilità su BTC sembrava la candidata, ma con i prezzi a cui si vende davvero il guadagno sta
fra zero e +11% annuo, e i nostri dati non bastano a dire dove.**

| Domanda | Risultato | Cosa farne |
|---|---|---|
| I risultati di W3.2 possono essere fortuna? | Da sola, lo Sharpe (1,2) è certamente sopra zero. Contando i tentativi fatti regge fino a una decina (91–98%); contro cento dipende dalle ipotesi (41–81%) | Non aggiungere altre regole a W3.2. Ogni variante provata abbassa la fiducia in tutte |
| Quanta leva su W3.2? | Kelly dice 4x. Ma già a 1x la probabilità di un drawdown oltre −35% in tre anni è del 16%; a 1,5x del 62%, a 2x del 91% | 1x al massimo. Per stare sotto −35% con margine, 0,5–0,75x |
| La volatilità implicita di BTC è troppo cara? | L'indice DVOL è stato sopra la volatilità realizzata nel 67% dei giorni, di 6 punti in media. Sulle opzioni al prezzo corrente il premio è 2 punti | Il premio esiste, ma gran parte sta nelle opzioni lontane dal prezzo |
| Basta vendere opzioni per incassarlo? | No. Straddle e strangle venduti senza copertura: da 10.000 $ a 600–1.500 $, drawdown −88/−95% | Mai opzioni vendute nude su BTC |
| E coprendo il delta ogni giorno? | Fra 0% e +11% annuo, drawdown −27%. Zero se si vende alla volatilità delle opzioni alla pari, +11% se si vende al livello del DVOL | Non dimostrata. Serve una prova con prezzi veri |
| Opzioni comprate al posto del perp per W3.2? | A 30 giorni con il 10% del capitale: 216.000 $ contro 247.000 $ di W3.2, con perdita massima per operazione −10% invece di −18%. A 180 giorni: 36.000 $ | Ipotesi interessante, non una conclusione: 20 operazioni, risultato che cambia di sei volte con la scadenza |
| I dati delle opzioni anticipano il prezzo? | No: inclinazione, volumi put/call e livello della volatilità non prevedono BTC a 4 settimane | Nessun segnale d'ingresso da qui |

Una verifica indipendente ha corretto tre punti della prima versione di questo studio: il premio incassato era calcolato
sull'indice DVOL invece che sulla volatilità delle opzioni alla pari (lo straddle coperto passava da +17% a zero), mancava
il funding sulla copertura, e il drawdown simulato era misurato su dati settimanali invece che giornalieri. I numeri qui
sono quelli corretti.

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
| **Leva e dimensione della posizione** | **Questo ciclo** | 1x al massimo | § 4 |
| **Volatilità come fonte di rendimento** | **Questo ciclo** | Premio reale nell'indice, non dimostrato nelle opzioni vendibili | § 5–7 |
| **Opzioni comprate come strumento** | **Questo ciclo** | Ipotesi aperta per scadenze brevi | § 8 |
| **Segnali dal mercato delle opzioni** | **Questo ciclo** | Nessuno sul prezzo | § 9 |
| Prezzi storici veri delle opzioni (per strike e scadenza) | Manca | Decide § 6 e § 8 | Storico Deribit a pagamento, oppure registrare da oggi i prezzi di OKX |
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

`σ_S` è quanto variano gli Sharpe fra i tentativi. Nelle nostre griglie è 0,31–0,37; nella tabella uso 0,5, più severo.

### I risultati

{{A1}}

Come leggere:

- **W3.2** ha uno Sharpe di 1,2. Preso da solo è sopra zero con certezza. Contro 10 tentativi regge: 91% con l'ipotesi
  severa, 98% con la dispersione misurata. Contro 100 il risultato dipende dall'ipotesi: 41% oppure 81%. La risposta onesta
  è che non lo sappiamo.
- Quanti tentativi contare per W3.2? È la versione 3.2 di un sistema che ha avuto più revisioni, tarata sul 2021–2026. Non
  sono mille, ma nemmeno uno. La cifra ragionevole è "decine". Il 2018–2020, che non è stato usato per tararla, dà uno
  Sharpe simile: è l'argomento migliore a suo favore.
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

La seconda tabella rimescola a blocchi di 56 giorni i rendimenti giornalieri di W3.2 e simula 4.000 percorsi di tre anni.

- Kelly dice 4x. Nello storico la leva migliore è 3,25–3,75x, e al doppio di quella si azzera il capitale: il giorno peggiore
  di W3.2 è stato −19%, quindi a 5,25x basta quel giorno.
- Con il vantaggio dimezzato la leva migliore scende a 1,5x.
- Con il tuo limite di drawdown a −35%: a 1x la probabilità di superarlo in tre anni è del 12–16%, a 1,5x del 60%, a 2x del
  90%. Nello storico W3.2 a 1x ha già toccato −37,3%.
- A 0,5x la probabilità è zero e la crescita mediana è il 20% annuo.

**La leva giusta per W3.2 è 1x al massimo.** Il rischio del 25% allo stop è già una scelta aggressiva: la versione a 10%
(W3.1) corrisponde a circa 0,4x. La leva fino a 5x che avevi indicato come tetto non serve: fra 1x e 2x il rendimento
mediano sale da +44% a +78%, ma la probabilità di uscire dai tuoi limiti passa dal 16% al 91%.

## 5. Il premio di volatilità

### La matematica

Il prezzo di un'opzione dipende da quanto il mercato si aspetta che BTC oscilli fino alla scadenza: la **volatilità
implicita**. Su Deribit l'indice DVOL la misura a 30 giorni. La **volatilità realizzata** è quella che poi c'è stata davvero.

Se l'implicita è stabilmente più alta della realizzata, chi vende opzioni incassa più di quanto paga: è il **premio di
volatilità**. Esiste su azioni, valute e materie prime per lo stesso motivo per cui un'assicurazione costa più del danno
medio: chi compra protezione accetta di pagarla cara.

Un dettaglio che cambia i conti: il DVOL, come il VIX, è una media su tutti i prezzi d'esercizio, comprese le opzioni
lontane dal prezzo, che sono le più care. Le opzioni **alla pari** (prezzo d'esercizio uguale al prezzo corrente) hanno una
volatilità più bassa: nei nostri dati il 92% del DVOL. Chi vende uno straddle alla pari incassa quella, non il DVOL.

### I risultati

{{C1}}

![Volatilità implicita e realizzata; strategie con opzioni](results/ricerca/opzioni.png)

- Misurato sull'indice il premio è 6 punti di volatilità, positivo due giorni su tre. Uno studio di CryptoQuant trova lo
  stesso su quattro anni (73,6% dei giorni).
- Misurato sulle opzioni alla pari il premio è 2 punti, positivo nel 60% dei giorni. La differenza sta nelle opzioni lontane
  dal prezzo: è lì che i compratori di protezione pagano di più.
- Si è ridotto: sull'indice, 12 punti nel 2021–2023 e 5 nel 2024–2026. Con più venditori (ETF con covered call, prodotti
  strutturati) il premio scende.
- Non è gratis: il giorno peggiore la realizzata ha superato l'implicita di 157 punti (marzo 2020).
- Il premio è alto quando BTC si muove poco e negativo quando si muove molto (correlazione −0,37 con l'ampiezza del
  movimento). Non dipende dalla direzione (0,06).

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

Opzioni a 30 giorni, sei comparti aperti a cinque giorni l'uno dall'altro, valore calcolato ogni giorno. Volatilità di
vendita: quella stimata delle opzioni alla pari. Costi: 4% del premio per lato come differenza denaro-lettera, 0,03% di
commissione, 0,015% al regolamento, 0,05% su ogni ribilanciamento della copertura, funding storico sul perp usato per coprire.

{{C2}}

- **Nude**: straddle e strangle venduti perdono quasi tutto. Il premio incassato non compensa le perdite di direzione: fra
  ottobre 2020 e aprile 2021 BTC ha fatto ×5 e le call vendute hanno assorbito tutto. Anche a un quarto dell'esposizione il
  risultato resta negativo.
- **Put venduta e covered call**: sono BTC comprato con il rialzo tagliato. La put venduta rende il 7,6% annuo con un
  drawdown del −39%; la covered call fa +26% con drawdown −61%, contro +47% e −77% di BTC tenuto.
- **Con il delta coperto**: lo straddle passa da −30% annuo a **zero**. La copertura toglie la scommessa sulla direzione, ma
  il premio di 2 punti che resta è mangiato da costi e funding.
- **Tutto dipende dal prezzo a cui si vende.** Se si riuscisse a vendere al livello del DVOL il risultato sarebbe +11% annuo
  con Sharpe 0,86 (riga di controllo). La verità sta fra i due: la nostra stima della volatilità alla pari viene dagli
  scambi della domenica, di cui non conosciamo la scadenza media, e potrebbe essere troppo bassa. Con questi dati
  l'intervallo non si stringe.
- **Il funding conta.** Quando BTC sale, lo straddle venduto diventa una posizione al ribasso e la copertura è un long sul
  perp, che paga il funding proprio quando è alto. Costa circa 4 punti l'anno (riga di controllo senza funding: +4%). Chi
  copre con il future della stessa scadenza delle opzioni evita questo costo.
- **Filtro "implicita > realizzata passata"**: non migliora. È la regola più citata e qui non funziona.
- **Filtro "implicita sopra la sua mediana a un anno"**: +7,6% annuo, drawdown −13%, Sharpe 1,10, positivo nei tre periodi.
  L'ho provato dopo aver visto § 9, cioè guardando gli stessi dati su cui lo misuro: è un'ipotesi, non un risultato.

### Quanto costa un giorno brutto

Uno straddle appena venduto, coperto alla chiusura del giorno prima: perdita in un solo giorno, in percentuale del
controvalore, se BTC si muove e la volatilità implicita sale.

{{E1}}

Un mese fermo rende l'11%. Un giorno da −20% con volatilità che sale costa il 13–19%: più di un mese di premio. Un giorno da
−40% come il 12/03/2020 costa il 31%. La copertura giornaliera non protegge dai salti dentro la giornata.

### L'esame dello Sharpe deflazionato

{{E2}}

L'asimmetria è negativa (−2): molti piccoli guadagni e poche perdite grandi, il contrario di W3.2 (+1,6). È il profilo di
chi vende assicurazioni. In questo ciclo ho provato una dozzina di varianti con opzioni, quindi la colonna da guardare è
"10 tentativi": anche nell'ipotesi ottimistica lo straddle coperto non passa sull'intero periodo (43%) e passa a fatica
sul periodo con il DVOL (78%).

## 7. Insieme a W3.2

{{C3}}

Il confronto giusto è con la riga "80% W3.2 + 20% liquidità": stessa esposizione a W3.2, con il 20% fermo. Sostituire
quella liquidità con lo straddle coperto non cambia nulla (+38,6% contro +38,3%). La correlazione mensile con W3.2 è
negativa (−0,25), quindi diversificherebbe: ma serve un rendimento proprio, e con i prezzi realistici non c'è.

La put venduta aggiunge tre punti, ma è BTC comprato in un'altra forma: sale con il mercato e perde quando W3.2 è già in
difficoltà.

## 8. W3.2 con opzioni comprate

Idea: invece di aprire spot o perp con lo stop, a ogni segnale di W3.2 comprare un'opzione alla pari (call per i long, put
per gli short) con una quota fissa del capitale. La perdita massima è il premio pagato, senza stop e senza liquidazione. Se
l'opzione scade prima che W3.2 esca, l'operazione finisce lì.

{{D1}}

- **La scadenza decide tutto.** Con il 10% del capitale per operazione: 216.000 $ a 30 giorni, 106.000 $ a 90, 36.000 $ a
  180. L'opzione corta costa meno e amplifica di più il movimento dei primi giorni, che è dove W3.2 guadagna.
- **A 30 giorni il risultato è vicino a W3.2 originale** (247.000 $) con una perdita massima per operazione del −10% invece
  del −18%, e una serie peggiore di perdite del −14% invece del −20%.
- **A rischio simile batte W3.1**: 72.000 $ con il 6% a 30 giorni, contro 49.000 $ di W3.1 con perdite paragonabili.
- **Regge a un prezzo più alto**: pagando l'opzione al livello del DVOL si scende a 168.000 $.
- Le operazioni in guadagno calano dall'85% al 75%: l'opzione perde valore ogni giorno, e un'operazione lenta chiude in
  perdita anche se la direzione era giusta.

Perché non è una conclusione:

1. Sono 20 operazioni. Tre perdite piene di fila a 10% fanno −27%, e nello storico non è mai successo solo perché W3.2 ha
   avuto l'85% di operazioni in guadagno.
2. La scadenza di 30 giorni è la migliore fra le tre provate, scelta a posteriori. Fra la migliore e la peggiore c'è un
   fattore sei.
3. I prezzi sono calcolati con una formula e una volatilità a 30 giorni, non osservati.
4. È leva in un'altra forma: il 10% in opzioni a 30 giorni muove circa 1,5 volte il capitale. § 4 dice cosa fa la leva
   quando il vantaggio è più piccolo del previsto.

È però l'unica idea di questo ciclo che, se confermata con prezzi veri, cambierebbe il modo di eseguire W3.2: stesso
segnale, rischio definito in partenza, nessuno stop che può essere saltato.

{{D2}}

## 9. I dati delle opzioni anticipano il prezzo?

Quattro segnali presi ogni domenica dai dati Deribit dal 2019, contro il rendimento di BTC e il premio di volatilità nelle
quattro settimane dopo.

{{E3}}

- **Sul prezzo: niente.** Nessun segnale ha una correlazione stabile con il rendimento di BTC. Il livello della volatilità
  implicita sembrava funzionare nel 2019–2022 (0,21) e non più dopo (0,05).
- **Sul premio: il livello della volatilità implicita.** Quando l'implicita è alta rispetto al suo ultimo anno, il premio
  incassato dopo è più alto (0,40 e 0,33 nei due periodi). È l'origine del filtro provato in § 6.
- L'inclinazione (put più care delle call) e il rapporto put/call non dicono nulla, né sul prezzo né sul premio.

## 10. Cosa cambia in pratica

Niente di operativo, e tre cose da tenere ferme:

1. **W3.2 a 1x, senza nuove regole.** Ogni variante aggiunta costa fiducia (§ 3) e ogni punto di leva oltre 1x costa
   drawdown più di quanto renda (§ 4).
2. **Nessuna opzione venduta**, né nuda né coperta, finché non ci sono prezzi veri. Il backtest dice "fra 0 e +11%" con un
   rischio di −31% in un giorno: non è una base per mettere soldi.
3. **Le opzioni comprate sui segnali di W3.2** sono l'ipotesi da verificare per prima. Si può fare senza rischio: a ogni
   segnale di W3.2 annotare il prezzo vero dell'opzione alla pari a 30 giorni su OKX, e dopo un anno confrontare.

## 11. Limiti

- **Prezzi delle opzioni calcolati, non osservati.** Formula di Black con un'unica volatilità per tutti i prezzi d'esercizio.
  Nella realtà le put lontane dal prezzo hanno volatilità più alta: il backtest sottostima il premio di strangle e put
  vendute.
- **La volatilità alla pari è una stima.** DVOL moltiplicato per il rapporto mediano delle ultime 8 domeniche fra la
  volatilità alla pari degli scambi e il DVOL. La scadenza media di quegli scambi non è nota. È il limite che pesa di più:
  sposta lo straddle coperto fra 0 e +11%.
- **Prima del 24/03/2021 non c'è il DVOL.** Uso la volatilità alla pari degli scambi della domenica, tenuta ferma fino alla
  domenica dopo. Nel marzo 2020 la volatilità usata resta al 53% per una settimana mentre quella vera superava il 150%: le
  perdite a mercato di quei giorni sono sottostimate.
- **Copertura alla chiusura giornaliera**, una volta al giorno.
- **Funding e base.** Le opzioni coperte sono prezzate sul prezzo a termine, stimato con il funding dei 7 giorni precedenti;
  la base vera dei future può essere diversa. Prima del 2020 il funding non c'è e uso la media storica (11,6% annuo).
- **Giorno di partenza.** Con sei comparti sfalsati il risultato dipende meno dal giorno in cui si comincia, ma i singoli
  comparti differiscono molto fra loro.
- **Lo Sharpe deflazionato dipende da due numeri scelti**: quanti tentativi contare e quanto variano fra loro. Per questo ho
  mostrato tre valori di N e due di dispersione.
- **Kelly e bootstrap usano i rendimenti passati di W3.2.** Se il vantaggio futuro è più basso, tutte le leve vanno ridotte.
  Il bootstrap a blocchi conserva le sequenze fino a 56 giorni, non i cicli di più anni.
- **Opzioni comprate (§ 8)**: volatilità a 30 giorni usata anche per le scadenze a 90 e 180.

## 12. Prossimo ciclo

In ordine di utilità:

1. **Registrare i prezzi veri delle opzioni.** OKX li pubblica: uno script che ogni giorno salva la catena delle opzioni su
   BTC risolve in pochi mesi il dubbio di § 6 e § 8. Si può aggiungere al radar.
2. **Opzioni comprate sui segnali di W3.2 con prezzi storici veri**, se si trova lo storico (Deribit lo vende; alcuni
   archivi sono gratuiti).
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
