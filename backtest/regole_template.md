# Analisi tecnica · come funziona, regole verificate e nuovo algoritmo

Ciclo di studio sull'analisi tecnica: come funziona secondo le fonti, quali regole reggono sui dati di BTC dal 2018, un nuovo
algoritmo costruito su quelle basi, il confronto con quello già fatto e la spiegazione di ogni operazione.
Data: 23/11/2026. Seguito di [`ANALISI_BTC.md`](ANALISI_BTC.md).

> Ricerca su dati storici, non una raccomandazione d'investimento.

## 1. Sintesi

**Il nuovo algoritmo a tre schermi (v2) non batte quello a voto (v1); usati insieme, metà e metà, danno il drawdown più
basso nel periodo di verifica. Oggi entrambi sono fuori dal mercato.**

| Dal 01/2018 al 22/11/2026 | v1 · voto di 17 indicatori | v2 · tre schermi (nuovo) | 50% v1 + 50% v2 | BTC tenuto |
|---|---|---|---|---|
| 10.000 $ diventano | 184.406 $ | 132.529 $ | 174.578 $ | 45.793 $ |
| Rendimento annuo | +38,8% | +33,7% | +37,9% | +18,7% |
| Max drawdown | −49,4% | −54,1% | −42,7% | −81,2% |
| Operazioni / vincenti | 30 / 47% | 9 / 56% | 25 / 44% | – |
| 2022–26 (verifica): rendimento annuo / drawdown | +17% / −34% | +12% / −33% | +16% / −26% | +5% / −67% |

Cosa ho imparato in questo ciclo:

1. **Regole confermate su BTC in entrambi i periodi**: le rotture dei massimi a 55 giorni, il volume alto come conferma della
   rottura, l'RSI sopra 70 come segno di forza (non di vendita), gli stop larghi e le uscite a trailing.
2. **Regole smentite o non confermate**: comprare il ritracciamento nel trend, le candele giapponesi, vendere la rottura dei
   minimi, il golden e death cross, la struttura a massimi e minimi crescenti come l'ho codificata.
3. **Scegliere i parametri migliori sul passato non serve**: fra le 126 varianti di v2 la correlazione tra il risultato
   2018–21 e quello 2022–26 è −0,04. Conta la struttura della regola, non il parametro.
4. **Perché long o short** si legge in due modi: in v1 dal voto dei 17 indicatori, in v2 da una frase per ogni operazione
   (capitolo 7).

![Confronto](results/regole/confronto.png)

## 2. Come funziona l'analisi tecnica secondo le fonti

| Tema | Idea | Come si traduce in regola |
|---|---|---|
| **Teoria di Dow** | Il mercato ha tre movimenti: primario (oltre un anno), secondario (almeno tre settimane, spesso un terzo o più del movimento precedente), minore. Un trend resta valido fino a un segnale chiaro di inversione. | Si decide prima la direzione sulla scala lunga; si opera solo in quella direzione. |
| **Struttura** | Trend rialzista = massimi e minimi crescenti; ribassista = decrescenti. Per invertire un rialzo servono un massimo più basso e un minimo più basso. | Si confrontano gli ultimi due massimi e gli ultimi due minimi di swing. |
| **Volume** | Il volume deve crescere nella direzione del trend; una divergenza segnala debolezza. | Una rottura conta di più se avviene con volume sopra la media. |
| **Tre schermi (Elder)** | Schermo 1: trend sulla scala lunga. Schermo 2: oscillatore sulla scala media per trovare il ritracciamento contro il trend. Schermo 3: ingresso su una rottura di breve nella direzione del trend. | Tre controlli in sequenza; se il primo non passa, non si guarda il resto. |
| **Rotture (Turtle)** | Ingresso sulla rottura del massimo a 55 giorni, uscita sulla rottura opposta a 20 giorni, stop a 2 ATR, dimensione proporzionale alla volatilità. | Canale di Donchian per l'ingresso; ATR per stop e dimensione. |
| **Chandelier exit (LeBeau)** | Stop mobile appeso al massimo raggiunto, a distanza di un multiplo dell'ATR. | Uscita quando il prezzo chiude sotto il massimo meno k ATR. |
| **Rischio per operazione** | Si decide prima quanto perdere, poi la quantità: capitale × rischio % ÷ distanza dello stop. | La dimensione dipende dallo stop, non dalla convinzione. |
| **Wyckoff** | Ciclo in quattro fasi: accumulo, rialzo, distribuzione, ribasso. È un quadro interpretativo, senza regole meccaniche standard. | Non codificabile in modo univoco: non l'ho testato. |
| **Candele giapponesi** | Figure di una-tre candele che anticiperebbero inversioni. Gli studi danno risultati misti o nulli dopo i costi. | Testate come eventi (capitolo 3). |

