## A1 sharpe

Dispersione dello Sharpe annuo fra le varianti provate in questa ricerca: 0,31 fra le 104 soglie di v1, 0,37 fra le 126 varianti di v2. Per la colonna "deflazionato" si assume una dispersione di 0,5 fra i tentativi. Sharpe che il migliore di N tentativi senza abilità raggiunge per caso, su base annua: N=10 → 0,79; N=100 → 1,27; N=1.000 → 1,63.

| Strategia | Anni | Sharpe annuo (settimanale) | Asimmetria | Probabilità che lo Sharpe vero sia > 0 | Deflazionato, 10 tentativi | 100 tentativi | 1.000 tentativi | Anni minimi per esserne certi al 95% |
|---|---|---|---|---|---|---|---|---|
| W3.2 radar, 2018–2026 | 8,9 | 1,19 | 1,6 | 100,0% | 91% | 41% | 7% | 1,5 |
| W3.2 radar, dal 2021 (dati reali) | 5,9 | 1,26 | 1,5 | 100,0% | 90% | 49% | 16% | 1,4 |
| v1 · voto di 17 indicatori, 2018–2026 | 8,9 | 0,91 | 1,1 | 99,8% | 65% | 13% | 1% | 2,9 |
| v1, solo verifica 2022–2026 | 4,9 | 0,64 | 1,4 | 93,3% | 37% | 7% | 1% | 5,9 |
| v2 · tre schermi, 2018–2026 | 8,9 | 0,95 | 1,2 | 99,9% | 70% | 16% | 2% | 2,7 |
| MACD a regime (altcoin), dal 2020 | 6,5 | 1,06 | 1,3 | 99,8% | 78% | 29% | 6% | 2,1 |
| Carry funding selettivo, dal 2021 | 5,9 | 2,84 | 4,1 | 100,0% | 100% | 100% | 100% | 0,1 |
| BTC comprato e tenuto, 2018–2026 | 8,9 | 0,56 | -0,1 | 95,0% | 25% | 2% | 0% | 8,9 |

## B1 kelly

| Campione | Rendimento medio annuo (aritmetico) | Volatilità annua | Leva di Kelly teorica (media / varianza) | Leva che massimizza la crescita nello storico | Crescita annua a 1x | a metà di quella leva | a quella leva | al doppio | Leva oltre cui la crescita diventa negativa |
|---|---|---|---|---|---|---|---|---|---|
| W3.2, 2018–2026 | +39,1% | +31,3% | 4,0x | 3,25x | +40,7% | +59,6% | +82,4% | -100,0% | 5,25x |
| W3.2, dal 2021 | +40,6% | +30,6% | 4,3x | 3,75x | +43,2% | +72,6% | +102,3% | -100,0% | 7,00x |
| W3.2 dal 2021, con il vantaggio dimezzato | +20,3% | +30,6% | 2,2x | 1,50x | +16,9% | +13,4% | +18,5% | +7,5% | 3,50x |

## B2 bootstrap

| Campione | Leva | CAGR mediano a 3 anni | 5° percentile | Probabilità di chiudere in perdita | Drawdown mediano | Probabilità di drawdown oltre −35% | oltre −50% |
|---|---|---|---|---|---|---|---|
| W3.2, 2018–2026 | 0,5x | +21,7% | +3,7% | 2% | -11,4% | 0% | 0% |
| W3.2, 2018–2026 | 1,0x | +44,4% | +5,5% | 3% | -22,1% | 10% | 1% |
| W3.2, 2018–2026 | 1,5x | +62,7% | +2,6% | 4% | -33,3% | 44% | 11% |
| W3.2, 2018–2026 | 2,0x | +79,7% | -2,3% | 6% | -43,5% | 75% | 32% |
| W3.2, 2018–2026 | 3,0x | +104,6% | -16,5% | 10% | -61,3% | 97% | 77% |
| W3.2, dal 2021 | 0,5x | +20,3% | +4,0% | 2% | -11,6% | 0% | 0% |
| W3.2, dal 2021 | 1,0x | +41,1% | +5,9% | 2% | -22,5% | 8% | 1% |
| W3.2, dal 2021 | 1,5x | +57,1% | +2,5% | 4% | -34,0% | 46% | 9% |
| W3.2, dal 2021 | 2,0x | +70,4% | -2,6% | 6% | -44,5% | 79% | 32% |
| W3.2, dal 2021 | 3,0x | +89,4% | -17,8% | 10% | -62,8% | 98% | 81% |

