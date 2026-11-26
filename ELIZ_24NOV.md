# Il piano di Eliz del 24/11/2026: cosa è successo e cosa dicono i dati

Analisi del post con tre scenari su BTC (grafico a 2 ore, range 55.134–64.600 $). Prezzi OKX fino al 26/11/2026, 14:00 UTC;
backtest su candele Binance a 15 minuti dal 2018.

> Ricerca su dati storici, non una raccomandazione d'investimento.

## 1. Sintesi

**Il metodo è sano: scenari, inneschi e invalidazioni decisi prima. Il 25/11 lo scenario 2 si è attivato quasi alla
perfezione. Ma le stesse tre regole, applicate in modo meccanico su otto anni, perdono dopo i costi e non fanno meglio di
ingressi casuali con stop e obiettivi uguali.** Il valore, se c'è, sta nella scelta discrezionale di Eliz su quali range e
quali livelli contano. Si può misurare solo sul suo storico reale: è il motivo per cui ha senso analizzare il canale.

| Scenario | Innesco | Cosa è successo dal post | Regola meccanica dal 2018 (N = 7 giorni) |
|---|---|---|---|
| 1 · short dopo la deviazione sopra il range (64.600–65.500 $) | Prezzo sopra il massimo, poi rientro nel range | Non attivato: massimo 61.631 $ | 370 operazioni, 33% in guadagno, −0,24% netto medio |
| 2 · long scalp al 75% (≈57.500 $) con conferma a 15 minuti | Tocco del livello e candela di rifiuto | **Attivato il 25/11**: minimo 57.300 $ alle 14:45 UTC, candela a martello, poi 60.400 $ in 4 ore e 61.631 $ nella notte | 82 operazioni, 20% in guadagno, −0,47 R medio |
| 3 · long dopo la deviazione sotto il minimo (52.000–53.000 $) | Rottura sotto, recupero, ritest | Non attivato | 305 operazioni, 35% in guadagno, −0,20% netto medio |

## 2. Il piano, in parole semplici

Eliz non prevede dove va BTC: disegna tre situazioni e dice cosa fare se si verificano.

- **Range**: BTC è chiuso fra il massimo della settimana precedente (64.600–65.500 $) e un minimo più largo (52.000–53.000 $).
- **Deviazione** (in inglese *swing failure* o *deviation*): il prezzo supera un estremo del range, prende gli stop di chi era
  posizionato dall'altra parte, poi rientra. Il rientro è il segnale: chi ha comprato la rottura è intrappolato.
- **Fibonacci**: i livelli 0,5 e 0,75 sono i ritracciamenti della salita da 55.134 $ (minimo del 21/11) a 64.600 $
  (massimo del 23/11). Il 75% cade a 57.500 $.
- **Inneschi e invalidazioni**: per ogni scenario c'è una condizione per entrare e un punto in cui l'idea è sbagliata (lo
  stop). "No trigger, no trade."

Sulla frase "con tante linee prima o poi ne prendi una": è vera solo in parte. Avere tre scenari non è barare, se si
contano anche le volte in cui l'innesco scatta e lo stop viene preso. È esattamente quello che fa il backtest qui sotto.

## 3. Lo scenario 2 il 25/11, candela per candela

| Ora UTC (15 minuti) | Minimo | Chiusura | Lettura |
|---|---|---|---|
| 14:30 | 57.358 $ | 57.385 $ | Il prezzo arriva sul livello |
| **14:45** | **57.300 $** | **58.236 $** | Rifiuto: tocca, scende 200 $ sotto il 75% e chiude 900 $ sopra. È la conferma |
| 15:15 | 57.691 $ | 57.988 $ | Ritest: non torna sotto il minimo |
| 17:30 | 59.112 $ | 59.742 $ | Il massimo della candela (59.950 $) supera il 50% di ritracciamento (59.867 $) |
| 26/11 00:00 | – | – | Massimo 61.631 $ |

Con ingresso alla chiusura delle 14:45 (58.236 $) e stop sotto il minimo (circa 57.240 $), il rischio era l'1,7%. Il primo
obiettivo naturale (50%, 59.867 $) dava +2,8%, cioè 1,6 volte il rischio; il massimo della notte +5,8%.

## 4. Le tre regole su otto anni

Per sapere se il metodo ha un vantaggio, ho tradotto ogni scenario in una regola senza discrezione e l'ho applicata a ogni
situazione simile dal 2018:

- **Range** = massimo e minimo dei 7 giorni che finiscono 48 ore prima (controllo: 14 giorni).
- **A (scenario 1)**: nelle ultime 48 ore il prezzo è andato sopra il massimo; una chiusura oraria rientra → short. Stop sopra
  il massimo della deviazione, obiettivo il centro del range, massimo 7 giorni.
