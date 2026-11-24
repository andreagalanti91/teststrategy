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

Dispersione dello Sharpe annuo fra le varianti provate in questa ricerca: 0,31 fra le 104 soglie di v1, 0,37 fra le 126 varianti di v2. Per la colonna "deflazionato" si assume una dispersione di 0,5 fra i tentativi. Sharpe che il migliore di N tentativi senza abilità raggiunge per caso, su base annua: N=10 → 0,79; N=100 → 1,27; N=1.000 → 1,63.

| Strategia | Anni | Sharpe annuo (settimanale) | Asimmetria | Probabilità che lo Sharpe vero sia > 0 | Deflazionato, 10 tentativi | 100 tentativi | 1.000 tentativi | Anni minimi per esserne certi al 95% |
|---|---|---|---|---|---|---|---|---|
| W3.2 radar, 2018–2026 | 8,9 | 1,19 | 1,6 | 100,0% | 91% | 41% | 7% | 1,5 |
| W3.2 radar, dal 2021 (dati reali) | 5,9 | 1,26 | 1,5 | 100,0% | 90% | 49% | 16% | 1,4 |
| v1 · voto di 17 indicatori, 2018–2026 | 8,9 | 0,91 | 1,1 | 99,8% | 65% | 13% | 1% | 2,9 |
| v1, solo verifica 2022–2026 | 4,9 | 0,64 | 1,4 | 93,3% | 37% | 7% | 1% | 5,9 |
| v2 · tre schermi, 2018–2026 | 8,9 | 0,95 | 1,2 | 99,9% | 70% | 16% | 2% | 2,7 |
| MACD a regime (altcoin), dal 2020 | 6,5 | 1,06 | 1,3 | 99,8% | 78% | 29% | 6% | 2,1 |
| Carry funding selettivo, dal 2021 | 5,9 | 2,84 | 4,1 | 100,0% | 100% | 100% | 100% | 0,1 |
| BTC comprato e tenuto, 2018–2026 | 8,9 | 0,56 | -0,1 | 95,0% | 25% | 2% | 0% | 8,9 |

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

| Campione | Rendimento medio annuo (aritmetico) | Volatilità annua | Leva di Kelly teorica (media / varianza) | Leva che massimizza la crescita nello storico | Crescita annua a 1x | a metà di quella leva | a quella leva | al doppio | Leva oltre cui la crescita diventa negativa |
|---|---|---|---|---|---|---|---|---|---|
| W3.2, 2018–2026 | +39,1% | +31,3% | 4,0x | 3,25x | +40,7% | +59,6% | +82,4% | -100,0% | 5,25x |
| W3.2, dal 2021 | +40,6% | +30,6% | 4,3x | 3,75x | +43,2% | +72,6% | +102,3% | -100,0% | 7,00x |
| W3.2 dal 2021, con il vantaggio dimezzato | +20,3% | +30,6% | 2,2x | 1,50x | +16,9% | +13,4% | +18,5% | +7,5% | 3,50x |

| Campione | Leva | CAGR mediano a 3 anni | 5° percentile | Probabilità di chiudere in perdita | Drawdown mediano | Probabilità di drawdown oltre −35% | oltre −50% |
|---|---|---|---|---|---|---|---|
| W3.2, 2018–2026 | 0,5x | +21,7% | +3,7% | 2% | -11,4% | 0% | 0% |
| W3.2, 2018–2026 | 1,0x | +44,4% | +5,5% | 3% | -22,1% | 10% | 1% |
| W3.2, 2018–2026 | 1,5x | +62,7% | +2,6% | 4% | -33,3% | 44% | 11% |
| W3.2, 2018–2026 | 2,0x | +79,7% | -2,3% | 6% | -43,5% | 75% | 32% |
| W3.2, 2018–2026 | 3,0x | +104,6% | -16,5% | 10% | -61,3% | 97% | 77% |
| W3.2, dal 2021 | 0,5x | +20,3% | +4,0% | 2% | -11,6% | 0% | 0% |
| W3.2, dal 2021 | 1,0x | +41,1% | +5,9% | 2% | -22,5% | 8% | 1% |
| W3.2, dal 2021 | 1,5x | +57,1% | +2,5% | 4% | -34,0% | 46% | 9% |
| W3.2, dal 2021 | 2,0x | +70,4% | -2,6% | 6% | -44,5% | 79% | 32% |
| W3.2, dal 2021 | 3,0x | +89,4% | -17,8% | 10% | -62,8% | 98% | 81% |

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

