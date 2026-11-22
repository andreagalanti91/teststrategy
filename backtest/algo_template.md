# Algoritmo "MACD a regime" · costruito sui dati

Hai chiesto di costruire io la regola, senza le tue risposte. L'ho ricavata dai dati: tutti i segnali MACD settimanali di 165
monete, le condizioni che separano i trade buoni dai cattivi, poi una regola completa testata come portafoglio.
Data: 22/11/2026. Seguito di [`SWING.md`](SWING.md).

> Ricerca su dati storici, non una raccomandazione d'investimento.

## 1. Sintesi

**L'algoritmo è il tuo MACD settimanale con due filtri di trend, uno stop e un trailing. Nello storico rende il 34% annuo con
drawdown −33,5% e leva 1x. Non raggiunge il 70% di operazioni vincenti (44%) e dal 2024 rende l'11% annuo.**

| | Risultato dal 06/2020 al 21/11/2026 |
|---|---|
| 10.000 $ diventano | 66.856 $ |
| Rendimento annuo | +34,1% |
| Max drawdown | −33,5% (entro il tuo limite di −35%) |
| Operazioni | 82, circa 13 l'anno; vincenti 44% |
| Vincita media / perdita media | +102% / −16% |
| 2020–23 e 2024–26 | +55% annuo e +11% annuo |
| Stesso risultato su due metà separate delle monete | sì: +40% e +33% annuo, drawdown −28% e −34% |
| Stato oggi | nessuna posizione: BTC è sotto la media a 40 settimane |

Tre cose da sapere prima di usarlo:

1. **Il 70% di vincenti non è compatibile con questa regola.** Guadagna perché le vincite sono sei volte le perdite, non
   perché vince spesso. I cinque trade migliori fanno il 73% del guadagno.
2. **È fermo da due anni.** Il massimo è di dicembre 2024; da allora il capitale è sceso fino a −33,5% (è il drawdown
   massimo di tutto lo storico) e oggi è a −20%: i rialzi delle altcoin sono stati brevi.
3. **Gli short non aggiungono rendimento.** La gamba short da sola fa +1,2% annuo. Il nucleo consigliato è solo long; quando
   il mercato è ribassista sta in liquidità.

Rispetto a W3 del repo radar su BTC (42% annuo, drawdown −21%) è peggiore da solo, ma i due insieme, metà e metà, danno il
39% annuo con drawdown −21%: è la combinazione migliore misurata finora.

![Algoritmo](results/algo/algoritmo.png)

## 2. Le regole

Si guarda la candela settimanale chiusa la domenica alle 00:00 UTC e si opera il lunedì.

| | Regola |
|---|---|
| **Regime** | BTC chiude la settimana sopra la sua media semplice a 40 settimane. Se è sotto: nessun nuovo acquisto. |
| **Monete** | Le 30 con più controvalore scambiato (mediana a 60 giorni), con almeno 40 settimane di storia. La lista si aggiorna ogni settimana. |
| **Ingresso long** | Il MACD (12, 26, 9) settimanale della moneta incrocia al rialzo la linea di segnale **e** la moneta chiude sopra la sua media a 40 settimane. Acquisto spot il lunedì. |
| **Stop** | Chiusura giornaliera a −20% dall'ingresso: si esce. |
| **Trailing** | Chiusura giornaliera a −30% dalla chiusura più alta raggiunta dopo l'ingresso: si esce. |
| **Uscita di segnale** | Il MACD settimanale incrocia al ribasso: si esce il lunedì. |
| **Dimensione** | Ogni posizione vale il 10% del capitale (rischio del 2% allo stop). Massimo 10 posizioni, nessuna leva. |
| **Tetto** | Una posizione che supera il 20% del capitale viene alleggerita al 15%. |
| **Precedenza** | Se i segnali sono più dei posti liberi, entrano le monete più liquide. |

Costi nel test: 0,20% per lato sullo spot. Dati Binance (TAO da Bitget) fino al 21/11/2026.

## 3. Da dove nascono i due filtri

Ho preso tutti gli incroci del MACD settimanale senza filtri e li ho divisi per le condizioni presenti all'ingresso.

{{A8}}

- **I long con BTC sotto la media perdono in entrambi i periodi** (−21% e −22% in media). È il long su SOL a 42 $ di agosto
  2022 che tu hai saltato.
- **I long con moneta e BTC sopra la media sono gli unici positivi in entrambi i periodi** (+114% e +6%).
- **Gli short non hanno una condizione stabile**: positivi dal 2024, negativi prima, con qualunque filtro.
- **Comprare l'inversione dal basso (MACD sotto zero) perde dal 2024.** È il contrario di comprare sul supporto.

## 4. Verifiche

Stessa regola, una modifica per volta:

{{A1}}

