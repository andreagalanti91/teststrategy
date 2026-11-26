# Aldo: tutte le operazioni, una per una, ed esempio con 10.000 €

Le 55 operazioni a leva del canale (12/05/2023 – 18/03/2024), ricostruite sui prezzi reali. Per ognuna: quanto ha fatto Aldo con
i suoi prezzi, quanto chi lo copiava con ordini limite sui livelli annunciati, quanto chi lo copiava a mercato dopo il messaggio.

> Ricerca su dati storici, non una raccomandazione d'investimento.

## 1. In sintesi

{{O2}}

- **Aldo vince 3 operazioni su 4**, e quando perde perde poco (−1,1% medio sul controvalore). Le vincenti valgono in media
  quasi cinque volte le perdenti.
- **Chi lo copia vince meno spesso** (58% con ordini limite, 44% a mercato), ma vincite e perdite medie sono simili alle sue: la
  differenza è che alcune operazioni vincenti per lui diventano piccole perdite per chi entra dopo.

## 2. Esempio con 10.000 € di capitale

{{O3}}

**Come leggerla, con 1.000 € di margine per operazione:**
- a **5x** chi copiava con ordini limite chiude a 14.600 € (+46%); a mercato a 12.700 € (+27%); Aldo con i suoi prezzi a 19.200 €;
- a **10x**, la leva tipica di Aldo, tutto raddoppia: +92% con ordini limite, ma la perdita peggiore sale a −444 € e il calo
  massimo del capitale al −6% sulle chiusure;
- con il margine fisso non c'è interesse composto: i numeri sono più bassi di quelli con rischio in percentuale del rapporto
  `CONFRONTO_FINALE.md`, ma più vicini a come operi tu.

**Attenzione alla leva 10x**: un movimento contrario del 10% azzera il margine. Nello storico nessuna operazione di Aldo ha
perso più del 4,4% sul controvalore alla chiusura, ma dentro le operazioni il prezzo può essersi mosso di più. Con stop sempre
impostato il rischio è sotto controllo; senza stop, a 10x, no.

## 3. Tutte le operazioni

{{O1}}

## 4. In euro, operazione per operazione

{{O4}}

## 5. Da ora: come lavoriamo sui suoi nuovi post

1. Mi giri lo screenshot del messaggio (e della schermata di Bybit o del grafico se c'è), con l'ora in cui l'hai visto.
2. Ti rispondo con: cosa ha fatto o annunciato Aldo, se è copiabile e come (ordine limite o a mercato, livello, stop, obiettivo
   per chiudere metà), dimensione per 500–1.000 € di margine con leva 5x, quanto perdi allo stop, e un mio parere sul setup
   (contesto di BTC, livelli, W3.2).
3. Registro ogni operazione in `results/aldo_live/registro.csv`: data, asset, verso, livelli, cosa hai fatto tu, esito. Ogni
   tanto ti faccio il punto con le stesse tabelle di questo rapporto, sui post nuovi.

Codice: `backtest/aldo_operazioni.py`. Dati: `results/telegram/`.
