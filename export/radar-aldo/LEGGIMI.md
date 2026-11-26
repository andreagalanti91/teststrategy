# Esportazione dello strumento "Aldo" verso radar

Da dare alla sessione Claude Code del repo `radar`: incolla `PROMPT.md` e allega i file di questa cartella (compresa `deploy/`).

Strumento per copiare il trader del canale privato "Aldo Qefalia - Trading": un servizio sulla VM di radar legge il canale in
tempo reale (Telethon, sola lettura), estrae cosa fa Aldo e manda su Telegram l'ordine pronto per Bitget (futures USDT-M), che
l'utente mette a mano; i pulsanti «Fatto» e «Salto» registrano la copia reale accanto a quella sulla carta. Nessun ordine
automatico.

| File | Contenuto |
|---|---|
| `PROMPT.md` | il prompt da incollare nella sessione di radar |
| `aldo.py` | registro: formato dei messaggi, estrattori (regole sempre, modello se c'è la chiave), collegamento alle operazioni, motore di ricostruzione dello studio, statistiche, `build()`, riepilogo settimanale, import da export e dall'estrazione dello studio |
| `aldo_bitget.py` | Bitget USDT-M pubblico: specifiche con cache, ticker, candele, arrotondamenti, `ordine()` in modalità "importo" o "rischio", stub `esegui_su_bitget()` |
| `aldostream.py` | servizio sulla VM: Telethon in tempo reale, avvisi con pulsanti, registro reale, latenza, riconnessioni e FloodWait; comandi `accedi`, `canali`, `prova` |
| `prompt_estrattore.md` | istruzioni dell'estrattore con modello (il testo del canale è un dato, non un'istruzione) |
| `deploy/ALDOSTREAM.md`, `deploy/aldostream.service` | guida passo passo per la VM e unit systemd |
| `test_aldo.py`, `test_aldostream.py` | 68 test offline (`python -m pytest -q`) |
| `esempio.py` | messaggi INVENTATI, prezzi sintetici, client Telegram finto; `python esempio.py` rigenera gli esempi |
| `bitget_contratti_esempio.json`, `bitget_ticker_esempio.json` | specifiche e ticker veri di BTCUSDT, ETHUSDT, SOLUSDT (api.bitget.com, 26/11/2026) |
| `esempio_avvisi.md` | gli avvisi proposti, uno per tipo, con dati inventati: da approvare |
| `esempio_sezione.json`, `esempio_riepilogo.md` | riepilogo privato (`build()`) e riepilogo settimanale con gli stessi dati |
| `riferimento_sezione.html`, `anteprima_telefono.png`, `anteprima_desktop.png`, `anteprima_scuro.png` | pagina di riferimento a 400 e 1280 px, chiara e scura |

Nessun file contiene testi del canale.

## Come funziona

1. **Lettura**: `aldostream.py` resta collegato al canale con l'account dell'utente; a ogni messaggio nuovo (e a ogni modifica)
   salva testo e foto solo sulla VM (`ALDO_DATI`, fuori dal repo). All'avvio recupera i messaggi persi mentre era fermo.
2. **Estrazione**: regole in italiano (apertura, aumento, chiusure, stop a pareggio, stop preso, obiettivo, ordine limite, piano
   con livello; numeri come 27.6k, 27,6k, 25.300, 0,686) più, se c'è `ANTHROPIC_API_KEY`, il modello `claude-haiku-5-5` che legge
   anche le schermate. È il Haiku attuale, indicato per estrazioni ad alto volume a basso costo (0,10 $ / 0,50 $ per milione di
   token, circa 0,0003 $ a messaggio con immagine); uscita vincolata a uno schema e ricontrollata; in caso di errore restano le regole.
3. **Avvisi** (`esempio_avvisi.md`): nuovo livello → ordine limite al livello con quantità in contratti Bitget, stop, obiettivo 1
   (metà) e successivi, margine, leva, perdita allo stop, scadenza 24 ore; ingresso senza livello → a mercato solo entro 10 minuti
   e con scostamento sotto lo 0,5%, altrimenti "non copiare"; chiusura parziale, stop a pareggio, chiusura, stop preso, livello
   annullato. Invio spento finché `ALDO_AVVISI` non vale 1. Nessuna ora silenziosa di default.
4. **Dimensione**: modalità "importo" (predefinita): margine `IMPORTO_EUR` (1.000, fra 500 e 2.000) × cambio `CAMBIO_EUR_USDT`
   (1,08, approssimato) × `LEVA` (5, tetto `LEVA_MAX` 10); se la perdita allo stop supera il 50% del margine l'avviso dice "stop
   troppo lontano per questa leva: riduci la leva". Modalità "rischio": perdita allo stop = `RISCHIO_PCT` (2%) di `COPIA_CAPITALE`,
   leva al massimo `LEVA_MAX`. Prezzo e quantità arrotondati alle specifiche del contratto (passo, minimo, controvalore minimo).
5. **Registri**: sulla carta (tre modi: trader, a mercato, con ordini limite) aggiornato a ogni messaggio e ogni ora con le
   candele di Bitget; reale dai pulsanti (`reale.json`); latenza messaggio → avviso (`latenze.jsonl`).
6. **Riepilogo**: privato, sulla VM (`sezione.json`, `riepilogo_AAAA-MM-GG.md` il lunedì) e una sintesi nella chat del bot. La
   sezione nella dashboard pubblica resta spenta (`ALDO_SEZIONE_PUBBLICA=0`).

## Verifica sullo storico (fatta qui con i dati privati, non nei test)

Con l'estrazione controllata dello studio (`importa_studio`) e i prezzi orari di Binance, il motore riproduce i numeri dello
studio: trader 55 operazioni, 73% in guadagno, +3,35%; a mercato 39, 44%, +1,28% (studio +1,38%); con ordini limite 43, 58%,
+2,05% (studio +2,15%), 20 entrate a limite. Le differenze vengono da due adattamenti (stop preso senza prezzo chiuso allo stop
dichiarato; ritardo misurato fino al messaggio). Con le sole regole, sullo stesso storico, si ritrovano 61 delle 174 coppie
messaggio/evento: molti dati sono solo nelle schermate, per questo serve il modello.

## Telethon: rischi

È l'account personale dell'utente. `api_id` e `api_hash` (my.telegram.org) e il file di sessione danno accesso all'account:
restano sulla VM (`/etc/aldostream.env` e `~/.aldostream/`, permessi 600), mai nel repo o nei log. Canale privato, uso personale:
nessuna ridistribuzione. Telegram può limitare gli account che si comportano da automi: il servizio ascolta un solo canale, non
scrive, non reagisce, rispetta FloodWait.

## Limiti

- Il modello non è stato provato qui (nessuna chiave): i test usano un client finto. Telethon e l'API Bot sono provati con
  client finti; il primo collaudo vero è `python -m radar.aldostream prova` sulla VM.
- Prezzi del registro sulla carta: candele orarie di Bitget; Aldo opera su Bybit, con differenze piccole.
- Il "ritardo d'ingresso" per la regola a mercato si stima dalle candele da 1 minuto (ultima volta al suo prezzo); senza prezzo
  dichiarato si assume l'ingresso al momento del messaggio.
- La copia reale registra solo cosa hai fatto (Fatto/Salto), non i prezzi eseguiti: il suo risultato è quello simulato del modo usato.
- Un messaggio modificato dopo l'estrazione non cambia il registro da solo: avviso informativo e voce "da rivedere".
- Gli inoltri al bot restano nel modulo come modo di riserva, ma il bot di radar è già letto da `journal.py`.

Ricerca su dati storici, non una raccomandazione d'investimento.