- **B (scenario 2)**: dopo una salita di almeno l'8%, il primo ritorno al 75%; una candela da 15 minuti scende sotto il
  livello e chiude sopra → long. Stop sotto il minimo della candela, obiettivo il 50%, massimo 3 giorni.
- **C (scenario 3)**: specchio di A sotto il minimo del range. Si entra al rientro, senza aspettare il ritest.
- **Controllo**: le stesse operazioni (verso, stop, obiettivo, durata) aperte in momenti casuali.

| Regola (dal post) | N giorni del range | Operazioni | Per anno | In guadagno | Rendimento medio per operazione (netto) | Risultato medio in R | Obiettivo raggiunto | Stop | 2018–2021: media | 2022–2026: media | Controllo casuale: media | Quante volte il caso fa meglio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A · short sulla deviazione sopra il range | 7 | 370 | 42,8 | 33% | -0,24% | -0,06 | 28% | 65% | -0,60% (165) | +0,05% (205) | -0,14% | 73% |
| B · long al 75% con conferma a 15 minuti | 7 | 82 | 10,2 | 20% | -0,26% | -0,47 | 20% | 80% | -0,00% (49) | -0,63% (33) | -0,12% | 74% |
| C · long sulla deviazione sotto il range | 7 | 305 | 34,9 | 35% | -0,20% | -0,06 | 30% | 59% | -0,11% (121) | -0,26% (184) | -0,16% | 63% |
| A · short sulla deviazione sopra il range | 14 | 262 | 30,6 | 32% | -0,09% | -0,02 | 23% | 67% | -0,31% (99) | +0,05% (163) | -0,15% | 35% |
| B · long al 75% con conferma a 15 minuti | 14 | 64 | 7,9 | 17% | -0,30% | -0,69 | 17% | 83% | -0,35% (32) | -0,25% (32) | -0,14% | 79% |
| C · long sulla deviazione sotto il range | 14 | 188 | 21,5 | 30% | -0,41% | -0,20 | 20% | 64% | -0,79% (68) | -0,19% (120) | -0,07% | 91% |

Rendimenti sul controvalore della singola operazione, al netto di commissioni (0,05% a mercato, 0,02% limite), slittamento e funding. R = rischio pianificato (distanza dello stop). 'Quante volte il caso fa meglio': quota delle 100 serie casuali con media pari o superiore.

| Regola, N = 7 | 10.000 $ con rischio 1% per operazione | Drawdown massimo (sulle chiusure) | Serie peggiore di stop di fila |
|---|---|---|---|
| A · short sulla deviazione sopra il range | 7.501 $ | -35,9% | 11 |
| B · long al 75% con conferma a 15 minuti | 6.661 $ | -32,6% | 15 |
| C · long sulla deviazione sotto il range | 8.096 $ | -27,6% | 11 |

- **Nessuna delle tre regole guadagna** dopo i costi, con nessuno dei due range.
- **Il caso fa uguale o meglio**: in due casi su tre le serie casuali con gli stessi stop e obiettivi rendono più delle regole.
  Il segnale "deviazione e rientro" non aggiunge informazione al semplice rapporto fra stop e obiettivo.
- **Lo scalp al 75% con stop stretto è il peggiore**: lo stop sotto una candela da 15 minuti viene preso 8 volte su 10. Il 25/11
  è andato bene; storicamente è l'eccezione.
- È coerente con tutto quello che abbiamo già visto su BTC: supporti e resistenze (`LIVELLI_BTC.md`), liquidazioni
  (`LIQUIDAZIONI.md`) e 1.224 regole intraday (`INTRADAY.md`) non danno un vantaggio d'ingresso meccanico.

## 5. Cosa non può dire questo test

- Eliz sceglie a mano quali range e quali livelli usare, e salta i casi che non le piacciono. Una regola meccanica non
  riproduce questa scelta: se il suo vantaggio sta lì, il test lo sottostima.
- La "conferma" e il "ritest" sono descritti a parole: ne ho usato una versione semplice.
- Un solo caso riuscito (il 25/11) non dice nulla sul metodo.

L'unico modo per misurare il suo vantaggio reale è il suo storico: tutti i piani pubblicati, quali si sono attivati, con
quali stop e obiettivi, e come sono finiti, contando anche quelli andati male. È il lavoro proposto sul canale Telegram.

Codice: `backtest/eliz_range.py`. Tabelle e operazioni: `results/eliz/`.
