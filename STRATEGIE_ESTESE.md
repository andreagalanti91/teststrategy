# Strategie estese: W3.2 su altre monete, strategia AE (Aldo + Eliz), come seguire Aldo

Tre lavori, con il periodo del canale (12/05/2023 – 18/03/2024) come riferimento, come richiesto, e lo storico più lungo
per verificare che i risultati non dipendano solo da quei dieci mesi.

> Ricerca su dati storici, non una raccomandazione d'investimento.

## 1. Sintesi

**W3.2 si estende solo in parte: con lo stesso codice del radar funziona su ETH, meno su SOL, e non funziona su TAO e DOGE.
BTC da solo resta la versione migliore; aggiungere monete abbassa il rendimento più di quanto riduca il drawdown. La mia strategia AE (presa di liquidità su livelli di 10 giorni nel trend di BTC, gestione alla Aldo)
è la prima regola di tutta la ricerca che batte ingressi casuali, ma rende poco e quasi solo nel 2020–2021. Per seguire Aldo
serve uno strumento: non posso collegarmi io al canale.**

| Domanda | Risposta |
|---|---|
| W3.2 funziona su altre monete? | Su ETH sì (+23% annuo dal 2021, drawdown −27,5%); su SOL meno (+17%, −40%); su INJ +33% ma con soli tre anni e drawdown −45%. Su TAO e DOGE no: TAO −36% (1 operazione su 12 in guadagno, dal 2025), DOGE −4% |
| Conviene un portafoglio di più monete? | Riduce poco il drawdown (BTC −21%, BTC + ETH −20%, BTC + ETH + SOL −19%) e abbassa il rendimento: BTC da solo resta il migliore |
| Nel periodo del canale? | W3.2: BTC ×1,94, ETH ×1,95, SOL ×2,57, DOGE ×1,32. Aldo, prezzi delle sue schermate e rischio 2%: ×5,1. Chi lo copiava con ordini limite: ×1,8 |
| La strategia AE? | Batte ingressi casuali (+0,33 contro −0,06 volte il rischio), ma non in modo significativo e quasi solo nel 2020–2021. Nel periodo del canale +21% (BTC, ETH, SOL, TAO, rischio 1%) |
| Posso collegarti al canale? | Non in modo diretto. Le strade sono l'inoltro dei post al bot di radar (consigliato), un client automatico con il tuo account, oppure esportazioni periodiche |
| Lo strumento per seguire Aldo? | Pronto come pacchetto per radar: legge i post (export, inoltro o client automatico), estrae operazioni e livelli, ricostruisce i risultati sui prezzi reali e propone gli ordini limite da mettere |

## 2. W3.2 estesa ad altre monete

Stesse regole e stesso codice del radar (`radar/weekly.py`), con i dati della moneta: prezzi spot Binance, flusso del perp
calcolato come in `radar/features.py` (acquisti aggressivi meno vendite aggressive sul perp, 14 giorni, z-score a 180 giorni) e
funding del perp. Backtest dal 2021, o da quando la moneta ha abbastanza storia (40 settimane per la media).

| Moneta | Backtest dal | Operazioni | In guadagno | 10.000 $ → | CAGR | Max DD | Comprata e tenuta, stesso periodo: CAGR / DD |
|---|---|---|---|---|---|---|---|
| BTC | 2021-01-17 | 13 | 92% | 81.503 | +43,7% | -21,1% | +14,3% / -76,6% |
| ETH | 2021-01-17 | 14 | 57% | 33.634 | +23,3% | -27,5% | +11,0% / -79,3% |
| SOL | 2021-10-01 | 19 | 37% | 22.136 | +16,9% | -39,8% | -9,8% / -96,3% |
| TAO | 2025-04-28 | 12 | 8% | 5.044 | -36,5% | -50,0% | -26,6% / -70,7% |
| INJ | 2023-09-03 | 14 | 36% | 24.769 | +33,3% | -44,7% | +1,9% / -94,7% |
| DOGE | 2021-07-27 | 25 | 24% | 7.932 | -4,3% | -53,9% | -17,3% / -85,2% |

Controllo su BTC: con gli archivi pubblici W3.2 fa ×8,2 dal 2021-01-17; il radar, con le sue serie, ×8,2. Correlazione dei rendimenti giornalieri 1,00.

