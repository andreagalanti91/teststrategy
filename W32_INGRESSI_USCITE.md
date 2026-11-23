# W3.2 · quando entra, quando esce, e i controlli con DCA

Analisi delle 23 operazioni di W3.2 (9 nel 2018–20 con flusso stimato, 14 dal 2021 con i dati reali del perp), delle regole
con cui entra ed esce, e prove di ingresso e uscita a scaglioni. Dati fino al 22/11/2026.

> Ricerca su dati storici, non una raccomandazione d'investimento.

## 1. Sintesi

**W3.2 entra tardi e tutta insieme, ed è giusto così: ogni forma di ingresso a scaglioni peggiora il risultato in tutti i
periodi. In uscita la regola migliore è già dentro la strategia (la "distribuzione"), e nessuna variante a scaglioni la
migliora davvero.**

| Domanda | Risposta dai dati |
|---|---|
| Quando entra? | Con il trend già partito: in mediana il prezzo è il 14% oltre la EMA 21 settimanale. Non compra ritracciamenti. |
| Conviene entrare a scaglioni? | No. Le 7 varianti di DCA in ingresso fanno peggio in tutti e tre i periodi: dal 2021, da 83.129 $ a 33.579–62.371 $. |
| Perché? | Nelle operazioni vincenti il prezzo migliore è quello del primo giorno: aspettare costa. Il DCA aiuta solo sulle perdenti, che sono poche e piccole. |
| Quando esce? | In tre modi, sette volte ciascuno: distribuzione, trailing, chiusura oltre la EMA 21. |
| Quale uscita è la migliore? | La distribuzione: incassa in media +35,7% e restituisce solo 4 punti dal massimo. Trailing ed EMA 21 ne restituiscono 24–27. |
| Esce troppo presto? | Non risulta. A 28 giorni dall'uscita il prezzo è in media a −2,7%, un valore non distinguibile da zero; solo 4 uscite su 20 sono seguite da oltre +5% a favore. |
| Conviene uscire a scaglioni? | No. Uscire metà al primo segnale peggiora; un target parziale non cambia quasi nulla; il trailing diviso in due metà sembra migliorare dal 2021, ma il vantaggio viene da una posizione più grande e da due operazioni. |

## 2. Quando entra

Le regole: chiusura settimanale oltre la EMA 21 nel verso del trend (SMA 40 ed EMA 20), con il flusso del perp a favore.
Ingresso il lunedì all'apertura, tutto insieme, con esposizione ridotta se lo stop è lontano.

