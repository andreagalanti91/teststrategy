# Aldo: tutte le operazioni ricostruite in dettaglio, ed esempio con 10.000 €

Le 55 operazioni a leva del canale (12/05/2023 – 18/03/2024), **ricostruite una seconda volta messaggio per messaggio e
schermata per schermata**, poi controllate sui prezzi reali (candele orarie Binance). Per ognuna: quanto ha fatto Aldo con i
suoi prezzi, quanto chi lo copiava con ordini limite sui livelli annunciati, quanto chi lo copiava a mercato dopo il messaggio.

> Ricerca su dati storici, non una raccomandazione d'investimento.

## 1. I dati sono affidabili? Cosa è cambiato con la revisione

**Sì, con una riserva.** I prezzi sono veri: quasi tutti i prezzi delle sue schermate sono stati toccati davvero dal mercato
poco prima del messaggio, e il ROI di ogni schermata torna con leva × movimento del prezzo.

{{V1}}

La prima ricostruzione però aveva un **errore sistematico**: quando Aldo aumentava una posizione, la schermata mostrava il
**prezzo medio** dopo l'aumento, e lo avevo registrato come prezzo della nuova tranche. Il medio risultava sbagliato e
l'esito sottostimato. Corrette anche alcune uscite (B07 aveva due uscite in profitto, non una in perdita), date d'ingresso
reali (C01, C03, C08) e un'operazione Bitget separata (B25).

{{R1}}

**La riserva.** Le operazioni si dividono per qualità dei dati:

{{R2}}

Le 14 operazioni ricostruite con affidabilità **bassa** sono **tutte vincenti**: 8 sono ingressi che Aldo comunica solo dopo,
a cose fatte; nelle altre 6 manca un prezzo (quasi sempre un'uscita) ed è stato ricostruito. Chi racconta un'operazione a posteriori tende a
raccontare più spesso quelle andate bene, e un'uscita dedotta può essere più favorevole di quella reale. Il dato
più onesto sulla sua bravura è quello delle 29 operazioni con dati completi: **69% vinte, +2,5% medio sul controvalore**.
Resta un risultato molto buono, ma più basso del totale. Per chi copia, comunque, le operazioni comunicate dopo non contano:
non si potevano copiare.

## 2. In sintesi

{{O2}}

- **Aldo vince 3 operazioni su 4** (prima stima 73%, ora 76%), e quando perde perde poco (−0,8% medio sul controvalore). Le
  vincenti valgono in media sei volte le perdenti.
- **Chi lo copia vince meno spesso**: 66% con ordini limite sui livelli annunciati, 58% a mercato dopo il messaggio. Alcune
  operazioni vincenti per lui diventano piccole perdite per chi entra dopo e a un prezzo peggiore.

## 3. Esempio con 10.000 € di capitale

{{O3}}

**Come leggerla, con 1.000 € di margine per operazione:**
- a **5x** chi copiava con ordini limite chiude a 15.100 € (+51%; prima stima 14.600 €); a mercato a 13.400 € (+34%); Aldo con i
  suoi prezzi a 20.200 €;
- a **10x**, la leva tipica di Aldo, tutto raddoppia: +102% con ordini limite, ma la perdita peggiore sale a −444 € e il calo
  massimo del capitale al −7,6% sulle chiusure;
- con **500 €** a operazione e 5x: +26% con ordini limite, +17% a mercato;
- margine fisso, quindi niente interesse composto.

**Attenzione alla leva 10x**: un movimento contrario del 10% azzera il margine. Nessuna operazione copiata ha perso più del
4,4% sul controvalore alla chiusura, ma dentro le operazioni il prezzo può essersi mosso di più. Con lo stop sempre impostato il
rischio è sotto controllo; senza stop, a 10x, no.

## 4. Tutte le operazioni

«Prima stima» è l'esito della prima ricostruzione, «Affidabilità» la qualità dei dati (vedi sopra). A22 (short BTC del
26/07/2023) è stata tolta: la chiusura non è mai dichiarata e il prezzo d'uscita è ignoto. C11 (long BTC del 17/03/2024) era
ancora aperta a fine export ed è valutata all'ultimo prezzo.

{{O1}}

## 5. In euro, operazione per operazione

{{O4}}

## 6. Schede: ogni evento di ogni operazione

Per ogni operazione: ogni messaggio che la muove (apertura, aumenti, chiusure, stop), con prezzo, quota della posizione piena
mossa in quell'evento, fonte (schermata Bybit/Bitget, grafico, testo, dedotto dai prezzi di mercato) e affidabilità. I testi
dei messaggi non sono riportati: il canale è privato.

{{R3}}

## 7. Da ora: come lavoriamo sui suoi nuovi post

1. Mi giri lo screenshot del messaggio (e della schermata di Bybit o del grafico se c'è), con l'ora in cui l'hai visto.
2. Ti rispondo con: cosa ha fatto o annunciato Aldo, se è copiabile e come (ordine limite o a mercato, livello, stop, obiettivo
   per chiudere metà), dimensione per 500–1.000 € di margine con leva 5x, quanto perdi allo stop, e un mio parere sul setup
   (contesto di BTC, livelli, W3.2).
3. Registro ogni operazione in `results/aldo_live/registro.csv`. Ogni tanto ti faccio il punto con le stesse tabelle.

Nota: `TELEGRAM_ALDO.md` e `CONFRONTO_FINALE.md` usano ancora la prima ricostruzione. Le conclusioni non cambiano (con la
revisione i numeri di Aldo e di chi lo copia salgono di poco).

Codice: `backtest/telegram_ricostruzione.py`, `backtest/telegram_verifica.py`, `backtest/aldo_operazioni.py` (con
`TELEGRAM_REVISIONE=1`). Dati: `results/telegram_rev/`.
