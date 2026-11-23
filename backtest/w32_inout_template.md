# W3.2 · quando entra, quando esce, e i controlli con DCA

Analisi delle 23 operazioni di W3.2 (9 nel 2018–20 con flusso stimato, 14 dal 2021 con i dati reali del perp), delle regole
con cui entra ed esce, e prove di ingresso e uscita a scaglioni. Dati fino al 22/11/2026.

> Ricerca su dati storici, non una raccomandazione d'investimento.

## 1. Sintesi

**W3.2 entra tardi e tutta insieme, ed è giusto così: ogni forma di ingresso a scaglioni peggiora il risultato in tutti i
periodi. In uscita la regola migliore è già dentro la strategia (la "distribuzione"); una sola variante è promettente, ma
non passa il 2018–20.**

| Domanda | Risposta dai dati |
|---|---|
| Quando entra? | Con il trend già partito: in mediana il prezzo è il 14% oltre la EMA 21 settimanale. Non compra ritracciamenti. |
| Conviene entrare a scaglioni? | No. Le 7 varianti di DCA in ingresso fanno peggio in tutti e tre i periodi: dal 2021, da 83.129 $ a 33.579–62.371 $. |
| Perché? | Nelle operazioni vincenti il prezzo migliore è quello del primo giorno: aspettare costa. Il DCA aiuta solo sulle perdenti, che sono poche e piccole. |
| Quando esce? | In tre modi, sette volte ciascuno: distribuzione, trailing, chiusura oltre la EMA 21. |
| Quale uscita è la migliore? | La distribuzione: incassa in media +35,7% e restituisce solo 5 punti dal massimo. Trailing ed EMA 21 ne restituiscono 24–27. |
| Esce troppo presto? | No. Dopo l'uscita il prezzo in media non prosegue a favore (−3,5% a 28 giorni); solo 4 uscite su 21 sono seguite da oltre +5%. |
| Conviene uscire a scaglioni? | Uscire metà al primo segnale peggiora. Un target parziale non cambia quasi nulla. Dividere il trailing in due metà (1,5 e 2,5 ATR) migliora dal 2021 ma peggiora nel 2018–20. |

## 2. Quando entra

Le regole: chiusura settimanale oltre la EMA 21 nel verso del trend (SMA 40 ed EMA 20), con il flusso del perp a favore.
Ingresso il lunedì all'apertura, tutto insieme, con esposizione ridotta se lo stop è lontano.

{{I1}}

"Peggior prezzo nei primi 14 giorni" è quanto il prezzo è andato contro l'operazione rispetto all'ingresso. "Giorno del
miglior prezzo" è il giorno, fra i primi 14, in cui si sarebbe entrati al prezzo più favorevole: 0 significa che il primo
giorno era il migliore.

### Cosa hanno in comune gli ingressi

{{I3}}

1. **Entra a trend avviato.** In mediana il prezzo è già il 14% oltre la EMA 21 e il 14% oltre la SMA 40. Non c'è nessun
   ingresso su ritracciamento.
2. **Nelle operazioni in guadagno il prezzo non torna indietro**: il prezzo migliore è quello del giorno d'ingresso, e il
   peggior momento dei primi 14 giorni è in mediana solo −2%.
3. **Le operazioni in perdita si riconoscono presto**: quattro su cinque sono andate contro di almeno il 5% nei primi 14
   giorni. Fra le 8 operazioni con un calo simile, 4 hanno perso; fra le altre 15, una sola.
4. **Le perdenti avevano lo stop più lontano** (mediana −41% contro −27%), quindi W3.2 le aveva già ridotte: esposizione
   0,40–0,62x nelle due perdite maggiori.
5. **Dal 2021 gli ingressi sono più puliti**: distanza dalla EMA 21 dell'11% contro il 23% del 2018–20, e solo il 14% delle
   operazioni scende del 5% nei primi 14 giorni contro il 67%.

Quello che non separa vincenti e perdenti: la distanza dalle medie e la forza del flusso. L'ingresso più esteso dal 2021
(+45% dalla EMA 21, gennaio 2021) è stato il migliore.

## 3. Quando esce

{{I2}}

"Restituito" è la differenza fra la miglior chiusura raggiunta e la mossa incassata. Le ultime due colonne dicono dove
sarebbe andato il prezzo dopo l'uscita, nel verso dell'operazione: positivo significa che uscire è costato.

### Cosa hanno in comune le uscite

{{I4}}

1. **La distribuzione è l'uscita migliore.** Chiude vicino al massimo (5 punti restituiti) e dopo il prezzo scende in media
   del 5,7% a 28 giorni. È la regola che distingue W3.2 dagli algoritmi fatti solo di prezzo.
2. **Trailing ed EMA 21 sono uscite di difesa**: scattano dopo che il prezzo ha già restituito 24–27 punti. L'uscita per EMA
   21 chiude in media in perdita (−2,9%) perché è quella che ferma le operazioni che non sono mai partite.