Due avvertenze che le fonti stesse danno: Dow non ha mai scritto un sistema di trading, e non ha definito come distinguere
un'inversione da un ritracciamento; quasi tutto il materiale divulgativo su Elder, Turtle e Wyckoff viene da siti di broker
e da script della comunità, non dai testi originali.

## 3. Le regole messe alla prova su BTC

Per ogni condizione: rendimento medio nei giorni successivi e quota di casi positivi, separati per periodo, da confrontare
con la riga di riferimento.

### 3.1 Trend

{{R1}}

### 3.2 Rotture e volume

{{R2}}

### 3.3 Oscillatori

{{R3}}

### 3.4 Scale temporali

{{R4}}

### 3.5 Candele giapponesi

{{R5}}

### 3.6 Verdetti

| Regola classica | Verdetto su BTC 2018–2026 | Evidenza |
|---|---|---|
| Le rotture dei massimi segnano continuazione | **confermata** | dopo una chiusura sopra il massimo a 55 giorni: +8,0% e +3,9% a 20 giorni, contro +3,4% e +1,3% di riferimento |
| Il volume conferma la rottura | **confermata**, su pochi casi | con volume alto +10,8% e +5,6%; con volume normale +6,1% e +2,3% |
| Ipercomprato = vendere | **smentita** | dopo un RSI sopra 70: +8,8% e +5,4%. È un segno di forza |
| Lascia correre i profitti, taglia le perdite | **confermata** | vincita media +51% contro perdita media −9% in v1; le uscite a trailing sono le migliori nello studio sulle altcoin |
| Stop larghi invece che stretti | **confermata** | con chandelier a 3 ATR il rendimento mediano 2018–21 è −8% annuo; a 4–5 ATR è +12% e +22% |
| Opera nella direzione del trend primario | **confermata in parte** | sopra la SMA 200 il rendimento a 20 giorni è migliore solo nel 2022–26; come filtro riduce i drawdown in entrambi i periodi e sulle altcoin è decisivo |
| Ipervenduto = comprare | **debole** | dopo un RSI sotto 30: in media nel 2018–21, meglio della media nel 2022–26, su 14 e 20 casi |
| Massimi e minimi crescenti = trend rialzista | **non confermata** come l'ho codificata | con struttura settimanale "rialzista" i 20 giorni successivi rendono meno della media: la conferma arriva tardi |
| Golden cross e death cross | **non verificabile** | 9 casi per tipo; dopo i death cross il prezzo è salito in media del 15–18% in 90 giorni |
| Vendi la rottura dei minimi | **non confermata** | dopo una chiusura sotto il minimo a 55 giorni: −1,6% e +1,4% |
| Compra il ritracciamento nel trend (secondo schermo di Elder) | **smentita** | −2,7% e −0,1% a 20 giorni, sotto il riferimento |
| Allinea le scale temporali | **non confermata** per il MACD | l'incrocio giornaliero rende di più con la scala settimanale contraria |
| Candele giapponesi | **nessun valore** | tutte le figure entro un punto dal riferimento, con segno che cambia fra i periodi |
| Sentiment estremo al contrario | **smentita** | paura estrema seguita da rendimenti pari o inferiori alla media (`ANALISI_BTC.md`) |
| Compra sul supporto testato | **non confermata** | su 165 altcoin, 44% di successi contro 45% con ingressi casuali (`SWING.md`) |

## 4. Regole per l'analisi tecnica

Regole operative che escono dalle fonti e che i dati di BTC non smentiscono. Sono regole di metodo, non una garanzia di
risultato.

**Lettura del mercato**

1. **Parti dalla scala settimanale.** Chiusura sopra o sotto la media a 40 settimane: decide se cerchi long o stai fermo.
2. **Non comprare con il prezzo sotto la media a 40 settimane.** Sulle altcoin vale anche per BTC: con BTC sotto la sua
   media, i long hanno perso in media il 21%.
3. **Un indicatore solo non basta.** Nessuno dei 20 testati regge da solo come long/short; usa il consenso di più famiglie
   (trend, momentum, rottura, volume).
4. **Leggi gli oscillatori nel verso del trend.** RSI sopra 70 in un rialzo è forza, non un segnale di vendita.
5. **Ignora le singole candele e i livelli di sentiment** come segnali operativi: descrivono, non anticipano.