## C1 premio

| Periodo | Giorni | Volatilità implicita media | Realizzata nei 30 giorni dopo | Differenza media | Mediana | Giorni in cui l'implicita è stata più alta | Giorno peggiore (realizzata − implicita) |
|---|---|---|---|---|---|---|---|
| 2019 – 03/2021 (IV approssimata) | 808 | 71% | 70% | 1,2 punti | 3,1 | 56% | 157 punti il 2020-02-29 |
| 03/2021 – 2023 (DVOL) | 1013 | 70% | 58% | 11,8 punti | 12,5 | 74% | 41 punti il 2021-04-28 |
| 2024 – 2026 (DVOL) | 1028 | 49% | 44% | 4,8 punti | 8,4 | 68% | 46 punti il 2026-01-28 |
| Tutto | 2849 | 63% | 57% | 6,3 punti | 9,0 | 67% | 157 punti il 2020-02-29 |

Correlazione fra il premio (implicita − realizzata dopo) e il rendimento di BTC negli stessi 30 giorni: 0,06. Con il valore assoluto del rendimento: -0,37.

## C2 strategie

| Strategia (scadenze a 30 giorni, 4 comparti sfalsati) | 10.000 $ → | CAGR | Max DD | Sharpe | Mese peggiore | Cicli in guadagno | CAGR / DD 2019–03/2021 | CAGR / DD 03/2021–2023 | CAGR / DD 2024–2026 |
|---|---|---|---|---|---|---|---|---|---|
| Straddle venduto alla pari, 1x | 1.358 | -22,4% | -93,3% | -0,32 | -42,0% | 57% di 380 | -63% / -93% | +11% / -39% | -3% / -37% |
| Straddle venduto, 0,25x | 7.568 | -3,5% | -39,6% | -0,31 | -10,6% | 57% di 380 | -17% / -40% | +5% / -9% | +0% / -10% |
| Straddle venduto con copertura giornaliera del delta, 1x | 26.056 | +13,0% | -25,4% | 0,96 | -12,7% | 61% di 380 | +5% / -25% | +23% / -14% | +11% / -7% |
| · controllo: senza funding (copertura con il future della stessa scadenza) | 35.410 | +17,4% | -20,3% | 1,28 | -9,3% | 63% di 380 | +13% / -20% | +28% / -14% | +13% / -7% |
| Straddle coperto, solo se implicita > realizzata passata | 18.846 | +8,4% | -14,6% | 0,80 | -8,0% | 59% di 282 | +6% / -15% | +14% / -15% | +6% / -6% |
| Straddle coperto, solo se implicita sopra la sua mediana a un anno | 24.757 | +12,2% | -11,8% | 1,58 | -6,1% | 76% di 138 | +16% / -12% | +13% / -12% | +10% / -6% |
| Strangle ±15% con copertura giornaliera del delta, 1x | 14.614 | +4,9% | -28,5% | 0,48 | -15,6% | 63% di 380 | -5% / -29% | +16% / -11% | +3% / -6% |
| Strangle venduto ±15%, 1x | 2.210 | -17,5% | -87,2% | -0,32 | -35,4% | 72% di 380 | -52% / -87% | +12% / -30% | -7% / -30% |
| Strangle ±15%, solo se implicita > realizzata passata | 5.740 | -6,8% | -56,4% | -0,16 | -21,6% | 72% di 282 | -22% / -56% | +8% / -25% | -7% / -24% |
| Put venduta −10% con liquidità a garanzia | 24.407 | +12,0% | -39,4% | 0,61 | -17,5% | 84% di 380 | +23% / -39% | +12% / -32% | +5% / -24% |
| Put venduta −10%, solo sopra la SMA 200 | 19.400 | +8,8% | -27,6% | 0,66 | -15,5% | 85% di 220 | +15% / -28% | +5% / -23% | +8% / -8% |
| BTC + call venduta +10% (covered call) | 84.874 | +31,3% | -56,2% | 0,86 | -30,0% | 66% di 380 | +94% / -50% | +8% / -56% | +17% / -44% |
| BTC comprato e tenuto (riferimento) | 205.074 | +46,8% | -76,6% | 0,94 | -37,3% | 57% di 380 | +242% / -63% | -7% / -77% | +19% / -53% |

