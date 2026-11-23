# Confronto con W3.2 del radar · tutte le movimentazioni

Gli algoritmi di analisi tecnica su BTC (v1 a voto, v2 a tre schermi, da [`REGOLE_AT.md`](REGOLE_AT.md)) messi a confronto
con W3.2, la strategia in uso nel repo radar dal 22/11/2026. Dati fino al 22/11/2026.

> Ricerca su dati storici, non una raccomandazione d'investimento.

## 1. Sintesi

**W3.2 è migliore di entrambi gli algoritmi tecnici: rende di più, ha meno drawdown e vince più spesso. La combinazione
metà W3.2 e metà v1 rende quanto W3.2 nel periodo intero, ma non la migliora dal 2021.**

| Dal 01/2018 al 22/11/2026 | W3.2 radar | v1 · voto | v2 · tre schermi | 50% W3.2 + 50% v1 |
|---|---|---|---|---|
| 10.000 $ diventano | 209.002 $ | 184.406 $ | 132.529 $ | 223.979 $ |
| Rendimento annuo | +40,8% | +38,8% | +33,7% | +41,9% |
| Max drawdown | −37,3% | −49,4% | −54,1% | −42,1% |
| Operazioni / vincenti | 23 / 78% | 30 / 47% | 9 / 56% | – |
| Dal 2021: rendimento annuo / drawdown | +43% / −21% | +30% / −34% | +17% / −54% | +38% / −21% |
| Posizione oggi | short dal 16/11 | fuori | fuori | – |

- **W3.2 vince dove conta**: dal 2021, con i dati reali del perp, non ha avuto un anno negativo e ha chiuso in guadagno 13
  operazioni su 14.
- **Gli algoritmi tecnici vincono solo nel 2018–20**, quando W3.2 usa un flusso stimato e parte con una perdita del 25% sulla
  prima operazione.
- **La differenza sta negli short e nelle uscite.** W3.2 ha guadagnato su 6 short su 7 (uno ancora aperto); v1 su 3 su 7; v2
  non ne ha fatti. W3.2 esce dai long quando il funding è alto e il flusso gira, prima che il prezzo scenda.
- **Sono quasi sempre dalla stessa parte**: quando W3.2 è long, v1 lo è nell'88% dei giorni; posizioni opposte solo nello
  0,1% dei giorni. Per questo combinarli aggiunge poco.

![Confronto](results/w32/confronto_w32.png)

## 2. Le regole a confronto

| | W3.2 radar | v1 · voto | v2 · tre schermi |
|---|---|---|---|
| Scala | settimanale | giornaliera | settimanale + giornaliera |
| Trend | chiusura sopra la SMA 40 settimane ed EMA 20 in salita | voto di 17 indicatori | chiusura sopra la SMA 40 settimane e struttura non ribassista |
| Ingresso | chiusura oltre la EMA 21 **e flusso del perp a favore** | voto ≥ 0,50 (long) o ≤ −0,90 (short) | chiusura sopra il massimo a 55 giorni |
| Uscita | trailing 2,5 ATR settimanali, chiusura oltre la EMA 21, **distribuzione (funding alto e flusso contrario)** | voto che rientra oltre ±0,25 | chandelier a 5 ATR giornalieri |
| Dimensione | rischio 25% allo stop: esposizione fra 0,4x e 1x | 1x fisso | 1x fisso |
| Dati usati | prezzo, flusso e funding del perp | solo prezzo e volume | solo prezzo |
| Testabile dal | 2021 con dati reali (2018–20 con flusso stimato) | 2018 | 2018 |

## 3. Risultati

{{W1}}

Anno per anno:

{{W2}}

- **2018–20**: v1 e v2 fanno meglio (+58% e +72% annuo contro +36%). W3.2 perde il 25% sulla prima operazione di gennaio
  2018 e il 18% sullo short di marzo 2020. In questo periodo W3.2 usa un flusso stimato dallo spot, non quello del perp.