Il controllo su BTC conferma che i dati pubblici danno lo stesso risultato del radar.

- **ETH**: funziona, con metà del rendimento di BTC e drawdown simile.
- **SOL e INJ**: positivi ma con drawdown del 40–45% e storia corta; nel 2024–2026 entrambi in perdita.
- **TAO e DOGE**: la regola non funziona. TAO ha solo un anno e mezzo di segnali (serve storia per la media a 40 settimane) e
  una sola operazione in guadagno su 12: va molto in su e in giù senza trend settimanali puliti.

| Moneta | Periodo del canale: 10.000 $ → | DD | 2024–2026: 10.000 $ → | DD |
|---|---|---|---|---|
| BTC | 19.371 | -16,8% | 24.395 | -21,1% |
| ETH | 19.456 | -13,7% | 14.108 | -27,5% |
| SOL | 25.653 | -26,6% | 7.991 | -39,7% |
| TAO | n/d (dati insufficienti) | – | 5.044 | -50,0% |
| INJ | n/d (dati insufficienti) | – | 7.824 | -35,4% |
| DOGE | 13.156 | -30,0% | 14.053 | -53,9% |

| Portafoglio (parti uguali, ribilanciato ogni giorno) | Dal | 10.000 $ → | CAGR | Max DD |
|---|---|---|---|---|
| BTC | 2021-01-18 | 81.503 | +43,7% | -21,1% |
| BTC + ETH | 2021-01-18 | 56.400 | +34,9% | -19,6% |
| BTC + ETH + SOL | 2021-10-02 | 29.108 | +23,4% | -18,8% |
| BTC + ETH + SOL + TAO | 2025-04-29 | 8.954 | -7,1% | -19,8% |

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

| Periodo | Versione | 10.000 $ → | CAGR | Max DD | Operazioni | In guadagno | Medio in R |
|---|---|---|---|---|---|---|---|
| Periodo del canale (12/05/2023–18/03/2024) | BTC, ETH, SOL, TAO, rischio 1% | 12.072 | +24,8% | -11,5% | 40 | 32% | 0,61 |
| Periodo del canale (12/05/2023–18/03/2024) | solo BTC, rischio 1% | 9.892 | -1,3% | -4,0% | 5 | 40% | -0,23 |
| Periodo del canale (12/05/2023–18/03/2024) | BTC, ETH, SOL, TAO, rischio 2% | 13.366 | +40,6% | -21,7% | 40 | 32% | 0,61 |
| Periodo del canale (12/05/2023–18/03/2024) | solo BTC, rischio 2% | 9.789 | -2,5% | -7,7% | 5 | 40% | -0,23 |
| Periodo del canale (12/05/2023–18/03/2024) | W3.2 (riferimento) | 19.371 | +117,4% | -16,8% | – | – | – |
| Periodo del canale (12/05/2023–18/03/2024) | BTC comprato e tenuto (riferimento) | 25.232 | +196,5% | -20,0% | – | – | – |
| 2020–2022 | BTC, ETH, SOL, TAO, rischio 1% | 21.057 | +28,2% | -24,5% | 137 | 31% | 0,67 |
| 2020–2022 | solo BTC, rischio 1% | 13.846 | +11,5% | -14,3% | 48 | 33% | 0,86 |
| 2020–2022 | BTC, ETH, SOL, TAO, rischio 2% | 34.287 | +50,8% | -43,7% | 137 | 31% | 0,67 |
| 2020–2022 | solo BTC, rischio 2% | 17.112 | +19,6% | -26,9% | 48 | 33% | 0,86 |
| 2020–2022 | W3.2 (riferimento) | 45.009 | +65,1% | -23,3% | – | – | – |
| 2020–2022 | BTC comprato e tenuto (riferimento) | 23.076 | +32,1% | -76,6% | – | – | – |
| 2023–2026 | BTC, ETH, SOL, TAO, rischio 1% | 9.743 | -0,7% | -19,9% | 202 | 32% | 0,03 |
| 2023–2026 | solo BTC, rischio 1% | 8.353 | -4,6% | -17,5% | 66 | 33% | -0,26 |
| 2023–2026 | BTC, ETH, SOL, TAO, rischio 2% | 8.335 | -4,6% | -36,3% | 202 | 32% | 0,03 |
| 2023–2026 | solo BTC, rischio 2% | 6.938 | -9,1% | -32,3% | 66 | 33% | -0,26 |
| 2023–2026 | W3.2 (riferimento) | 35.979 | +39,7% | -21,1% | – | – | – |
| 2023–2026 | BTC comprato e tenuto (riferimento) | 47.154 | +49,9% | -53,0% | – | – | – |
| Tutto (2020–2026) | BTC, ETH, SOL, TAO, rischio 1% | 20.297 | +10,9% | -35,5% | 339 | 32% | 0,29 |
| Tutto (2020–2026) | solo BTC, rischio 1% | 11.565 | +2,2% | -29,3% | 114 | 33% | 0,21 |
| Tutto (2020–2026) | BTC, ETH, SOL, TAO, rischio 2% | 28.015 | +16,3% | -59,1% | 339 | 32% | 0,29 |
| Tutto (2020–2026) | solo BTC, rischio 2% | 11.872 | +2,5% | -50,5% | 114 | 33% | 0,21 |
| Tutto (2020–2026) | W3.2 (riferimento) | 161.939 | +50,3% | -23,3% | – | – | – |
| Tutto (2020–2026) | BTC comprato e tenuto (riferimento) | 108.812 | +41,8% | -76,6% | – | – | – |