| Periodo | Giorni | Volatilità implicita media | Realizzata nei 30 giorni dopo | Differenza media | Mediana | Giorni in cui l'implicita è stata più alta | Giorno peggiore (realizzata − implicita) |
|---|---|---|---|---|---|---|---|
| 2019 – 03/2021 (IV approssimata) | 808 | 71% | 70% | 1,2 punti | 3,1 | 56% | 157 punti il 2020-02-29 |
| 03/2021 – 2023 (DVOL) | 1013 | 70% | 58% | 11,8 punti | 12,5 | 74% | 41 punti il 2021-04-28 |
| 2024 – 2026 (DVOL) | 1028 | 49% | 44% | 4,8 punti | 8,4 | 68% | 46 punti il 2026-01-28 |
| Tutto | 2849 | 63% | 57% | 6,3 punti | 9,0 | 67% | 157 punti il 2020-02-29 |

Correlazione fra il premio (implicita − realizzata dopo) e il rendimento di BTC negli stessi 30 giorni: 0,06. Con il valore assoluto del rendimento: -0,37.

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

| Strategia (scadenze a 30 giorni, 4 comparti sfalsati) | 10.000 $ → | CAGR | Max DD | Sharpe | Mese peggiore | Cicli in guadagno | CAGR / DD 2019–03/2021 | CAGR / DD 03/2021–2023 | CAGR / DD 2024–2026 |
|---|---|---|---|---|---|---|---|---|---|
| Straddle venduto alla pari, 1x | 1.358 | -22,4% | -93,3% | -0,32 | -42,0% | 57% di 380 | -63% / -93% | +11% / -39% | -3% / -37% |
| Straddle venduto, 0,25x | 7.568 | -3,5% | -39,6% | -0,31 | -10,6% | 57% di 380 | -17% / -40% | +5% / -9% | +0% / -10% |
| Straddle venduto con copertura giornaliera del delta, 1x | 26.056 | +13,0% | -25,4% | 0,96 | -12,7% | 61% di 380 | +5% / -25% | +23% / -14% | +11% / -7% |
| · controllo: senza funding (copertura con il future della stessa scadenza) | 35.410 | +17,4% | -20,3% | 1,28 | -9,3% | 63% di 380 | +13% / -20% | +28% / -14% | +13% / -7% |
| Straddle coperto, solo se implicita > realizzata passata | 18.846 | +8,4% | -14,6% | 0,80 | -8,0% | 59% di 282 | +6% / -15% | +14% / -15% | +6% / -6% |
| Straddle coperto, solo se implicita sopra la sua mediana a un anno | 24.757 | +12,2% | -11,8% | 1,58 | -6,1% | 76% di 138 | +16% / -12% | +13% / -12% | +10% / -6% |
| Strangle ±15% con copertura giornaliera del delta, 1x | 14.614 | +4,9% | -28,5% | 0,48 | -15,6% | 63% di 380 | -5% / -29% | +16% / -11% | +3% / -6% |
| Strangle venduto ±15%, 1x | 2.210 | -17,5% | -87,2% | -0,32 | -35,4% | 72% di 380 | -52% / -87% | +12% / -30% | -7% / -30% |
| Strangle ±15%, solo se implicita > realizzata passata | 5.740 | -6,8% | -56,4% | -0,16 | -21,6% | 72% di 282 | -22% / -56% | +8% / -25% | -7% / -24% |
| Put venduta −10% con liquidità a garanzia | 24.407 | +12,0% | -39,4% | 0,61 | -17,5% | 84% di 380 | +23% / -39% | +12% / -32% | +5% / -24% |
| Put venduta −10%, solo sopra la SMA 200 | 19.400 | +8,8% | -27,6% | 0,66 | -15,5% | 85% di 220 | +15% / -28% | +5% / -23% | +8% / -8% |
| BTC + call venduta +10% (covered call) | 84.874 | +31,3% | -56,2% | 0,86 | -30,0% | 66% di 380 | +94% / -50% | +8% / -56% | +17% / -44% |
| BTC comprato e tenuto (riferimento) | 205.074 | +46,8% | -76,6% | 0,94 | -37,3% | 57% di 380 | +242% / -63% | -7% / -77% | +19% / -53% |

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

