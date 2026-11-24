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

W3.2 2018–2026 con la dispersione misurata invece di 0,5: con 0,37 il deflazionato è 98% / 81% / 49%; con 0,31 è 99% / 91% / 73% (10 / 100 / 1.000 tentativi). I rendimenti settimanali di W3.2 hanno autocorrelazione 0,14: tenendone conto lo Sharpe annuo scende da 1,19 a circa 1,06.

## B1 kelly

| Campione | Rendimento medio annuo (aritmetico) | Volatilità annua | Leva di Kelly teorica (media / varianza) | Leva che massimizza la crescita nello storico | Crescita annua a 1x | a metà di quella leva | a quella leva | al doppio | Leva oltre cui la crescita diventa negativa |
|---|---|---|---|---|---|---|---|---|---|
| W3.2, 2018–2026 | +39,1% | +31,3% | 4,0x | 3,25x | +40,7% | +59,6% | +82,4% | -100,0% | 5,25x |
| W3.2, dal 2021 | +40,6% | +30,6% | 4,3x | 3,75x | +43,2% | +72,6% | +102,3% | -100,0% | 7,00x |
| W3.2 dal 2021, con il vantaggio dimezzato | +20,3% | +30,6% | 2,2x | 1,50x | +16,9% | +13,4% | +18,5% | +7,5% | 3,50x |

## B2 bootstrap

| Campione | Leva | CAGR mediano a 3 anni | 5° percentile | Probabilità di chiudere in perdita | Drawdown mediano | Probabilità di drawdown oltre −35% | oltre −50% |
|---|---|---|---|---|---|---|---|
| W3.2, 2018–2026 | 0,5x | +21,5% | +3,5% | 2% | -13,4% | 0% | 0% |
| W3.2, 2018–2026 | 1,0x | +44,3% | +5,1% | 3% | -25,9% | 16% | 1% |
| W3.2, 2018–2026 | 1,5x | +62,4% | +1,8% | 4% | -38,5% | 62% | 18% |
| W3.2, 2018–2026 | 2,0x | +78,1% | -3,4% | 6% | -49,7% | 91% | 49% |
| W3.2, 2018–2026 | 3,0x | +98,6% | -19,1% | 11% | -68,6% | 100% | 91% |
| W3.2, dal 2021 | 0,5x | +19,8% | +4,1% | 2% | -13,1% | 0% | 0% |
| W3.2, dal 2021 | 1,0x | +40,6% | +6,1% | 2% | -25,1% | 12% | 1% |
| W3.2, dal 2021 | 1,5x | +56,5% | +3,1% | 4% | -37,2% | 60% | 13% |
| W3.2, dal 2021 | 2,0x | +70,4% | -1,7% | 6% | -48,1% | 90% | 44% |
| W3.2, dal 2021 | 3,0x | +89,0% | -17,2% | 11% | -66,4% | 100% | 90% |

## C1 premio

| Periodo | Giorni | Volatilità implicita media (indice DVOL) | Realizzata nei 30 giorni dopo | Differenza media | Mediana | Giorni in cui l'implicita è stata più alta | Giorno peggiore (realizzata − implicita) | Implicita delle opzioni alla pari (stima) | Differenza media alla pari | Giorni in cui è stata più alta |
|---|---|---|---|---|---|---|---|---|---|---|
| 2019 – 03/2021 (IV approssimata) | 808 | 71% | 70% | 1,2 punti | 3,1 | 56% | 157 punti il 2020-02-29 | 71% | 1,2 punti | 56% |
| 03/2021 – 2023 (DVOL) | 1013 | 70% | 58% | 11,8 punti | 12,5 | 74% | 41 punti il 2021-04-28 | 61% | 3,0 punti | 63% |
| 2024 – 2026 (DVOL) | 1028 | 49% | 44% | 4,8 punti | 8,4 | 68% | 46 punti il 2026-01-28 | 46% | 2,0 punti | 62% |
| Tutto | 2849 | 63% | 57% | 6,3 punti | 9,0 | 67% | 157 punti il 2020-02-29 | 59% | 2,1 punti | 60% |

Correlazione fra il premio (implicita − realizzata dopo) e il rendimento di BTC negli stessi 30 giorni: 0,06. Con il valore assoluto del rendimento: -0,37.

## C2 strategie

