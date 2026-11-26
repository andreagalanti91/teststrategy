# Prompt per la sessione Claude Code del repo `radar`

Incolla tutto il testo qui sotto nella sessione di radar e allega i file di questa cartella.

---

Voglio in Radar uno strumento per seguire **Aldo**, il trader del canale Telegram privato "Aldo Qefalia - Trading" (supergruppo
privato a pagamento: io sono membro, non amministratore). Deve registrare i suoi messaggi, ricavarne le operazioni, ricostruirle
sui prezzi veri e mostrarmi nella dashboard **i livelli che annuncia prima, da mettere a ordine limite**, le sue posizioni aperte e
come sarebbe andato chi lo copiava. Tutto **sulla carta**: Radar non invia ordini.

## Da dove viene

L'ho studiato in un altro repo (`teststrategy`, file `TELEGRAM_ALDO.md` e `ALDO_ELIZ_INTRADAY.md`). In breve, sui messaggi dal
05/2023 al 03/2024:

- con i prezzi delle sue schermate (autentiche) Aldo ha 55 operazioni, 73% in guadagno, +3,35% medio sul controvalore;
- chi lo copiava **a mercato dopo il messaggio**: 39 operazioni copiabili, 44% in guadagno, +1,4% medio;
- chi metteva **ordini limite sui livelli annunciati prima**: 43 operazioni, 58% in guadagno, +2,1% medio. È l'unico modo di
  copiarlo che conserva una parte del suo vantaggio;
- il suo stile: livelli decisi prima, ingresso con ordine limite, metà al primo obiettivo, stop a pareggio, BTC e altcoin, leva
  circa 10x su Bybit.

## Cosa ti allego

| File | A cosa serve |
|---|---|
| `aldo.py` | Modulo autonomo (libreria standard + pandas/numpy): ingresso dei messaggi (export, inoltri al bot, Telethon), estrattore a regole e con modello, registro, motore di ricostruzione dello studio, statistiche, avvisi proposti, `build()` per la dashboard, riepilogo settimanale, `giro()` |
| `prompt_estrattore.md` | Le istruzioni dell'estrattore con modello |
| `test_aldo.py`, `esempio.py` | 44 test offline; `esempio.py` contiene 12 messaggi inventati e prezzi sintetici |
| `esempio_sezione.json` | Uscita di `build()`: è lo schema della sezione |
| `esempio_riepilogo.md` | Il riepilogo settimanale con gli stessi dati |
| `riferimento_sezione.html`, `anteprima_*.png` | Come immagino la sezione (stato attivo e vuoto, chiaro e scuro). In Radar va rifatta con i componenti e i colori della dashboard |
| `LEGGIMI.md` | Dettagli: modi d'ingresso, scelta del modello, verifica sullo storico, rischi di Telethon, limiti |

## Cosa deve mostrare la sezione

Una nuova scheda (o card) **"Aldo"**, con l'etichetta "su carta" ben visibile:

1. **Stato** in una riga con etichetta (`PIANI`, `POSIZIONI`, `ATTESA`, `VUOTO`): campi `stato`, `titolo`, `testo`.
2. **Livelli da mettere a ordine limite** (`piani`): asset, verso, livello, distanza dal prezzo, stop (se manca: 2% oltre il livello,
   segnalato), obiettivi, quantità con rischio 1% del capitale (controvalore e leva), annunciato, scadenza (7 giorni), stato
   ("in attesa" o "livello toccato").
3. **Posizioni aperte di Aldo** (`posizioni`): dal, prezzo medio, adesso, quota aperta, stop (o "a pareggio"), risultato del
   trader, di chi copiava a mercato e con ordini limite.
4. **Ultime operazioni chiuse** (`chiuse`, 10): trader contro chi copiava, con le note "entrata con ordine limite" e "comunicata dopo".
5. **Statistiche** (`statistiche`, `ritardo`): per i tre modi, operazioni, % in guadagno, medio, capitale con rischio 1% e 2%;
   ritardo fra il prezzo dichiarato e il messaggio.
