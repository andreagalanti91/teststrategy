# Avvisi in tempo reale dal canale di Aldo: lettore Telethon sulla VM di radar

**Perché serve.** Aldo pubblica i livelli nel suo canale Telegram privato e chi lo copia deve mettere l'ordine limite prima che
il prezzo ci arrivi; per gli ingressi senza livello conta ogni minuto. `radar/aldostream.py` resta collegato 24 ore su 24 al canale
con il tuo account Telegram (Telethon, sola lettura), estrae gli eventi da ogni messaggio (regole, più il modello se c'è la
chiave Anthropic), aggiorna il registro sulla carta e ti manda su Telegram l'ordine pronto per Bitget (futures USDT-M) entro pochi
secondi, con i pulsanti «Fatto» e «Salto». Misura e salva la latenza (ora del messaggio → ora dell'avviso).

Cosa **non** fa: non scrive nel canale, non reagisce, non segna come letti i messaggi, non entra o esce da chat; non invia
ordini a Bitget. Testi e foto del canale restano solo sulla VM, in una cartella fuori dal repo: niente commit, niente push.

Rischi da conoscere: è il tuo account personale, non un bot. Il file di sessione equivale a un accesso completo all'account. I
contenuti del canale privato sono per uso personale: nessuna ridistribuzione. Telegram può limitare o bloccare gli account che si
comportano da automi: il servizio si limita ad ascoltare un canale e rispetta le attese che Telegram chiede (FloodWait).

Costo: 0 € (stessa VM del raccoglitore delle liquidazioni). Modello facoltativo: circa 0,0003 $ a messaggio con un'immagine.
Tempo: circa 20 minuti la prima volta.

---

## 0. Prerequisito: la VM
Si usa la VM già creata per il raccoglitore delle liquidazioni (`deploy/LIQSTREAM.md`, passi 1–4: sistema aggiornato, fuso UTC,
repo in `~/radar`, ambiente `.venv`). Se non esiste ancora, seguire prima quei passi.

## 1. Creare l'app Telegram (api_id e api_hash)
1. Dal PC aprire <https://my.telegram.org>, inserire il proprio numero (formato internazionale, `+39…`) e il codice che arriva
   nell'app Telegram.
2. **API development tools** → compilare il modulo: App title `radar-aldo`, Short name `radaraldo`, Platform `Desktop`, il resto
   vuoto → **Create application**.
3. Annotare **App api_id** (un numero) e **App api_hash** (32 caratteri). Sono legati al tuo account: non vanno mai nel repo, in
   chat, nei Secrets di GitHub o negli screenshot.

## 2. Bot per gli avvisi
Consigliato un **bot dedicato** solo ad Aldo: il bot di radar viene già letto ogni ora da `radar/journal.py` (getUpdates) e un
secondo lettore sulla stessa coda ruberebbe i messaggi al diario. Con un bot dedicato il servizio legge solo i pulsanti.
1. In Telegram scrivere a **@BotFather** → `/newbot` → nome `Radar Aldo`, username a scelta che finisce in `bot`.
2. Copiare il token (`123456:ABC…`): andrà in `ALDO_BOT_TOKEN`.
3. Aprire la chat con il nuovo bot e premere **Avvia** (un bot non può scrivere per primo).
4. `TELEGRAM_CHAT_ID` è lo stesso che usa già radar (la tua chat).

Senza bot dedicato il servizio usa `TELEGRAM_BOT_TOKEN` di radar: gli avvisi arrivano, ma senza pulsanti (niente registro reale).

## 3. Installare
```bash
cd ~/radar
git pull
.venv/bin/pip install telethon            # obbligatorio per il servizio
.venv/bin/pip install anthropic           # solo se si usa l'estrattore con modello
mkdir -p ~/aldo-dati ~/.aldostream && chmod 700 ~/aldo-dati ~/.aldostream
```
`~/aldo-dati` (testi, foto, registro, avvisi, latenze) e `~/.aldostream` (sessione) sono fuori dal repo: git non li vede.

## 4. Variabili d'ambiente (fuori dal repo)
```bash
sudo tee /etc/aldostream.env >/dev/null <<'EOF'
# lettura del canale (passo 1)
TELEGRAM_API_ID=1234567
TELEGRAM_API_HASH=0123456789abcdef0123456789abcdef
ALDO_CANALE_ID=-1001984997641
ALDO_SESSIONE=/home/ubuntu/.aldostream/aldo
ALDO_DATI=/home/ubuntu/aldo-dati
# avvisi (passo 2)
ALDO_BOT_TOKEN=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
# 0 = avvisi solo registrati in ALDO_DATI/avvisi.json; 1 = inviati (dopo aver approvato i testi)
ALDO_AVVISI=0
# dimensione: "importo" (margine fisso con leva fissa) oppure "rischio" (perdita allo stop = RISCHIO_PCT del capitale)
MODALITA=importo
IMPORTO_EUR=1000
CAMBIO_EUR_USDT=1.08
LEVA=5
LEVA_MAX=10
COPIA_CAPITALE=10000
RISCHIO_PCT=2
# regole di copia
COPIA_MAX_MINUTI=10
COPIA_MAX_SCOSTAMENTO_PCT=0.5
ORDINE_ORE=24
ORE_SILENZIOSE=
ALDO_FUSO=Europe/Rome
# facoltativa: estrattore con modello (legge anche le schermate)
ANTHROPIC_API_KEY=
EOF
sudo chmod 600 /etc/aldostream.env
sudo nano /etc/aldostream.env     # inserire i valori veri
```
`ALDO_CANALE_ID`: l'id dell'export di Telegram Desktop (`1984997641`) con `-100` davanti; per controllarlo, dopo il passo 5,
`python -m radar.aldostream canali` elenca id e nome di gruppi e canali dell'account. `IMPORTO_EUR` è ammesso fra 500 e 2000;
`LEVA_MAX` non va oltre 10. Il cambio EUR/USDT è approssimato e lo dicono anche gli avvisi.

## 5. Primo accesso (interattivo, una volta sola)
```bash
cd ~/radar
set -a; source <(sudo cat /etc/aldostream.env); set +a
.venv/bin/python -m radar.aldostream accedi
```
Chiede il numero (`+39…`), poi il **codice che Telegram manda nell'app** (non per SMS) e, se attiva, la password della verifica
in due passaggi. La sessione viene salvata in `~/.aldostream/aldo.session` con permessi 600. Controllo:
```bash
ls -l ~/.aldostream/        # -rw------- aldo.session
```
La sessione resta solo su questa VM: mai nel repo, nei log, nei backup condivisi. Se la VM viene compromessa o dismessa:
Telegram → Impostazioni → Dispositivi → terminare la sessione `radar-aldo`.

## 6. Prova a mano (nessun messaggio inviato)
```bash
.venv/bin/python -m radar.aldostream canali     # trova l'id del canale
.venv/bin/python -m radar.aldostream prova      # sessione, canale, specifiche e prezzo Bitget, bot
```
Atteso: `canale: Aldo Qefalia - Trading · ultimo messaggio …`, `Bitget BTCUSDT: {'sizeMultiplier': '0.0001', …} · prezzo …`,
`bot: <username del bot>`.

## 7. Servizio permanente (systemd)
```bash
sudo cp ~/radar/deploy/aldostream.service /etc/systemd/system/aldostream.service
# se l'utente non è "ubuntu" o il repo è altrove, correggere User, WorkingDirectory ed ExecStart nel file
sudo systemctl daemon-reload
sudo systemctl enable --now aldostream
systemctl status aldostream
journalctl -u aldostream -f          # log dal vivo (Ctrl+C per uscire)
```
Atteso nel log: `avvisi spenti (solo registrati), pulsanti sì, modalità importo, …` e `in ascolto (ultimo messaggio N)`.
All'avvio recupera i messaggi arrivati mentre era fermo (solo registro: nessun avviso per messaggi più vecchi di 24 ore).
Se la connessione cade riprova da solo (attesa 5 s → 5 min); se Telegram chiede di aspettare (FloodWait) aspetta il tempo
indicato. Il servizio si riavvia da solo se cade e al riavvio della VM. Ogni ora aggiorna il registro sulla carta con le candele
di Bitget; il lunedì mattina scrive `riepilogo_AAAA-MM-GG.md` della settimana.

## 8. Verifica
- A ogni messaggio di Aldo il log scrive `messaggio N: X eventi, Y avvisi, latenza Z s` (nessun testo del messaggio nel log).
- Con `ALDO_AVVISI=0` gli avvisi restano in `~/aldo-dati/avvisi.json` con stato `proposto`: rileggerli
  (`python3 -c "import json;[print(a['testo'],'\n') for a in json.load(open('/home/ubuntu/aldo-dati/avvisi.json'))[-5:]]"`).
- Approvati i testi: `ALDO_AVVISI=1` in `/etc/aldostream.env` e `sudo systemctl restart aldostream`. Da lì gli avvisi arrivano
  nella chat del bot; «Fatto» e «Salto» finiscono in `~/aldo-dati/reale.json`.
- Latenze: `~/aldo-dati/latenze.jsonl` (una riga per messaggio: ora del messaggio, ricezione, avviso pronto, secondi).

## Cosa resta sulla VM (`ALDO_DATI`)
`messaggi.json` e `foto/` (contenuti del canale), `eventi.json` (eventi e piani estratti), `operazioni.json` (registro sulla
carta, senza testi), `avvisi.json`, `reale.json` (pulsanti), `latenze.jsonl`, `sezione.json` (riepilogo privato per la dashboard,
senza testi), `riepilogo_*.md`, `prezzi/` e `bitget_contratti.json` (cache). Nulla di questo va nel repo o nel sito pubblico; la
sezione "Aldo" nella dashboard resta spenta (`ALDO_SEZIONE_PUBBLICA=0`).

## Manutenzione
- Aggiornare il codice: `cd ~/radar && git pull && sudo systemctl restart aldostream`.
- Spazio: le foto pesano circa 100–300 KB l'una; controllare ogni tanto `du -sh ~/aldo-dati`.
- Spegnere tutto: `sudo systemctl disable --now aldostream`. Revocare l'accesso: Telegram → Dispositivi → terminare la sessione;
  su my.telegram.org si può anche eliminare l'app.
- Sicurezza: `/etc/aldostream.env` e la sessione con permessi 600; nessuna porta aperta oltre a SSH; aggiornamenti automatici
  (`sudo apt -y install unattended-upgrades`).