| Strategia (scadenze a 30 giorni, 6 comparti sfalsati) | 10.000 $ → | CAGR | Max DD | Sharpe | Mese peggiore | Cicli in guadagno | CAGR / DD 2019–03/2021 | CAGR / DD 03/2021–2023 | CAGR / DD 2024–2026 |
|---|---|---|---|---|---|---|---|---|---|
| Straddle venduto alla pari, 1x | 642 | -29,5% | -95,0% | -0,53 | -41,6% | 56% di 569 | -61% / -92% | -13% / -49% | -10% / -40% |
| Straddle venduto, 0,25x | 6.187 | -5,9% | -43,2% | -0,57 | -10,6% | 56% di 569 | -16% / -38% | -2% / -13% | -1% / -11% |
| Straddle venduto con copertura giornaliera del delta, 1x | 10.032 | +0,0% | -26,8% | 0,07 | -11,4% | 54% di 569 | +2% / -27% | -3% / -16% | +2% / -9% |
| · controllo: senza funding (copertura con il future della stessa scadenza) | 13.831 | +4,2% | -21,6% | 0,39 | -7,9% | 56% di 569 | +10% / -22% | +1% / -13% | +3% / -9% |
| · controllo: premio incassato al livello del DVOL (ottimistico) | 23.008 | +11,2% | -26,8% | 0,86 | -11,4% | 60% di 569 | +2% / -27% | +22% / -13% | +10% / -8% |
| Straddle coperto, solo se implicita > realizzata passata | 9.460 | -0,7% | -21,4% | -0,03 | -9,5% | 51% di 358 | +4% / -16% | -4% / -16% | -0% / -8% |
| Straddle coperto, solo se implicita sopra la sua mediana a un anno | 17.836 | +7,6% | -13,3% | 1,10 | -7,1% | 67% di 206 | +16% / -13% | +3% / -13% | +6% / -6% |
| Strangle ±15% con copertura giornaliera del delta, 1x | 8.038 | -2,7% | -28,9% | -0,19 | -15,2% | 54% di 569 | -5% / -29% | -2% / -13% | -2% / -7% |
| Strangle venduto ±15%, 1x | 1.462 | -21,7% | -87,6% | -0,48 | -34,9% | 70% di 569 | -49% / -85% | -6% / -32% | -9% / -31% |
| Strangle ±15%, solo se implicita > realizzata passata | 4.380 | -10,0% | -61,9% | -0,34 | -19,4% | 69% di 358 | -17% / -52% | -6% / -28% | -8% / -26% |
| Put venduta −10% con liquidità a garanzia | 17.808 | +7,6% | -39,1% | 0,44 | -20,1% | 84% di 569 | +25% / -39% | -0% / -33% | +3% / -23% |
| Put venduta −10%, solo sopra la SMA 200 | 16.278 | +6,4% | -33,6% | 0,48 | -18,5% | 86% di 332 | +14% / -34% | +0% / -25% | +7% / -8% |
| BTC + call venduta +10% (covered call) | 61.775 | +26,1% | -60,6% | 0,76 | -32,0% | 65% di 569 | +99% / -49% | -4% / -61% | +15% / -45% |
| BTC comprato e tenuto (riferimento) | 210.946 | +47,4% | -76,6% | 0,95 | -37,3% | 57% di 569 | +241% / -63% | -7% / -77% | +21% / -53% |

## C3 insieme

| Combinazione (ribilanciata ogni giorno, dal 2019) | CAGR | Max DD | Sharpe | Correlazione mensile con W3.2 |
|---|---|---|---|---|
| W3.2 da sola | +48,5% | -37,3% | 1,39 | – |
| 80% W3.2 + 20% liquidità (riferimento) | +38,3% | -30,7% | 1,39 | – |
| 80% W3.2 + 20% straddle venduto con copertura giornaliera del delta, 1x | +38,6% | -31,5% | 1,41 | -0,25 |
| 80% W3.2 + 20% put venduta −10% con liquidità a garanzia | +41,1% | -30,1% | 1,46 | 0,12 |
| 80% W3.2 + 20% put venduta −10%, solo sopra la sma 200 | +40,2% | -32,5% | 1,42 | 0,32 |

## D1 opzioni

