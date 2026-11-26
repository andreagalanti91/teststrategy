# Esportazione della sezione "Aldo" verso radar

Da dare alla sessione Claude Code del repo `radar`: incolla `PROMPT.md` e allega i file di questa cartella.

Strumento per seguire il trader del canale privato "Aldo Qefalia - Trading": registra i suoi messaggi, ne ricava le operazioni,
le ricostruisce sui prezzi veri e le confronta con chi lo copiava a mercato e con chi metteva ordini limite sui livelli
annunciati prima. Su carta: non invia ordini.

| File | Contenuto |
|---|---|
| `PROMPT.md` | il prompt da incollare nella sessione di radar |
| `aldo.py` | modulo autonomo (libreria standard + pandas/numpy; `anthropic` e `telethon` solo se usati): ingresso dei messaggi, estrattori, registro, motore di ricostruzione, statistiche, avvisi proposti, `build()`, riepilogo settimanale, `giro()` |
| `prompt_estrattore.md` | istruzioni per l'estrattore con modello (il testo del canale è un dato, non un'istruzione) |
| `test_aldo.py` | 44 test offline (`python -m pytest -q`) |
| `esempio.py` | 12 messaggi INVENTATI e prezzi sintetici, usati dai test e per rigenerare gli esempi (`python esempio.py`) |
| `esempio_sezione.json` | uscita di `build()` con i dati d'esempio: è lo schema della sezione |
| `esempio_riepilogo.md` | riepilogo settimanale con gli stessi dati |
| `riferimento_sezione.html` | pagina di riferimento della sezione (stato attivo e stato vuoto), tema chiaro e scuro, senza librerie |
| `anteprima_telefono.png`, `anteprima_desktop.png`, `anteprima_scuro.png` | la pagina a 400 e 1280 px |

Nessun file contiene testi del canale: i messaggi d'esempio sono scritti apposta.

## I tre modi di far arrivare i messaggi

1. **Export di Telegram Desktop** (`da_export_desktop`, oppure `python aldo.py importa result.json`): per lo storico e i recuperi.
   Usa `date_unixtime` (il campo `date` è nell'ora locale del computer che esporta). Le foto vengono prese se l'export le include.
2. **Inoltro al bot di radar** (consigliato, nessuna credenziale in più): inoltri i post di Aldo al bot che radar usa già;
   a ogni giro `leggi_inoltri` legge la coda (getUpdates, Telegram la conserva 24 ore), tiene solo gli inoltri arrivati dalla
   tua chat e con origine "Aldo"/"Qefalia", e li salva con la data originale del post (`forward_origin.date`).
3. **Telethon** (opzionale, spento): legge il canale con il tuo account. Vedi sotto i rischi.

I tre modi producono lo stesso formato (`id`, `data` UTC, `testo`, `foto`, `risposta_a`) e `unisci` toglie i doppioni.

## Estrazione

- **Regole** (sempre): espressioni regolari in italiano per apertura, aumento, chiusure (metà, 80%, un terzo, il resto), stop a
  pareggio, stop spostato, stop preso, obiettivo preso, ordine limite, ordine annullato, piani condizionali ("se torna a 61,2k
  short"). Numeri come 27.6k, 27,6k, 25.300, 0,686, 27,187.9, letti col prezzo di mercato del momento. Asset: BTC se non scritto.
  Ogni evento ha `affidabilita`; sotto 0,5 va rivisto.
- **Modello** (solo con `ANTHROPIC_API_KEY`): Claude legge testo, immagine e posizioni aperte. Modello `claude-haiku-5-5`
  (modificabile con `RADAR_ALDO_MODELLO`): è il Haiku attuale indicato dalla documentazione per estrazioni ad alto volume a basso
  costo, legge le immagini, costa 0,10 $ / 0,50 $ per milione di token (circa 0,0003 $ a messaggio con una schermata). Effort
  `low`, uscita vincolata a uno schema JSON e poi rivalidata nel modulo (tipi, quote, prezzi entro ±60% dal mercato). Se il modello
  non risponde, rifiuta o sbaglia formato, resta il risultato a regole.

## Verifica sullo storico (fatta qui, non riproducibile nei test perché usa i dati privati)

Con l'estrazione controllata dello studio (`importa_studio` su `telegram/estrazione/eventi_*.json` e `piani_*.json`) e i prezzi
orari di Binance, il motore del modulo riproduce i numeri di `ALDO_ELIZ_INTRADAY.md`:

| | Operazioni | In guadagno | Medio | Studio |
|---|---|---|---|---|
| Trader, prezzi suoi | 55 | 73% | +3,35% | 55 · 73% · +3,35% |
| Chi copiava a mercato | 39 | 44% | +1,28% | 39 · 44% · +1,38% |
| Chi copiava con ordini limite | 43 (20 entrate a limite) | 58% | +2,05% | 43 · 58% · +2,15% (20) |

Le piccole differenze vengono da due adattamenti: lo stop preso senza prezzo si chiude allo stop dichiarato (nello studio sempre a
pareggio) e il ritardo si misura fino al messaggio (nello studio fino a 59 minuti dopo).

Con le **sole regole** sullo stesso storico (812 messaggi) si ritrovano 61 delle 174 coppie messaggio/evento dello studio: molti
dati sono solo nelle schermate. Per lo storico usare `importa_studio` o l'estrattore con modello; le regole servono per i messaggi
scritti in chiaro.

## Telethon: rischi

È l'account Telegram personale dell'utente, non un bot. `api_id` e `api_hash` si prendono su my.telegram.org; il file di sessione
equivale a un accesso completo all'account: resta solo sulla macchina di radar (`~/.radar/aldo.session`, permessi 600), mai nel
repo, nei log o nei backup condivisi. I contenuti del canale sono a pagamento e per uso personale: niente ridistribuzione, nemmeno
attraverso la dashboard se il sito è pubblico. Telegram può limitare o bloccare gli account che si comportano da automi: il modulo
legge al massimo 200 messaggi nuovi a giro, solo dal canale indicato. Disattivato finché `RADAR_ALDO_TELETHON` non vale 1.

## Limiti

- Le regole non leggono le immagini; senza modello le operazioni annunciate solo con una schermata restano "da rivedere".
- Gli inoltri dal bot non portano l'id originale del messaggio (tranne dai canali): i doppioni si riconoscono da data e testo.
  Un post modificato dopo l'inoltro non si aggiorna; un album arriva come messaggi separati.
- Operazioni comunicate solo dopo l'ingresso: si vedono quando escono e restano fuori dalle simulazioni di chi copia.
- Prezzi orari spot (OKX, oppure Binance con `RADAR_ALDO_PREZZI=binance`): le sue posizioni sono perpetual su Bybit, con
  differenze piccole ma non nulle.
- Il modello non è stato provato qui (nessuna chiave in questo ambiente): i test usano un client finto.

Ricerca su dati storici, non una raccomandazione d'investimento.