- **I filtri contano**: senza, il rendimento scende dal 34% al 26% annuo con il quadruplo delle operazioni.
- **Trailing e tetto riducono il drawdown** da −47% a −33% senza togliere rendimento.
- **I parametri vicini danno risultati simili**: fra il 25% e il 37% annuo con stop, trailing e media diversi. Con 15 monete
  il drawdown scende a −27%; con 60 il rendimento sale al 50% ma con monete meno liquide.
- **Due metà separate delle monete danno lo stesso quadro.** I filtri sono stati scelti guardando tutte le monete, quindi
  non è una prova fuori campione completa, ma esclude che il risultato dipenda da poche monete.

Anno per anno:

{{A2}}

I trade:

{{A3}}

Le operazioni chiuse dal trailing sono le migliori (70% vincenti, +94% medio): è la risposta dei dati a "quando vendere".

## 5. Rischio e leva

{{A4}}

- **Il tuo limite di −35% corrisponde al 2% di rischio per trade senza leva.** Già all'1,5x il drawdown storico è −44%.
- **Il 70% annuo richiede circa 2,5x**, con drawdown intorno a −60%. A 5x il drawdown è −94%.
- Per stare più comodi sotto il limite: rischio 1,5% per trade (25% annuo, drawdown −27%).

Con W3 del repo radar:

{{A5}}

## 6. Su SOL e TAO

Trade che l'algoritmo avrebbe fatto, compresa la gamba short per confronto con le tue operazioni:

{{A6}}

- **Su SOL prende gli stessi tre long che hai fatto tu, con esiti peggiori**: 24 → 84 contro il tuo 20 → 160, 177 → 189
  contro 170 → 200, e il long di maggio 2025 esce in stop a −22% mentre tu hai chiuso a 200. In più fa il long di agosto
  2021 (+148%) che non era fra i tuoi. Non fa i tuoi short del 2021 e del 2025, perché BTC era sopra la media.
- **Su TAO perde**: in quattro trade nessun guadagno vero. TAO si muove in un intervallo, e le regole di trend lì non
  funzionano; è il motivo per cui comprare sul supporto ti ha reso di più.

## 7. Cosa dice oggi

{{A7}}

- **Per TAO**: nessun acquisto. Il prezzo è nella tua zona 150–190, ma moneta e BTC sono sotto la media a 40 settimane. È la
  situazione in cui, nello storico, i long hanno perso in media il 21%.
- **Per rientrare** servono tre cose insieme: BTC sopra 72.160 $ a fine settimana, la moneta sopra la sua media a 40
  settimane e l'incrocio del MACD al rialzo.

## 8. Come usarlo con i tuoi capitali

| Parte | Regola | Con 45.000 $ |
|---|---|---|
| Nucleo spot | l'algoritmo, 10% per posizione, massimo 10 posizioni | 4.500 $ per posizione, perdita allo stop circa 900 $ |
| Leva (2–3 mila $) | stessi segnali, solo sulle 3 monete più liquide, 3x isolato, stop a mercato a −20% | con 2.500 $ a 3x: perdita allo stop circa 1.500 $ |
| W3 su BTC | metà del capitale, se vuoi la combinazione con drawdown più basso | segue il repo radar |
| Fuori regola | acquisti sul supporto come TAO: al massimo una posizione normale (10%), con stop a 126 $ | 4.500 $, non 40–50 mila |

L'ultima riga è il cambiamento più grande rispetto a come hai operato: 40–50 mila $ su una sola moneta sono dieci volte la
dimensione che l'algoritmo assegna a un'operazione.

## 9. Limiti

- **Costruito e testato sugli stessi dati.** I filtri sono stati scelti guardando il 2020–2026; la verifica vera è il
  comportamento da oggi in poi. Consiglio 3–6 mesi su carta, come fa il repo radar.
- **Rendimento concentrato nel 2020–21.** Senza il 2021 (+150%) il rendimento annuo scende molto; dal 2024 è l'11% annuo.
- **Pochi trade grandi.** Cinque operazioni fanno il 73% del guadagno: se ne manchi una, il risultato cambia.
- **Lista di monete scelta da me** (165, con molte poi crollate): distorsione da sopravvivenza ridotta, non eliminata.
- **Esecuzione**: stop e trailing sono calcolati sulla chiusura giornaliera; nei crolli lampo si esce peggio.
- **Tasse non considerate.**
- La gamba short non è validata e non è nel nucleo.

## 10. Riproducibilità

```bash
python backtest/fetch_alts.py alts
```

```bash
python backtest/algo_report.py
```

```bash
python backtest/build_report.py
```

Codice: `backtest/algo.py` (regole e simulatore), `backtest/algo_research.py` (studio dei filtri),
`backtest/algo_report.py` (tabelle e grafico). Risultati in `results/algo/`: `trade_finale.csv` (tutte le operazioni),
`equity_finale.csv`, `trade_macd_tutti.csv` (i 2.381 trade dello studio dei filtri).