## C3 insieme

| Combinazione (ribilanciata ogni giorno, dal 2019) | CAGR | Max DD | Sharpe | Correlazione mensile con W3.2 |
|---|---|---|---|---|
| W3.2 da sola | +48,5% | -37,3% | 1,39 | – |
| 80% W3.2 + 20% liquidità (riferimento) | +38,3% | -30,7% | 1,39 | – |
| 80% W3.2 + 20% straddle venduto con copertura giornaliera del delta, 1x | +42,1% | -31,1% | 1,51 | -0,27 |
| 80% W3.2 + 20% put venduta −10% con liquidità a garanzia | +42,3% | -30,6% | 1,49 | 0,11 |
| 80% W3.2 + 20% put venduta −10%, solo sopra la sma 200 | +40,7% | -32,6% | 1,43 | 0,34 |

## D1 opzioni

Operazioni di W3.2 dal 2019-01-06 (prima non c'è volatilità implicita): 20. A ogni ingresso si compra un'opzione alla pari (call per i long, put per gli short) spendendo una quota fissa del capitale; si rivende quando W3.2 esce, o si incassa il valore a scadenza. Costo denaro-lettera: 4% del premio per lato.

| Versione | Capitale finale da 10.000 $ | Operazioni in guadagno | Operazione peggiore | Operazione migliore | Perdita massima per operazione | Capitale composto nelle sole perdenti consecutive peggiori |
|---|---|---|---|---|---|---|
| W3.2 originale (spot e perp) | 246.794 | 85% | -17,9% | +52,2% | fino a −25% (stop) | -20,0% |
| W3.1 (stessi segnali, rischio 10% allo stop) | 49.142 | 85% | -7,2% | +24,6% | fino a −10% (stop) | -8,1% |
| Opzione a 90 giorni, 3% del capitale per operazione | 21.946 | 70% | -2,9% | +12,1% | −3% | -3,2% |
| Opzione a 90 giorni, 6% del capitale per operazione | 45.059 | 70% | -5,9% | +24,3% | −6% | -6,5% |
| Opzione a 90 giorni, 10% del capitale per operazione | 107.767 | 70% | -9,8% | +40,5% | −10% | -10,7% |
| Opzione a 180 giorni, 3% del capitale per operazione | 15.842 | 60% | -2,7% | +8,2% | −3% | -2,9% |
| Opzione a 180 giorni, 6% del capitale per operazione | 24.372 | 60% | -5,5% | +16,4% | −6% | -5,8% |
| Opzione a 180 giorni, 10% del capitale per operazione | 41.577 | 60% | -9,2% | +27,4% | −10% | -9,7% |

## D2 dettaglio

| Operazione W3.2 | Verso | Entra | Esce | W3.2 originale | Con opzione a 90 giorni (6% del capitale) |
|---|---|---|---|---|---|
| 1 | long | 2019-05-13 | 2019-06-27 | +51,1% | +21,3% |
| 2 | long | 2020-02-10 | 2020-02-17 | -2,6% | -0,6% |
| 3 | short | 2020-03-16 | 2020-04-27 | -17,9% | -5,9% |
| 4 | long | 2020-05-04 | 2020-08-03 | +16,0% | +7,4% |
| 5 | long | 2020-10-26 | 2020-11-23 | +40,8% | +18,2% |
| 6 | long | 2020-12-14 | 2020-12-31 | +50,4% | +22,6% |
| 7 | long | 2021-02-01 | 2021-02-22 | +52,2% | +13,7% |
| 8 | long | 2021-08-02 | 2021-09-27 | +4,3% | -1,0% |
| 9 | long | 2021-10-04 | 2021-11-08 | +20,9% | +5,8% |
| 10 | short | 2022-01-03 | 2022-03-28 | +1,0% | -4,4% |
| 11 | short | 2022-08-15 | 2023-01-16 | +8,3% | +6,7% |
| 12 | long | 2023-01-23 | 2023-08-17 | +13,3% | +4,6% |
| 13 | long | 2023-10-23 | 2024-01-01 | +40,5% | +17,6% |
| 14 | long | 2024-02-12 | 2024-03-11 | +42,2% | +18,9% |
| 15 | long | 2024-09-23 | 2025-02-26 | +30,8% | +24,3% |
| 16 | long | 2025-04-28 | 2025-10-10 | +11,3% | +9,6% |
| 17 | short | 2025-12-01 | 2026-04-27 | +11,9% | +9,5% |
| 18 | short | 2026-05-25 | 2026-08-20 | +5,7% | +1,8% |
| 19 | long | 2026-08-24 | 2026-11-09 | -4,1% | -5,0% |
| 20 | short | 2026-11-16 | aperta | +5,9% | -0,4% |

## E1 sforzo

| Movimento di BTC in un giorno | Volatilità implicita 50% → 50% | 50% → 80% | 50% → 120% |
|---|---|---|---|
| fermo | +0,2% | -6,5% | -15,4% |
| +5% | -0,5% | -7,1% | -16,1% |
| -5% | -0,5% | -6,8% | -15,3% |
| +10% | -2,4% | -8,5% | -17,3% |
| -10% | -2,7% | -8,0% | -15,9% |
| +20% | -8,9% | -13,3% | -21,1% |
| -20% | -10,3% | -13,1% | -18,9% |
| -30% | -20,3% | -21,2% | -24,5% |
| -40% | -30,9% | -31,0% | -32,3% |

Premio incassato all'apertura: 11,4% del controvalore. Guadagno massimo se BTC resta fermo fino a scadenza: lo stesso 11,4%.

## E2 esame

| Serie | Anni | Sharpe annuo (settimanale) | Asimmetria | Giorno peggiore | Settimana peggiore | Probabilità che lo Sharpe vero sia > 0 | Deflazionato, 10 tentativi | 100 tentativi |
|---|---|---|---|---|---|---|---|---|
| Straddle coperto, 2019–2026 | 7,9 | 0,80 | -2,3 | -13,9% | -17,6% | 97,6% | 52% | 13% |
| Straddle coperto, solo DVOL (dal 24/03/2021) | 5,7 | 1,23 | -2,0 | -8,2% | -12,7% | 99,3% | 81% | 47% |
| Straddle coperto, 2024–2026 | 2,9 | 1,23 | -1,0 | -3,6% | -5,0% | 97,1% | 75% | 48% |

## E3 segnali

| Segnale la domenica | Settimane | BTC nelle 4 settimane dopo: terzo basso del segnale | terzo medio | terzo alto | Correlazione col rendimento, 2019–2022 | 2023–2026 | Correlazione col premio poi incassato (implicita − realizzata dopo), 2019–2022 | 2023–2026 |
|---|---|---|---|---|---|---|---|---|
| Inclinazione: put lontane − call lontane (punti di volatilità) | 408 | +7,4% | +1,1% | +5,2% | -0,02 | -0,03 | 0,12 | -0,13 |
| Livello della volatilità implicita (posizione nelle 52 settimane prima) | 357 | +2,8% | +1,3% | +8,0% | 0,21 | 0,05 | 0,40 | 0,33 |
| Premio atteso: implicita − realizzata dei 30 giorni prima | 408 | +7,7% | +2,7% | +3,2% | -0,12 | -0,04 | -0,01 | -0,11 |
| Volumi: put / call | 408 | +4,6% | +5,3% | +3,8% | -0,06 | -0,02 | -0,02 | 0,05 |

Rendimento medio di BTC a 4 settimane su tutte le domeniche: +4,6%. Le finestre si sovrappongono (4 settimane su dati settimanali): le osservazioni indipendenti sono circa 102 per l'intero periodo, la metà per ogni sottoperiodo; una correlazione sotto 0,2 in valore assoluto non è distinguibile dal caso.
