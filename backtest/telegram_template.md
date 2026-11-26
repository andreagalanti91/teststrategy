# Canale Telegram "Aldo Qefalia - Trading": strategia ricostruita, risultati veri, versione meccanica

Analisi di tutti i messaggi esportati (11/05/2023 – 18/03/2024), con i grafici e le schermate Bybit allegate. Ogni operazione
è ricostruita sui prezzi reali; poi lo stile del trader è tradotto in una strategia meccanica e verificato dal 2018.

> Ricerca su dati storici, non una raccomandazione d'investimento. L'esportazione ricevuta è incompleta: si ferma al 18/03/2024.

## 1. Sintesi

**Con i prezzi delle sue schermate il trader ha fatto bene: 55 operazioni, 73% in guadagno, +3,4% medio per operazione. Chi
copiava i messaggi in tempo reale ha fatto molto meno: 44% in guadagno e +1,4% medio, con BTC in perdita. In entrambi i casi
meno di chi teneva BTC (×2,5) o seguiva W3.2 (×1,9) nello stesso periodo, a meno di usare leva. La strategia meccanica
costruita sul suo stile non ha vantaggio su otto anni.**

| Domanda | Risposta |
|---|---|
| Che trader è | Discrezionale, su perpetual Bybit a leva 10x (5–14,5x). Operazioni brevi (mediana 19 ore), su 4 ore e 1 ora. BTC long e short, altcoin quasi solo long |
| Che setup usa | Rottura e retest di livelli (orizzontali e diagonali), prese di liquidità sopra i massimi, medie a 200, divergenze RSI, notizie macro. Alt long finché BTC regge |
| Come gestisce | Entra a scalare, chiude metà al primo obiettivo, stop a pareggio molto presto, lascia correre il resto |
| Ha guadagnato? | Sì, con i suoi prezzi: ×5,7 componendo le operazioni con controvalore 1x. Ma 16 operazioni su 55 sono state mostrate solo dopo l'ingresso, quasi tutte già in guadagno (88%) |
| E chi lo seguiva? | ×1,6 con controvalore 1x. Su BTC chi copiava ha perso (33% in guadagno); il risultato viene da poche operazioni su altcoin (DOGE +29%, INJ +11%) |
| Meglio di BTC tenuto? | No: BTC nello stesso periodo ha fatto ×2,5. Con leva 3x chi copiava avrebbe fatto ×3,5, con un rischio molto più alto |
| La sua strategia, resa meccanica, funziona? | No: dal 2018 perde (−5% annuo su BTC e 8 altcoin, −1% solo su BTC), con 42% di operazioni in guadagno e risultato medio di zero volte il rischio. Ingressi casuali con la stessa gestione fanno meglio |

Seconda analisi più approfondita (autenticità delle schermate, chi copiava con ordini limite, strategia scritta come regole,
nuova strategia intraday con Eliz): [`ALDO_ELIZ_INTRADAY.md`](ALDO_ELIZ_INTRADAY.md).

## 2. Il trader, dai suoi messaggi

{{T1}}

### Come lavora

- **Analisi dall'alto in basso**: livelli sul giornaliero e sul settimanale (supporti, resistenze, media a 200 settimanale),
  ingresso sulle 4 ore o sull'ora.
- **Setup preferito**: rottura di un supporto diagonale seguita da un retest negativo, poi short. Lo dice lui stesso
  ("con questo semplice setup almeno 4-5 ottimi short").
