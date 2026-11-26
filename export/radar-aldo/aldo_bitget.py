"""Bitget, futures USDT-M (perpetual): specifiche pubbliche dei contratti, prezzi, arrotondamenti e ordine pronto per la copia
di Aldo. Solo endpoint pubblici (nessuna chiave): Radar non invia ordini.

- Specifiche: GET /api/v2/mix/market/contracts?productType=USDT-FUTURES -> sizeMultiplier (passo della quantita'), minTradeNum
  (quantita' minima), pricePlace + priceEndStep (passo del prezzo = priceEndStep x 10^-pricePlace), volumePlace, minTradeUSDT.
  Su Bitget la quantita' si scrive nella moneta base (BTC, ETH…), in multipli di sizeMultiplier ("contratti").
- Prezzi: GET /api/v2/mix/market/ticker (prezzo ora), /candles (1 minuto, per stimare da quanto Aldo e' dentro),
  /history-candles (1 ora, per il registro sulla carta).
- Dimensione, due modalita' (MODALITA): "importo" = margine fisso in euro con leva fissa (predefinita); "rischio" = perdita allo
  stop pari a RISCHIO_PCT del capitale.
- esegui_su_bitget(): solo punto d'aggancio per un futuro pulsante "Esegui su Bitget". Non implementato e spento.
"""
from __future__ import annotations

import json
import math
import time
import urllib.request
from decimal import ROUND_DOWN, ROUND_HALF_UP, Decimal
from pathlib import Path

import pandas as pd

BASE = "https://api.bitget.com"
PRODOTTO = "USDT-FUTURES"
ORE_CACHE = 24                    # le specifiche cambiano di rado: si riscaricano una volta al giorno


def _get_json(url: str):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "radar"}), timeout=20) as r:
        return json.loads(r.read().decode())


def _dati(risposta) -> list:
    if not isinstance(risposta, dict) or risposta.get("code") not in ("00000", 0, "0"):
        raise RuntimeError(f"Bitget: risposta non valida ({(risposta or {}).get('msg') if isinstance(risposta, dict) else type(risposta).__name__})")
    return risposta.get("data") or []


def simbolo(asset: str) -> str:
    return f"{asset.upper()}USDT"


# ---- specifiche dei contratti ----------------------------------------------------------------------------------------------

def scarica_contratti(get=_get_json) -> dict:
    """Tutte le specifiche USDT-M, per simbolo."""
    return {c["symbol"]: c for c in _dati(get(f"{BASE}/api/v2/mix/market/contracts?productType={PRODOTTO}"))}


def carica_contratti(file) -> dict:
    """Da un file JSON salvato (formato della risposta di Bitget, o {symbol: spec})."""
    d = json.loads(Path(file).read_text(encoding="utf-8"))
    if isinstance(d, dict) and "data" in d:
        return {c["symbol"]: c for c in d["data"]}
    return d


class Contratti:
    """Specifiche con cache su disco (cache_file). Se Bitget non risponde, si usa la cache anche vecchia."""

    def __init__(self, cache_file=None, get=_get_json, dati: dict | None = None):
        self.cache_file = Path(cache_file) if cache_file else None
        self.get = get
        self.dati = dict(dati or {})
        self.scaricato = time.time() if dati else 0.0

    def _aggiorna(self):
        if self.dati and time.time() - self.scaricato < ORE_CACHE * 3600:
            return
        if not self.dati and self.cache_file and self.cache_file.exists():
            self.dati = carica_contratti(self.cache_file)
            self.scaricato = self.cache_file.stat().st_mtime
            if time.time() - self.scaricato < ORE_CACHE * 3600:
                return
        try:
            nuovi = scarica_contratti(self.get)
        except Exception:
            if self.dati:
                return                                     # si resta sulla cache
            raise
        self.dati, self.scaricato = nuovi, time.time()
        if self.cache_file:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            self.cache_file.write_text(json.dumps({"data": list(nuovi.values())}, ensure_ascii=False), encoding="utf-8")

    def spec(self, asset: str) -> dict | None:
        self._aggiorna()
        s = self.dati.get(simbolo(asset))
        return s if s and s.get("symbolStatus", "normal") == "normal" else None


def passo_prezzo(spec: dict) -> Decimal:
    return Decimal(str(spec.get("priceEndStep") or 1)) * Decimal(10) ** -int(spec["pricePlace"])


