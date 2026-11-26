## X0 sintesi

| Domanda | Risposta |
|---|---|
| W3.2 funziona su altre monete? | Su ETH sì (+23% annuo dal 2021, drawdown −27,5%); su SOL meno (+17%, −40%); su INJ +33% ma con soli tre anni e drawdown −45%. Su TAO e DOGE no: TAO −36% (1 operazione su 12 in guadagno, dal 2025), DOGE −4% |
| Conviene un portafoglio di più monete? | Riduce poco il drawdown (BTC −21%, BTC + ETH −20%, BTC + ETH + SOL −19%) e abbassa il rendimento: BTC da solo resta il migliore |
| Nel periodo del canale? | W3.2: BTC ×1,94, ETH ×1,95, SOL ×2,57, DOGE ×1,32. Aldo, prezzi delle sue schermate e rischio 2%: ×5,1. Chi lo copiava con ordini limite: ×1,8 |
| La strategia AE? | Batte ingressi casuali (+0,33 contro −0,06 volte il rischio), ma non in modo significativo e quasi solo nel 2020–2021. Nel periodo del canale +21% (BTC, ETH, SOL, TAO, rischio 1%) |
| Posso collegarti al canale? | Non in modo diretto. Le strade sono l'inoltro dei post al bot di radar (consigliato), un client automatico con il tuo account, oppure esportazioni periodiche |
| Lo strumento per seguire Aldo? | Pronto come pacchetto per radar: legge i post (export, inoltro o client automatico), estrae operazioni e livelli, ricostruisce i risultati sui prezzi reali e propone gli ordini limite da mettere |

## A0 strumento

Pacchetto pronto per radar in `export/radar-aldo/` (prompt da incollare, modulo `aldo.py`, 44 test che passano, anteprime).

| Pezzo | Cosa fa |
|---|---|
| Ingresso | Tre modi nello stesso formato: export di Telegram Desktop; post inoltrati al bot di radar (consigliato, nessuna credenziale in più); client automatico Telethon, spento di default |
| Estrazione | Regole in italiano sempre attive ("short", "chiuso metà", "stop a pareggio", livelli come 27,6k); in più, se c'è la chiave dell'API, un modello (Claude Haiku) che legge anche le schermate. Le sole regole ritrovano circa un terzo degli eventi: molti prezzi sono solo nelle immagini |
| Ricostruzione | Stesso motore di questo studio, sui prezzi reali di OKX: trader, chi copia a mercato, chi copia con ordini limite. Sullo storico riproduce i numeri dello studio (55 operazioni e 73% per il trader; 43 e 58% con ordini limite) |
| Dashboard | Sezione "Aldo": livelli da mettere a ordine limite (con quantità a rischio 1%), posizioni aperte, operazioni chiuse, statistiche, nessun testo del canale |
| Avvisi | Proposti ma spenti finché non approvi il testo: nuovo livello da mettere a limite, metà chiusa, stop a pareggio |
| Riepilogo | Un file settimanale in markdown, da passare a una sessione di analisi |

Due cautele scritte nel prompt: il canale è privato e a pagamento, quindi i livelli non vanno pubblicati se il sito di radar è
pubblico; i messaggi e la sessione di Telethon restano fuori dal repository.
