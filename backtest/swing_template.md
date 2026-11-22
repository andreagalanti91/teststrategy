# TAO e SOL · le tue operazioni, misurate

Analisi di due modi di operare che hai usato: comprare TAO sul supporto (150–170 → 300–500) e seguire MACD e RSI su SOL
(sette operazioni long/short). Obiettivo: capire se dietro c'è una regola coerente e quando vendere. Data: 22/11/2026.
Ottica dichiarata: speculazione, nessuna posizione tenuta per convinzione, stop sotto 140–120 su TAO, spot 40–50 mila $ più
2–3 mila $ a leva su Bitget.

> Ricerca su dati storici, non una raccomandazione d'investimento.

## 1. Sintesi

**Le due regole hanno funzionato su TAO e su SOL, ma nessuna delle due regge sulle altre monete: non sono un algoritmo
generale. Il tuo vantaggio, per quanto si vede dai dati, sta nella scelta di quali segnali prendere, non nel segnale.**

1. **SOL: i tuoi sette trade sono l'incrocio del MACD settimanale.** La regola meccanica entra e esce quasi ai tuoi stessi
   prezzi. Però la regola fa 15 trade, tu ne hai fatti 7: hai saltato 8 segnali, di cui 6 in perdita. Senza costi la regola
   fa x3,3, i tuoi sette trade x52.
2. **La stessa regola altrove perde.** Su TAO porta il capitale a un decimo. Su 161 altcoin dal 2021 guadagna nel 23% dei
   casi, con capitale finale mediano x0,20. Nessuna variante con RSI o stop supera il 42% di monete in guadagno.
3. **TAO: comprare sul supporto testato non dà vantaggio sulle altre alt.** Su 947 eventi di 165 monete il prezzo arriva a
   +30% prima dello stop nel 44% dei casi; con ingressi in giorni casuali nel 45%. TAO è un'eccezione: 5 eventi su 7 a +50%.
4. **Quando vendere**: nessuna regola di uscita è la migliore in entrambi i periodi. Sul campione ampio i target fissi sono
   i peggiori e le uscite che lasciano correre (trailing, media mobile) le migliori in media; su TAO, che si muove in un
   intervallo, è stato il contrario. I rimbalzi si accorciano: il massimo successivo è in mediana il 67% del precedente.
5. **Oggi i tuoi due metodi su TAO sono in disaccordo**: il prezzo è nella zona d'acquisto, ma il MACD settimanale è sotto
   la linea di segnale (la regola è short da 217 $ dal 09/11).
6. **Leva**: con stop a 126 $ da un ingresso a 170 $ la leva massima sensata è 3x. Il 10/10/2025 il perp TAO su Bitget è
   sceso del 62% in giornata: un long a leva aperto più in alto sarebbe stato liquidato prima della chiusura.

![TAO settimanale](results/tao/tao.png)

## 2. SOL: i tuoi trade contro la regola

Regola: long quando il MACD (12, 26, 9) settimanale è sopra la linea di segnale, short quando è sotto; si opera alla chiusura
della settimana. Dati Binance SOLUSDT fino al 10/2026.

{{M1}}

Lettura:

- **Hai preso 7 segnali su 15, tutti nello stesso verso e a prezzi vicini a quelli della regola.** Sei dei tuoi sette sono in
  guadagno e uno in pari.
- **Gli 8 segnali che non hai fatto**: sei in perdita (−68%, −56%, −34%, −27%, −19%, −3%) e due in guadagno (+223% nel 2021 e
  il long aperto ad aprile 2026). È questa selezione che separa x52 da x3,3.
- **Sei uscito meglio della regola negli short**: 200 → 95 contro 204 → 173, e 160 in pari contro −28%.

Non posso ricostruire dai soli sette trade il criterio con cui hai scartato gli altri: è la prima cosa che ti chiedo al
capitolo 8. Senza quel criterio, la regola meccanica da sola non è il tuo metodo.

## 3. La regola MACD/RSI sulle altre monete