Operazioni di W3.2 dal 2019-01-06 (prima non c'è volatilità implicita): 20. A ogni ingresso si compra un'opzione alla pari (call per i long, put per gli short) spendendo una quota fissa del capitale; si rivende quando W3.2 esce, o si incassa il valore a scadenza. Costo denaro-lettera: 4% del premio per lato.

| Versione | Capitale finale da 10.000 $ | Operazioni in guadagno | Operazione peggiore | Operazione migliore | Perdita massima per operazione | Capitale composto nelle sole perdenti consecutive peggiori |
|---|---|---|---|---|---|---|
| W3.2 originale (spot e perp) | 246.794 | 85% | -17,9% | +52,2% | fino a −25% (stop) | -20,0% |
| W3.1 (stessi segnali, rischio 10% allo stop) | 49.142 | 85% | -7,2% | +24,6% | fino a −10% (stop) | -8,1% |
| Opzione a 30 giorni, 6% del capitale per operazione | 72.223 | 75% | -6,0% | +40,9% | −6% | -8,5% |
| Opzione a 30 giorni, 10% del capitale per operazione | 216.082 | 75% | -10,0% | +68,1% | −10% | -13,9% |
| Opzione a 90 giorni, 6% del capitale per operazione | 44.763 | 65% | -5,9% | +25,8% | −6% | -7,3% |
| Opzione a 90 giorni, 10% del capitale per operazione | 106.384 | 65% | -9,8% | +42,9% | −10% | -12,0% |
| Opzione a 180 giorni, 6% del capitale per operazione | 22.173 | 50% | -5,5% | +16,5% | −6% | -5,8% |
| Opzione a 180 giorni, 10% del capitale per operazione | 35.646 | 50% | -9,2% | +27,5% | −10% | -9,7% |
| Opzione a 30 giorni, 10% del capitale per operazione, pagata al livello del DVOL | 167.639 | 70% | -10,0% | +68,1% | −10% | -13,9% |
| Opzione a 90 giorni, 10% del capitale per operazione, pagata al livello del DVOL | 87.497 | 65% | -9,8% | +40,5% | −10% | -12,2% |

## D2 dettaglio

| Operazione W3.2 | Verso | Entra | Esce | W3.2 originale | Con opzione a 30 giorni (10% del capitale) | Con opzione a 90 giorni (10% del capitale) |
|---|---|---|---|---|---|---|
| 1 | long | 2019-05-13 | 2019-06-27 | +51,1% | +2,1% | +18,0% |
| 2 | long | 2020-02-10 | 2020-02-17 | -2,6% | -2,7% | -1,1% |
| 3 | short | 2020-03-16 | 2020-04-27 | -17,9% | -10,0% | -9,8% |
| 4 | long | 2020-05-04 | 2020-08-03 | +16,0% | -1,8% | +12,3% |
| 5 | long | 2020-10-26 | 2020-11-23 | +40,8% | +56,4% | +30,2% |
| 6 | long | 2020-12-14 | 2020-12-31 | +50,4% | +68,1% | +37,8% |
| 7 | long | 2021-02-01 | 2021-02-22 | +52,2% | +44,1% | +22,8% |
| 8 | long | 2021-08-02 | 2021-09-27 | +4,3% | +9,6% | -1,5% |
| 9 | long | 2021-10-04 | 2021-11-08 | +20,9% | +26,4% | +12,4% |
| 10 | short | 2022-01-03 | 2022-03-28 | +1,0% | +13,5% | -7,5% |
| 11 | short | 2022-08-15 | 2023-01-16 | +8,3% | +12,4% | +13,5% |
| 12 | long | 2023-01-23 | 2023-08-17 | +13,3% | +3,1% | +12,1% |
| 13 | long | 2023-10-23 | 2024-01-01 | +40,5% | +29,0% | +36,1% |
| 14 | long | 2024-02-12 | 2024-03-11 | +42,2% | +62,2% | +34,0% |
| 15 | long | 2024-09-23 | 2025-02-26 | +30,8% | +0,4% | +42,9% |
| 16 | long | 2025-04-28 | 2025-10-10 | +11,3% | +19,2% | +16,9% |
| 17 | short | 2025-12-01 | 2026-04-27 | +11,9% | -6,3% | +16,9% |
| 18 | short | 2026-05-25 | 2026-08-20 | +5,7% | +35,1% | -3,3% |
| 19 | long | 2026-08-24 | 2026-11-09 | -4,1% | +12,8% | -8,4% |
| 20 | short | 2026-11-16 | aperta | +5,9% | -0,4% | -0,6% |

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
| Straddle coperto, 2019–2026 | 7,9 | 0,09 | -2,1 | -12,6% | -16,5% | 59,6% | 3% | 0% |
| Straddle coperto, dal 24/03/2021 | 5,7 | -0,03 | -2,0 | -6,4% | -11,7% | 47,5% | 3% | 0% |
| Con il premio al livello del DVOL, 2019–2026 | 7,9 | 0,72 | -2,1 | -12,6% | -16,5% | 96,6% | 43% | 8% |
| Con il premio al livello del DVOL, dal 24/03/2021 | 5,7 | 1,16 | -1,8 | -6,9% | -11,7% | 99,1% | 78% | 41% |

## E3 segnali

| Segnale la domenica | Settimane | BTC nelle 4 settimane dopo: terzo basso del segnale | terzo medio | terzo alto | Correlazione col rendimento, 2019–2022 | 2023–2026 | Correlazione col premio poi incassato (implicita − realizzata dopo), 2019–2022 | 2023–2026 |
|---|---|---|---|---|---|---|---|---|
| Inclinazione: put lontane − call lontane (punti di volatilità) | 408 | +7,4% | +1,1% | +5,2% | -0,02 | -0,03 | 0,12 | -0,13 |
| Livello della volatilità implicita (posizione nelle 52 settimane prima) | 357 | +2,8% | +1,3% | +8,0% | 0,21 | 0,05 | 0,40 | 0,33 |
| Premio atteso: implicita − realizzata dei 30 giorni prima | 408 | +7,7% | +2,7% | +3,2% | -0,12 | -0,04 | -0,01 | -0,11 |
| Volumi: put / call | 408 | +4,6% | +5,3% | +3,8% | -0,06 | -0,02 | -0,02 | 0,05 |

Rendimento medio di BTC a 4 settimane su tutte le domeniche: +4,6%. Le finestre si sovrappongono (4 settimane su dati settimanali): le osservazioni indipendenti sono circa 102 per l'intero periodo, la metà per ogni sottoperiodo; una correlazione sotto 0,2 in valore assoluto non è distinguibile dal caso.
