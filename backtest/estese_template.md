# Strategie estese: W3.2 su altre monete, strategia AE (Aldo + Eliz), come seguire Aldo

Tre lavori, con il periodo del canale (12/05/2023 – 18/03/2024) come riferimento, come richiesto, e lo storico più lungo
per verificare che i risultati non dipendano solo da quei dieci mesi.

> Ricerca su dati storici, non una raccomandazione d'investimento.

## 1. Sintesi

**W3.2 si estende bene: con lo stesso codice del radar funziona anche su ETH, SOL e altre monete, e un portafoglio di più
monete riduce il drawdown. La mia strategia AE (presa di liquidità su livelli di 10 giorni nel trend di BTC, gestione alla Aldo)
è la prima regola di tutta la ricerca che batte ingressi casuali, ma rende poco e quasi solo nel 2020–2021. Per seguire Aldo
serve uno strumento: non posso collegarmi io al canale.**

{{X0}}

## 2. W3.2 estesa ad altre monete

Stesse regole e stesso codice del radar (`radar/weekly.py`), con i dati della moneta: prezzi spot Binance, flusso del perp
calcolato come in `radar/features.py` (acquisti aggressivi meno vendite aggressive sul perp, 14 giorni, z-score a 180 giorni) e
funding del perp. Backtest dal 2021, o da quando la moneta ha abbastanza storia (40 settimane per la media).

{{X1}}

Il controllo su BTC conferma che i dati pubblici danno lo stesso risultato del radar.

{{X2}}

{{X3}}

## 3. La strategia AE (Aldo + Eliz)

Costruita sulle lezioni delle prove precedenti: l'intraday perde per i costi, il trend settimanale di BTC funziona, le prese di
liquidità sono il setup migliore di Aldo, il rientro dopo la deviazione è l'idea di Eliz.

**Regole** (fissate prima dei risultati):

1. **Trend di BTC, settimanale** (come W3.2, senza flusso): long ammessi se BTC chiude sopra la media a 40 settimane con la
   EMA 20 in salita; short ammessi nel caso opposto. È il "long sulle alt finché BTC regge" di Aldo.
2. **Trend della moneta**: chiusura giornaliera sopra (long) o sotto (short) la sua EMA 50.
3. **Livello**: minimo (massimo) dei 10 giorni che finiscono 24 ore prima. È l'estremo del range di Eliz e il "pool di
   liquidità" di Aldo.
4. **Ingresso**: il prezzo scende sotto il livello di almeno lo 0,2% e una chiusura oraria torna sopra entro 8 ore → long
   all'ora successiva. Specchio per gli short.
5. **Stop** sotto il minimo della deviazione (−0,3%).
6. **Gestione alla Aldo**: metà a +2 volte il rischio, stop a pareggio; il resto esce alla prima chiusura giornaliera sotto la
   EMA 20 (si lascia correre il trend). Massimo 30 giorni.
7. **Rischio** 1% del capitale per operazione (variante 2%); al massimo 4 posizioni insieme; costi 0,08% per lato e funding.

{{S1}}

{{S2}}

{{S3}}

**Lettura onesta:**

- **Batte il caso**: +0,33 volte il rischio per operazione contro −0,06 di ingressi casuali con la stessa gestione. È la prima
  regola di tutta la ricerca che lo fa.
- **Ma non è solida**: t-stat 1,3 (non significativo), le 10 operazioni migliori valgono più del risultato totale, e dal 2022 è
  vicina a zero. Il guadagno viene dal 2020–2021.
- **Gli short perdono** (−0,11 volte il rischio), i long guadagnano (+0,51): coerente con Aldo, che dal 2024 non fa più short.
- **Rende molto meno di W3.2** in ogni periodo, anche in quello del canale (+21% contro +94%).
- **Livelli più corti (5 giorni) fanno un po' meglio**, quelli più lunghi (20 giorni) peggio: la regola non dipende da una
  scelta fortunata del 10, ma non va nemmeno ottimizzata sul passato.

Se la si usa, la versione sensata è **solo long, come complemento a W3.2 sulle altcoin**, con rischio piccolo. Da tenere in prova
sulla carta prima.

## 4. Seguire Aldo

### Posso collegarmi io al canale?

No, non in modo diretto. Questa sessione non ha accesso a Telegram e non deve usare il tuo account. Le strade sono tre:

| Modo | Come funziona | Pro | Contro |
|---|---|---|---|
| **Inoltro al bot di radar** (consigliato) | Inoltri i post di Aldo al bot di radar che già usi; radar li legge con la data originale | Nessuna credenziale in più, nessun rischio per il tuo account | Serve il gesto manuale dell'inoltro |
| **Client automatico (Telethon)** | radar legge il canale con il tuo account, tramite le chiavi personali di my.telegram.org | Tutto automatico, in tempo reale | È il tuo account personale: Telegram può limitare gli account automatizzati; la sessione va custodita sul server di radar |
| **Esportazione periodica** | Ogni tanto esporti il canale e lo carichi | Nessuna configurazione | Niente tempo reale |

Un bot normale non può leggere il canale: Telegram lo permette solo agli amministratori.

### Lo strumento ad hoc

{{A0}}

## 5. Cosa farei

1. **Portare W3.2 su ETH e SOL in radar** (ETH c'è già), con una quota di capitale per moneta. È l'estensione con il miglior
   rapporto fra risultato e solidità.
2. **Seguire Aldo con lo strumento**, in modalità inoltro e solo sulla carta per qualche settimana: misura il ritardo reale e
   quanto rende copiarlo con ordini limite, prima di metterci soldi.
3. **La strategia AE**, solo long sulle altcoin, sulla carta, come terzo pezzo.

Codice: `backtest/w32_estesa.py`, `backtest/fetch_w32_estesa.py`, `backtest/strategia_ae.py`. Risultati: `results/w32_estesa/`,
`results/strategia_ae/`. Strumento: `export/radar-aldo/`.