| Movimento di BTC in un giorno | Volatilità implicita 50% → 50% | 50% → 80% | 50% → 120% |
|---|---|---|---|
| fermo | +0,2% | -6,5% | -15,4% |
| +5% | -0,5% | -7,1% | -16,1% |
| -5% | -0,5% | -6,8% | -15,3% |
| +10% | -2,4% | -8,5% | -17,3% |
| -10% | -2,7% | -8,0% | -15,9% |
| +20% | -8,9% | -13,3% | -21,1% |
| -20% | -10,3% | -13,1% | -18,9% |
| -30% | -20,3% | -21,2% | -24,5% |
| -40% | -30,9% | -31,0% | -32,3% |

Premio incassato all'apertura: 11,4% del controvalore. Guadagno massimo se BTC resta fermo fino a scadenza: lo stesso 11,4%.

Un mese fermo rende l'11%. Un giorno da −20% con volatilità che sale costa il 13–19%: più di un mese di premio. Un giorno da
−40% come il 12/03/2020 costa il 31%. La copertura giornaliera non protegge dai salti dentro la giornata.

### L'esame dello Sharpe deflazionato

| Serie | Anni | Sharpe annuo (settimanale) | Asimmetria | Giorno peggiore | Settimana peggiore | Probabilità che lo Sharpe vero sia > 0 | Deflazionato, 10 tentativi | 100 tentativi |
|---|---|---|---|---|---|---|---|---|
| Straddle coperto, 2019–2026 | 7,9 | 0,80 | -2,3 | -13,9% | -17,6% | 97,6% | 52% | 13% |
| Straddle coperto, solo DVOL (dal 24/03/2021) | 5,7 | 1,23 | -2,0 | -8,2% | -12,7% | 99,3% | 81% | 47% |
| Straddle coperto, 2024–2026 | 2,9 | 1,23 | -1,0 | -3,6% | -5,0% | 97,1% | 75% | 48% |

L'asimmetria è negativa (−2): molti piccoli guadagni e poche perdite grandi, il contrario di W3.2 (+1,6). È il profilo di
chi vende assicurazioni. In questo ciclo ho provato una dozzina di varianti con opzioni: la colonna da guardare è "10
tentativi". Sull'intero periodo lo straddle coperto non passa (52%). Sul solo periodo DVOL passa (81%), ma sono meno di sei
anni. Il giudizio corretto è: promettente, non dimostrato.

## 7. Insieme a W3.2

| Combinazione (ribilanciata ogni giorno, dal 2019) | CAGR | Max DD | Sharpe | Correlazione mensile con W3.2 |
|---|---|---|---|---|
| W3.2 da sola | +48,5% | -37,3% | 1,39 | – |
| 80% W3.2 + 20% liquidità (riferimento) | +38,3% | -30,7% | 1,39 | – |
| 80% W3.2 + 20% straddle venduto con copertura giornaliera del delta, 1x | +42,1% | -31,1% | 1,51 | -0,27 |
| 80% W3.2 + 20% put venduta −10% con liquidità a garanzia | +42,3% | -30,6% | 1,49 | 0,11 |
| 80% W3.2 + 20% put venduta −10%, solo sopra la sma 200 | +40,7% | -32,6% | 1,43 | 0,34 |

