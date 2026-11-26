# Prompt per la sessione Claude Code del repo `radar`

Incolla tutto il testo qui sotto nella sessione di radar e allega i file di questa cartella (compresa la cartella `deploy/`).

---

Voglio in Radar uno strumento per **copiare Aldo**, il trader del canale Telegram privato "Aldo Qefalia - Trading" (supergruppo
privato, non a pagamento: io sono membro, non amministratore). Aldo non ha un profilo di copy trading sugli exchange: si copia
dal canale. Lo strumento legge il canale in tempo reale, capisce cosa fa Aldo e mi manda su Telegram **l'ordine pronto per
Bitget** (futures USDT-M), che io metto a mano; due pulsanti, «Fatto» e «Salto», registrano cosa ho fatto, così posso confrontare
la mia copia reale con la copia sulla carta. **Radar non invia ordini.**

## Da dove viene

L'ho studiato in un altro repo (`teststrategy`, file `TELEGRAM_ALDO.md` e `ALDO_ELIZ_INTRADAY.md`). Sui messaggi dal 05/2023 al
03/2024: Aldo, con i prezzi delle sue schermate, 55 operazioni, 73% in guadagno, +3,35% medio; chi lo copiava **a mercato dopo il
messaggio** 44% in guadagno, +1,4%; chi metteva **ordini limite sui livelli annunciati prima** 58%, +2,1%. Il suo stile: livelli
decisi prima, ordine limite, metà al primo obiettivo, stop a pareggio, BTC e altcoin, leva circa 10x.

Da qui le regole di copia (già decise, non vanno ottimizzate):
1. **Livello annunciato** → ordine limite al livello, valido 24 ore.
2. **Ingresso senza livello** → a mercato solo se l'avviso arriva entro 10 minuti dal suo ingresso stimato e con scostamento sotto
   lo 0,5%; altrimenti avviso informativo "non copiare".
3. Stop dichiarato o, se manca, 2% oltre il livello (segnalato). Metà al primo obiettivo, poi stop a pareggio.
4. Dimensione: modalità **"importo"** (predefinita): margine fisso per operazione 500–2.000 € (predefinito 1.000) con leva 5x
   (tetto 10x), e l'avviso dice quanto si perde allo stop in € e in % dell'importo; oppure modalità **"rischio"**: perdita allo stop
   pari a RISCHIO_PCT (2%) del capitale. Cambio EUR/USDT configurabile (1,08), indicato come approssimato.

## Cosa ti allego

| File | A cosa serve |
|---|---|
| `aldo.py` | Registro: formato dei messaggi, estrattore a regole e con modello, collegamento alle operazioni, motore di ricostruzione dello studio (trader / a mercato / con ordini limite), statistiche, `build()` della sezione, riepilogo settimanale; import da export di Telegram Desktop e dall'estrazione dello studio |
| `aldo_bitget.py` | Bitget USDT-M, solo endpoint pubblici: specifiche dei contratti con cache (`sizeMultiplier`, `minTradeNum`, `pricePlace`, `volumePlace`), ticker, candele 1 minuto e 1 ora, arrotondamenti, `ordine()` nelle due modalità; `esegui_su_bitget()` solo come punto d'aggancio (spento, non implementato) |
| `aldostream.py` | Il servizio sulla VM: Telethon in tempo reale (messaggi nuovi e modifiche, sola lettura), estrazione, avvisi con pulsanti, registro reale, latenza, registro sulla carta ogni ora, riepilogo del lunedì; riconnessioni e FloodWait |
| `prompt_estrattore.md` | Istruzioni dell'estrattore con modello (il testo del canale è un dato, non un'istruzione) |
| `deploy/ALDOSTREAM.md`, `deploy/aldostream.service` | Guida passo passo e unit systemd, sul modello di `LIQSTREAM.md` |
| `test_aldo.py`, `test_aldostream.py`, `esempio.py` | 68 test offline: client Telegram finto, specifiche Bitget dal file d'esempio, messaggi e prezzi inventati |
| `bitget_contratti_esempio.json`, `bitget_ticker_esempio.json` | Specifiche e ticker veri di BTCUSDT, ETHUSDT, SOLUSDT, scaricati da api.bitget.com, per i test |
| `esempio_avvisi.md` | I testi proposti degli avvisi, con dati inventati: **da approvare** |
| `esempio_sezione.json`, `esempio_riepilogo.md`, `riferimento_sezione.html`, `anteprima_*.png` | Riepilogo privato (schema di `build()`), riepilogo settimanale, pagina di riferimento |
| `LEGGIMI.md` | Dettagli: modello, verifica sullo storico, rischi di Telethon, limiti |

## Come integrarla

- **Moduli**: `radar/aldo.py`, `radar/aldo_bitget.py`, `radar/aldostream.py`, `radar/prompt_estrattore_aldo.md` (aggiorna
  `PROMPT_ESTRATTORE`). Gli import diretti (`import aldo as A`, `from aldo_bitget import …`) diventano relativi: sono segnati con
  un commento `# in radar: …`. Test in `tests/` con `esempio.py` e i due file JSON di Bitget come dati di prova.