**Ingresso**

6. **Entra sulla rottura, non sul ritracciamento.** Chiusura sopra il massimo a 55 giorni, nel verso della scala lunga.
7. **Chiedi conferma al volume.** Una rottura con volume oltre una volta e mezza la media a 20 giorni vale di più.
8. **Short solo con consenso quasi totale.** Su BTC gli short hanno reso poco o nulla; servono tutti gli indicatori d'accordo,
   e anche così il vantaggio non è dimostrato.

**Uscita e rischio**

9. **Stop largo, definito all'ingresso**: 4–5 ATR giornalieri. Gli stop stretti peggiorano il risultato.
10. **Esci con un trailing, non con un target.** Lo stop segue il massimo raggiunto; i pochi trade grandi fanno il risultato.
11. **Decidi la perdita prima della quantità.** Quantità = capitale × rischio % ÷ distanza dello stop.
12. **Niente leva oltre 1,5–2x.** Oltre, il rendimento composto scende; per restare entro −35% di drawdown serve stare sotto 1x.

**Metodo**

13. **Aspettati meno del 50% di operazioni vincenti.** Le regole di trend guadagnano con vincite molte volte più grandi
    delle perdite. Un 70% di vincenti si ottiene solo con target vicini e stop lontani, e nei test perde.
14. **Verifica ogni regola su dati non usati per sceglierla**, e non fidarti del parametro migliore: fra le 126 varianti
    di v2, il risultato del primo periodo non dice nulla sul secondo.
15. **Scrivi il motivo di ogni operazione** prima di aprirla. Se non riesci a scriverlo in una frase, non è un segnale.

## 5. Il nuovo algoritmo: v2 a tre schermi

| Schermo | Regola |
|---|---|
| **1 · Marea** (settimanale) | Rialzista se la chiusura settimanale è sopra la media a 40 settimane e la struttura dei massimi e minimi di swing non è ribassista. Ribassista se la chiusura è sotto la media, la media scende da 4 settimane e la struttura è ribassista. Altrimenti neutra: nessuna operazione. |
| **2 · Onda** (giornaliero) | Con marea rialzista: chiusura sopra il massimo dei 55 giorni precedenti. Con marea ribassista: chiusura sotto il minimo a 55 giorni. |
| **3 · Rischio** | Stop iniziale a 5 ATR(22) dall'ingresso. Uscita chandelier: chiusura sotto la chiusura più alta dall'ingresso meno 5 ATR. |
| Esecuzione | Decisione alla chiusura giornaliera, long in spot, short in perp, 1x, costi 0,10% per lato. |

{{V1}}

Cosa dice la griglia:

- **L'ingresso su rottura batte quello su ritracciamento** nel 2018–21 (+42% contro +5% mediano) e ha il drawdown più basso
  in entrambi i periodi. Coincide con il verdetto del capitolo 3.
- **Gli short non migliorano**: nella variante scelta la versione severa non scatta mai; nelle altre fa pochi short e
  peggiora il periodo di verifica; quella simmetrica perde nel 2018–21. v2 è di fatto un algoritmo solo long.
- **Lo stop a 3 ATR è il peggiore.**

## 6. Confronto con quanto già fatto

{{V2}}

Anno per anno:

{{V3}}

Lettura:

1. **v1 resta il migliore fra i due** per rendimento e per risultato nel periodo di verifica. v2 fa poche operazioni (9 in
   nove anni), con più vincenti (56%) ma un drawdown più profondo, perché tiene le posizioni con uno stop molto largo.
2. **I due sbagliano in momenti diversi**: v1 ha sofferto nel 2026 (−21%), v2 nel 2022 (−19%). Insieme, metà e metà, il
   drawdown nel periodo di verifica scende a −26%.
3. **Nessuno dei due raggiunge W3 del repo radar** dal 2021 (+42% annuo, drawdown −21%, 92% di vincenti). W3 usa il flusso
   sul perp oltre al prezzo: è l'informazione in più che fa la differenza su BTC.
4. **Tutti battono il comprare e tenere** soprattutto perché evitano i ribassi del 2018, 2022 e 2026.

## 7. Perché long o short

### 7.1 Tutte le operazioni di v2, con il motivo

{{V4}}

### 7.2 Come leggere v1

In v1 il motivo è il voto: ogni indicatore dice long, short o neutro, e la posizione nasce dal conteggio. Long quando almeno
13 su 17 sono rialzisti; short quando 16 sono ribassisti e nessuno rialzista. La tabella con il voto di oggi, indicatore per
indicatore, è in [`ANALISI_BTC.md`](ANALISI_BTC.md), capitolo 4: 15 short, 2 long, quindi fuori.