6. **Avvisi proposti** (chiusi di default) e **come si copia** (`regole`), la riga sulla fonte (`fonte`: messaggi per origine,
   estrattore, eventi da rivedere, ultimo messaggio) e l'**avvertenza fissa** (`avvertenza`).

La sezione contiene solo numeri e livelli: **nessun testo dei messaggi del canale**.

## Come integrarla

- **Modulo**: `aldo.py` in `radar/aldo.py`, `prompt_estrattore.md` in `radar/prompt_estrattore_aldo.md` (aggiorna
  `PROMPT_ESTRATTORE`), test in `tests/` con `esempio.py` come dati di prova. Per i prezzi usa `_get` e le convenzioni di rete che
  radar ha già (`radar/data.py` chiama `www.okx.com`): `Prezzi(cartella, get=...)`. Niente fonti nuove oltre OKX (Binance solo
  come alternativa configurabile).
- **A ogni giro orario**: `aldo.giro("data/aldo", chiama_bot=..., chat_autorizzate=[la mia chat])` dentro `_soft`, e l'uscita nel
  report sotto la chiave `aldo`. Un errore qui non deve fermare il giro né toccare il resto. `giro` salva i file solo se cambiano.
- **Inoltri al bot** (il modo principale): guarda come radar usa oggi il bot Telegram.
  - Se il bot solo invia messaggi, scrivi `chiama_bot(metodo, parametri)` con lo stesso token per `getUpdates`; l'offset sta in
    `data/aldo/eventi.json`.
  - Se radar legge già gli update (getUpdates o webhook), passa gli update a `da_aggiornamento_bot` dal lettore esistente: mai due
    lettori sulla stessa coda (con un webhook attivo getUpdates non funziona).
  - Chat autorizzata: la chat a cui radar manda già gli avvisi. Filtro sull'origine: `RADAR_ALDO_ORIGINI` (predefinito
    "aldo,qefalia").
  - Le foto degli inoltri si scaricano (getFile) solo se c'è l'estrattore con modello.
  - Il bot **non risponde** agli inoltri: una conferma ("salvato") sarebbe un messaggio nuovo. Se pensi serva, proponimi il testo.
  - Il token non deve comparire in log o messaggi d'errore (attenzione alle URL con il token dentro).
- **Estrattore con modello**: attivo solo se nell'ambiente di radar c'è `ANTHROPIC_API_KEY` (segreto della macchina o del
  servizio, mai nel repo). Modello `claude-haiku-5-5`, modificabile con `RADAR_ALDO_MODELLO`; al massimo 50 messaggi per giro.
  `anthropic` è una dipendenza opzionale: importata solo se serve.
- **Telethon**: opzionale, spento (`RADAR_ALDO_TELETHON=1` per accenderlo, con `RADAR_ALDO_TG_API_ID`, `RADAR_ALDO_TG_API_HASH`,
  `RADAR_ALDO_TG_SESSIONE`, `RADAR_ALDO_TG_CANALE`). La sessione si crea una volta a mano con `python -m radar.aldo accedi` e resta
  fuori dal repo. `telethon` non va nei requisiti obbligatori. Non accenderlo tu: leggi i rischi in `LEGGIMI.md`.
- **Storico**: due strade, da propormi.
  - `importa_studio(...)` con i file `telegram/estrazione/eventi_*.json` e `piani_*.json` di teststrategy più l'export
    `result.json`: li copio io sulla macchina di radar (contengono testi del canale: **non nel repo**). Con questi il modulo
    riproduce i numeri dello studio (vedi `LEGGIMI.md`).
  - `python -m radar.aldo importa result.json`: con le sole regole lo storico viene ricostruito male (61 eventi su 174), serve il modello.