| # | Verso | Segnale | Entra a | Sopra/sotto EMA 21 | Sopra/sotto SMA 40 | Flusso perp | Stop a | Esposizione | Peggior prezzo nei primi 14 giorni | Giorno del miglior prezzo d'ingresso | Risultato finale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | long | 2018-01-07 | 16.235 | +72,5% | +203,9% | 1,29 | -41% | 0,62x | -44,3% | 8 | -25,1% |
| 2 | long | 2018-04-29 | 9.426 | +3,6% | +13,8% | 0,42 | -63% | 0,40x | -13,5% | 12 | -3,3% |
| 3 | short | 2018-10-14 | 6.333 | -9,6% | -20,8% | -0,47 | -42% | 0,59x | -21,3% | 0 | +16,7% |
| 4 | long | 2019-05-12 | 6.975 | +42,2% | +37,4% | 0,73 | -24% | 1,00x | -1,5% | 0 | +51,1% |
| 5 | long | 2020-02-09 | 10.162 | +19,3% | +12,6% | 0,68 | -27% | 0,93x | -7,0% | 7 | -2,6% |
| 6 | short | 2020-03-15 | 5.355 | -36,0% | -40,8% | -2,20 | -62% | 0,40x | -29,9% | 9 | -17,9% |
| 7 | long | 2020-05-03 | 8.903 | +14,1% | +4,9% | 0,37 | -37% | 0,67x | -8,8% | 6 | +16,0% |
| 8 | long | 2020-10-25 | 13.043 | +22,6% | +38,1% | 0,17 | -21% | 1,00x | -2,1% | 0 | +40,8% |
| 9 | long | 2020-12-13 | 19.194 | +37,0% | +77,0% | 0,14 | -21% | 1,00x | -1,0% | 0 | +50,4% |
| 10 | long | 2021-01-31 | 33.126 | +44,6% | +117,1% | 0,24 | -35% | 0,72x | -2,5% | 0 | +52,2% |
| 11 | long | 2021-08-01 | 39.890 | +1,0% | +4,0% | 1,67 | -46% | 0,54x | -6,4% | 3 | +4,3% |
| 12 | long | 2021-10-03 | 48.248 | +9,8% | +7,9% | 0,87 | -37% | 0,68x | -2,8% | 0 | +20,9% |
| 13 | short | 2022-01-02 | 47.239 | -7,7% | -1,9% | -0,14 | -39% | 0,64x | -0,7% | 0 | +1,0% |
| 14 | short | 2022-08-14 | 24.281 | -14,7% | -34,9% | -0,29 | -45% | 0,56x | -3,8% | 0 | +8,3% |
| 15 | long | 2023-01-22 | 22.729 | +15,1% | +2,1% | 1,95 | -26% | 0,95x | -1,9% | 2 | +13,3% |
| 16 | long | 2023-10-22 | 30.022 | +8,9% | +10,9% | 1,12 | -18% | 1,00x | -0,5% | 0 | +40,5% |
| 17 | long | 2024-02-11 | 48.348 | +24,4% | +46,1% | 1,02 | -18% | 1,00x | -1,3% | 0 | +42,2% |
| 18 | long | 2024-09-22 | 63.642 | +4,7% | +7,3% | 1,63 | -27% | 0,91x | -6,0% | 10 | +30,8% |
| 19 | long | 2025-04-27 | 93.843 | +7,5% | +15,4% | 3,38 | -25% | 0,99x | -1,1% | 0 | +11,3% |
| 20 | short | 2025-11-30 | 90.270 | -14,4% | -12,8% | -1,04 | -28% | 0,89x | -4,8% | 8 | +11,9% |
| 21 | short | 2026-05-24 | 76.988 | -1,9% | -13,7% | -0,50 | -23% | 1,00x | -1,4% | 1 | +5,7% |
| 22 | long | 2026-08-23 | 77.812 | +11,7% | +4,4% | 2,30 | -21% | 1,00x | -2,0% | 9 | -4,1% |
| 23 | short | 2026-11-15 | 65.286 | -13,5% | -9,4% | -0,93 | -26% | 0,97x | -0,6% | 0 | +5,9% |

"Peggior prezzo nei primi 14 giorni" è quanto il prezzo è andato contro l'operazione rispetto all'ingresso. "Giorno del
miglior prezzo" è il giorno, fra i primi 14, in cui si sarebbe entrati al prezzo più favorevole: 0 significa che il primo
giorno era il migliore.

### Cosa hanno in comune gli ingressi

| Gruppo | Operazioni | Distanza mediana dalla EMA 21 | Distanza mediana dalla SMA 40 | Flusso mediano | Stop mediano | Prezzo peggiore nei primi 14 giorni (mediana) | Con almeno −5% nei primi 14 giorni | Miglior prezzo d'ingresso: giorno mediano |
|---|---|---|---|---|---|---|---|---|
| Tutte | 23 | +14,1% | +13,7% | 0,87 | -27% | -2,5% | 35% | 0 |
| Long | 16 | +14,6% | +13,2% | 0,94 | -27% | -2,3% | 38% | 1 |
| Short | 7 | +13,5% | +13,7% | 0,50 | -39% | -3,8% | 29% | 0 |
| In guadagno | 18 | +13,8% | +13,3% | 0,80 | -27% | -2,0% | 22% | 0 |
| In perdita | 5 | +19,3% | +13,8% | 1,29 | -41% | -13,5% | 80% | 9 |
| Dal 2021 | 14 | +10,7% | +10,2% | 1,03 | -27% | -1,9% | 14% | 0 |
| 2018–20 | 9 | +22,6% | +37,4% | 0,47 | -37% | -8,8% | 67% | 6 |

1. **Entra a trend avviato.** In mediana il prezzo è già il 14% oltre la EMA 21 e il 14% oltre la SMA 40. Non c'è nessun
   ingresso su ritracciamento.