def arrotonda_prezzo(spec: dict, prezzo: float, verso: str | None = None, tipo: str = "ingresso") -> float:
    """Prezzo al passo di Bitget. Ingresso: al passo piu' vicino. Stop: verso l'esterno (long in giu', short in su), cosi'
    l'arrotondamento non stringe lo stop."""
    p = passo_prezzo(spec)
    x = Decimal(str(prezzo)) / p
    if tipo == "stop" and verso in ("long", "short"):
        q = x.to_integral_value(rounding="ROUND_FLOOR" if verso == "long" else "ROUND_CEILING")
    else:
        q = x.to_integral_value(rounding=ROUND_HALF_UP)
    return float(q * p)


def arrotonda_quantita(spec: dict, quantita: float) -> float:
    """Quantita' in moneta base, per difetto al multiplo di sizeMultiplier (mai sopra la dimensione calcolata). 0 se sotto il minimo."""
    passo = Decimal(str(spec["sizeMultiplier"]))
    q = (Decimal(str(quantita)) / passo).to_integral_value(rounding=ROUND_DOWN) * passo
    q = q.quantize(Decimal(10) ** -int(spec.get("volumePlace", 8)), rounding=ROUND_DOWN)
    return float(q) if q >= Decimal(str(spec["minTradeNum"])) else 0.0


# ---- prezzi ----------------------------------------------------------------------------------------------------------------

def ticker(asset: str, get=_get_json) -> float | None:
    d = _dati(get(f"{BASE}/api/v2/mix/market/ticker?productType={PRODOTTO}&symbol={simbolo(asset)}"))
    return float(d[0]["lastPr"]) if d else None


def _df(righe) -> pd.DataFrame:
    if not righe:
        return pd.DataFrame(columns=["open", "high", "low", "close"], dtype=float)
    df = pd.DataFrame([r[:5] for r in righe], columns=["ts", "open", "high", "low", "close"])
    df.index = pd.to_datetime(df.pop("ts").astype("int64"), unit="ms")
    df.index.name = None
    return df.astype(float).sort_index().loc[lambda x: ~x.index.duplicated(keep="last")]


def candele_minuto(asset: str, get=_get_json, limite: int = 200) -> pd.DataFrame:
    """Ultime candele da 1 minuto (indice UTC senza fuso)."""
    return _df(_dati(get(f"{BASE}/api/v2/mix/market/candles?productType={PRODOTTO}&symbol={simbolo(asset)}&granularity=1m&limit={limite}")))


def candele_ora(asset: str, inizio: pd.Timestamp, fine: pd.Timestamp, get=_get_json) -> pd.DataFrame:
    """Candele orarie fra inizio e fine (history-candles, 200 per chiamata, all'indietro da fine). Stessa firma di
    aldo.candele_okx: si passa a aldo.Prezzi con fonte="bitget"."""
    ms0 = int(pd.Timestamp(inizio).tz_localize("UTC").timestamp() * 1000)
    fino = int(pd.Timestamp(fine).tz_localize("UTC").timestamp() * 1000) + 3_600_000
    righe = []
    for _ in range(500):
        d = _dati(get(f"{BASE}/api/v2/mix/market/history-candles?productType={PRODOTTO}&symbol={simbolo(asset)}&granularity=1H&limit=200&endTime={fino}"))
        if not d:
            break
        righe += d
        primo = min(int(r[0]) for r in d)
        if primo <= ms0 or primo >= fino:
            break
        fino = primo - 1
    return _df(righe)


def minuti_dal_prezzo(c1m: pd.DataFrame, prezzo: float, t_messaggio: pd.Timestamp, tolleranza: float = 0.0015) -> float | None:
    """Da quanti minuti (rispetto al messaggio) il mercato era l'ultima volta al prezzo dichiarato da Aldo: stima del suo ingresso.
    None se nelle candele disponibili non lo tocca mai."""
    if c1m is None or c1m.empty or not prezzo:
        return None
    seg = c1m.loc[:t_messaggio]
    hit = seg[(seg["low"] <= prezzo * (1 + tolleranza)) & (seg["high"] >= prezzo * (1 - tolleranza))]
    if hit.empty:
        return None
    return max(0.0, (t_messaggio - hit.index[-1]).total_seconds() / 60)


# ---- ordine pronto ---------------------------------------------------------------------------------------------------------