- **File di stato**: in `data/aldo/` vanno `messaggi.json`, `eventi.json`, `operazioni.json`, `foto/`, `prezzi/`, `riepilogo_*.md`.
  `messaggi.json`, `eventi.json` (contiene estratti di 120 caratteri), `foto/` e i riepiloghi sono **contenuti privati**: fuori dal
  repo (`.gitignore`) e fuori da quello che si pubblica. Se radar salva lo stato facendo commit di `data/`, fermati e chiedimi come
  tenerli fuori.
- **Pubblicazione**: se il sito di radar è pubblico, la sezione mostrerebbe a chiunque i livelli di un canale a pagamento. Prima del
  deploy verifica se il sito è pubblico: in quel caso non pubblicare la sezione (pagina protetta, oppure visibile solo in locale) e
  chiedimi come procedere.
- **Capitale**: `RADAR_ALDO_CAPITALE` (se manca, 10.000 $ indicati come "d'esempio").
- **Riepilogo settimanale**: al primo giro del lunedì, `riepilogo_settimanale` della settimana appena finita in
  `data/aldo/riepilogo_AAAA-MM-GG.md`. Nessun invio: lo passo io a una sessione di analisi.
- **Avvisi Telegram**: il modulo prepara i testi (ordine limite suggerito con quantità al rischio 1%, chiusura parziale, stop a
  pareggio) ma `avvisi_da_inviare` resta vuoto finché `RADAR_ALDO_AVVISI` non vale 1. **Fammi vedere i testi prima di attivarli.**
  Messaggi più vecchi di 6 ore non generano avvisi.

## Vincoli

- Segui le regole del progetto: skill gengar, file `stato/STATO-aldo.md`, test, suite verde, render a 400 e 1280 px, deploy e
  verifica (con il limite sulla pubblicazione scritto sopra).
- **W3.2 non si tocca**: nessuna modifica a `radar/weekly.py`, ai segnali, agli stop o al capitale.
- **Nessun avviso Telegram nuovo senza la mia approvazione** dei testi.
- **Nessuna credenziale nel repo**: né chiavi Anthropic, né `api_id`/`api_hash`, né file di sessione Telethon, né token del bot.
- **Nessun ordine, nessuna chiave di borsa**: solo prezzi pubblici.
- Le regole di copia (solo livelli annunciati prima, stop dichiarato o 2%, rischio 1%, piano valido 7 giorni) non si ottimizzano:
  se trovi un motivo per cambiarle, dimmelo prima.
- Testi sobri: deve essere chiaro che è un registro su carta, ricostruito, per uso personale, e che chi copiava a mercato faceva
  molto peggio del trader.
- Tema chiaro e scuro; dal telefono nessuno scorrimento orizzontale della pagina (le tabelle scorrono nel loro riquadro).

## Come capisco che è fatto

1. `python -m pytest` verde, con i 44 test di `test_aldo.py` adattati al modulo in `radar/` (estrattore a regole, ingresso dal bot
   e dall'export, ricostruzione nei tre modi, dimensione al rischio 1%, `build()` in tutti gli stati, avvisi spenti, estrattore con
   modello finto, giro offline).
2. Un test che dimostra che un errore di rete (bot, OKX, modello) non ferma il giro di radar.
3. Screenshot della sezione a 400 e 1280 px, tema chiaro e scuro, nello stato "vuoto" e con i miei primi messaggi inoltrati.
4. La prova dell'inoltro: inoltro due o tre post di Aldo al bot e al giro dopo li vedo in `data/aldo/messaggi.json` con la data
   originale, e nella sezione.
5. `.gitignore` aggiornato e conferma che nessun file privato di `data/aldo/` è nel repo o nel sito pubblicato.
6. I testi proposti per gli avvisi, in attesa del mio via libera.
7. Un riepilogo finale: cosa hai cambiato rispetto ad `aldo.py`, come legge gli update del bot, dove sta la sezione, cosa resta spento.