2. **Nelle operazioni in guadagno il prezzo non torna indietro**: il prezzo migliore è quello del giorno d'ingresso, e il
   peggior momento dei primi 14 giorni è in mediana solo −2%.
3. **Quattro perdenti su cinque sono andate contro di almeno il 5% nei primi 14 giorni**, ma sono tutte del 2018–20. Dal
   2021 i casi con un calo simile sono solo due, entrambi chiusi in guadagno: non è un segnale su cui contare.
4. **Le perdenti avevano lo stop più lontano** (mediana −41% contro −27%), quindi W3.2 le aveva già ridotte: esposizione
   0,40–0,62x nelle due perdite maggiori.
5. **Dal 2021 gli ingressi sono più puliti**: distanza dalla EMA 21 dell'11% contro il 23% del 2018–20, e solo il 14% delle
   operazioni scende del 5% nei primi 14 giorni contro il 67%.

Quello che non separa vincenti e perdenti: la distanza dalle medie e la forza del flusso. L'ingresso più esteso dal 2021
(+45% dalla EMA 21, gennaio 2021) è stato il migliore.

## 3. Quando esce

| # | Verso | Entra | Esce | Giorni | Motivo | Massimo guadagno toccato | Miglior chiusura | Mossa incassata | Restituito | Prezzo 14 giorni dopo l'uscita | 28 giorni dopo |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | long | 2018-01-08 | 2018-01-16 | 8 | trailing | +0,5% | -8,2% | -40,5% | +32,4% | +6,0% | -11,5% |
| 2 | long | 2018-04-30 | 2018-05-14 | 14 | EMA 21 | +6,3% | +4,6% | -8,0% | +12,7% | -18,1% | -20,7% |
| 3 | short | 2018-10-15 | 2019-04-02 | 169 | trailing | +50,2% | +49,3% | +28,1% | +21,1% | -13,7% | -16,9% |
| 4 | long | 2019-05-13 | 2019-06-27 | 45 | trailing | +100,3% | +87,7% | +51,4% | +36,3% | +7,4% | -6,4% |
| 5 | long | 2020-02-10 | 2020-02-17 | 7 | distribuzione | +3,3% | +1,8% | -2,6% | +4,4% | -10,0% | -49,2% |
| 6 | short | 2020-03-16 | 2020-04-27 | 42 | EMA 21 | +17,0% | +6,1% | -43,8% | +49,9% | -11,2% | -15,6% |
| 7 | long | 2020-05-04 | 2020-08-03 | 91 | distribuzione | +36,2% | +32,6% | +24,2% | +8,3% | +11,0% | +5,3% |
| 8 | long | 2020-10-26 | 2020-11-23 | 28 | distribuzione | +45,4% | +43,4% | +41,0% | +2,4% | +4,2% | +23,5% |
| 9 | long | 2020-12-14 | aperta | 17 | aperta | +52,7% | +50,7% | +50,7% | +0,0% | n/d | n/d |
| 10 | long | 2021-02-01 | 2021-02-22 | 21 | distribuzione | +76,2% | +73,3% | +73,1% | +0,2% | -8,7% | -5,7% |
| 11 | long | 2021-08-02 | 2021-09-27 | 56 | EMA 21 | +32,7% | +32,0% | +8,1% | +23,9% | +33,3% | +46,3% |
| 12 | long | 2021-10-04 | 2021-11-08 | 35 | distribuzione | +40,5% | +36,8% | +31,0% | +5,8% | -11,0% | -20,2% |
| 13 | short | 2022-01-03 | 2022-03-28 | 84 | EMA 21 | +30,3% | +25,8% | +0,8% | +25,0% | +15,7% | +13,8% |
| 14 | short | 2022-08-15 | 2023-01-16 | 154 | EMA 21 | +36,3% | +35,0% | +13,9% | +21,1% | -9,2% | -4,2% |
| 15 | long | 2023-01-23 | 2023-08-17 | 206 | trailing | +39,9% | +38,4% | +14,2% | +24,1% | -0,1% | +2,1% |
| 16 | long | 2023-10-23 | 2024-01-01 | 70 | distribuzione | +48,9% | +47,1% | +40,7% | +6,4% | +0,6% | +2,5% |
| 17 | long | 2024-02-12 | 2024-03-11 | 28 | distribuzione | +50,6% | +42,6% | +42,5% | +0,1% | +1,4% | +4,0% |
| 18 | long | 2024-09-23 | 2025-02-26 | 156 | trailing | +72,2% | +66,8% | +34,0% | +32,8% | -1,8% | +1,9% |
| 19 | long | 2025-04-28 | 2025-10-10 | 165 | trailing | +34,5% | +32,8% | +11,6% | +21,3% | +6,0% | -1,3% |
| 20 | short | 2025-12-01 | 2026-04-27 | 147 | EMA 21 | +33,5% | +30,3% | +12,8% | +17,5% | -3,8% | +1,8% |
| 21 | short | 2026-05-25 | 2026-08-20 | 87 | trailing | +24,9% | +23,9% | +4,8% | +19,0% | -10,9% | -4,3% |
| 22 | long | 2026-08-24 | 2026-11-09 | 77 | EMA 21 | +12,3% | +11,3% | -3,9% | +15,2% | n/d | n/d |
| 23 | short | 2026-11-16 | aperta | 6 | aperta | +15,6% | +9,7% | +6,1% | +3,6% | n/d | n/d |

