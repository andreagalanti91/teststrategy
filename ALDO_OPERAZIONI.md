# Aldo: tutte le operazioni ricostruite in dettaglio, ed esempio con 10.000 €

Le 55 operazioni a leva del canale (12/05/2023 – 18/03/2024), **ricostruite una seconda volta messaggio per messaggio e
schermata per schermata**, poi controllate sui prezzi reali (candele orarie Binance). Per ognuna: quanto ha fatto Aldo con i
suoi prezzi, quanto chi lo copiava con ordini limite sui livelli annunciati, quanto chi lo copiava a mercato dopo il messaggio.

> Ricerca su dati storici, non una raccomandazione d'investimento.

## 1. I dati sono affidabili? Cosa è cambiato con la revisione

**Sì, con una riserva.** I prezzi sono veri: quasi tutti i prezzi delle sue schermate sono stati toccati davvero dal mercato
poco prima del messaggio, e il ROI di ogni schermata torna con leva × movimento del prezzo.

| Prezzi dichiarati nelle schermate | Quanti | Toccati davvero dal mercato nelle 72 ore prima del messaggio | Ritardo mediano fra l'ultima volta che il mercato era a quel prezzo e il messaggio | Un quarto oltre |
|---|---|---|---|---|
| Ingressi e aumenti | 68 | 99% | 0,2 ore | 1,8 ore |
| Uscite | 81 | 100% | -0,2 ore | 0,2 ore |

La prima ricostruzione però aveva un **errore sistematico**: quando Aldo aumentava una posizione, la schermata mostrava il
**prezzo medio** dopo l'aumento, e lo avevo registrato come prezzo della nuova tranche. Il medio risultava sbagliato e
l'esito sottostimato. Corrette anche alcune uscite (B07 aveva due uscite in profitto, non una in perdita), date d'ingresso
reali (C01, C03, C08) e un'operazione Bitget separata (B25).

Operazioni il cui esito è cambiato di almeno mezzo punto rispetto alla prima ricostruzione (rendimento di Aldo sul controvalore, dopo i costi).

| Operazione | Asset | Verso | Prima | Adesso | Differenza | Affidabilità |
|---|---|---|---|---|---|---|
| A18 | INJ | long | +5,31% | +10,67% | +5,36% | media |
| B07 | BTC | short | -0,67% | +3,51% | +4,18% | bassa |
| B01 | INJ | long | +1,22% | +4,03% | +2,81% | bassa |
| C01 | BTC | long | +4,23% | +6,31% | +2,08% | bassa |
| A19 | WOO | long | -1,65% | -0,08% | +1,58% | media |
| B20 | ETH | long | -3,85% | -2,64% | +1,22% | media |
| A23 | BTC | long | +1,42% | +2,40% | +0,97% | media |
| A07 | BTC | long | +3,84% | +2,93% | -0,91% | media |
| A15 | BTC | short | -2,07% | -1,41% | +0,66% | media |
| A01 | BTC | short | +0,25% | +0,89% | +0,65% | media |
| A02 | BTC | short | -0,36% | +0,23% | +0,59% | alta |
| B13 | INJ | long | +16,06% | +15,54% | -0,52% | bassa |
| B25 | BTC | long | assente | -0,05% | – | alta |

Operazioni modificate: 13 su 55. Tolte perché non calcolabili (chiusura mai dichiarata, prezzo ignoto): A22.

**La riserva.** Le operazioni si dividono per qualità dei dati:

| Affidabilità della ricostruzione | Operazioni | In guadagno | Medio per operazione |
|---|---|---|---|
| alta | 29 | 69% | +2,47% |
| media | 12 | 67% | +4,16% |
| bassa | 14 | 100% | +5,87% |

Alta: prezzi d'ingresso e d'uscita leggibili nelle schermate, ROI coerente. Media: un prezzo ricavato (medio, stima su dati di mercato). Bassa: un ingresso o un'uscita mai dichiarati, ricostruiti.