Stesse regole, stessi parametri, a 1x sul perp, costi 0,11% per lato e funding 0,01% ogni 8 ore. SOL, BTC ed ETH dal 06/2021,
TAO dal 06/2024.

{{M2}}

Su tutte le altcoin con almeno due anni di storia:

{{M3}}

- **SOL è il caso migliore, non il caso tipico.** Su SOL quasi ogni variante guadagna; su TAO, BTC ed ETH quasi nessuna.
- **Lo stop al 15% è l'unica modifica che migliora in modo costante**: le monete in guadagno passano dal 23% al 39–42%. Resta
  una regola in perdita sulla moneta mediana.
- Le regole long/short battono il "comprare e tenere" nel 57–85% delle monete solo perché tenere le altcoin dal 2021 è andato
  peggio (mediana x0,13): è un confronto con un'alternativa pessima, non un guadagno.
- È lo stesso esito che il tuo repo radar aveva già trovato su BTC, ETH e SOL (MACD settimanale, "non adottato").

Stato attuale della regola (ultima settimana chiusa nei dati):

{{M4}}

## 4. TAO: il supporto testato, misurato su 165 monete

Ho tradotto il tuo schema in una definizione uguale per tutte le monete: un minimo settimanale da cui il prezzo è risalito
di almeno il 60%; quando il prezzo ci torna, acquisto limite al 5% sopra quel livello; stop su chiusura giornaliera il 12%
sotto il minimo più basso della zona (per TAO: 126 $, dentro il tuo intervallo 140–120). Per TAO lo storico è Bitget spot dal
03/2023; per le altre l'archivio Binance, con le monete poi crollate o delistate (LUNA, FTT, SRM e simili) incluse.

{{S1}}

"Arriva a +X%" = il prezzo tocca quel guadagno prima che scatti lo stop. L'ultima riga usa le stesse monete e la stessa
distanza dello stop, ma con ingressi in giorni scelti a caso.

- **Il supporto non aggiunge nulla al caso**: 44% contro 45% a +30%, 33% contro 35% a +50%.
- **Il numero di tocchi non peggiora le probabilità**: al terzo e quarto tocco sono leggermente migliori che al secondo, e
  tornano nella media dal quinto in poi. TAO oggi è al sesto.
- **Il regime di BTC non cambia il risultato.**
- **TAO è molto sopra la media** (71% a +50% su 7 eventi), ma sette eventi su una moneta scelta perché ha funzionato non
  sono una prova.

{{S5}}

Per TAO: il massimo precedente è 341 $. Il 67% di 341 è circa 230 $; i massimi di TAO finora sono scesi al 95%, 72%, 70% e
90% del precedente, cioè fra 240 e 325 $ se il passo resta quello.

## 5. Quando vendere

Stessi ingressi e stesso stop, 19 regole di uscita. La colonna da guardare è il rendimento per 100 giorni di capitale
impegnato, perché tu ragioni per opportunità e il capitale fermo ha un costo.

{{S2}}

{{S3}}

Sui soli eventi di TAO (pochi, da leggere come esempio):

{{S4}}

Conclusioni:

1. **Il risultato tipico di un singolo trade è lo stop**: il rendimento mediano è intorno a −18/−20% con qualunque uscita, e i
   vincenti sono il 25–45%. Il rendimento medio positivo viene da pochi trade molto grandi.
2. **I target fissi tagliano proprio quei pochi trade grandi**: sul campione ampio sono in fondo alla classifica; il target
   +30% ha rendimento medio zero.
3. **Le uscite che lasciano correre sono le migliori in media**: trailing, chandelier e media a 50 giorni sono positive in
   entrambi i periodi, mentre i target fissi sono negativi nel 2019–22. Il vantaggio però si è ridotto molto: dal 2023 tutte
   le regole stanno fra −3% e +7% per operazione.
4. **Su TAO ha vinto il target fisso** (+59% medio con target +100% contro +32% del trailing 25%), perché TAO si muove in un
   intervallo. Vale finché l'intervallo regge, e i massimi si stanno abbassando.
5. **La tua sensazione di "troppo esposto" corrisponde a una regola precisa**: vendere una parte a un target vicino al
   massimo atteso e lasciare il resto a un trailing. È la combinazione che perde meno in entrambi gli scenari.