### 7.3 Perché oggi nessuna posizione

{{V5}}

- **Non è long** perché il primo schermo non passa: il prezzo è il 15% sotto la media a 40 settimane.
- **Non è short** per due motivi. In v2 la struttura settimanale risulta ancora rialzista: gli ultimi massimi e minimi
  confermati sono quelli del rialzo di settembre, e il nuovo minimo non è ancora confermato. In v1 mancano due voti su 17.
- **Cosa lo farebbe diventare short**: una chiusura sotto 55.130 $ e, in v2, la conferma di un massimo e di un minimo di
  swing più bassi dei precedenti.
- **Cosa lo farebbe diventare long**: il ritorno sopra la media a 40 settimane (circa 72.000 $) e poi una chiusura sopra il
  massimo a 55 giorni.

## 8. Limiti

- **v2 ha solo 9 operazioni**: ogni numero che lo riguarda è molto incerto.
- **Le verifiche del capitolo 3 usano pochi casi** in diverse righe (da 2 a 40); le ho indicate. I verdetti "confermata"
  riguardano BTC dal 2018, non i mercati in generale.
- **La struttura di Dow è codificata in un solo modo** (punti di swing su 3 settimane per lato): un'altra definizione può
  dare un verdetto diverso.
- **Non ho costruito una terza versione con le regole confermate** (rottura con volume, RSI forte): l'avrei disegnata
  guardando anche il periodo di verifica. È un'ipotesi da seguire su carta, non un risultato.
- Wyckoff, linee di tendenza e figure grafiche (testa e spalle, triangoli) non sono testati: non hanno una definizione
  meccanica univoca.
- Dati, costi ed esecuzione come in `ANALISI_BTC.md`. Tasse non considerate.

## 9. Riproducibilità

```bash
python backtest/btc_rules.py
```

```bash
python backtest/build_report.py
```

Codice: `backtest/btc_v2.py` (i tre schermi e il registro dei motivi), `backtest/btc_rules.py` (verifiche, griglia,
confronto), `backtest/btc_ta.py` (indicatori e v1). Risultati in `results/regole/`: `operazioni_v2.csv` (con i motivi),
`griglia_v2.csv`.

## Fonti

- Teoria di Dow: [Britannica](https://britannica.com/topic/Dow-theory) · [Forex.com — Dow theory explained](https://www.forex.com/en-sg/news-and-analysis/dow-theory-explained/) · [BabyPips](https://www.babypips.com/forexpedia/dow-theory) · [IG](https://ig.com/ae/trading-strategies/dow-theory-explained--what-is-it-and-what-are-its-principles-180823)
- Tre schermi di Elder: [Admiral Markets](https://admiralmarkets.com/education/articles/forex-strategy/triple-screen-trading-system) · [DailyForex](https://dailyforex.com/forex-articles/2020/09/elder-triple-screen-system/151378) · [RoboForex](https://roboforex.com/blog/education/triple-screen-trading-system-how-to/)
- Turtle, Donchian e chandelier exit: [TakeProfit — Turtle trading system](https://takeprofitapp.com/en/learn/turtle-trading-system) · [Groww — What is turtle trading](https://groww.in/blog/turtle-trading) · [LuxAlgo — Chandelier exit](https://www.luxalgo.com/library/indicator/chandelier-exit.md) · [NexusFi — Chandelier exit](https://nexusfi.com/a/indicators/chandelier-exit)
- Wyckoff: [Binance Academy](https://www.binance.com/ro/academy/articles/the-wyckoff-method-explained) · [CMC Markets](https://www.cmcmarkets.com/en-gb/trading-strategy/what-is-wyckoff-method)
- Candele giapponesi: [Caginalp, Laurent — The predictive power of price patterns (1998)](https://econpapers.repec.org/RePEc:taf:apmtfi:v:5:y:1998:i:3-4:p:181-205) · [studio sulla borsa di Johannesburg](https://open.uct.ac.za/bitstreams/e6c53889-2344-4794-8d72-5f41177a3f36/download) · [studio su hammer e shooting star, S&P 500](https://www.dlsu.edu.ph/wp-content/uploads/pdf/conferences/research-congress-proceedings/2019/ebm-I-002.pdf)
- Letteratura sulla redditività delle regole tecniche: vedi le fonti di [`ANALISI_BTC.md`](ANALISI_BTC.md).