"Restituito" è la differenza fra la miglior chiusura raggiunta e la mossa incassata. Le ultime due colonne dicono dove
sarebbe andato il prezzo dopo l'uscita, nel verso dell'operazione: positivo significa che uscire è costato.

### Cosa hanno in comune le uscite

| Motivo di uscita | Operazioni | In guadagno | Mossa media incassata | Miglior chiusura media | Restituito in media | Prezzo 14 giorni dopo (media, nel verso del trade) | 28 giorni dopo | Uscite seguite da un movimento a favore oltre +5% a 28 giorni |
|---|---|---|---|---|---|---|---|---|
| EMA 21 | 7 | 57% | -2,9% | +20,7% | +23,6% | +1,1% | +3,6% | 2 su 6 |
| distribuzione | 7 | 86% | +35,7% | +39,7% | +3,9% | -1,8% | -5,7% | 2 su 7 |
| trailing | 7 | 86% | +14,8% | +41,5% | +26,7% | -1,0% | -5,2% | 0 su 7 |
| Tutte le chiuse | 21 | 76% | +15,9% | +34,0% | +18,1% | -0,6% | -2,7% | 4 su 20 |

Durata mediana: 70 giorni (in guadagno 86, in perdita 14). Somma dei massimi guadagni toccati: +792%; somma delle mosse incassate: +333%.

Per periodo, prezzo 28 giorni dopo l'uscita: 2018–20 -11,4% su 8 uscite, dal 2021 +3,1% su 12. Statistica t della media complessiva: -0,65 (sotto 2 in valore assoluto = non distinguibile da zero).

Operazioni andate contro di almeno il 5% nei primi 14 giorni: 2018–20 6, di cui 4 in perdita; dal 2021 2, di cui 0 in perdita.

1. **La distribuzione è l'uscita migliore.** Chiude vicino al massimo (4 punti restituiti) e dopo il prezzo scende in media
   del 5,7% a 28 giorni. È la regola che distingue W3.2 dagli algoritmi fatti solo di prezzo.
2. **Trailing ed EMA 21 sono uscite di difesa**: scattano dopo che il prezzo ha già restituito 24–27 punti. L'uscita per EMA
   21 chiude in media in perdita (−2,9%) perché è quella che ferma le operazioni che non sono mai partite.
3. **Dopo l'uscita il prezzo in media non prosegue**, ma il dato è debole: la media a 28 giorni non è distinguibile da zero
   e cambia segno fra i periodi (−11,4% nel 2018–20, +3,1% dal 2021). Le uscite seguite da oltre +5% a favore sono quattro: novembre 2020 (+23% nei 28 giorni
   dopo), settembre 2021 (+46%), marzo 2022 (+14%, uno short) e agosto 2020 (+5%).
4. **W3.2 restituisce più di metà del movimento**: la somma dei massimi toccati è +792%, quella delle mosse incassate +333%.
   È il costo di restare dentro i trend lunghi, già misurato nel radar (lezione 109).