def ordine(spec: dict, verso: str, livello: float, stop: float | None, *, modalita: str = "importo", importo_eur: float = 1000.0,
           cambio_eur_usdt: float = 1.08, leva: float = 5.0, leva_max: float = 10.0, capitale_usdt: float = 10_000.0,
           rischio_pct: float = 2.0, stop_mancante: float = 0.02) -> dict:
    """Ordine pronto per Bitget USDT-M, con prezzo e quantita' arrotondati alle specifiche del contratto.
    - modalita "importo": margine = importo_eur x cambio (approssimato), controvalore = margine x leva (leva <= leva_max);
      mostra quanto si perde allo stop in euro e in % del margine; avviso se supera il 50% ("stop troppo lontano per questa leva").
    - modalita "rischio": perdita allo stop = rischio_pct del capitale; leva necessaria = controvalore / capitale, al massimo
      leva_max (se servirebbe di piu' la quantita' si riduce e lo si dice).
    Stop non dichiarato: stop_mancante (2%) oltre il livello, segnalato."""
    note = []
    lv = arrotonda_prezzo(spec, livello)
    stimato = stop is None
    if stimato:
        stop = livello * (1 + stop_mancante if verso == "short" else 1 - stop_mancante)
    st = arrotonda_prezzo(spec, stop, verso, "stop")
    dist = abs(lv - st)
    if dist <= 0 or (verso == "long" and st >= lv) or (verso == "short" and st <= lv):
        return {"errore": "stop dalla parte sbagliata del livello"}
    if modalita == "importo":
        leva_usata = min(max(leva, 1.0), leva_max)
        if leva > leva_max:
            note.append(f"leva {leva:g}x oltre il tetto: uso {leva_max:g}x")
        margine = importo_eur * cambio_eur_usdt
        q = arrotonda_quantita(spec, margine * leva_usata / lv)
    else:
        rischio_usdt = capitale_usdt * rischio_pct / 100
        q_teorica = rischio_usdt / dist
        leva_nec = q_teorica * lv / capitale_usdt
        if leva_nec > leva_max:
            q_teorica = leva_max * capitale_usdt / lv
            note.append(f"servirebbe leva {leva_nec:.1f}x, oltre il tetto di {leva_max:g}x: quantità ridotta")
        q = arrotonda_quantita(spec, q_teorica)
        margine = None
    if q <= 0:
        return {"errore": f"quantità sotto il minimo di Bitget ({spec['minTradeNum']} {spec.get('baseCoin', '')})"}
    controvalore = q * lv
    if controvalore < float(spec.get("minTradeUSDT") or 0):
        return {"errore": f"controvalore sotto il minimo di Bitget ({spec['minTradeUSDT']} USDT)"}
    perdita_usdt = q * dist
    out = {"simbolo": spec["symbol"], "verso": verso, "lato": "compra" if verso == "long" else "vendi", "livello": lv, "stop": st,
           "stop_stimato": stimato, "quantita": q, "unita": spec.get("baseCoin") or spec["symbol"].replace("USDT", ""),
           "contratti": int(round(q / float(spec["sizeMultiplier"]))), "passo_quantita": float(spec["sizeMultiplier"]),
           "controvalore_usdt": round(controvalore, 2), "distanza_stop_pct": round(dist / lv * 100, 2),
           "perdita_stop_usdt": round(perdita_usdt, 2), "modalita": modalita, "note": note}
    if modalita == "importo":
        out.update(importo_eur=importo_eur, cambio_eur_usdt=cambio_eur_usdt, margine_usdt=round(margine, 2),
                   leva=round(controvalore / margine, 2), perdita_stop_eur=round(perdita_usdt / cambio_eur_usdt, 2),
                   perdita_stop_pct_importo=round(perdita_usdt / margine * 100, 1))
        if perdita_usdt > 0.5 * margine:
            out["note"].append("stop troppo lontano per questa leva: riduci la leva")
    else:
        out.update(capitale_usdt=capitale_usdt, rischio_pct=rischio_pct, leva=round(controvalore / capitale_usdt, 2),
                   perdita_stop_pct_capitale=round(perdita_usdt / capitale_usdt * 100, 2))
    return out


def esegui_su_bitget(ordine: dict, **_):
    """Punto d'aggancio per un futuro pulsante "Esegui su Bitget" (API privata con chiavi dell'utente, ordine limite + stop).
    NON implementato e spento: oggi l'ordine si mette a mano. Prima di implementarlo servono l'approvazione dell'utente, chiavi
    con il solo permesso di trading (mai prelievo) salvate fuori dal repo, e un limite di importo per ordine."""
    raise NotImplementedError("Esecuzione automatica su Bitget non attiva: l'ordine si mette a mano")