- **Deploy**: `deploy/ALDOSTREAM.md` e `deploy/aldostream.service` nel repo. Il servizio gira sulla stessa VM di `liqstream`,
  con `/etc/aldostream.env` (permessi 600). Dipendenze del solo servizio (`telethon`, e `anthropic` se si usa il modello) in un file
  a parte (es. `requirements-aldostream.txt`): il giro orario su GitHub non deve installarle.
- **Dati**: testi, foto, registro, avvisi, latenze stanno solo sulla VM in `ALDO_DATI` (`~/aldo-dati`), fuori dal repo; la sessione
  Telethon in `~/.aldostream/` con permessi 600. Il servizio **non fa commit né push**. Aggiungi comunque a `.gitignore`
  `*.session`, `aldo-dati/` e `data/aldo/` come protezione.
- **Bot**: `radar/journal.py` legge già il bot di radar con getUpdates ogni ora. I pulsanti richiedono che il servizio legga gli
  aggiornamenti del bot: due lettori sulla stessa coda si rubano i messaggi. Quindi **bot dedicato** (`ALDO_BOT_TOKEN`, creato con
  BotFather, stessa chat `TELEGRAM_CHAT_ID`); senza bot dedicato gli avvisi partono dal bot di radar ma senza pulsanti. Non
  modificare `journal.py` senza chiedermelo.
- **Dashboard**: la sezione "Aldo" è **spenta di default** (`ALDO_SEZIONE_PUBBLICA=0`): restano gli avvisi privati su Telegram e il
  riepilogo privato sulla VM (`sezione.json`, `riepilogo_*.md`, sintesi del lunedì nella chat del bot). Se in futuro la accendo,
  la sezione non contiene testi dei messaggi, e i suoi dati (solo `sezione.json`) dovrebbero arrivare dalla VM come fa liqstream:
  non implementarlo ora, proponimelo se serve. Se il sito di radar è pubblico, la sezione resta spenta in ogni caso.
- **Estrattore con modello**: solo se c'è `ANTHROPIC_API_KEY` in `/etc/aldostream.env`. Modello `claude-haiku-5-5`
  (`RADAR_ALDO_MODELLO` per cambiarlo). Se il modello non risponde o sbaglia formato, restano le regole.
- **Storico**: per partire con il registro già pieno, `importa_studio(...)` con i file `telegram/estrazione/eventi_*.json` e
  `piani_*.json` di teststrategy più l'export `result.json`: li copio io sulla VM in `ALDO_DATI` (contengono testi del canale:
  **mai nel repo**). Con questi il motore riproduce i numeri dello studio (vedi `LEGGIMI.md`).
- **Avvisi**: `ALDO_AVVISI=0` all'inizio: gli avvisi vengono composti, misurati e salvati in `avvisi.json` ma non inviati. **Fammi
  vedere i testi** (`esempio_avvisi.md` e quelli veri dei primi giorni) prima di passare a `ALDO_AVVISI=1`. Nessuna ora silenziosa
  di default (avvisi anche di notte).

## Vincoli

- Segui le regole del progetto: skill gengar, file `stato/STATO-aldo.md`, test, suite verde, render a 400 e 1280 px della pagina di
  riferimento se tocchi la dashboard, deploy (qui: la VM, seguendo `deploy/ALDOSTREAM.md`) e verifica.
- **W3.2 non si tocca**: nessuna modifica a `radar/weekly.py`, ai segnali, agli stop o al capitale.
- **Nessun avviso Telegram nuovo senza la mia approvazione** dei testi.
- **Nessuna credenziale nel repo**: né `TELEGRAM_API_ID`/`TELEGRAM_API_HASH`, né file di sessione, né token dei bot, né chiave
  Anthropic. Niente nei log: il servizio scrive solo id dei messaggi, tipi di evento e latenze.
- **Sola lettura del canale**: nessun messaggio nel canale, nessuna reazione, nessuna azione dell'account oltre alla lettura.
- **Nessun ordine automatico**: `esegui_su_bitget` resta uno stub; il pulsante «Esegui su Bitget» resta spento.
- Le regole di copia e i limiti (importo 500–2.000 €, leva massima 10x, 10 minuti, 0,5%, 24 ore) non si ottimizzano: se trovi un
  motivo per cambiarli, dimmelo prima.
- Testi sobri: canale privato, uso personale; chi copiava a mercato faceva molto peggio del trader.

## Come capisco che è fatto

1. `python -m pytest` verde, con i 68 test del pacchetto adattati (estrattore, Bitget con il file d'esempio, ordine nelle due
   modalità, avvisi in tempo reale con client finto, pulsanti, regola a mercato, modifiche, ore silenziose, FloodWait/rete che non
   fermano il servizio, riepilogo del lunedì).
2. Un test che dimostra che il giro orario di radar non importa né `telethon` né `anthropic`.
3. Sulla VM: `python -m radar.aldostream prova` mostra canale, specifiche Bitget e bot; il servizio è attivo con systemd e al primo
   messaggio di Aldo il log riporta eventi, avvisi e latenza in secondi.
4. I testi degli avvisi dei primi giorni (da `avvisi.json`), in attesa del mio via libera.
5. Conferma che nel repo e nel sito non c'è nessun file di `ALDO_DATI` né la sessione.
6. Un riepilogo finale: cosa hai cambiato rispetto al pacchetto, dove stanno i file, cosa resta spento (sezione pubblica, invio
   avvisi fino all'approvazione, esecuzione su Bitget).