5. **Le perdenti durano poco**: 14 giorni in mediana contro 86 delle vincenti.

## 4. Controlli con DCA

Stesso motore a scaglioni usato nel radar, con il rischio di W3.2 (25%). Una variante "migliora" solo se ha un rapporto
rendimento/drawdown più alto di W3.2 in tutti e tre i periodi: 2021–23, 2024–26 e 2018–20.

| Variante | 10.000 $ → (dal 2021) | CAGR | Max DD | CAGR/DD | Operazioni | Vincenti | Peggiore | 2021–23: finale | 2024–26: finale | 2018–20: finale / DD | Operazioni migliorate / peggiorate | Esito |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| W3.2 (tutto subito, tutto insieme) | 83.129 | +43,3% | -21,1% | 2,05 | 14 | 93% | -4,1% | 33.477 | 24.881 | 25.142 / -37% | – | riferimento |
| Ingresso: 1/3 lunedì, mercoledì, venerdì | 62.371 | +36,5% | -20,6% | 1,77 | 14 | 86% | -5,4% | 27.626 | 22.622 | 21.030 / -39% | 3 / 17 | migliora in 0 periodi su 3 |
| Ingresso: 1/3 ogni lunedì per 3 settimane (senza condizioni) | 43.003 | +28,1% | -22,9% | 1,23 | 14 | 71% | -5,1% | 21.353 | 20.179 | 20.634 / -37% | 6 / 16 | migliora in 0 periodi su 3 |
| Ingresso: 1/2 subito, 1/2 la settimana dopo se il segnale regge | 55.063 | +33,6% | -21,1% | 1,60 | 14 | 86% | -4,1% | 25.859 | 21.337 | 17.520 / -31% | 2 / 19 | migliora in 0 periodi su 3 |
| Ingresso: 1/3 a settimana per 3 settimane se il segnale regge | 33.579 | +22,8% | -19,3% | 1,18 | 14 | 71% | -2,7% | 20.902 | 16.097 | 16.085 / -27% | 5 / 18 | migliora in 0 periodi su 3 |
| Ingresso: 1/2 subito, 1/2 con limite a −0,25 ATR (5 giorni) | 60.399 | +35,7% | -20,3% | 1,76 | 14 | 86% | -4,2% | 27.400 | 22.087 | 23.217 / -36% | 6 / 15 | migliora in 0 periodi su 3 |
| Ingresso: 1/2 subito, 1/2 con limite a −0,5 ATR (5 giorni) | 57.437 | +34,6% | -22,0% | 1,57 | 14 | 86% | -4,2% | 26.449 | 21.759 | 21.898 / -40% | 1 / 18 | migliora in 0 periodi su 3 |
| Ingresso: 1/2 subito, 1/2 con limite a −1 ATR (10 giorni) | 53.323 | +32,9% | -22,0% | 1,50 | 14 | 79% | -3,9% | 23.972 | 22.289 | 23.683 / -36% | 6 / 14 | migliora in 0 periodi su 3 |
| Uscita: 1/2 al primo segnale, 1/2 alla conferma | 66.694 | +38,0% | -21,1% | 1,80 | 13 | 92% | -6,3% | 28.555 | 24.217 | 23.110 / -43% | 3 / 9 | migliora in 0 periodi su 3 |
| Uscita: 1/3 al primo segnale, 2/3 alla conferma | 65.656 | +37,7% | -21,1% | 1,78 | 13 | 92% | -7,0% | 28.701 | 23.996 | 22.442 / -45% | 3 / 9 | migliora in 0 periodi su 3 |
| Uscita: due metà con trailing a 2,0 e 3,0 ATR | 72.133 | +39,9% | -19,0% | 2,10 | 14 | 93% | -4,4% | 30.169 | 23.957 | 25.170 / -37% | 2 / 4 | migliora in 2 periodi su 3 |
| Uscita: due metà con trailing a 1,5 e 2,5 ATR | 96.158 | +46,9% | -17,7% | 2,65 | 14 | 93% | -2,4% | 36.023 | 26.721 | 22.503 / -34% | 11 / 7 | migliora in 2 periodi su 3 |
| Uscita: 1/3 a +2R (target), resto con le regole | 84.303 | +43,6% | -21,1% | 2,06 | 14 | 93% | -4,1% | 32.860 | 25.690 | 24.427 / -33% | 2 / 5 | migliora in 2 periodi su 3 |
| Uscita: 1/3 a +1R e 1/3 a +2R, resto con le regole | 82.875 | +43,2% | -19,3% | 2,24 | 14 | 93% | -4,1% | 30.444 | 27.241 | 20.813 / -30% | 7 / 6 | migliora in 1 periodi su 3 |
| Uscita: 1/2 a +1R, resto con le regole | 80.626 | +42,5% | -19,3% | 2,20 | 14 | 93% | -4,1% | 29.809 | 27.077 | 19.745 / -31% | 6 / 7 | migliora in 1 periodi su 3 |
| Entrambi: ingresso lun/mer/ven + uscita in due metà | 51.925 | +32,3% | -21,6% | 1,49 | 13 | 85% | -7,6% | 24.451 | 22.019 | 19.194 / -45% | 3 / 17 | migliora in 0 periodi su 3 |
| Entrambi: ingresso con limite −0,5 ATR + 1/3 a +2R | 57.835 | +34,7% | -22,0% | 1,58 | 14 | 86% | -4,2% | 26.191 | 22.119 | 21.561 / -38% | 2 / 17 | migliora in 0 periodi su 3 |