## 6. Leva su Bitget

{{S6}}

- **Fino a 3x** lo stop a 126 $ scatta prima della liquidazione; a 5x no.
- **I due ingressi liquidati nella tabella erano a 302 $**, fuori dalla tua zona, ma mostrano il rischio: il 10/10/2025 il
  prezzo ha chiuso a 291 $ dopo aver toccato 133 $. Uno stop su chiusura non protegge una posizione a leva da un minimo di
  poche ore; serve uno stop a mercato sull'exchange, che in quei momenti si esegue molto sotto il livello.
- **Dimensione**: con 2.500 $ di margine a 3x controlli 7.500 $; allo stop perdi circa 1.950 $, a +50% guadagni 3.750 $.
- Sullo spot, 45.000 $ con stop a 126 $ da 170 $ sono circa 11.700 $ di perdita se lo stop scatta.

## 7. Proposta per procedere

Non c'è una regola validata da darti. C'è un procedimento che rende le tue operazioni misurabili e limita il danno mentre si
raccolgono i dati. Tutti i livelli sono proposte da confermare.

**A · TAO, se decidi di rientrare (spot)**

| Passo | Regola |
|---|---|
| Ingresso | ordini limite a 190, 170 e 150 $, un terzo ciascuno |
| Stop | chiusura giornaliera sotto 126 $: esci da tutto |
| Prima uscita | metà posizione a 240 $ (70% del massimo precedente di 341 $) |
| Seconda uscita | l'altra metà con trailing del 25% dal massimo di chiusura, attivo da +30% |
| Rottura | con chiusura settimanale sopra 341 $ il trailing passa al 35% |
| Aspettativa | dalle probabilità di base: circa una volta su due si arriva a +30% prima dello stop. Guadagno atteso sottile: ad esempio 0,5 × (+35%) − 0,5 × (−26%) ≈ +5% per operazione |
| Conflitto | il MACD settimanale è ancora short: se vuoi coerenza con il metodo SOL, aspetta l'incrocio al rialzo |

**B · SOL e altre, metodo MACD settimanale**

| Passo | Regola |
|---|---|
| Segnale | incrocio del MACD settimanale, valutato alla chiusura della domenica |
| Filtro | il tuo criterio di selezione, da scrivere prima del prossimo segnale (capitolo 8) |
| Stop | 15% dall'ingresso su chiusura giornaliera; si rientra solo al segnale successivo |
| Monete | solo quelle su cui decidi prima; la regola non va estesa a un paniere di alt |

**C · Leva**: al massimo 3x, margine isolato, solo sulla parte da 2–3 mila $, stop a mercato sull'exchange.

**D · Registro**: ogni segnale preso o scartato va annotato con il motivo. Dopo 15–20 segnali si può misurare se il tuo
filtro vale davvero. Il repo radar ha già un registro dei trade via Telegram che si può riusare.

## 8. Domande

1. **Perché hai saltato gli 8 segnali MACD su SOL?** In particolare il long a 42 $ di agosto 2022 e i due segnali di gennaio
   2025. Guardavi l'RSI, il trend di BTC, la struttura del grafico, le notizie? È il pezzo che manca per scrivere la regola.
2. **I sette trade su SOL sono tutti quelli che hai fatto**, o ci sono operazioni in perdita, anche su altre monete, che non
   hai elencato? Per misurare il tuo vantaggio servono anche quelle.
3. **Mi puoi dare le date** di ingresso e uscita, anche approssimate? Con le date posso confrontare ogni trade con gli
   indicatori di quel momento.
4. **Come uscivi dagli short** prima della regola (95 $ invece di 173 $)? RSI in ipervenduto, un supporto, un target?
5. **Su TAO, quale dei due metodi comanda** quando sono in disaccordo, come adesso?
6. **Qual è la perdita massima in dollari** che accetti su una singola operazione? Con 45.000 $ e stop a 126 $ sono 11.700 $.
7. **Vuoi che testi il tuo filtro** su SOL e sulle altre monete, una volta che me lo descrivi?

