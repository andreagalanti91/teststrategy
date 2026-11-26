"""Servizio permanente sulla VM di radar: legge in tempo reale il canale privato di Aldo con Telethon (account dell'utente, sola
lettura), estrae gli eventi, aggiorna il registro sulla carta e manda su Telegram (bot, chat dell'utente) l'ordine pronto per
Bitget, con i pulsanti "Fatto" e "Salto" che registrano cosa ha fatto l'utente. Radar non invia ordini.

    python -m radar.aldostream accedi     # primo accesso, interattivo (codice di Telegram), una volta sola
    python -m radar.aldostream canali     # elenca id e nome di gruppi e canali (per ALDO_CANALE_ID)
    python -m radar.aldostream prova      # si collega, controlla il canale e il bot, non manda niente
    python -m radar.aldostream            # servizio (systemd: deploy/aldostream.service)

Cosa NON fa: non scrive nel canale, non reagisce, non segna come letti, non entra o esce da chat; non invia ordini.
Testi, foto e registro restano solo sulla VM, nella cartella ALDO_DATI (fuori dal repo). Guida: deploy/ALDOSTREAM.md.

Parametri (variabili d'ambiente, file /etc/aldostream.env):
  TELEGRAM_API_ID, TELEGRAM_API_HASH, ALDO_CANALE_ID, ALDO_SESSIONE, ALDO_DATI      lettura del canale
  TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, ALDO_BOT_TOKEN (bot dedicato, per i pulsanti)  avvisi
  ALDO_AVVISI=1                       invio attivo (solo dopo l'approvazione dei testi; prima: avvisi solo registrati)
  MODALITA=importo|rischio, IMPORTO_EUR (1000, fra 500 e 2000), CAMBIO_EUR_USDT (1,08), LEVA (5), LEVA_MAX (10),
  COPIA_CAPITALE (10000 USDT), RISCHIO_PCT (2), COPIA_MAX_MINUTI (10), COPIA_MAX_SCOSTAMENTO_PCT (0,5), ORDINE_ORE (24),
  ORE_SILENZIOSE ("" = nessuna; es. "23-7"), ALDO_FUSO (Europe/Rome), ALDO_SEZIONE_PUBBLICA (0), ANTHROPIC_API_KEY (facoltativa)
"""
from __future__ import annotations

import json
import os
import sys
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

import aldo as A                    # in radar: from . import aldo as A
import aldo_bitget as B             # in radar: from . import aldo_bitget as B

UTC = timezone.utc
_fmt = A._fmt


def log(*parti):
    print(f"[aldostream {datetime.now(UTC):%H:%M:%S}]", *parti, flush=True)


# ------------------------------------------------------------------------------------------------------------------------------
# Configurazione
# ------------------------------------------------------------------------------------------------------------------------------

def _f(env, k, d):
    try:
        return float(str(env.get(k, d)).replace(",", "."))
    except ValueError:
        return float(d)


@dataclass
class Config:
    api_id: str = ""
    api_hash: str = ""
    canale: str = ""
    sessione: Path = Path("~/.aldostream/aldo").expanduser()
    dati: Path = Path("~/aldo-dati").expanduser()
    bot_token: str = ""
    chat_id: str = ""
    bot_dedicato: bool = False          # ALDO_BOT_TOKEN: bot solo per Aldo, il servizio ne legge i pulsanti
    avvisi_attivi: bool = False
    modalita: str = "importo"
    importo_eur: float = 1000.0
    cambio_eur_usdt: float = 1.08
    leva: float = 5.0
    leva_max: float = 10.0
    capitale_usdt: float = 10_000.0
    rischio_pct: float = 2.0
    stop_mancante: float = A.STOP_MANCANTE
    max_minuti: float = 10.0
    max_scostamento_pct: float = 0.5
    ordine_ore: float = 24.0
    ore_silenziose: str = ""
    fuso: str = "Europe/Rome"
    sezione_pubblica: bool = False
    avvertenze: list = field(default_factory=list)

    @classmethod
    def da_ambiente(cls, env=None) -> "Config":
        env = os.environ if env is None else env
        c = cls(api_id=env.get("TELEGRAM_API_ID", ""), api_hash=env.get("TELEGRAM_API_HASH", ""), canale=env.get("ALDO_CANALE_ID", ""),
                sessione=Path(env.get("ALDO_SESSIONE", "~/.aldostream/aldo")).expanduser(),
                dati=Path(env.get("ALDO_DATI", "~/aldo-dati")).expanduser(),
                bot_token=env.get("ALDO_BOT_TOKEN") or env.get("TELEGRAM_BOT_TOKEN", ""), chat_id=str(env.get("TELEGRAM_CHAT_ID", "")),
                bot_dedicato=bool(env.get("ALDO_BOT_TOKEN")) or env.get("ALDO_PULSANTI_STESSO_BOT") == "1",
                avvisi_attivi=env.get("ALDO_AVVISI", "0") == "1", modalita=env.get("MODALITA", "importo").strip().lower(),
                importo_eur=_f(env, "IMPORTO_EUR", 1000), cambio_eur_usdt=_f(env, "CAMBIO_EUR_USDT", 1.08), leva=_f(env, "LEVA", 5),
                leva_max=_f(env, "LEVA_MAX", 10), capitale_usdt=_f(env, "COPIA_CAPITALE", 10_000), rischio_pct=_f(env, "RISCHIO_PCT", 2),
                max_minuti=_f(env, "COPIA_MAX_MINUTI", 10), max_scostamento_pct=_f(env, "COPIA_MAX_SCOSTAMENTO_PCT", 0.5),
                ordine_ore=_f(env, "ORDINE_ORE", 24), ore_silenziose=env.get("ORE_SILENZIOSE", "").strip(),
                fuso=env.get("ALDO_FUSO", "Europe/Rome"), sezione_pubblica=env.get("ALDO_SEZIONE_PUBBLICA", "0") == "1")
        if c.modalita not in ("importo", "rischio"):
            c.avvertenze.append(f"MODALITA '{c.modalita}' sconosciuta: uso 'importo'")
            c.modalita = "importo"
        if not 500 <= c.importo_eur <= 2000:
            nuovo = min(max(c.importo_eur, 500.0), 2000.0)
            c.avvertenze.append(f"IMPORTO_EUR {c.importo_eur:g} fuori da 500–2000: uso {nuovo:g}")
            c.importo_eur = nuovo
        if c.leva_max > 10:
            c.avvertenze.append(f"LEVA_MAX {c.leva_max:g} oltre 10: uso 10")
            c.leva_max = 10.0
        if c.leva > c.leva_max:
            c.avvertenze.append(f"LEVA {c.leva:g} oltre LEVA_MAX: uso {c.leva_max:g}")
            c.leva = c.leva_max
        return c

    def copia(self) -> dict:
        """Parametri per aldo_bitget.ordine (e per la sezione)."""
        return {"modalita": self.modalita, "importo_eur": self.importo_eur, "cambio_eur_usdt": self.cambio_eur_usdt, "leva": self.leva,
                "leva_max": self.leva_max, "capitale_usdt": self.capitale_usdt, "rischio_pct": self.rischio_pct, "stop_mancante": self.stop_mancante,
                "max_minuti": self.max_minuti, "max_scostamento_pct": self.max_scostamento_pct, "ordine_ore": self.ordine_ore}

    def silenzioso(self, t: datetime) -> bool:
        """Ore silenziose ("23-7", ora locale ALDO_FUSO): l'avviso arriva lo stesso, ma senza suono. Predefinito: nessuna."""
        if not self.ore_silenziose or "-" not in self.ore_silenziose:
            return False
        try:
            a, b = (int(x) for x in self.ore_silenziose.split("-", 1))
        except ValueError:
            return False
        h = t.astimezone(ZoneInfo(self.fuso)).hour
        return (a <= h < b) if a < b else (h >= a or h < b)