Le 14 operazioni ricostruite con affidabilità **bassa** sono **tutte vincenti**: 8 sono ingressi che Aldo comunica solo dopo,
a cose fatte; nelle altre 6 manca un prezzo (quasi sempre un'uscita) ed è stato ricostruito. Chi racconta un'operazione a posteriori tende a
raccontare più spesso quelle andate bene, e un'uscita dedotta può essere più favorevole di quella reale. Il dato
più onesto sulla sua bravura è quello delle 29 operazioni con dati completi: **69% vinte, +2,5% medio sul controvalore**.
Resta un risultato molto buono, ma più basso del totale. Per chi copia, comunque, le operazioni comunicate dopo non contano:
non si potevano copiare.

## 2. In sintesi

| Chi | Operazioni | Vinte | Perse | % vinte | Guadagno medio delle vinte | Perdita media delle perse | Migliore | Peggiore |
|---|---|---|---|---|---|---|---|---|
| Aldo, prezzi suoi | 55 | 42 | 13 | 76% | +5,11% | -0,83% | +29,4% | -2,6% |
| Copia con ordini limite | 44 | 29 | 15 | 66% | +4,09% | -1,07% | +29,5% | -4,4% |
| Copia a mercato | 43 | 25 | 18 | 58% | +3,44% | -0,95% | +29,5% | -4,4% |

Percentuali sul controvalore (movimento del prezzo). Sul margine vanno moltiplicate per la leva.

- **Aldo vince 3 operazioni su 4** (prima stima 73%, ora 76%), e quando perde perde poco (−0,8% medio sul controvalore). Le
  vincenti valgono in media sei volte le perdenti.
- **Chi lo copia vince meno spesso**: 66% con ordini limite sui livelli annunciati, 58% a mercato dopo il messaggio. Alcune
  operazioni vincenti per lui diventano piccole perdite per chi entra dopo e a un prezzo peggiore.

## 3. Esempio con 10.000 € di capitale

Capitale iniziale 10.000 €, un margine fisso per operazione, tutte le operazioni in sequenza (12/05/2023 – 18/03/2024).

| Chi copia | Margine per operazione | Leva | Capitale finale | Guadagno | Operazione migliore | Operazione peggiore | Peggior calo del capitale | Operazioni |
|---|---|---|---|---|---|---|---|---|
| Aldo, prezzi suoi (riferimento) | 500 € | 5x | 15.092 € | +51% | +735 € | −66 € | -0,5% | 55 |
| Aldo, prezzi suoi (riferimento) | 500 € | 10x | 20.185 € | +102% | +1.470 € | −132 € | -0,9% | 55 |
| Aldo, prezzi suoi (riferimento) | 1.000 € | 5x | 20.185 € | +102% | +1.470 € | −132 € | -0,9% | 55 |
| Aldo, prezzi suoi (riferimento) | 1.000 € | 10x | 30.370 € | +204% | +2.940 € | −264 € | -1,6% | 55 |
| Copia con ordini limite | 500 € | 5x | 12.561 € | +26% | +736 € | −111 € | -1,9% | 44 |
| Copia con ordini limite | 500 € | 10x | 15.122 € | +51% | +1.473 € | −222 € | -3,8% | 44 |
| Copia con ordini limite | 1.000 € | 5x | 15.122 € | +51% | +1.473 € | −222 € | -3,8% | 44 |
| Copia con ordini limite | 1.000 € | 10x | 20.244 € | +102% | +2.945 € | −444 € | -7,6% | 44 |
| Copia a mercato | 500 € | 5x | 11.721 € | +17% | +736 € | −111 € | -1,7% | 43 |
| Copia a mercato | 500 € | 10x | 13.441 € | +34% | +1.473 € | −222 € | -3,3% | 43 |
| Copia a mercato | 1.000 € | 5x | 13.441 € | +34% | +1.473 € | −222 € | -3,3% | 43 |
| Copia a mercato | 1.000 € | 10x | 16.883 € | +69% | +2.945 € | −444 € | -6,6% | 43 |

Il calo del capitale è misurato alla chiusura delle operazioni: dentro un'operazione la perdita latente può essere maggiore.

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

Rendimento sul controvalore, dopo i costi. Con leva 10x l'effetto sul margine è dieci volte tanto (colonna «Sul margine a 10x»).

| # | Operazione | Asset | Verso | Apertura | Durata | Aldo | Esito | Sul margine a 10x | Prima stima | Affidabilità | Copia con ordini limite | Copia a mercato | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | A01 | BTC | short | 14/05/23 | 2 giorni | +0,89% | ✅ | +8,9% | +0,25% | media | +0,65% | +0,02% |  |
| 2 | A02 | BTC | short | 28/05/23 | 39 ore | +0,23% | ✅ | +2,3% | -0,36% | alta | -0,58% | -0,60% |  |
| 3 | A03 | BTC | long | 03/06/23 | 2 giorni | -1,58% | ❌ | -15,8% | -1,58% | alta | -4,44% | -4,44% |  |
| 4 | A05 | BTC | short | 07/06/23 | 1 ore | +2,08% | ✅ | +20,8% | +2,08% | alta | non copiabile | non copiabile | comunicata dopo l'ingresso |
| 5 | A06 | MATIC | short | 13/06/23 | 2 ore | +2,56% | ✅ | +25,6% | +2,56% | alta | +1,34% | +1,34% |  |
| 6 | A07 | BTC | long | 16/06/23 | 6 ore | +2,93% | ✅ | +29,3% | +3,84% | media | +1,85% | +1,61% |  |
| 7 | A08 | BTC | short | 20/06/23 | 1 ore | -1,25% | ❌ | -12,5% | -1,25% | alta | -1,61% | -0,16% |  |
| 8 | A09 | BTC | short | 28/06/23 | 5 giorni | +2,54% | ✅ | +25,4% | +2,08% | bassa | +1,24% | +1,05% |  |
| 9 | A10 | INJ | long | 01/07/23 | 5 giorni | +5,27% | ✅ | +52,7% | +5,27% | bassa | non copiabile | non copiabile | comunicata dopo l'ingresso |
| 10 | A11 | FET | long | 01/07/23 | 5 giorni | +4,27% | ✅ | +42,7% | +4,27% | bassa | non copiabile | non copiabile | comunicata dopo l'ingresso |
| 11 | A12 | WOO | long | 01/07/23 | 5 giorni | +9,22% | ✅ | +92,2% | +9,22% | bassa | non copiabile | non copiabile | comunicata dopo l'ingresso |
| 12 | A13 | BTC | short | 05/07/23 | 22 ore | -0,09% | ❌ | -0,9% | -0,16% | alta | non copiabile | non copiabile | comunicata dopo l'ingresso |
| 13 | A15 | BTC | short | 13/07/23 | 9 ore | -1,41% | ❌ | -14,1% | -2,07% | media | -2,08% | -2,08% |  |
| 14 | A17 | INJ | long | 13/07/23 | 0 ore | +0,98% | ✅ | +9,8% | +0,98% | alta | -0,16% | -0,16% |  |
| 15 | A16 | WOO | long | 13/07/23 | 0 ore | +1,17% | ✅ | +11,7% | +1,17% | alta | -0,16% | -0,16% |  |
| 16 | A18 | INJ | long | 14/07/23 | 12 ore | +10,67% | ✅ | +106,7% | +5,31% | media | +4,46% | +4,46% |  |
| 17 | A19 | WOO | long | 14/07/23 | 6 ore | -0,08% | ❌ | -0,8% | -1,65% | media | -3,03% | -3,03% |  |
| 18 | A20 | BTC | long | 25/07/23 | 16 ore | -0,03% | ❌ | -0,3% | -0,03% | alta | -0,11% | -0,18% |  |
| 19 | A21 | BTC | short | 26/07/23 | 6 giorni | +1,61% | ✅ | +16,1% | +1,34% | bassa | +1,23% | +1,34% |  |
| 20 | A23 | BTC | long | 18/08/23 | 5 giorni | +2,40% | ✅ | +24,0% | +1,42% | media | +1,31% | +0,45% |  |
| 21 | A24 | BTC | long | 29/08/23 | 2 ore | +2,95% | ✅ | +29,5% | +2,95% | alta | +1,69% | +1,69% |  |
| 22 | A25 | BTC | short | 29/08/23 | 46 ore | +4,67% | ✅ | +46,7% | +4,39% | alta | +5,02% | +6,05% |  |
| 23 | B01 | INJ | long | 15/09/23 | 6 giorni | +4,03% | ✅ | +40,3% | +1,22% | bassa | non copiabile | non copiabile | comunicata dopo l'ingresso |
| 24 | B02 | BNB | short | 21/09/23 | 26 ore | +0,94% | ✅ | +9,4% | +0,94% | alta | +0,92% | +0,92% |  |
| 25 | B03 | BTC | long | 22/09/23 | 3 giorni | -1,47% | ❌ | -14,7% | -1,84% | alta | -1,38% | -1,89% |  |
| 26 | B04 | BTC | long | 26/09/23 | 19 ore | +2,08% | ✅ | +20,8% | +2,08% | alta | non copiabile | non copiabile | comunicata dopo l'ingresso |
| 27 | B05 | BTC | short | 28/09/23 | 3 ore | +0,41% | ✅ | +4,1% | +0,41% | alta | +0,21% | -0,31% |  |
| 28 | B06 | BTC | long | 29/09/23 | 3 giorni | +4,29% | ✅ | +42,9% | +4,42% | bassa | +4,70% | non copiabile | comunicata dopo l'ingresso |
| 29 | B07 | BTC | short | 02/10/23 | 31 ore | +3,51% | ✅ | +35,1% | -0,67% | bassa | +3,18% | +2,88% |  |
| 30 | B08 | BTC | short | 09/10/23 | 47 ore | +2,34% | ✅ | +23,4% | +2,34% | bassa | +2,42% | +2,71% |  |
| 31 | B09 | BTC | long | 11/10/23 | 2 giorni | +0,19% | ✅ | +1,9% | -0,17% | media | +0,22% | +0,07% |  |
| 32 | B25 | BTC | long | 11/10/23 | 2 giorni | -0,05% | ❌ | -0,5% | nuova | alta | +0,16% | +0,16% |  |
| 33 | B10 | BTC | short | 18/10/23 | 0 ore | -0,68% | ❌ | -6,8% | -0,68% | alta | -0,16% | -0,16% |  |
| 34 | B11 | BTC | short | 18/10/23 | 21 ore | +0,03% | ✅ | +0,3% | +0,03% | alta | -0,41% | -0,41% |  |
| 35 | B12 | BTC | short | 19/10/23 | 11 ore | -0,87% | ❌ | -8,7% | -1,24% | media | -1,45% | -1,31% |  |
| 36 | B14 | DOGE | long | 23/10/23 | 31 ore | +3,11% | ✅ | +31,1% | +3,11% | alta | +2,07% | +2,07% |  |
| 37 | B13 | INJ | long | 23/10/23 | 22 ore | +15,54% | ✅ | +155,4% | +16,06% | bassa | +9,82% | +9,82% |  |
| 38 | B15 | INJ | long | 27/10/23 | 5 giorni | +13,85% | ✅ | +138,5% | +13,85% | alta | non copiabile | non copiabile | comunicata dopo l'ingresso |
| 39 | B16 | SOL | short | 01/11/23 | 1 ore | +6,54% | ✅ | +65,4% | +6,54% | alta | +6,51% | +4,21% |  |
| 40 | B17 | BTC | short | 02/11/23 | 30 ore | +1,32% | ✅ | +13,2% | +1,32% | alta | +0,41% | +0,41% |  |
| 41 | B18 | INJ | long | 09/11/23 | 7 ore | +0,22% | ✅ | +2,2% | +0,22% | alta | -0,16% | -0,16% |  |
| 42 | B19 | DOGE | long | 09/11/23 | 36 giorni | +29,40% | ✅ | +294,0% | +28,93% | media | +29,45% | +29,45% |  |
| 43 | B20 | ETH | long | 13/11/23 | 22 ore | -2,64% | ❌ | -26,4% | -3,85% | media | -0,16% | -0,16% |  |
| 44 | B21 | BTC | long | 13/11/23 | 0 ore | +0,38% | ✅ | +3,8% | +0,38% | alta | +0,06% | -0,16% |  |
| 45 | B22 | BTC | long | 16/11/23 | 5 giorni | +2,20% | ✅ | +22,0% | +2,20% | alta | +1,74% | +1,05% |  |
| 46 | B23 | BTC | short | 28/11/23 | 9 ore | -0,54% | ❌ | -5,4% | -0,54% | alta | +0,06% | -1,53% |  |
| 47 | B24 | BTC | long | 11/12/23 | 29 ore | +1,58% | ✅ | +15,8% | +1,32% | bassa | +1,26% | +1,00% |  |
| 48 | C01 | BTC | long | 19/12/23 | 13 giorni | +6,31% | ✅ | +63,1% | +4,23% | bassa | non copiabile | non copiabile | comunicata dopo l'ingresso |
| 49 | C02 | BTC | long | 03/01/24 | 6 giorni | +10,39% | ✅ | +103,9% | +10,39% | alta | +5,12% | +2,22% |  |
| 50 | C03 | ETH | long | 10/01/24 | 21 giorni | +6,17% | ✅ | +61,7% | +5,70% | bassa | non copiabile | non copiabile | comunicata dopo l'ingresso |
| 51 | C05 | BTC | long | 22/01/24 | 3 ore | -0,13% | ❌ | -1,3% | -0,13% | alta | -0,16% | -0,16% |  |
| 52 | C06 | INJ | long | 17/02/24 | 40 ore | +4,88% | ✅ | +48,8% | +4,97% | media | +5,40% | +2,39% |  |
| 53 | C07 | INJ | long | 28/02/24 | 6 ore | +21,27% | ✅ | +212,7% | +21,27% | alta | +23,41% | +7,25% |  |
| 54 | C08 | BTC | long | 28/02/24 | 9 giorni | +15,57% | ✅ | +155,7% | +15,57% | bassa | non copiabile | non copiabile | comunicata dopo l'ingresso |
| 55 | C11 | BTC | long | 17/03/24 | 24 ore | +3,54% | ✅ | +35,4% | +3,54% | media | +2,60% | +1,27% |  |

## 5. In euro, operazione per operazione

Lo stesso esempio, operazione per operazione: margine 1.000 €, leva 5x, guadagno o perdita in euro.

| # | Asset | Verso | Apertura | Aldo | Copia con ordini limite | Copia a mercato |
|---|---|---|---|---|---|---|
| 1 | BTC | short | 14/05/23 | +45 € | +32 € | +1 € |
| 2 | BTC | short | 28/05/23 | +12 € | −29 € | −30 € |
| 3 | BTC | long | 03/06/23 | −79 € | −222 € | −222 € |
| 4 | BTC | short | 07/06/23 | +104 € | – | – |
| 5 | MATIC | short | 13/06/23 | +128 € | +67 € | +67 € |
| 6 | BTC | long | 16/06/23 | +146 € | +92 € | +81 € |
| 7 | BTC | short | 20/06/23 | −63 € | −80 € | −8 € |
| 8 | BTC | short | 28/06/23 | +127 € | +62 € | +53 € |
| 9 | INJ | long | 01/07/23 | +263 € | – | – |
| 10 | FET | long | 01/07/23 | +214 € | – | – |
| 11 | WOO | long | 01/07/23 | +461 € | – | – |
| 12 | BTC | short | 05/07/23 | −5 € | – | – |
| 13 | BTC | short | 13/07/23 | −71 € | −104 € | −104 € |
| 14 | INJ | long | 13/07/23 | +49 € | −8 € | −8 € |
| 15 | WOO | long | 13/07/23 | +59 € | −8 € | −8 € |
| 16 | INJ | long | 14/07/23 | +533 € | +223 € | +223 € |
| 17 | WOO | long | 14/07/23 | −4 € | −151 € | −151 € |
| 18 | BTC | long | 25/07/23 | −2 € | −5 € | −9 € |
| 19 | BTC | short | 26/07/23 | +81 € | +61 € | +67 € |
| 20 | BTC | long | 18/08/23 | +120 € | +66 € | +22 € |
| 21 | BTC | long | 29/08/23 | +148 € | +84 € | +84 € |
| 22 | BTC | short | 29/08/23 | +233 € | +251 € | +303 € |
| 23 | INJ | long | 15/09/23 | +201 € | – | – |
| 24 | BNB | short | 21/09/23 | +47 € | +46 € | +46 € |
| 25 | BTC | long | 22/09/23 | −74 € | −69 € | −95 € |
| 26 | BTC | long | 26/09/23 | +104 € | – | – |
| 27 | BTC | short | 28/09/23 | +21 € | +10 € | −15 € |
| 28 | BTC | long | 29/09/23 | +214 € | +235 € | – |
| 29 | BTC | short | 02/10/23 | +175 € | +159 € | +144 € |
| 30 | BTC | short | 09/10/23 | +117 € | +121 € | +135 € |
| 31 | BTC | long | 11/10/23 | +10 € | +11 € | +4 € |
| 32 | BTC | long | 11/10/23 | −3 € | +8 € | +8 € |
| 33 | BTC | short | 18/10/23 | −34 € | −8 € | −8 € |
| 34 | BTC | short | 18/10/23 | +1 € | −20 € | −20 € |
| 35 | BTC | short | 19/10/23 | −43 € | −73 € | −66 € |
| 36 | DOGE | long | 23/10/23 | +155 € | +103 € | +103 € |
| 37 | INJ | long | 23/10/23 | +777 € | +491 € | +491 € |
| 38 | INJ | long | 27/10/23 | +693 € | – | – |
| 39 | SOL | short | 01/11/23 | +327 € | +325 € | +211 € |
| 40 | BTC | short | 02/11/23 | +66 € | +21 € | +21 € |
| 41 | INJ | long | 09/11/23 | +11 € | −8 € | −8 € |
| 42 | DOGE | long | 09/11/23 | +1.470 € | +1.473 € | +1.473 € |
| 43 | ETH | long | 13/11/23 | −132 € | −8 € | −8 € |
| 44 | BTC | long | 13/11/23 | +19 € | +3 € | −8 € |
| 45 | BTC | long | 16/11/23 | +110 € | +87 € | +52 € |
| 46 | BTC | short | 28/11/23 | −27 € | +3 € | −77 € |
| 47 | BTC | long | 11/12/23 | +79 € | +63 € | +50 € |
| 48 | BTC | long | 19/12/23 | +315 € | – | – |
| 49 | BTC | long | 03/01/24 | +520 € | +256 € | +111 € |
| 50 | ETH | long | 10/01/24 | +308 € | – | – |
| 51 | BTC | long | 22/01/24 | −7 € | −8 € | −8 € |
| 52 | INJ | long | 17/02/24 | +244 € | +270 € | +120 € |
| 53 | INJ | long | 28/02/24 | +1.063 € | +1.170 € | +362 € |
| 54 | BTC | long | 28/02/24 | +779 € | – | – |
| 55 | BTC | long | 17/03/24 | +177 € | +130 € | +64 € |
| | | | **Totale** | **+10.185 €** | **+5.122 €** | **+3.441 €** |

## 6. Schede: ogni evento di ogni operazione

Per ogni operazione: ogni messaggio che la muove (apertura, aumenti, chiusure, stop), con prezzo, quota della posizione piena
mossa in quell'evento, fonte (schermata Bybit/Bitget, grafico, testo, dedotto dai prezzi di mercato) e affidabilità. I testi
dei messaggi non sono riportati: il canale è privato.

**A01 · BTC short** — esito +0,89% (dopo i costi), prezzo medio 27377.6, affidabilità media

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-05-14 20:04 | #175 | apertura | 27187.9 | 0.5 | schermata | alta |
| 2023-05-15 19:48 | #178 | aumento | 27567.3 | 0.5 | schermata | media |
| 2023-05-15 19:48 | #178 | chiusura parziale | 27377.6 | 0.5 | testo | alta |
| 2023-05-16 14:10 | #180 | stop a pareggio | – | – | testo | alta |
| 2023-05-17 07:53 | #184 | obiettivo preso | 26800 | 0.5 | schermata | media |

**A02 · BTC short** — esito +0,23% (dopo i costi), prezzo medio 27945.9, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-05-28 18:24 | #206 | apertura | 27650 | 0.5 | schermata | alta |
| 2023-05-29 07:07 | #208 | aumento | 28315.8 | 0.4 | schermata | alta |
| 2023-05-30 09:49 | #209 | chiusura | 27835.9 | 0.9 | schermata | alta |

**A03 · BTC long** — esito -1,58% (dopo i costi), prezzo medio 27160.6, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-06-03 14:03 | #215 | apertura | 27160.6 | 1 | schermata | alta |
| 2023-06-05 15:37 | #219 | chiusura | 26774.7 | 1 | schermata | alta |

**A05 · BTC short** — esito +2,08% (dopo i costi), prezzo medio 27143.8, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-06-07 14:04 | #227 | apertura | 27143.8 | 1 | schermata | alta |
| 2023-06-07 14:04 | #227 | chiusura parziale | 26721.5 | 0.5 | schermata | alta |
| 2023-06-07 14:04 | #227 | stop a pareggio | – | – | testo | alta |
| 2023-06-07 15:08 | #229 | chiusura | 26349.3 | 0.5 | schermata | alta |

**A06 · MATIC short** — esito +2,56% (dopo i costi), prezzo medio 0.6547, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-06-13 12:56 | #241 | apertura | 0.6547 | 1 | schermata | alta |
| 2023-06-13 14:47 | #245 | chiusura | 0.6369 | 1 | schermata | alta |

**A07 · BTC long** — esito +2,93% (dopo i costi), prezzo medio 25584.6, affidabilità media

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-06-16 13:56 | #249 | apertura | 25360.3 | 0.5 | schermata | alta |
| 2023-06-16 20:02 | #254 | aumento | 25808.9 | 0.5 | schermata | media |
| 2023-06-16 20:02 | #254 | chiusura | 26375 | 1 | schermata | alta |

**A08 · BTC short** — esito -1,25% (dopo i costi), prezzo medio 27400, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-06-20 17:03 | #265 | apertura | 27400 | 1 | schermata | alta |
| 2023-06-20 17:48 | #267 | chiusura | 27700 | 1 | schermata | alta |

**A09 · BTC short** — esito +2,54% (dopo i costi), prezzo medio 30801.1, affidabilità bassa

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-06-28 17:46 | #281 | apertura | 30436.6 | 0.5 | schermata | alta |
| 2023-06-30 12:13 | #284 | aumento | 31165.6 | 0.5 | schermata | media |
| 2023-06-30 13:49 | #286 | chiusura parziale | 29680.1 | 0.5 | schermata | alta |
| 2023-06-30 13:49 | #286 | stop a pareggio | – | – | testo | alta |
| 2023-06-30 14:00 | #287 | chiusura parziale | 29900 | 0.3 | schermata | alta |
| 2023-07-03 19:36 | #298 | stop colpito | 30801.1 | 0.2 | dedotto | bassa |

**A10 · INJ long** — esito +5,27% (dopo i costi), prezzo medio 8.0875, affidabilità bassa

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-07-01 07:43 | #290 | apertura | 8.0875 | 1 | schermata | alta |
| 2023-07-01 16:17 | #295 | chiusura parziale | 8.5355 | 0.5 | schermata | media |
| 2023-07-04 08:42 | #304 | chiusura parziale | 8.8043 | 0.3 | schermata | alta |
| 2023-07-04 08:42 | #304 | stop a pareggio | – | – | testo | alta |
| 2023-07-06 14:00 | #342 | stop colpito | 8.0875 | 0.2 | dedotto | bassa |

**A11 · FET long** — esito +4,27% (dopo i costi), prezzo medio 0.225, affidabilità bassa

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-07-01 07:43 | #290 | apertura | 0.225 | 1 | schermata | alta |
| 2023-07-01 16:17 | #295 | chiusura parziale | 0.23642 | 0.5 | schermata | media |
| 2023-07-04 08:42 | #304 | chiusura parziale | 0.2392 | 0.3 | schermata | alta |
| 2023-07-04 08:42 | #304 | stop a pareggio | – | – | testo | alta |
| 2023-07-06 14:00 | #342 | stop colpito | 0.225 | 0.2 | dedotto | bassa |

**A12 · WOO long** — esito +9,22% (dopo i costi), prezzo medio 0.2248, affidabilità bassa

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-07-01 07:43 | #290 | apertura | 0.2248 | 1 | schermata | alta |
| 2023-07-01 16:17 | #295 | chiusura parziale | 0.2482 | 0.5 | schermata | media |
| 2023-07-04 08:42 | #304 | chiusura parziale | 0.2561 | 0.3 | schermata | alta |
| 2023-07-04 08:42 | #304 | stop a pareggio | – | – | testo | alta |
| 2023-07-06 14:00 | #342 | stop colpito | 0.2248 | 0.2 | dedotto | bassa |

**A13 · BTC short** — esito -0,09% (dopo i costi), prezzo medio 31013.9, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-07-05 12:05 | #307 | apertura | 31013.9 | 1 | schermata | alta |
| 2023-07-06 10:35 | #310 | stop colpito | 30992.4 | 1 | schermata | alta |

**A15 · BTC short** — esito -1,41% (dopo i costi), prezzo medio 30857.4, affidabilità media

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-07-13 08:40 | #321 | apertura | 30459.8 | 0.5 | schermata | alta |
| 2023-07-13 15:55 | #328 | aumento | 31255 | 0.5 | schermata | media |
| 2023-07-13 18:08 | #335 | chiusura | 31244.5 | 1 | schermata | alta |

**A17 · INJ long** — esito +0,98% (dopo i costi), prezzo medio 8.472, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-07-13 18:05 | #334 | apertura | 8.472 | 0.5 | schermata | alta |
| 2023-07-13 18:17 | #336 | chiusura | 8.5685 | 0.5 | schermata | alta |

**A16 · WOO long** — esito +1,17% (dopo i costi), prezzo medio 0.24, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-07-13 18:05 | #334 | apertura | 0.24 | 0.5 | schermata | alta |
| 2023-07-13 18:17 | #336 | chiusura | 0.2432 | 0.5 | schermata | alta |

**A18 · INJ long** — esito +10,67% (dopo i costi), prezzo medio 8.3992, affidabilità media

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-07-14 06:16 | #342 | apertura | 8.3992 | 0.5 | testo | media |
| 2023-07-14 06:16 | #342 | aumento | 8.3992 | 0.5 | schermata | media |
| 2023-07-14 12:17 | #348 | chiusura parziale | 9.1445 | 0.5 | schermata | alta |
| 2023-07-14 17:05 | #352 | chiusura parziale | 9.6825 | 0.3 | schermata | alta |
| 2023-07-14 18:43 | #353 | chiusura | 9.158 | 0.2 | schermata | alta |

**A19 · WOO long** — esito -0,08% (dopo i costi), prezzo medio 0.2438, affidabilità media

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-07-14 06:16 | #342 | apertura | 0.2438 | 0.5 | testo | media |
| 2023-07-14 06:16 | #342 | aumento | 0.2438 | 0.5 | schermata | media |
| 2023-07-14 12:17 | #348 | chiusura | 0.244 | 1 | schermata | alta |

**A20 · BTC long** — esito -0,03% (dopo i costi), prezzo medio 29162.7, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-07-25 16:25 | #365 | apertura | 29162.7 | 1 | schermata | alta |
| 2023-07-26 08:33 | #367 | chiusura | 29200.4 | 1 | schermata | alta |

**A21 · BTC short** — esito +1,61% (dopo i costi), prezzo medio 29322.5, affidabilità bassa

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-07-26 18:02 | #370 | apertura | 29322.5 | 1 | grafico | bassa |
| 2023-08-01 16:14 | #375 | obiettivo preso | 28802.5 | 1 | grafico | bassa |

**A23 · BTC long** — esito +2,40% (dopo i costi), prezzo medio 25884.7, affidabilità media

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-08-18 15:16 | #392 | apertura | 25944.8 | 0.5 | schermata | alta |
| 2023-08-23 21:46 | #402 | aumento | 25824.6 | 0.5 | schermata | media |
| 2023-08-23 21:46 | #402 | obiettivo preso | 26546.4 | 1 | schermata | alta |

**A24 · BTC long** — esito +2,95% (dopo i costi), prezzo medio 26989, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-08-29 14:36 | #406 | apertura | 26989 | 1 | schermata | alta |
| 2023-08-29 16:37 | #409 | chiusura | 27828.4 | 1 | schermata | alta |

**A25 · BTC short** — esito +4,67% (dopo i costi), prezzo medio 27868.9, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-08-29 18:44 | #413 | apertura | 27868.9 | 1 | schermata | alta |
| 2023-08-31 16:40 | #419 | chiusura | 26523.3 | 1 | schermata | alta |

**B01 · INJ long** — esito +4,03% (dopo i costi), prezzo medio 6.961, affidabilità bassa

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-09-15 00:00 | #458 | apertura | – | 0.5 | testo | bassa |
| 2023-09-18 00:00 | #458 | aumento | 6.961 | 1 | testo | media |
| 2023-09-21 07:55 | #465 | chiusura | 7.2525 | 1 | schermata | alta |

**B02 · BNB short** — esito +0,94% (dopo i costi), prezzo medio 213.35, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-09-21 08:28 | #466 | apertura | 213.35 | 1 | schermata | alta |
| 2023-09-22 10:32 | #471 | chiusura | 211 | 1 | schermata | alta |

**B03 · BTC long** — esito -1,47% (dopo i costi), prezzo medio 26475.1, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-09-22 14:31 | #472 | apertura | 26575.3 | 0.5 | schermata | alta |
| 2023-09-24 21:50 | #475 | aumento | 26475.1 | 1 | schermata | alta |
| 2023-09-25 06:09 | #477 | chiusura | 26128.2 | 1 | schermata | alta |

**B04 · BTC long** — esito +2,08% (dopo i costi), prezzo medio 26229.5, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-09-26 16:41 | #479 | apertura | 26229.5 | 1 | schermata | alta |
| 2023-09-27 12:06 | #482 | chiusura | 26817.5 | 1 | schermata | alta |

**B05 · BTC short** — esito +0,41% (dopo i costi), prezzo medio 27247.6, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-09-28 16:29 | #497 | apertura | 27247.6 | 1 | schermata | alta |
| 2023-09-28 19:45 | #498 | chiusura | 27091.7 | 1 | schermata | alta |

**B06 · BTC long** — esito +4,29% (dopo i costi), prezzo medio 26911.9, affidabilità bassa

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-09-29 14:00 | #509 | apertura | 26911.9 | 1 | schermata | media |
| 2023-10-02 06:33 | #509 | chiusura parziale | 28030 | 0.5 | testo | bassa |
| 2023-10-02 07:31 | #511 | chiusura | 28187.4 | 1 | schermata | alta |

**B07 · BTC short** — esito +3,51% (dopo i costi), prezzo medio 28400, affidabilità bassa

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-10-02 07:46 | #512 | apertura | 28400 | 1 | schermata | alta |
| 2023-10-02 13:14 | #514 | chiusura parziale | – | – | testo | bassa |
| 2023-10-02 22:42 | #517 | chiusura parziale | 27416.9 | 0.5 | schermata | alta |
| 2023-10-03 14:53 | #521 | chiusura | 27299.5 | 1 | schermata | alta |

**B08 · BTC short** — esito +2,34% (dopo i costi), prezzo medio 27896.5, affidabilità bassa

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-10-09 03:00 | #534 | apertura | 27896.5 | 1 | schermata | alta |
| 2023-10-09 17:48 | #534 | stop a pareggio | – | – | testo | alta |
| 2023-10-11 02:00 | #534 | obiettivo preso | 27200 | 1 | dedotto | bassa |

**B09 · BTC long** — esito +0,19% (dopo i costi), prezzo medio 26651.2, affidabilità media

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-10-11 15:34 | #537 | apertura | 26718.5 | 0.5 | testo | alta |
| 2023-10-11 17:00 | #538 | aumento | 26651.2 | 1 | schermata | media |
| 2023-10-13 17:32 | #544 | chiusura | 26745 | 1 | schermata | alta |

**B25 · BTC long** — esito -0,05% (dopo i costi), prezzo medio 26707.2, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-10-11 16:34 | #540 | apertura | 26707.2 | 1 | schermata | alta |
| 2023-10-13 17:32 | #544 | chiusura | 26735.4 | 1 | schermata | alta |

**B10 · BTC short** — esito -0,68% (dopo i costi), prezzo medio 28770, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-10-17 20:39 | #561 | ordine limite | 28770 | – | testo | alta |
| 2023-10-18 04:00 | #562 | apertura | 28770 | 1 | schermata | alta |
| 2023-10-18 04:00 | #562 | stop colpito | 28920.1 | 1 | schermata | alta |

**B11 · BTC short** — esito +0,03% (dopo i costi), prezzo medio 28394.8, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-10-18 12:34 | #564 | apertura | 28394.8 | 1 | schermata | alta |
| 2023-10-19 09:46 | #565 | chiusura | 28341.7 | 1 | schermata | alta |

**B12 · BTC short** — esito -0,87% (dopo i costi), prezzo medio 28757, affidabilità media

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-10-19 15:37 | #567 | apertura | – | 0.5 | testo | media |
| 2023-10-19 16:21 | #570 | aumento | 28757 | 1 | testo | media |
| 2023-10-20 02:30 | #571 | chiusura | 28959.8 | 1 | schermata | alta |

**B14 · DOGE long** — esito +3,11% (dopo i costi), prezzo medio 0.06431, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-10-23 14:00 | #583 | apertura | 0.06431 | 1 | schermata | alta |
| 2023-10-24 20:47 | #593 | chiusura | 0.06641 | 1 | schermata | alta |

**B13 · INJ long** — esito +15,54% (dopo i costi), prezzo medio 10.512, affidabilità bassa

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-10-23 22:50 | #583 | apertura | 10.512 | 1 | testo | alta |
| 2023-10-24 09:26 | #585 | chiusura parziale | 11.87 | – | testo | bassa |
| 2023-10-24 10:50 | #587 | chiusura parziale | 12.44 | 0.5 | schermata | alta |
| 2023-10-24 20:47 | #593 | chiusura | 11.8845 | 1 | schermata | alta |

**B15 · INJ long** — esito +13,85% (dopo i costi), prezzo medio 12.3572, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-10-27 08:00 | #603 | apertura | 12.3572 | 1 | schermata | alta |
| 2023-10-30 21:13 | #611 | chiusura parziale | 13.5685 | 0.5 | schermata | alta |
| 2023-11-01 13:28 | #614 | chiusura | 14.609 | 1 | schermata | alta |

**B16 · SOL short** — esito +6,54% (dopo i costi), prezzo medio 46.133, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-11-01 18:38 | #619 | apertura | 46.133 | 1 | schermata | alta |
| 2023-11-01 19:04 | #620 | chiusura parziale | 44.082 | 0.5 | schermata | alta |
| 2023-11-01 19:42 | #622 | chiusura | 42 | 1 | schermata | alta |

**B17 · BTC short** — esito +1,32% (dopo i costi), prezzo medio 35200, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-11-02 13:20 | #626 | apertura | 35200 | 1 | schermata | alta |
| 2023-11-02 14:27 | #628 | chiusura parziale | 34845.6 | 0.5 | schermata | alta |
| 2023-11-02 14:27 | #628 | stop a pareggio | – | – | testo | alta |
| 2023-11-03 19:01 | #632 | chiusura | 34510.9 | 1 | schermata | alta |

**B18 · INJ long** — esito +0,22% (dopo i costi), prezzo medio 17.1803, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-11-09 09:18 | #647 | apertura | 17.1803 | 1 | testo | alta |
| 2023-11-09 11:19 | #651 | stop a pareggio | – | – | testo | alta |
| 2023-11-09 16:02 | #652 | stop colpito | 17.2455 | 1 | schermata | alta |

**B19 · DOGE long** — esito +29,40% (dopo i costi), prezzo medio 0.07612, affidabilità media

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-11-09 10:20 | #648 | apertura | 0.07612 | 1 | schermata | alta |
| 2023-12-06 08:07 | #745 | chiusura parziale | 0.10295 | 0.3 | schermata | media |
| 2023-12-15 09:16 | #770 | chiusura | 0.09677 | 1 | schermata | media |

**B20 · ETH long** — esito -2,64% (dopo i costi), prezzo medio 2026.95, affidabilità media

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-11-13 21:17 | #667 | apertura | 2052.54 | 0.5 | schermata | alta |
| 2023-11-13 21:54 | #673 | stop spostato | – | – | testo | alta |
| 2023-11-14 18:00 | #677 | aumento | 2026.95 | 1 | schermata | media |
| 2023-11-14 19:19 | #677 | stop colpito | 1976.72 | 1 | schermata | alta |

**B21 · BTC long** — esito +0,38% (dopo i costi), prezzo medio 36450, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-11-13 21:29 | #670 | apertura | 36450 | 1 | schermata | alta |
| 2023-11-13 21:29 | #670 | chiusura | 36647.5 | 1 | schermata | alta |

**B22 · BTC long** — esito +2,20% (dopo i costi), prezzo medio 35650, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-11-16 19:30 | #684 | apertura | 35650 | 1 | schermata | alta |
| 2023-11-16 21:17 | #684 | stop a pareggio | – | – | testo | alta |
| 2023-11-17 17:10 | #691 | chiusura parziale | 36764.8 | 0.75 | schermata | alta |
| 2023-11-22 00:00 | #710 | stop colpito | 35678 | 1 | schermata | alta |

**B23 · BTC short** — esito -0,54% (dopo i costi), prezzo medio 37949.6, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-11-28 23:05 | #724 | apertura | 37949.6 | 1 | schermata | alta |
| 2023-11-29 08:04 | #726 | chiusura | 38094.4 | 1 | schermata | alta |

**B24 · BTC long** — esito +1,58% (dopo i costi), prezzo medio 40600, affidabilità bassa

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-12-11 20:52 | #754 | apertura | 40600 | 1 | schermata | alta |
| 2023-12-12 09:16 | #756 | chiusura parziale | 42014.7 | 0.5 | schermata | media |
| 2023-12-12 15:42 | #759 | stop a pareggio | – | – | testo | alta |
| 2023-12-13 02:00 | #759 | stop colpito | 40600 | 1 | dedotto | bassa |

**C01 · BTC long** — esito +6,31% (dopo i costi), prezzo medio 41882.3, affidabilità bassa

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2023-12-19 17:30 | #783 | apertura | 41882.3 | – | testo | bassa |
| 2023-12-20 14:00 | #783 | chiusura parziale | 43721.4 | 0.5 | schermata | media |
| 2023-12-22 10:08 | #785 | ordine limite | 45459.7 | – | grafico | media |
| 2024-01-02 03:00 | #794 | chiusura | 45459.7 | 0.5 | grafico | bassa |

**C02 · BTC long** — esito +10,39% (dopo i costi), prezzo medio 40750, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2024-01-03 12:00 | #796 | apertura | 40750 | 1 | testo | alta |
| 2024-01-03 12:15 | #798 | stop a pareggio | – | – | testo | alta |
| 2024-01-03 12:15 | #800 | chiusura parziale | 42200 | 0.5 | testo | alta |
| 2024-01-09 21:15 | #818 | chiusura | 47899.3 | 0.5 | schermata | alta |

**C03 · ETH long** — esito +6,17% (dopo i costi), prezzo medio 2355.94, affidabilità bassa

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2024-01-10 00:00 | #822 | apertura | 2355.94 | 1 | testo | media |
| 2024-01-11 10:45 | #831 | chiusura parziale | 2644.92 | 0.5 | testo | alta |
| 2024-01-11 11:02 | #831 | stop a pareggio | – | – | testo | media |
| 2024-01-30 23:24 | #875 | chiusura | 2365 | 0.5 | testo | bassa |

**C05 · BTC long** — esito -0,13% (dopo i costi), prezzo medio 39476.8, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2024-01-22 19:30 | #850 | apertura | 39476.8 | 0.5 | testo | alta |
| 2024-01-22 22:18 | #851 | stop a pareggio | – | – | testo | alta |
| 2024-01-22 22:45 | #853 | stop colpito | 39488.1 | 1 | testo | alta |

**C06 · INJ long** — esito +4,88% (dopo i costi), prezzo medio 36.6494, affidabilità media

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2024-02-17 22:32 | #914 | apertura | 36.6494 | 0.5 | testo | alta |
| 2024-02-18 21:00 | #918 | chiusura parziale | 39.592 | 0.5 | testo | alta |
| 2024-02-18 21:46 | #918 | stop a pareggio | – | – | testo | alta |
| 2024-02-19 14:05 | #923 | chiusura | 37.4 | 0.5 | testo | media |

**C07 · INJ long** — esito +21,27% (dopo i costi), prezzo medio 36.735, affidabilità alta

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2024-02-28 17:30 | #950 | apertura | 36.735 | 1 | testo | alta |
| 2024-02-29 00:00 | #962 | chiusura | 44.606 | 1 | testo | alta |

**C08 · BTC long** — esito +15,57% (dopo i costi), prezzo medio 59909.3, affidabilità bassa

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2024-02-28 18:15 | #1010 | apertura | 59909.3 | 1 | dedotto | bassa |
| 2024-03-08 15:15 | #1010 | chiusura | 69333.1 | 1 | testo | alta |

**C11 · BTC long** — esito +3,54% (dopo i costi), prezzo medio 66557.7, affidabilità media

| Data UTC | Msg | Evento | Prezzo | Quota | Fonte | Affidabilità |
|---|---|---|---|---|---|---|
| 2024-03-17 10:00 | #1021 | apertura | 66557.7 | 0.5 | testo | alta |
| 2024-03-18 10:08 | #1025 | obiettivo preso | 69020.1 | – | grafico | media |

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