| Asset | Dati dal | Operazioni | Per anno | Long / short | In guadagno | Medio in R | Medio per operazione | Nel periodo del canale: operazioni, medio in R |
|---|---|---|---|---|---|---|---|---|
| BTC | 01/2018 | 130 | 14,7 | 83 / 47 | 31% | 0,26 | +0,19% | 5, -0,23 |
| ETH | 01/2018 | 101 | 11,4 | 62 / 39 | 33% | 0,41 | +1,37% | 8, -0,19 |
| SOL | 08/2020 | 95 | 15,3 | 54 / 41 | 28% | 0,56 | +2,22% | 14, 2,42 |
| TAO | 03/2023 | 41 | 11,4 | 32 / 9 | 32% | -0,18 | -1,17% | 13, -0,51 |

| Giorni del livello | Primo obiettivo (volte il rischio) | Operazioni (4 asset, 2020–2026) | Medio in R | 10.000 $ → con rischio 1% (2020–2026) | Periodo del canale: 10.000 $ → |
|---|---|---|---|---|---|
| 5 | 1,5 | 566 | 0,30 | 35.066 | 16.676 |
| 5 | 2,0 | 543 | 0,32 | 36.544 | 16.635 |
| 5 | 3,0 | 514 | 0,39 | 40.811 | 18.870 |
| 10 | 1,5 | 342 | 0,29 | 20.367 | 12.814 |
| 10 | 2,0 | 339 | 0,29 | 20.297 | 12.072 |
| 10 | 3,0 | 335 | 0,32 | 21.365 | 14.769 |
| 20 | 1,5 | 108 | -0,01 | 9.745 | 9.818 |
| 20 | 2,0 | 108 | 0,10 | 10.917 | 9.868 |
| 20 | 3,0 | 105 | -0,00 | 9.717 | 9.371 |

Controllo: stessi stop e stessa gestione, ingressi spostati a caso di ±10 giorni rispetto ai segnali (1069 prove): medio -0,06 R, contro 0,33 R della regola.

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

In preparazione.

## 5. Cosa farei

1. **W3.2 su BTC resta la base.** ETH come seconda moneta va bene (radar lo ha già); SOL solo con una quota piccola; TAO e DOGE
   no: lì la regola settimanale non ha funzionato.
2. **Seguire Aldo con lo strumento**, in modalità inoltro e solo sulla carta per qualche settimana: misura il ritardo reale e
   quanto rende copiarlo con ordini limite, prima di metterci soldi.
3. **La strategia AE**, solo long sulle altcoin, sulla carta, come terzo pezzo.

Codice: `backtest/w32_estesa.py`, `backtest/fetch_w32_estesa.py`, `backtest/strategia_ae.py`. Risultati: `results/w32_estesa/`,
`results/strategia_ae/`. Strumento: `export/radar-aldo/`.