- **Altri setup**: presa di liquidità poco sopra un massimo e poi short; riconquista di un livello e poi long ("reclaim
  pulito dei 25,3k"); retest della media a 200 come resistenza; testa-spalle rovesciato; divergenze RSI; riempimento dei gap del
  future CME.
- **Altcoin**: long su INJ, FET, WOO, DOGE, SOL, ETH quando BTC tiene un livello e la dominance di BTC scende. In più accumuli
  spot sul tema intelligenza artificiale (TAO, RNDR, FET, PAAL, 0x0, ORAI, ARC, BAI), tenuti fuori dai trade.
- **Gestione**: entrata a scalare e medie contro il movimento ("DCA dello short"); chiusura del 50% al primo obiettivo, spesso
  80% poco dopo; stop a pareggio quasi subito; stop spesso condizionali ("sopra i 31,4k sono out").
- **Notizie**: CPI, FOMC, SEC contro Binance e Coinbase, sentenza XRP, ETF su BTC ed ETH. Chiude spesso prima degli eventi.
- **Dal 2024 cambia**: quasi solo long ("non shorto BTC in trend rialzista") e più altcoin.

## 3. Le operazioni ricostruite

Ogni operazione è ricostruita evento per evento (apertura, aumenti, chiusure parziali, stop a pareggio, chiusura) in due
modi:

- **Prezzi del trader**: quelli scritti o visibili nelle sue schermate Bybit.
- **Chi copiava**: ogni evento al primo prezzo disponibile dopo il messaggio (apertura dell'ora successiva). Le operazioni
  comunicate solo dopo l'ingresso restano fuori: non si potevano copiare.

{{T2}}

Il punto chiave è la differenza fra le due righe. Il trader entra prima di scrivere, spesso con ordini limite eseguiti nei
minimi, e pubblica la schermata dopo. Chi legge entra più tardi e a un prezzo peggiore: in media 1,5 punti per operazione,
che su operazioni da qualche punto percentuale sono quasi tutto il guadagno.

Le 16 operazioni comunicate dopo sono un problema diverso: si vedono solo quando sono già andate bene (88% in guadagno).
Non è detto che siano scelte apposta, ma chi guarda il canale vede uno storico migliore di quello che poteva seguire.

{{T3}}

- **BTC**: il trader guadagna l'1,7% medio, chi copiava perde. Il vantaggio su BTC è tutto nel prezzo d'ingresso.
- **Altcoin**: il risultato migliore, per tutti. Ma conta il periodo: da ottobre 2023 a marzo 2024 le altcoin sono salite
  molto, e quasi ogni long ha funzionato.
- **Short**: anche con i prezzi del trader rendono poco (+0,9%); per chi copiava sono in pari.

{{T4}}

Nessun setup si distingue con chiarezza: i campioni sono piccoli (2–16 operazioni) e i risultati di chi copiava sono vicini
a zero per quasi tutti.

{{T5}}

{{T6}}

## 4. La strategia meccanica ricavata dal suo stile

Ho tradotto in regole fisse quello che fa più spesso e che si può misurare senza discrezione:

1. **Regime**: long solo se BTC ha chiuso il giorno prima sopra la sua media a 50 giorni (e la moneta sopra la sua); short
   solo nel caso opposto. È il suo "long sulle alt finché BTC regge" e "non shorto BTC in trend rialzista".
2. **Rottura e retest**: sulle 4 ore, chiusura sopra il massimo delle 30 candele precedenti; entro 3 giorni il prezzo torna sul
   livello rotto, lo tocca e chiude sopra → long. Specchio per lo short (il suo "retest negativo").
3. **Stop** sotto la candela del retest, meno un quarto di ATR.
4. **Gestione come la sua**: metà posizione a +1,5 volte il rischio, stop a pareggio, il resto a +3 volte o dopo 7 giorni.
5. **Rischio**: 1% del capitale allo stop, controvalore massimo 3x, al massimo 4 posizioni insieme.
6. **Universo**: BTC e le 8 altcoin che ha tradato di più (ETH, SOL, BNB, DOGE, INJ, FET, MATIC, WOO), dal 2018 dove ci sono i dati.

La rottura diagonale non è nella regola: una linea tracciata a mano non si traduce in modo univoco.

{{M1}}

{{M3}}

- **Non ha vantaggio**: su otto anni perde, da −1% annuo (solo BTC) a −7% (BTC e altcoin, long e short), con drawdown fino a
  −69%. Il risultato medio è zero volte il rischio: la gestione a metà posizione con stop a pareggio trasforma molte operazioni
  in piccole perdite e lascia pochi guadagni pieni. Peggio dal 2022 che nel 2018–2021.
- **Nel periodo del canale** va da −3% (solo long) a +9% (long e short), contro ×2,5 di BTC e ×1,9 di W3.2.
- **Ingressi casuali con la stessa gestione fanno meglio** della regola (+0,21 contro −0,04 volte il rischio): il segnale
  "rottura e retest" non aggiunge informazione.
- **Per moneta**: nessuna si salva in modo netto; DOGE e FET leggermente positive, WOO e MATIC le peggiori.

## 5. Confronto

{{M2}}

Tre letture:

1. **Il valore del trader, se c'è, sta nella discrezione**: quali livelli contano, quando non entrare, quali altcoin. Una
   regola meccanica che ne copia la forma non lo riproduce.
2. **Per chi lo segue conta il ritardo.** Le sue operazioni sono brevi e con obiettivi vicini: entrare un'ora dopo costa quasi
   tutto il vantaggio. Funziona meglio sulle operazioni lunghe (DOGE, 36 giorni) che sugli scalp su BTC.
3. **Nel periodo analizzato la cosa più redditizia era non fare trading**: BTC tenuto ha fatto ×2,5, W3.2 ×1,9 con drawdown −17%.

## 6. Limiti

- **Esportazione incompleta**: si ferma al 18/03/2024. Con lo storico completo fino a oggi le conclusioni possono cambiare,
  soprattutto perché da marzo 2024 il mercato è stato più difficile.
- **Ricostruzione**: alcune chiusure non sono mai annunciate (residui con stop a pareggio): le ho chiuse con una regola
  (stop o primo obiettivo entro 30 giorni). Sono segnate nell'elenco.
- **Dimensione delle posizioni**: non si sa quanta parte del capitale usasse. Per questo i risultati sono sul controvalore e
  composti a 1x e 3x, non in euro guadagnati.
- **Prezzi di chi copiava**: apertura dell'ora successiva al messaggio, senza differenza denaro-lettera. Chi era più veloce
  ha fatto un po' meglio, chi era più lento peggio.
- **Accumuli spot**: TAO, RNDR e le altre altcoin di intelligenza artificiale non sono nel conto (prezzi mancanti per molte).
  Nel periodo sono salite molto.

## 7. Prossimi passi

1. **Esportazione completa**: rifarla aspettando la fine ("Esportazione completata"), poi ripeto l'analisi fino a oggi.
2. **Controllo dal vivo**: con radar si può registrare l'ora e il prezzo di ogni messaggio nuovo del canale e misurare il
   ritardo reale di chi lo segue.

Codice: `backtest/telegram_ricostruzione.py`, `backtest/telegram_report.py`, `backtest/aldo_meccanico.py`. Operazioni
ricostruite: `results/telegram/`. Messaggi e schermate: non nel repository.