- **2021–23**: W3.2 e v1 simili per rendimento (+50% e +45%), ma W3.2 con drawdown −19% contro −32%.
- **2024–26**: W3.2 nettamente avanti (+37% annuo contro +14% e +25%). Nel 2026 W3.2 fa +17%, v1 −21%.

## 4. Quanto si somigliano

{{W3}}

- Quando W3.2 è long, gli algoritmi tecnici lo sono quasi sempre. La differenza è nei periodi in cui W3.2 è fuori o short:
  lì v1 resta long nel 29% dei giorni.
- Quando W3.2 è short, v1 è per lo più fuori (68%) e short solo un terzo del tempo: la soglia di v1 per lo short è molto
  severa.

## 5. Movimentazioni di W3.2

Esposizione = quota del capitale impegnata. "Sul capitale" = risultato dopo costi e funding, sull'intero capitale.

{{W4}}

## 6. Movimentazioni di v1 (voto di 17 indicatori)

Esposizione sempre 1x. Risultato dopo costi e funding. La prima riga è una posizione già aperta a fine 2017.

{{W5}}

## 7. Movimentazioni di v2 (tre schermi)

Esposizione sempre 1x. Il motivo di ogni ingresso e uscita è in [`REGOLE_AT.md`](REGOLE_AT.md), capitolo 7.

{{W6}}

## 8. Posizione oggi

{{W7}}

W3.2 è l'unica in posizione: è short dal 16/11 perché il flusso del perp era negativo con il prezzo sotto la EMA 21 e la
media a 40 settimane in calo. Gli algoritmi tecnici non hanno ancora il consenso richiesto per lo short.

## 9. Cosa prendere da questo confronto

1. **Tenere W3.2 come strategia principale.** Nessuno dei due algoritmi tecnici la supera su rendimento, drawdown o
   percentuale di vincenti.
2. **v1 è utile come controllo indipendente**, non come sostituto: usa solo il prezzo, quindi conferma o smentisce W3.2 senza
   dipendere dagli stessi dati. Quando W3.2 è long e il voto è negativo, è un caso raro (12% dei giorni long) da guardare.
3. **La combinazione metà e metà non migliora W3.2 dal 2021** (+38% annuo e −21% contro +43% e −21%). Ha senso solo se si
   teme che il vantaggio del flusso del perp sparisca.
4. **Il vantaggio di W3.2 sono il flusso e l'uscita "distribuzione"**: 7 delle sue 23 operazioni escono così, tutte in
   guadagno tranne una. È anche il suo punto fragile, già segnalato nel radar.

## 10. Limiti

- **W3.2 nel 2018–20 usa un flusso stimato** dal volume spot (il frame lungo del radar): quei tre anni non sono confrontabili
  alla pari con il periodo dal 2021. Le due parti sono unite al 31/12/2020, dove la posizione aperta viene chiusa e riaperta
  dal segnale successivo.
- **Costi leggermente diversi**: W3.2 usa i costi del radar (spot 0,1% + slippage 0,1%; perp 0,05% + 0,1%); v1 e v2 usano
  0,10% per lato. La differenza è di pochi decimi di punto l'anno.
- **Dimensione diversa**: W3.2 riduce l'esposizione quando lo stop è lontano (0,4–1x), v1 e v2 stanno sempre a 1x. Parte del
  drawdown più basso di W3.2 viene da qui.
- **Poche operazioni** per tutte (23, 30 e 9): le percentuali di vincenti sono stime grossolane.
- W3.2 è stata sviluppata guardando il periodo dal 2021; v1 e v2 hanno i parametri scelti sul 2018–21.

## 11. Riproducibilità

```bash
python backtest/w32_compare.py
```

```bash
python backtest/build_report.py
```

`vendor/radar_weekly_w32.py` è `radar/weekly.py` al commit `2ec2afd` del repo radar; `data/btc/f_radar_live.csv.gz` e
`data/btc/f_long_radar.csv.gz` sono i frame del radar. Le movimentazioni sono anche in `results/w32/movimenti_w32.csv`,
`movimenti_v1.csv` e `movimenti_v2.csv`.