Il confronto giusto è con la riga "80% W3.2 + 20% liquidità": stessa esposizione a W3.2, con il 20% fermo. Sostituire
quella liquidità con lo straddle coperto porta il rendimento da +38,3% a +42,1% e lo Sharpe da 1,39 a 1,51, con lo stesso
drawdown (−31%). La correlazione mensile con W3.2 è negativa (−0,27): lo straddle guadagna nei mesi fermi, quando W3.2 è
fuori o perde poco, e perde nei mesi di forte movimento, quando W3.2 guadagna.

Il miglioramento è reale ma piccolo: quattro punti l'anno. W3.2 da sola a 1x rende di più (+48,5%) con un drawdown più alto
(−37%). La scelta è fra più rendimento e meno drawdown, non c'è un pasto gratis.

## 8. W3.2 con opzioni comprate

Idea: invece di aprire spot o perp con lo stop, a ogni segnale di W3.2 comprare un'opzione (call per i long, put per gli
short). La perdita massima è il premio pagato, senza stop e senza liquidazione.

Operazioni di W3.2 dal 2019-01-06 (prima non c'è volatilità implicita): 20. A ogni ingresso si compra un'opzione alla pari (call per i long, put per gli short) spendendo una quota fissa del capitale; si rivende quando W3.2 esce, o si incassa il valore a scadenza. Costo denaro-lettera: 4% del premio per lato.

| Versione | Capitale finale da 10.000 $ | Operazioni in guadagno | Operazione peggiore | Operazione migliore | Perdita massima per operazione | Capitale composto nelle sole perdenti consecutive peggiori |
|---|---|---|---|---|---|---|
| W3.2 originale (spot e perp) | 246.794 | 85% | -17,9% | +52,2% | fino a −25% (stop) | -20,0% |
| W3.1 (stessi segnali, rischio 10% allo stop) | 49.142 | 85% | -7,2% | +24,6% | fino a −10% (stop) | -8,1% |
| Opzione a 90 giorni, 3% del capitale per operazione | 21.946 | 70% | -2,9% | +12,1% | −3% | -3,2% |
| Opzione a 90 giorni, 6% del capitale per operazione | 45.059 | 70% | -5,9% | +24,3% | −6% | -6,5% |
| Opzione a 90 giorni, 10% del capitale per operazione | 107.767 | 70% | -9,8% | +40,5% | −10% | -10,7% |
| Opzione a 180 giorni, 3% del capitale per operazione | 15.842 | 60% | -2,7% | +8,2% | −3% | -2,9% |
| Opzione a 180 giorni, 6% del capitale per operazione | 24.372 | 60% | -5,5% | +16,4% | −6% | -5,8% |
| Opzione a 180 giorni, 10% del capitale per operazione | 41.577 | 60% | -9,2% | +27,4% | −10% | -9,7% |

- Le operazioni in guadagno scendono dall'85% al 70%: l'opzione perde valore ogni giorno, e un'operazione che chiude in
  piccolo guadagno sul perp chiude in perdita con l'opzione.
- Confronto a rischio simile: l'opzione a 90 giorni con il 6% del capitale fa 45.059 $ con perdita peggiore −5,9%; W3.1 fa
  49.142 $ con perdita peggiore −7,2%. Con il 10% l'opzione fa 107.767 $ e perdita peggiore −9,8%. Per unità di rischio i due
  sono equivalenti, entro l'errore del modello.
- Contro W3.2 originale (246.794 $) nessuna versione con opzioni si avvicina.
- Le opzioni a 180 giorni rendono meno: costano di più e W3.2 esce in media dopo due o tre mesi.

Lo stop di W3.2 funziona già come un'opzione che non si paga in anticipo. Le opzioni comprate avrebbero senso solo se gli
stop venissero saltati spesso da movimenti improvvisi, e nello storico non è successo.

| Operazione W3.2 | Verso | Entra | Esce | W3.2 originale | Con opzione a 90 giorni (6% del capitale) |
|---|---|---|---|---|---|
| 1 | long | 2019-05-13 | 2019-06-27 | +51,1% | +21,3% |
| 2 | long | 2020-02-10 | 2020-02-17 | -2,6% | -0,6% |
| 3 | short | 2020-03-16 | 2020-04-27 | -17,9% | -5,9% |
| 4 | long | 2020-05-04 | 2020-08-03 | +16,0% | +7,4% |
| 5 | long | 2020-10-26 | 2020-11-23 | +40,8% | +18,2% |
| 6 | long | 2020-12-14 | 2020-12-31 | +50,4% | +22,6% |
| 7 | long | 2021-02-01 | 2021-02-22 | +52,2% | +13,7% |
| 8 | long | 2021-08-02 | 2021-09-27 | +4,3% | -1,0% |
| 9 | long | 2021-10-04 | 2021-11-08 | +20,9% | +5,8% |
| 10 | short | 2022-01-03 | 2022-03-28 | +1,0% | -4,4% |
| 11 | short | 2022-08-15 | 2023-01-16 | +8,3% | +6,7% |
| 12 | long | 2023-01-23 | 2023-08-17 | +13,3% | +4,6% |
| 13 | long | 2023-10-23 | 2024-01-01 | +40,5% | +17,6% |
| 14 | long | 2024-02-12 | 2024-03-11 | +42,2% | +18,9% |
| 15 | long | 2024-09-23 | 2025-02-26 | +30,8% | +24,3% |
| 16 | long | 2025-04-28 | 2025-10-10 | +11,3% | +9,6% |
| 17 | short | 2025-12-01 | 2026-04-27 | +11,9% | +9,5% |
| 18 | short | 2026-05-25 | 2026-08-20 | +5,7% | +1,8% |
| 19 | long | 2026-08-24 | 2026-11-09 | -4,1% | -5,0% |
| 20 | short | 2026-11-16 | aperta | +5,9% | -0,4% |

## 9. I dati delle opzioni anticipano il prezzo?

Quattro segnali presi ogni domenica dai dati Deribit dal 2019, contro il rendimento di BTC e il premio di volatilità nelle
quattro settimane dopo.

| Segnale la domenica | Settimane | BTC nelle 4 settimane dopo: terzo basso del segnale | terzo medio | terzo alto | Correlazione col rendimento, 2019–2022 | 2023–2026 | Correlazione col premio poi incassato (implicita − realizzata dopo), 2019–2022 | 2023–2026 |
|---|---|---|---|---|---|---|---|---|
| Inclinazione: put lontane − call lontane (punti di volatilità) | 408 | +7,4% | +1,1% | +5,2% | -0,02 | -0,03 | 0,12 | -0,13 |
| Livello della volatilità implicita (posizione nelle 52 settimane prima) | 357 | +2,8% | +1,3% | +8,0% | 0,21 | 0,05 | 0,40 | 0,33 |
| Premio atteso: implicita − realizzata dei 30 giorni prima | 408 | +7,7% | +2,7% | +3,2% | -0,12 | -0,04 | -0,01 | -0,11 |
| Volumi: put / call | 408 | +4,6% | +5,3% | +3,8% | -0,06 | -0,02 | -0,02 | 0,05 |

Rendimento medio di BTC a 4 settimane su tutte le domeniche: +4,6%. Le finestre si sovrappongono (4 settimane su dati settimanali): le osservazioni indipendenti sono circa 102 per l'intero periodo, la metà per ogni sottoperiodo; una correlazione sotto 0,2 in valore assoluto non è distinguibile dal caso.

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