### Operazione per operazione

Differenza sul capitale rispetto a W3.2, per ogni operazione:

| Segnale | Verso | W3.2 | DCA lun/mer/ven | DCA 3 settimane | Limite −0,5 ATR | Uscita in due metà | Trailing 2,0/3,0 | 1/3 a +2R |
|---|---|---|---|---|---|---|---|---|
| 2018-01-07 | long | -25,1% | -0,1% | +8,3% | -0,1% | +0,0% | -0,0% | +0,0% |
| 2018-04-29 | long | -3,3% | +0,1% | +0,7% | -0,6% | -0,3% | +0,0% | +0,0% |
| 2018-10-14 | short | +16,7% | +4,2% | +2,3% | +5,2% | +0,0% | +0,0% | +0,0% |
| 2019-05-12 | long | +51,1% | -12,0% | -34,1% | -4,0% | +0,0% | -0,0% | -1,2% |
| 2020-02-09 | long | -2,6% | -0,5% | +1,7% | -0,9% | -6,3% | -0,0% | +0,0% |
| 2020-03-15 | short | -17,9% | -0,6% | -0,5% | -0,2% | -2,1% | +0,1% | -0,0% |
| 2020-05-03 | long | +16,0% | -3,8% | -10,7% | -3,1% | +2,2% | +0,0% | +0,0% |
| 2020-10-25 | long | +40,8% | -3,6% | -9,9% | -2,8% | -0,9% | +0,0% | +0,2% |
| 2020-12-13 | long | +50,4% | -8,6% | -22,7% | -12,8% | -0,0% | +0,0% | -3,3% |
| 2021-01-31 | long | +52,2% | -5,8% | -15,5% | -6,8% | -13,2% | +0,0% | -0,9% |
| 2021-08-01 | long | +4,3% | +0,5% | -5,1% | -2,0% | +13,7% | +0,0% | +0,0% |
| 2021-10-03 | long | +20,9% | -4,4% | -9,2% | -3,5% | n/d | +0,0% | +0,0% |
| 2022-01-02 | short | +1,0% | -2,5% | -2,9% | -3,7% | +0,3% | -0,0% | +0,0% |
| 2022-08-14 | short | +8,3% | -1,3% | -5,7% | -4,0% | -0,5% | +0,7% | +0,0% |
| 2023-01-22 | long | +13,3% | -0,1% | -6,2% | -0,8% | +0,0% | -11,9% | -0,0% |
| 2023-10-22 | long | +40,5% | -11,1% | -12,9% | -8,1% | -4,7% | +0,0% | -1,7% |
| 2024-02-11 | long | +42,2% | -4,6% | -17,6% | -5,2% | -0,6% | -9,5% | -2,1% |
| 2024-09-22 | long | +30,8% | -1,9% | -11,1% | -2,0% | -0,0% | -0,0% | +6,3% |
| 2025-04-27 | long | +11,3% | -1,3% | -3,9% | -1,8% | +0,0% | +4,1% | +0,0% |
| 2025-11-30 | short | +11,9% | +1,8% | -7,9% | +0,2% | +0,0% | -0,3% | +0,0% |
| 2026-05-24 | short | +5,7% | -2,0% | -8,4% | -2,4% | -0,0% | +0,0% | +0,0% |
| 2026-08-23 | long | -4,1% | -1,3% | +1,4% | -0,1% | -2,2% | -0,3% | -0,0% |
| 2026-11-15 | short | +5,9% | -1,9% | -3,9% | -4,5% | +0,0% | +0,0% | +0,0% |
| **Somma delle differenze** | | | -61,0% | -173,7% | -63,9% | -14,7% | -17,0% | -2,7% |