## 9. Contesto e fonti

| Tema | Cosa dicono le fonti |
|---|---|
| Bittensor | Primo halving previsto per il 14/12/2025: emissione giornaliera da 7.200 a 3.600 TAO; offerta massima 21 milioni, circa 9,6 milioni in circolazione prima dell'halving. dTAO da febbraio 2025 rende investibili le singole subnet. Le fonti trovate sono precedenti all'halving: l'esito non è verificato. |
| Triangolo discendente | Sul sito di Bulkowski il triangolo discendente può rompere in entrambe le direzioni; le percentuali che circolano (53% al rialzo, 47% al ribasso) vengono da articoli di terzi e non le ho potute verificare sul testo. |
| Sopravvivenza delle altcoin | CoinMarketCap via Fortune (11/2026): quasi due terzi delle 100 maggiori altcoin del 2021 hanno perso oltre il 90%. Blockworks Research: l'86% dei token che avevano battuto BTC nel 2020–21 ha poi perso almeno il 90%. Coerente con la mediana x0,13 di questo studio. |
| Regole di uscita | Fonti per lo più di operatori, risultati misti: i trailing stop aiutano dove c'è momentum e peggiorano altrove; i target stretti spesso falliscono. Nessuna evidenza accademica conclusiva. |

- [The Block — Bittensor halving](https://www.theblock.co/news/ecosystems/2025-12-07-bittensors-halving-tao-price-381638) · [Cointelegraph](https://cointelegraph.com/news/crypto-other-halving-bittensor-maturation-milestone) · [Crypto.com](https://crypto.com/en/market-updates/bittensor-halving-all-you-need-to-know)
- [Bulkowski — ThePatternSite, descending triangles](https://www.thepatternsite.com/BustDescTriangles.html)
- [Fortune — altcoins lost 90%](https://fortune.com/2026/11/06/altcoins-lost-90-percent-coinmarketcap-data/) · [Blockworks Research — One in Twenty-Four](https://app.blockworksresearch.com/unlocked/one-in-twenty-four) · [CoinGecko — how many cryptocurrencies failed](https://www.coingecko.com/research/publications/how-many-cryptocurrencies-failed)
- [Interactive Brokers — Exiting your trades: what works best](https://www.interactivebrokers.com/campus/ibkr-quant-news/exiting-your-trades-what-works-best/) · [StockCharts — momentum rotation and stops](https://stockcharts.com/articles/arthurhill/2017/08/systemtrader---reworking-the-chartcon-momentum-rotation-strategy---cut-your-profits-and-dont-worry-about-stops--.html)

## 10. Limiti

- I tuoi trade su SOL sono ricostruiti dai prezzi che hai indicato, senza date: l'abbinamento ai segnali è mio.
- Le 165 altcoin sono una lista scelta da me di monete quotate su Binance, con molte monete crollate ma non tutte quelle
  esistite: la distorsione da sopravvivenza è ridotta, non eliminata.
- Gli eventi sono concentrati nelle stesse settimane di mercato: 947 eventi non sono 947 prove indipendenti.
- La definizione di "supporto" è una sola, fissata prima dei risultati; altre definizioni possono dare numeri diversi.
- Dati delle alt fino al 10/2026; TAO Bitget fino al 21/11/2026. Funding storico di TAO disponibile solo per 90 giorni.
- Stop simulati sulla chiusura giornaliera: nei crolli lampo l'esecuzione reale è peggiore.

## 11. Riproducibilità

```bash
python backtest/fetch_alts.py
```

```bash
python backtest/support_report.py
```

```bash
python backtest/macd_report.py
```

```bash
python backtest/build_report.py
```

Codice: `backtest/support_study.py` (definizione dell'evento e uscite), `backtest/macd_rsi.py` (regole MACD/RSI),
`backtest/tao_range.py`, `backtest/tao_chart.py`. Risultati in `results/tao/`: `eventi_alt.csv` (tutti gli eventi),
`uscite_alt.csv`, `macd_universo.csv`, `macd_incrocio_per_moneta.csv`.