# ------------------------------------------------------------------------------------------------------------------------------
# Bot Telegram (API Bot, solo libreria standard; il token non compare mai nei log)
# ------------------------------------------------------------------------------------------------------------------------------

class BotTelegram:
    def __init__(self, token: str, chat_id: str, post=None):
        self.token, self.chat_id = token, str(chat_id)
        self._post = post or self._post_http

    def _post_http(self, metodo: str, dati: dict) -> dict:
        req = urllib.request.Request(f"https://api.telegram.org/bot{self.token}/{metodo}", data=json.dumps(dati).encode(),
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            try:
                return json.loads(e.read().decode())
            except Exception:
                return {"ok": False, "description": f"HTTP {e.code}"}
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            return {"ok": False, "description": type(e).__name__}

    def api(self, metodo: str, **dati) -> dict:
        r = self._post(metodo, dati)
        attesa = ((r or {}).get("parameters") or {}).get("retry_after")
        if not (r or {}).get("ok") and attesa:                      # limite dell'API Bot: si aspetta e si riprova una volta
            time.sleep(min(int(attesa), 60))
            r = self._post(metodo, dati)
        if not (r or {}).get("ok"):
            log(f"bot {metodo}: {str((r or {}).get('description', 'errore'))[:120]}")
        return r or {}

    def invia(self, testo: str, pulsanti=None, silenzioso: bool = False) -> int | None:
        dati = {"chat_id": self.chat_id, "text": testo, "parse_mode": "HTML", "disable_web_page_preview": True, "disable_notification": silenzioso}
        if pulsanti:
            dati["reply_markup"] = {"inline_keyboard": pulsanti}
        r = self.api("sendMessage", **dati)
        return (r.get("result") or {}).get("message_id") if r.get("ok") else None

    def rispondi_pulsante(self, callback_id: str, testo: str):
        self.api("answerCallbackQuery", callback_query_id=callback_id, text=testo[:190])

    def chiudi_avviso(self, message_id: int, testo: str):
        self.api("editMessageText", chat_id=self.chat_id, message_id=message_id, text=testo, parse_mode="HTML",
                 disable_web_page_preview=True, reply_markup={"inline_keyboard": []})

    def aggiornamenti(self, offset: int | None, timeout: int = 30) -> list:
        par = {"timeout": timeout, "allowed_updates": ["callback_query"]}
        if offset:
            par["offset"] = offset
        r = self.api("getUpdates", **par)
        return r.get("result") or [] if r.get("ok") else []


def pulsanti(id_avviso: str, esegui_bitget: bool = False) -> list:
    """Tastiera dell'avviso. "Esegui su Bitget" e' solo un punto d'aggancio: spento (aldo_bitget.esegui_su_bitget non e' implementato)."""
    riga = [{"text": "Fatto", "callback_data": f"aldo:f:{id_avviso}"}, {"text": "Salto", "callback_data": f"aldo:s:{id_avviso}"}]
    out = [riga]
    if esegui_bitget:
        out.append([{"text": "Esegui su Bitget", "callback_data": f"aldo:b:{id_avviso}"}])
    return out


# ------------------------------------------------------------------------------------------------------------------------------
# Testi degli avvisi
# ------------------------------------------------------------------------------------------------------------------------------

def _esc(s) -> str:
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _px(v, spec=None) -> str:
    if v is None:
        return "–"
    return _fmt(v, int(spec["pricePlace"])) if spec else _fmt(v)


def _q(v, spec=None) -> str:
    return _fmt(v, int(spec.get("volumePlace", 4))) if spec else _fmt(v, None)


def _ora(t: datetime) -> str:
    return f"{t.astimezone(UTC):%d/%m %H:%M} UTC"


def righe_ordine(o: dict, spec: dict | None, cfg: Config) -> list[str]:
    """Le righe di dimensione comuni a ordine limite e ingresso a mercato."""
    r = []
    if o.get("modalita") == "importo" and o.get("margine_usdt") is not None:
        r.append(f"Margine {_fmt(o['importo_eur'], 0)} € (≈ {_fmt(o['margine_usdt'], 0)} USDT, cambio {_fmt(o['cambio_eur_usdt'], 2)} approssimato)"
                 f" · leva {_fmt(o['leva'], 1)}x · controvalore {_fmt(o['controvalore_usdt'], 0)} USDT")
        r.append(f"Allo stop perdi ≈ {_fmt(o['perdita_stop_eur'], 0)} € ({_fmt(o['perdita_stop_pct_importo'], 1)}% dell'importo)")
    else:
        r.append(f"Rischio {_fmt(o.get('rischio_pct', cfg.rischio_pct), 1)}% di {_fmt(o.get('capitale_usdt', cfg.capitale_usdt), 0)} USDT"
                 f" = perdita allo stop {_fmt(o.get('perdita_stop_usdt'), 0)} USDT · controvalore {_fmt(o.get('controvalore_usdt'), 0)} USDT"
                 f" · leva {_fmt(o.get('leva'), 1)}x (tetto {_fmt(cfg.leva_max, 0)}x)")
    for n in o.get("note") or []:
        r.append(f"<b>Attenzione</b>: {_esc(n)}")
    return r


def _riga_quantita(o: dict, spec: dict | None) -> str:
    if spec and o.get("contratti") is not None:
        return f"{_q(o['quantita'], spec)} {o['unita']} = {_fmt(o['contratti'], 0)} contratti da {_q(o['passo_quantita'], spec)}"
    return f"{_fmt(o.get('quantita'), None)} {o.get('unita', '')}"


def _riga_stop_obiettivi(o: dict, spec, obiettivi: list) -> list[str]:
    stop = f"Stop {_px(o['stop'], spec)}" + (" (non indicato da Aldo: 2% oltre il prezzo d'ingresso)" if o.get("stop_stimato") else " (dichiarato)")
    r = [stop + f" · distanza {_fmt(o.get('distanza_stop_pct'), 2)}%"]
    if obiettivi:
        r.append(f"Obiettivo 1: {_px(obiettivi[0], spec)} → chiudi metà, poi stop a pareggio"
                 + (f" · poi {' / '.join(_px(t, spec) for t in obiettivi[1:])}" if len(obiettivi) > 1 else ""))
    else:
        r.append("Obiettivi non indicati: segui i suoi messaggi di chiusura")
    return r


PIEDE = "Lo metti tu a mano su Bitget. «Fatto» / «Salto» registrano cosa hai fatto."


# ------------------------------------------------------------------------------------------------------------------------------
# Servizio
# ------------------------------------------------------------------------------------------------------------------------------

class Servizio:
    """Il cuore del servizio, senza Telethon: riceve messaggi nel formato interno di aldo.py e pressioni dei pulsanti.
    Tutte le dipendenze esterne sono iniettabili (bot, specifiche Bitget, prezzi, orologio): nei test sono finte."""

    def __init__(self, cfg: Config, bot: BotTelegram | None = None, contratti: B.Contratti | None = None, prezzo_ora=None,
                 candele_1m=None, prezzi: A.Prezzi | None = None, client_modello=None, orologio=None):
        self.cfg = cfg
        self.bot = bot
        self.dati = Path(cfg.dati)
        (self.dati / "foto").mkdir(parents=True, exist_ok=True)
        self.contratti = contratti or B.Contratti(self.dati / "bitget_contratti.json")
        self.prezzo_ora = prezzo_ora or B.ticker
        self.candele_1m = candele_1m or B.candele_minuto
        self.prezzi = prezzi or A.Prezzi(self.dati / "prezzi", fonte="bitget")
        self.client_modello = client_modello
        self.orologio = orologio or (lambda: datetime.now(UTC))
        self.messaggi = A.carica_json(self.dati / "messaggi.json", [])
        self.registro = A.carica_json(self.dati / "eventi.json", A.registro_vuoto())
        self.avvisi = A.carica_json(self.dati / "avvisi.json", [])
        self.reale = A.carica_json(self.dati / "reale.json", {"scelte": [], "offset": None})
        self._blocco = threading.Lock()

    # ---- stato ----
    def _salva(self):
        A.salva_json(self.dati / "messaggi.json", self.messaggi)
        A.salva_json(self.dati / "eventi.json", self.registro)
        A.salva_json(self.dati / "avvisi.json", self.avvisi)
        A.salva_json(self.dati / "reale.json", self.reale)

    def ultimo_id(self) -> int:
        return max((int(m["id"]) for m in self.messaggi if str(m["id"]).isdigit()), default=0)

    def _latenza(self, riga: dict):
        with open(self.dati / "latenze.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(riga) + "\n")

    def latenze(self) -> list[dict]:
        p = self.dati / "latenze.jsonl"
        return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()] if p.exists() else []

    # ---- prezzi (ogni errore di rete diventa None: l'avviso parte comunque, con meno dettagli) ----
    def _spec(self, asset):
        try:
            return self.contratti.spec(asset)
        except Exception as e:
            log(f"specifiche Bitget {asset}: {type(e).__name__}")
            return None

    def _ora(self, asset):
        try:
            return self.prezzo_ora(asset)
        except Exception as e:
            log(f"ticker Bitget {asset}: {type(e).__name__}")
            return None

    def _c1m(self, asset):
        try:
            return self.candele_1m(asset)
        except Exception as e:
            log(f"candele 1m Bitget {asset}: {type(e).__name__}")
            return None

    # ---- messaggi ----
    def su_messaggio(self, msg: dict, ricevuto: datetime | None = None) -> list[dict]:
        """Un messaggio nuovo del canale: registro, estrazione, avvisi, latenza. Restituisce gli avvisi composti."""
        with self._blocco:
            adesso = self.orologio()
            ricevuto = ricevuto or adesso
            self.messaggi, n = A.unisci(self.messaggi, [msg])
            if not n or msg["id"] in self.registro["elaborati"]:
                return []
            t = A._dt(msg["data"])
            for a in set(A.trova_asset(msg.get("testo", ""))) | {"BTC"} | {e["asset"] for e in A.aperte(self.registro, adesso).values()}:
                try:
                    self.prezzi.aggiorna(a, t - timedelta(days=3), adesso)
                except Exception as e:
                    log(f"candele orarie {a}: {type(e).__name__}")
            self.registro, aggiunti = A.elabora(self.messaggi, self.registro, self.prezzi, client=self.client_modello, adesso=adesso)
            composti = [av for a in aggiunti if (av := self.componi(a, msg, adesso))]
            for av in composti:
                self._invia(av)
            pronto = self.orologio()
            self._latenza({"msg_id": msg["id"], "data_msg": msg["data"], "ricevuto": A._iso(ricevuto), "pronto": A._iso(pronto),
                           "latenza_s": round((pronto - t).total_seconds(), 1), "eventi": [a.get("tipo") for a in aggiunti],
                           "avvisi": len(composti), "inviati": sum(1 for a in composti if a["stato"] == "inviato"),
                           "estrattore": self.registro["elaborati"].get(msg["id"])})
            log(f"messaggio {msg['id']}: {len(aggiunti)} eventi, {len(composti)} avvisi, latenza {(pronto - t).total_seconds():.1f} s")
            self._salva()
        self.aggiorna_carta(adesso)
        return composti

    def su_modifica(self, msg: dict, ricevuto: datetime | None = None) -> list[dict]:
        """Messaggio modificato. Se non aveva prodotto nulla si rilegge da capo (es. "Short" a cui aggiunge il prezzo); se aveva gia'
        prodotto eventi o piani il registro non cambia da solo: avviso informativo e voce "da rivedere"."""
        vecchio = next((m for m in self.messaggi if m["id"] == msg["id"]), None)
        if vecchio is None:
            return self.su_messaggio(msg, ricevuto)
        if vecchio["testo"] == msg["testo"] and vecchio.get("foto") == msg.get("foto"):
            return []
        with self._blocco:
            vecchio.update(testo=msg["testo"], foto=msg.get("foto") or vecchio.get("foto"), modificato=msg.get("modificato"))
            prodotti = [e for e in self.registro["eventi"] if e["msg_id"] == msg["id"]] + [p for p in self.registro["piani"] if p["msg_id"] == msg["id"]]
            if not prodotti:
                self.registro["elaborati"].pop(msg["id"], None)
                self.messaggi = [m for m in self.messaggi if m["id"] != msg["id"]]
        if not prodotti:
            return self.su_messaggio(msg, ricevuto)
        with self._blocco:
            adesso = self.orologio()
            self.registro.setdefault("da_rivedere", []).append({"msg_id": msg["id"], "motivo": "messaggio modificato dopo l'estrazione"})
            p = prodotti[0]
            cosa = f"{A.NOMI_TIPO.get(p.get('tipo'), 'piano')} {p['asset']} {p.get('verso') or ''}".strip()
            av = self._nuovo_avviso({"tipo": "modifica", "asset": p["asset"], "verso": p.get("verso"), "msg_id": msg["id"], "utc": p["utc"], "trade": p.get("trade")},
                                    msg, adesso, f"<b>Aldo ha modificato un messaggio già letto</b> ({_esc(cosa)}).\n"
                                                 "Il registro non cambia da solo: controlla nel canale se livelli o stop sono diversi.", azionabile=False)
            self._invia(av)
            self._salva()
            return [av]

    # ---- composizione ----
    def _nuovo_avviso(self, a: dict, msg: dict, adesso: datetime, testo: str, azionabile: bool, ordine: dict | None = None) -> dict:
        return {"id": None, "tipo": a.get("tipo"), "asset": a.get("asset"), "verso": a.get("verso"), "trade": a.get("trade"),
                "msg_id": a["msg_id"], "data_msg": msg["data"], "creato": A._iso(adesso), "azionabile": azionabile, "testo": testo,
                "ordine": ordine, "stato": None, "telegram_id": None, "scelta": None}

    def _scelta_ingresso(self, trade: str | None) -> dict | None:
        """L'ultima scelta dell'utente sull'avviso d'ingresso di un'operazione (ordine limite sul piano collegato, o ingresso a mercato)."""
        if not trade:
            return None
        piani = {p["msg_id"] for p in self.registro["piani"] if p.get("trade_collegato") == trade}
        cand = [a for a in self.avvisi if a.get("scelta") and a["tipo"] in ("piano", "apertura") and a.get("azionabile")
                and (a.get("trade") == trade or (a["tipo"] == "piano" and a["msg_id"] in piani))]
        return cand[-1] if cand else None

    def componi(self, a: dict, msg: dict, adesso: datetime) -> dict | None:
        """Avviso per un evento o un piano appena estratto. None se non serve (messaggio vecchio, evento senza operazione…)."""
        cfg = self.cfg
        eta_min = (adesso - A._dt(msg["data"])).total_seconds() / 60
        if eta_min > cfg.ordine_ore * 60:
            return None                                            # recupero di messaggi vecchi: solo registro, nessun avviso
        tipo, asset, verso = a.get("tipo"), a.get("asset"), a.get("verso")
        V = (verso or "").upper()
        spec = self._spec(asset)
        px = self._ora(asset)
        testa = lambda titolo: f"<b>Aldo · {asset} {V} · {titolo}</b>".replace("  ", " ")

        if tipo == "piano":
            if not a.get("livello_innesco") or verso not in ("long", "short"):
                return None
            obiettivi = a.get("target") or []
            if not spec:
                return self._nuovo_avviso(a, msg, adesso, testa("nuovo livello") + f"\nLivello {_px(a['livello_innesco'])}, stop {_px(a.get('stop'))}.\n"
                                          f"<b>Attenzione</b>: {asset}USDT non trovato fra i futures USDT-M di Bitget: quantità non calcolata.", False)
            o = B.ordine(spec, verso, a["livello_innesco"], a.get("stop"), **self._kw())
            if o.get("errore"):
                return self._nuovo_avviso(a, msg, adesso, testa("nuovo livello") + f"\nLivello {_px(a['livello_innesco'], spec)}: {_esc(o['errore'])}.", False)
            scade = A._dt(msg["data"]) + timedelta(hours=cfg.ordine_ore)
            r = [testa("nuovo livello"),
                 f"<b>ORDINE LIMITE</b>: {o['lato']} {_riga_quantita(o, spec)} a <b>{_px(o['livello'], spec)}</b> · Bitget {o['simbolo']} (USDT-M)"]
            r += _riga_stop_obiettivi(o, spec, obiettivi)
            r += righe_ordine(o, spec, cfg)
            if px:
                r.append(f"Prezzo ora {_px(px, spec)} (livello a {A._p(round((o['livello'] / px - 1) * 100, 2))}) · ordine valido {_fmt(cfg.ordine_ore, 0)} ore, fino al {_ora(scade)}")
                if (verso == "short" and px >= o["livello"]) or (verso == "long" and px <= o["livello"]):
                    r.append("<b>Attenzione</b>: il prezzo è già oltre il livello: l'ordine limite verrebbe eseguito subito")
            else:
                r.append(f"Ordine valido {_fmt(cfg.ordine_ore, 0)} ore, fino al {_ora(scade)}")
            r.append(PIEDE)
            return self._nuovo_avviso(a, msg, adesso, "\n".join(r), True, o)

        if tipo == "apertura":
            piano = next((p for p in self.registro["piani"] if a.get("trade") and p.get("trade_collegato") == a["trade"]), None)
            if piano:
                txt = (testa("entrato sul livello annunciato") + f"\nAldo è entrato vicino a {_px(piano['livello_innesco'], spec)}, il livello annunciato"
                       f" il {_ora(A._dt(piano['utc']))}.\nSe hai messo l'ordine limite, controlla che sia eseguito e che ci sia lo stop.")
                return self._nuovo_avviso(a, msg, adesso, txt, False)
            return self._ingresso_a_mercato(a, msg, adesso, spec, px, eta_min, testa)

        if not a.get("trade") and tipo != "ordine_non_eseguito":
            return None
        scelta = self._scelta_ingresso(a.get("trade"))
        copiata = ("Risulta copiata da te (Fatto il " + _ora(A._dt(scelta["scelta_alle"])) + ")") if scelta and scelta["scelta"] == "fatto" else \
            ("Non risulta copiata da te" if scelta else "Copia non registrata")
        ora = f"Prezzo ora {_px(px, spec)}." if px else ""
        tua = (scelta or {}).get("ordine") if scelta and scelta["scelta"] == "fatto" else None
        if tipo == "chiusura_parziale":
            q = a.get("quota") or 0.5
            dett = ""
            if tua and spec:
                qt = B.arrotonda_quantita(spec, tua["quantita"] * q)
                dett = f" = {_q(qt, spec)} {tua['unita']} della tua posizione" if qt else ""
            txt = testa(f"chiuso il {q * 100:.0f}%") + f"\n<b>Chiudi il {q * 100:.0f}% a mercato</b>{dett}. {ora}\n{copiata}."
        elif tipo == "stop_pareggio":
            tuo = f" (il tuo: {_px(tua['livello'], spec)})" if tua else ""
            txt = testa("stop a pareggio") + f"\n<b>Sposta lo stop a prezzo d'ingresso</b>{tuo}. {ora}\n{copiata}."
        elif tipo == "stop_spostato":
            if not a.get("stop"):
                return None
            txt = testa("stop spostato") + f"\n<b>Sposta lo stop a {_px(a['stop'], spec)}</b>. {ora}\n{copiata}."
        elif tipo in ("chiusura_totale", "target_preso"):
            dedotta = "dedotta" in str(a.get("note"))
            txt = testa("chiuso tutto" if not dedotta else "operazione chiusa (dedotto)") + \
                (f"\n<b>Chiudi il resto a mercato</b>. {ora}" if not dedotta else
                 f"\nAldo ha aperto una nuova operazione sullo stesso asset: la precedente risulta chiusa. Se l'avevi copiata, <b>chiudila a mercato</b>. {ora}") + \
                f"\n{copiata}."
        elif tipo == "stop_preso":
            txt = testa("stop preso") + f"\nAldo è uscito allo stop. <b>Se il tuo stop non è scattato, chiudi a mercato</b>. {ora}\n{copiata}."
        elif tipo == "ordine_non_eseguito":
            txt = testa("livello annullato") + f"\n<b>Cancella l'ordine limite</b> su {asset}USDT, se l'avevi messo."
        elif tipo in ("aumento", "ordine_limite"):
            txt = testa("aumenta la posizione" if tipo == "aumento" else "ordine per aumentare") + \
                f"\nLa copia non aumenta: nessuna azione. {ora}"
            return self._nuovo_avviso(a, msg, adesso, txt, False)
        else:
            return None
        return self._nuovo_avviso(a, msg, adesso, txt + "\n" + PIEDE, True)

    def _kw(self) -> dict:
        c = self.cfg.copia()
        return {k: c[k] for k in ("modalita", "importo_eur", "cambio_eur_usdt", "leva", "leva_max", "capitale_usdt", "rischio_pct", "stop_mancante")}

    def _ingresso_a_mercato(self, a, msg, adesso, spec, px, eta_min, testa) -> dict | None:
        """Apertura senza livello annunciato: a mercato solo se entro COPIA_MAX_MINUTI dal suo ingresso stimato e con scostamento
        sfavorevole sotto COPIA_MAX_SCOSTAMENTO_PCT; altrimenti avviso informativo "non copiare"."""
        cfg, verso = self.cfg, a.get("verso")
        if verso not in ("long", "short"):
            return None
        t_msg = A._ts(msg["data"])
        prezzo_suo = a.get("prezzo")
        minuti, rif = None, prezzo_suo
        if prezzo_suo:
            m = B.minuti_dal_prezzo(self._c1m(a["asset"]), prezzo_suo, t_msg)
            minuti = None if m is None else m + eta_min
        else:
            minuti = eta_min                                                     # ingresso stimato al momento del messaggio
            c = self._c1m(a["asset"])
            if c is not None and len(c.loc[:t_msg]):
                rif = float(c.loc[:t_msg, "close"].iloc[-1])
            rif = rif or px
        scost = ((px / rif - 1) * 100 * (1 if verso == "long" else -1)) if px and rif else None   # positivo = prezzo peggiore del suo
        ok = minuti is not None and minuti <= cfg.max_minuti and scost is not None and scost < cfg.max_scostamento_pct and spec
        if not ok:
            if eta_min > 60:
                return None
            motivi = []
            if minuti is None:
                motivi.append("il suo prezzo d'ingresso non si trova nelle ultime ore: è entrato da molto")
            elif minuti > cfg.max_minuti:
                motivi.append(f"è dentro da circa {_fmt(minuti, 0)} minuti (regola: entro {_fmt(cfg.max_minuti, 0)})")
            if scost is not None and scost >= cfg.max_scostamento_pct:
                motivi.append(f"scostamento {A._p(round(scost, 2))} (regola: sotto {_fmt(cfg.max_scostamento_pct, 1)}%)")
            if not spec:
                motivi.append(f"{a['asset']}USDT non trovato fra i futures di Bitget")
            if scost is None and minuti is not None:
                motivi.append("prezzo di Bitget non disponibile")
            txt = (testa("aperta senza livello annunciato") + "\n<b>NON COPIARE</b>: " + "; ".join(motivi) + "."
                   + (f"\nPrezzo suo {_px(prezzo_suo, spec)}" if prezzo_suo else "") + (f" · prezzo ora {_px(px, spec)}" if px else ""))
            return self._nuovo_avviso(a, msg, adesso, txt, False)
        o = B.ordine(spec, verso, px, a.get("stop"), **self._kw())
        if o.get("errore"):
            return self._nuovo_avviso(a, msg, adesso, testa("aperta") + f"\n{_esc(o['errore'])}.", False)
        r = [testa("ingresso a mercato"),
             f"<b>A MERCATO</b>: Aldo è già dentro da {'meno di un minuto' if minuti < 1 else _fmt(minuti, 0) + ' minuti'}"
             + (f", prezzo suo {_px(prezzo_suo, spec)}" if prezzo_suo else "") + f", prezzo ora {_px(px, spec)}, scostamento {A._p(round(scost, 2))}",
             f"Ordine a mercato: {o['lato']} {_riga_quantita(o, spec)} · Bitget {o['simbolo']} (USDT-M)"]
        r += _riga_stop_obiettivi(o, spec, a.get("target") or [])
        r += righe_ordine(o, spec, cfg)
        r.append(PIEDE)
        return self._nuovo_avviso(a, msg, adesso, "\n".join(r), True, o)

    def _invia(self, av: dict):
        adesso = self.orologio()
        av["id"] = f"{av['msg_id']}.{sum(1 for x in self.avvisi if x['msg_id'] == av['msg_id']) + 1}"   # entra nei pulsanti
        if self.cfg.avvisi_attivi and self.bot:
            tastiera = pulsanti(av["id"]) if av["azionabile"] and self.cfg.bot_dedicato else None
            mid = self.bot.invia(av["testo"], tastiera, silenzioso=self.cfg.silenzioso(adesso))
            av["stato"], av["telegram_id"] = ("inviato", mid) if mid else ("errore", None)
            av["inviato_alle"] = A._iso(self.orologio())
        else:
            av["stato"] = "proposto"                                # invio spento finche' l'utente non approva i testi
            av["inviato_alle"] = None
        av["latenza_s"] = round(((A._dt(av["inviato_alle"]) if av["inviato_alle"] else adesso) - A._dt(av["data_msg"])).total_seconds(), 1)
        self.avvisi.append(av)

    # ---- pulsanti ----
    def su_pulsante(self, cb: dict) -> str | None:
        """Pressione di "Fatto" / "Salto" (callback_query dell'API Bot). Solo dalla chat dell'utente. Restituisce la scelta registrata."""
        msg = cb.get("message") or {}
        if str((msg.get("chat") or {}).get("id")) != str(self.cfg.chat_id):
            return None
        parti = str(cb.get("data", "")).split(":", 2)
        if len(parti) != 3 or parti[0] != "aldo":
            return None
        azione, aid = parti[1], parti[2]
        with self._blocco:
            av = next((x for x in self.avvisi if x["id"] == aid), None)
            if av is None:
                self.bot and self.bot.rispondi_pulsante(cb["id"], "Avviso non trovato")
                return None
            if azione == "b":
                self.bot and self.bot.rispondi_pulsante(cb["id"], "Esecuzione su Bitget non attiva: metti l'ordine a mano")
                return None
            scelta = {"f": "fatto", "s": "salto"}.get(azione)
            if not scelta:
                return None
            if av.get("scelta"):
                self.bot and self.bot.rispondi_pulsante(cb["id"], f"Già registrato: {av['scelta']}")
                return av["scelta"]
            adesso = self.orologio()
            av["scelta"], av["scelta_alle"] = scelta, A._iso(adesso)
            self.reale["scelte"].append({"avviso": aid, "scelta": scelta, "quando": A._iso(adesso), "tipo": av["tipo"], "asset": av["asset"],
                                         "trade": av.get("trade"), "msg_id": av["msg_id"], "prezzo_ora": self._ora(av["asset"])})
            self._salva()
        if self.bot:
            self.bot.rispondi_pulsante(cb["id"], f"Registrato: {scelta}")
            if msg.get("message_id"):
                self.bot.chiudi_avviso(msg["message_id"], av["testo"] + f"\n<i>Registrato: {scelta}, {_ora(adesso)}</i>")
        return scelta

    def ascolta_pulsanti(self, fermo: threading.Event | None = None):
        """Ciclo dei pulsanti (getUpdates, attesa lunga 30 s). Solo con un bot dedicato: un secondo lettore sullo stesso bot di radar
        ruberebbe i messaggi a radar/journal.py."""
        fermo = fermo or threading.Event()
        attesa = 5
        while not fermo.is_set():
            try:
                upd = self.bot.aggiornamenti(self.reale.get("offset"), timeout=30)
                for u in upd:
                    self.reale["offset"] = int(u["update_id"]) + 1
                    if u.get("callback_query"):
                        self.su_pulsante(u["callback_query"])
                if upd:
                    with self._blocco:
                        A.salva_json(self.dati / "reale.json", self.reale)
                attesa = 5
            except Exception as e:
                log(f"pulsanti: {type(e).__name__}, riprovo fra {attesa} s")
                fermo.wait(attesa)
                attesa = min(attesa * 2, 120)

    # ---- registro sulla carta, sezione privata, riepilogo ----
    def aggiorna_carta(self, adesso: datetime | None = None) -> dict:
        adesso = adesso or self.orologio()
        with self._blocco:
            for a in {e["asset"] for e in self.registro["eventi"]} | {p["asset"] for p in A.piani_aperti(self.registro, adesso)}:
                try:
                    self.prezzi.aggiorna(a, min(A._dt(e["utc"]) for e in self.registro["eventi"] + self.registro["piani"] if e["asset"] == a) - timedelta(days=3), adesso)
                except Exception as e:
                    log(f"candele orarie {a}: {type(e).__name__}")
            ops = A.ricostruisci(self.registro, self.prezzi, adesso, self.cfg.capitale_usdt, self.contratti, self.cfg.copia())
            A.salva_json(self.dati / "operazioni.json", {k: v for k, v in ops.items() if k != "aggiornato"})
            sez = A.build(self.registro, ops, adesso, self.messaggi, self.avvisi, statistiche_reali(self.avvisi, self.registro, ops),
                          latenza(self.latenze()), self.cfg.copia())
            A.salva_json(self.dati / "sezione.json", {k: v for k, v in sez.items() if k != "aggiornato"})
            return sez

    def ogni_ora(self, adesso: datetime | None = None):
        adesso = adesso or self.orologio()
        sez = self.aggiorna_carta(adesso)
        if adesso.weekday() == 0 and adesso.hour >= 7:                     # lunedi': riepilogo della settimana appena finita
            dom = (adesso - timedelta(days=1)).date()
            p = self.dati / f"riepilogo_{dom:%Y-%m-%d}.md"
            if not p.exists():
                ops = A.carica_json(self.dati / "operazioni.json", {})
                A.riepilogo_settimanale(self.registro, ops, dom.isoformat(), self.dati, self.messaggi)
                if self.cfg.avvisi_attivi and self.bot:
                    self.bot.invia(sintesi_settimanale(sez, dom), silenzioso=True)


def statistiche_reali(avvisi: list[dict], registro: dict, operazioni: dict) -> dict:
    """Copia reale (pulsanti) contro copia sulla carta. Un'operazione e' "copiata" se l'utente ha premuto Fatto sul suo avviso
    d'ingresso (ordine limite sul piano collegato, o ingresso a mercato); il risultato e' quello simulato del modo usato
    (con ordini limite o a mercato), perche' i prezzi eseguiti davvero il modulo non li conosce."""
    az = [a for a in avvisi if a.get("azionabile")]
    piano_trade = {p["msg_id"]: p.get("trade_collegato") for p in registro.get("piani", []) if p.get("trade_collegato")}
    ops = {o["trade"]: o for o in operazioni.get("operazioni", [])}
    copiate, saltate = {}, set()
    for a in az:
        if a["tipo"] not in ("piano", "apertura") or not a.get("scelta"):
            continue
        t = a.get("trade") or piano_trade.get(a["msg_id"])
        if not t:
            continue
        if a["scelta"] == "fatto":
            copiate[t] = "limite" if a["tipo"] == "piano" else "mercato"
        else:
            saltate.add(t)
    r = []
    for t, modo in copiate.items():
        o = ops.get(t)
        if o and not o.get("aperta") and (o.get(modo) or {}).get("rendimento_pct") is not None:
            r.append(o[modo]["rendimento_pct"])
    return {"avvisi": len(avvisi), "azionabili": len(az), "fatti": sum(1 for a in az if a.get("scelta") == "fatto"),
            "saltati": sum(1 for a in az if a.get("scelta") == "salto"), "senza_risposta": sum(1 for a in az if not a.get("scelta")),
            "operazioni_copiate": len(copiate), "operazioni_saltate": len(saltate - set(copiate)), "copiate_chiuse": len(r),
            "in_guadagno_pct": round(sum(x > 0 for x in r) / len(r) * 100) if r else None,
            "medio_pct": round(sum(r) / len(r), 2) if r else None}


def latenza(righe: list[dict]) -> dict:
    """Ora del messaggio -> avviso pronto (e inviato), in secondi, sui messaggi che hanno prodotto avvisi."""
    v = sorted(r["latenza_s"] for r in righe if r.get("avvisi"))
    if not v:
        return {"n": 0}
    return {"n": len(v), "mediana_s": v[len(v) // 2], "p90_s": v[min(len(v) - 1, int(len(v) * 0.9))], "ultima_s": [r["latenza_s"] for r in righe if r.get("avvisi")][-1]}


def sintesi_settimanale(sez: dict, domenica) -> str:
    st, re_, la = sez.get("statistiche", {}), sez.get("reale", {}), sez.get("latenza", {})
    f = lambda s: "–" if not s or not s.get("operazioni") else f"{s['operazioni']} op., {_fmt(s['in_guadagno_pct'], 0)}% in guadagno, medio {A._p(s['medio_pct'])}"
    return "\n".join([f"<b>Aldo · riepilogo fino al {domenica:%d/%m}</b>",
                      f"Trader: {f(st.get('trader'))}", f"Carta, ordini limite: {f(st.get('limite'))}", f"Carta, a mercato: {f(st.get('mercato'))}",
                      f"Copia reale: {re_.get('operazioni_copiate', 0)} copiate, {re_.get('operazioni_saltate', 0)} saltate"
                      + (f", chiuse {re_['copiate_chiuse']}: {_fmt(re_['in_guadagno_pct'], 0)}% in guadagno, medio {A._p(re_['medio_pct'])}" if re_.get("copiate_chiuse") else ""),
                      f"Avvisi: {re_.get('azionabili', 0)} da eseguire, {re_.get('fatti', 0)} fatti, {re_.get('saltati', 0)} saltati"
                      + (f" · latenza mediana {_fmt(la['mediana_s'], 0)} s" if la.get("n") else ""),
                      "Il riepilogo completo è sulla VM (ALDO_DATI/riepilogo_*.md)."])


# ------------------------------------------------------------------------------------------------------------------------------
# Telethon: ascolto del canale (sola lettura)
# ------------------------------------------------------------------------------------------------------------------------------

class NonAutorizzato(RuntimeError):
    pass


def _client(cfg: Config):
    from telethon import TelegramClient
    return TelegramClient(str(cfg.sessione), int(cfg.api_id), cfg.api_hash, auto_reconnect=True, connection_retries=None,
                          retry_delay=5, flood_sleep_threshold=120)


def _messaggio(m, foto) -> dict:
    return A.messaggio(m.id, m.date, m.message or "", foto=foto, risposta_a=getattr(m, "reply_to_msg_id", None), origine="telethon",
                       modificato=getattr(m, "edit_date", None))


async def _ascolta(cfg: Config, servizio: Servizio):
    import asyncio
    from telethon import events
    client = _client(cfg)
    await client.connect()
    try:
        if not await client.is_user_authorized():
            raise NonAutorizzato("sessione non autorizzata: eseguire `python -m radar.aldostream accedi` sulla VM")
        canale = await client.get_entity(int(cfg.canale))
        loop = asyncio.get_running_loop()
        coda = asyncio.Lock()

        async def gestisci(m, modifica: bool):
            ricevuto = datetime.now(UTC)
            foto = None
            if getattr(m, "photo", None):
                foto = await client.download_media(m, file=str(Path(cfg.dati) / "foto" / f"{m.id}.jpg"))
            d = _messaggio(m, foto)
            async with coda:                                        # un messaggio alla volta, nell'ordine di arrivo
                await loop.run_in_executor(None, servizio.su_modifica if modifica else servizio.su_messaggio, d, ricevuto)

        async def nuovo(ev):
            await gestisci(ev.message, False)

        async def modificato(ev):
            await gestisci(ev.message, True)

        client.add_event_handler(nuovo, events.NewMessage(chats=canale))
        client.add_event_handler(modificato, events.MessageEdited(chats=canale))
        ultimo = servizio.ultimo_id()                               # recupero dei messaggi arrivati mentre il servizio era fermo
        async for m in client.iter_messages(canale, min_id=ultimo, reverse=True, limit=500):
            await gestisci(m, False)
        log(f"in ascolto (ultimo messaggio {servizio.ultimo_id()})")

        async def orario():
            while True:
                await asyncio.sleep(3600 - time.time() % 3600 + 20)
                async with coda:
                    await loop.run_in_executor(None, servizio.ogni_ora)

        compito = asyncio.create_task(orario())
        try:
            await client.run_until_disconnected()
        finally:
            compito.cancel()
    finally:
        await client.disconnect()


def attesa_dopo_errore(e: Exception, attesa: int) -> tuple[int, int]:
    """Quanto aspettare dopo un errore e l'attesa successiva: FloodWait = secondi chiesti da Telegram + 5 (l'attesa crescente non
    cambia); altri errori = attesa crescente 5 s -> 5 min."""
    secondi = getattr(e, "seconds", None)
    if type(e).__name__ == "FloodWaitError" and secondi:
        return int(secondi) + 5, attesa
    return attesa, min(attesa * 2, 300)


def avvia(cfg: Config | None = None):
    """Servizio: riconnessione con attese crescenti (5 s -> 5 min), FloodWait rispettato (attesa indicata da Telegram + 5 s)."""
    import asyncio
    cfg = cfg or Config.da_ambiente()
    for a in cfg.avvertenze:
        log("configurazione:", a)
    if not (cfg.api_id and cfg.api_hash and cfg.canale):
        raise SystemExit("mancano TELEGRAM_API_ID, TELEGRAM_API_HASH o ALDO_CANALE_ID (vedi deploy/ALDOSTREAM.md)")
    bot = BotTelegram(cfg.bot_token, cfg.chat_id) if cfg.bot_token and cfg.chat_id else None
    servizio = Servizio(cfg, bot)
    log(f"avvisi {'ATTIVI' if cfg.avvisi_attivi else 'spenti (solo registrati)'}, pulsanti {'sì' if cfg.bot_dedicato and bot else 'no'}, "
        f"modalità {cfg.modalita}, modello {'sì' if os.environ.get('ANTHROPIC_API_KEY') else 'no'}")
    if bot and cfg.bot_dedicato:
        threading.Thread(target=servizio.ascolta_pulsanti, daemon=True).start()
    attesa = 5
    while True:
        try:
            asyncio.run(_ascolta(cfg, servizio))
            attesa = 5
        except KeyboardInterrupt:
            return
        except NonAutorizzato as e:
            log(str(e))
            time.sleep(600)
        except Exception as e:
            secondi, attesa = attesa_dopo_errore(e, attesa)
            log(f"Telegram chiede di aspettare {secondi} s (FloodWait)" if type(e).__name__ == "FloodWaitError"
                else f"connessione persa: {type(e).__name__}, riprovo fra {secondi} s")
            time.sleep(secondi)


def accedi(cfg: Config | None = None):
    """Primo accesso interattivo (numero e codice di Telegram). La sessione resta in ALDO_SESSIONE con permessi 600."""
    cfg = cfg or Config.da_ambiente()
    Path(cfg.sessione).parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    with _client(cfg).start():
        pass
    for p in (Path(str(cfg.sessione)), Path(str(cfg.sessione) + ".session")):
        if p.exists():
            os.chmod(p, 0o600)
    print("sessione salvata in", cfg.sessione)


def prova(cfg: Config | None = None):
    """Controlli senza inviare niente: sessione, canale (solo nome e numero di messaggi), specifiche e ticker Bitget, bot."""
    import asyncio
    cfg = cfg or Config.da_ambiente()

    async def _p():
        client = _client(cfg)
        await client.connect()
        try:
            if not await client.is_user_authorized():
                print("sessione: NON autorizzata (eseguire accedi)")
                return
            ent = await client.get_entity(int(cfg.canale))
            msgs = await client.get_messages(ent, limit=1)
            print(f"canale: {getattr(ent, 'title', '?')} · ultimo messaggio {msgs[0].id if msgs else '–'} del {msgs[0].date:%d/%m %H:%M} UTC" if msgs else "canale: nessun messaggio")
        finally:
            await client.disconnect()

    asyncio.run(_p())
    s = B.Contratti(Path(cfg.dati) / "bitget_contratti.json").spec("BTC")
    print("Bitget BTCUSDT:", {k: s[k] for k in ("sizeMultiplier", "minTradeNum", "pricePlace", "volumePlace")} if s else "non trovato", "· prezzo", B.ticker("BTC"))
    if cfg.bot_token and cfg.chat_id:
        r = BotTelegram(cfg.bot_token, cfg.chat_id).api("getMe")
        print("bot:", (r.get("result") or {}).get("username", "non raggiungibile"))
    for a in cfg.avvertenze:
        print("configurazione:", a)


def canali(cfg: Config | None = None):
    """Elenca gruppi e canali dell'account (id e nome), per trovare ALDO_CANALE_ID. Non legge messaggi."""
    import asyncio
    cfg = cfg or Config.da_ambiente()

    async def _c():
        client = _client(cfg)
        await client.connect()
        try:
            if not await client.is_user_authorized():
                print("sessione: NON autorizzata (eseguire accedi)")
                return
            async for d in client.iter_dialogs():
                if d.is_group or d.is_channel:
                    print(d.id, d.name)
        finally:
            await client.disconnect()

    asyncio.run(_c())


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "avvia"
    {"accedi": accedi, "prova": prova, "canali": canali, "avvia": avvia}[cmd]()