Lettura:

- **DCA in ingresso: peggiora sempre.** Entrare in tre giorni costa 61 punti in tutto, in tre settimane 174. Le perdite si
  concentrano sulle operazioni migliori (maggio 2019 −12 e −34 punti, ottobre 2023 −11 e −13), dove il prezzo scappa. Il
  guadagno sulle perdenti è minimo, perché W3.2 le aveva già ridotte.
- **Ordine limite sul ritracciamento: peggiora in 18 operazioni su 23.** Il ritracciamento arriva quasi solo nelle operazioni
  che poi perdono.
- **Uscita in due metà al primo segnale**: fa perdere il rientro successivo (ottobre 2021) e costa 13 punti su gennaio 2021.
- **Target parziale a +2R**: quasi neutro (−2,7 punti in tutto). Scatta poche volte.

### Il trailing diviso in due metà: sembra meglio, non lo è

| Variante | 10.000 $ → (dal 2021) | Max DD | CAGR/DD | Esposizione media all'ingresso | 2021–23: finale | 2024–26: finale | 2018–20: finale / DD | Peggiore |
|---|---|---|---|---|---|---|---|---|
| W3.2: trailing unico a 2,5 ATR | 83.129 | -21,1% | 2,05 | 0,85x | 33.477 | 24.881 | 25.142 / -37% | -4,1% |
| Due metà 1,5 e 2,5 ATR | 96.158 | -17,7% | 2,65 | 0,92x | 36.023 | 26.721 | 22.503 / -34% | -2,4% |
| Due metà 1,25 e 2,5 | 100.219 | -16,3% | 2,94 | 0,94x | 39.882 | 25.155 | 14.859 / -36% | -1,5% |
| Due metà 1,75 e 2,5 | 89.902 | -19,4% | 2,33 | 0,91x | 33.665 | 26.759 | 21.693 / -34% | -3,4% |
| Due metà 2,0 e 2,5 | 82.000 | -20,3% | 2,12 | 0,89x | 32.285 | 25.449 | 26.088 / -38% | -4,4% |
| Due metà 1,5 e 3,0 | 86.332 | -17,8% | 2,48 | 0,89x | 33.098 | 26.111 | 21.420 / -34% | -2,4% |
| Due metà 1,0 e 3,0 | 66.414 | -15,2% | 2,49 | 0,92x | 32.812 | 20.263 | 13.724 / -35% | -0,6% |
| Due metà 2,0 e 3,0 | 72.133 | -19,0% | 2,10 | 0,85x | 30.169 | 23.957 | 25.170 / -37% | -4,4% |
| Trailing unico a 2,0 ATR (stessa dimensione di 1,5 e 2,5) | 61.423 | -36,8% | 0,98 | 0,93x | 24.660 | 24.958 | 27.153 / -38% | -11,9% |
| Trailing unico a 2,25 ATR | 81.867 | -29,7% | 1,44 | 0,90x | 29.918 | 27.419 | 26.054 / -38% | -13,7% |
| Trailing unico a 1,5 ATR | 75.765 | -27,2% | 1,51 | 0,99x | 29.907 | 25.385 | 14.684 / -50% | -10,3% |
| Trailing unico a 3,0 ATR | 64.427 | -19,9% | 1,87 | 0,74x | 29.599 | 21.811 | 22.506 / -36% | -4,0% |