3. **Dopo l'uscita il prezzo di solito non prosegue.** Le eccezioni sono quattro uscite: novembre 2020 (+23% nei 28 giorni
   dopo), settembre 2021 (+46%), marzo 2022 (+14%, uno short) e agosto 2020 (+5%).
4. **W3.2 restituisce più di metà del movimento**: la somma dei massimi toccati è +792%, quella delle mosse incassate +333%.
   È il costo di restare dentro i trend lunghi, già misurato nel radar (lezione 109).
5. **Le perdenti durano poco**: 14 giorni in mediana contro 86 delle vincenti.

## 4. Controlli con DCA

Stesso motore a scaglioni usato nel radar, con il rischio di W3.2 (25%). Una variante "migliora" solo se ha un rapporto
rendimento/drawdown più alto di W3.2 in tutti e tre i periodi: 2021–23, 2024–26 e 2018–20.

{{I5}}

### Operazione per operazione

Differenza sul capitale rispetto a W3.2, per ogni operazione:

{{I6}}

Lettura:

- **DCA in ingresso: peggiora sempre.** Entrare in tre giorni costa 61 punti in tutto, in tre settimane 174. Le perdite si
  concentrano sulle operazioni migliori (maggio 2019 −12 e −34 punti, ottobre 2023 −11 e −13), dove il prezzo scappa. Il
  guadagno sulle perdenti è minimo, perché W3.2 le aveva già ridotte.
- **Ordine limite sul ritracciamento: peggiora in 18 operazioni su 23.** Il ritracciamento arriva quasi solo nelle operazioni
  che poi perdono.
- **Uscita in due metà al primo segnale**: fa perdere il rientro successivo (ottobre 2021) e costa 13 punti su gennaio 2021.
- **Target parziale a +2R**: quasi neutro (−2,7 punti in tutto). Scatta poche volte.

### L'unica variante promettente: trailing diviso in due metà

{{I7}}

- **Metà posizione con trailing a 1,5 ATR e metà a 2,5 ATR**: dal 2021 porta 10.000 $ a 96.158 $ invece di 83.129 $, con
  drawdown −17,7% invece di −21,1%, e migliora sia nel 2021–23 sia nel 2024–26.
- **Non è solo un effetto della dimensione**: un trailing unico a 2,0 ATR, che usa la stessa esposizione, fa molto peggio
  (61.423 $, drawdown −37%).
- **Ma nel 2018–20 peggiora** (22.503 $ contro 25.142 $), e la versione ancora più stretta (1,25 ATR) lì crolla a 14.859 $.
  Le varianti vicine dal 2021 vanno da 66.414 a 100.219 $: il risultato dipende dal parametro.
- È stata trovata fra 28 varianti provate sugli stessi dati: va trattata come ipotesi da seguire su carta, non come modifica.

## 5. La coerenza di W3.2, in regole

**Ingresso**

1. Entra quando il trend è già confermato, non prima: chiusura settimanale oltre la EMA 21 con il flusso a favore.
2. Tutto subito, il lunedì all'apertura. Nessuno scaglione, nessun ordine limite sul ritracciamento.
3. La dimensione la decide la distanza dello stop: più è lontano, meno si entra.
4. Se nei primi 14 giorni il prezzo va contro di oltre il 5%, l'operazione ha una probabilità su due di chiudere in
   perdita. Non è una regola di uscita (lo stop resta dov'è), ma è il momento in cui non aggiungere.

**Uscita**

5. La prima uscita utile è la distribuzione: funding alto con il flusso che gira. È quella che chiude vicino ai massimi.
6. Trailing ed EMA 21 sono la rete di sicurezza: accettano di restituire circa 25 punti per restare nei trend lunghi.
7. Tutto insieme: uscire a metà fa perdere i rientri.
8. Dopo l'uscita non si rientra a mano: il prezzo in media non prosegue. Si aspetta il segnale successivo.

**Cosa non fare**

9. Non mediare in perdita e non entrare a scaglioni: nei dati costa da 21.000 a 50.000 $ su 83.000.
10. Non mettere target fissi sull'intera posizione: nel radar il target a +10/15% dimezza il risultato (lezione 109).

## 6. Limiti

- **23 operazioni, 14 con dati reali.** Ogni confronto fra gruppi (5 perdenti, 7 uscite per tipo) poggia su pochissimi casi.
- **Il 2018–20 usa un flusso stimato** e non ha funding per due anni: è un controllo, non una misura.
- **Le varianti DCA sono quelle previste dal motore del radar**; altre forme (per esempio aggiungere solo in guadagno) non
  sono testate qui. Nel radar la piramidazione è già stata respinta (lezione 100).
- **Il campanello dei 14 giorni** è un'osservazione fatta dopo, su 8 casi: non è una regola validata.
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