Scomposizione di "due metà 1,5 e 2,5 ATR" dal 2021: rapporto fra capitale finale della variante e di W3.2 1,16; senza le 2 operazioni più favorevoli (2021-01-31 +13,0%, 2024-09-22 +9,5%) 0,99. Esposizione media all'ingresso 0,92x contro 0,85x. Riportando ogni operazione alla dimensione di W3.2 (stima lineare) il rapporto diventa 0,94.

- **In apparenza migliora**: metà posizione con trailing a 1,5 ATR e metà a 2,5 ATR porta 10.000 $ a 96.158 $ invece di
  83.129 $ dal 2021, con drawdown −17,7% invece di −21,1%.
- **Il vantaggio viene dalla dimensione, non dall'uscita.** Il motore calcola la posizione sulla distanza media dei due stop
  (2,0 ATR invece di 2,5), quindi entra fino al 25% più grande. L'operazione di gennaio 2021 esce nello stesso giorno in
  entrambe le versioni e guadagna di più solo perché è più grande. Riportando ogni operazione alla dimensione di W3.2, la
  variante finisce sotto il riferimento.
- **Dipende da due operazioni**: senza gennaio 2021 e settembre 2024 il vantaggio sparisce.
- **Nel 2018–20 peggiora** (22.503 $ contro 25.142 $), e le versioni vicine più strette lì crollano (14.859 e 13.724 $).

Conclusione: nessuna delle 28 varianti a scaglioni provate migliora W3.2.

## 5. La coerenza di W3.2, in regole

**Ingresso**

1. Entra quando il trend è già confermato, non prima: chiusura settimanale oltre la EMA 21 con il flusso a favore.
2. Tutto subito, il lunedì all'apertura. Nessuno scaglione, nessun ordine limite sul ritracciamento.
3. La dimensione la decide la distanza dello stop: più è lontano, meno si entra.
4. Non aggiungere a una posizione che va contro. Nel 2018–20 quattro operazioni su sei andate contro di oltre il 5% nei
   primi 14 giorni hanno chiuso in perdita; dal 2021 il campione è troppo piccolo per dirlo.

**Uscita**

5. La prima uscita utile è la distribuzione: funding alto con il flusso che gira. È quella che chiude vicino ai massimi.
6. Trailing ed EMA 21 sono la rete di sicurezza: accettano di restituire circa 25 punti per restare nei trend lunghi.
7. Tutto insieme: uscire a metà fa perdere i rientri.
8. Dopo l'uscita non si rientra a mano: non c'è evidenza che il prezzo prosegua. Si aspetta il segnale successivo.

**Cosa non fare**

9. Non mediare in perdita e non entrare a scaglioni: nei dati costa da 21.000 a 50.000 $ su 83.000.
10. Non mettere target fissi sull'intera posizione: nel radar il target a +10/15% dimezza il risultato (lezione 109).

## 6. Limiti

- **23 operazioni, 14 con dati reali.** Ogni confronto fra gruppi (5 perdenti, 7 uscite per tipo) poggia su pochissimi casi.
- **Il 2018–20 usa un flusso stimato** e non ha funding per due anni: è un controllo, non una misura.
- **Le varianti DCA sono quelle previste dal motore del radar**; altre forme (per esempio aggiungere solo in guadagno) non
  sono testate qui. Nel radar la piramidazione è già stata respinta (lezione 100).
- **Verifica indipendente**: un secondo agente ha rieseguito le varianti (numeri confermati) e ha corretto tre punti della
  prima stesura: il vantaggio del trailing in due metà è un effetto di dimensione, la finestra dei 28 giorni dopo l'uscita
  era troncata per l'ultima operazione chiusa, e le osservazioni sui primi 14 giorni e sul dopo-uscita poggiano sul 2018–20.
- W3.2 è stata tarata sul periodo dal 2021: le sue stesse regole di uscita sono "in campione".

## 7. Riproducibilità

```bash
python backtest/w32_inout.py
```

```bash
python backtest/build_report.py
```

`vendor/radar_iu_engine.py` è il motore a scaglioni del radar (`research/ingressi_uscite/iu_engine.py`, commit `2ec2afd`)
adattato al rischio 25%. Risultati in `results/w32_inout/`: `anatomia_operazioni.csv`, `varianti_dca.csv`,
`vicini_trailing.csv`.
