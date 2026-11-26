"""Dati d'esempio INVENTATI per i test e per gli esempi del pacchetto: messaggi scritti apposta (non copiati dal canale) e prezzi
sintetici di BTC, ETH e SOL costruiti per far succedere le operazioni dei messaggi. Le sole cose vere sono le specifiche dei
contratti Bitget (bitget_contratti_esempio.json, scaricate da api.bitget.com).

    python esempio.py      # rigenera esempio_sezione.json, esempio_riepilogo.md, esempio_avvisi.md e i dati di riferimento_sezione.html
"""
from __future__ import annotations

import json
import re
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

import aldo as A
import aldo_bitget as B
import aldostream as S

QUI = Path(__file__).resolve().parent
ADESSO = "2026-11-26T12:00:00Z"
CONTRATTI = B.carica_contratti(QUI / "bitget_contratti_esempio.json")

# (asset, [(ora UTC, prezzo), ...]): percorso a tratti, interpolato
PERCORSI = {
    "BTC": [("2026-11-07 00:00", 60100), ("2026-11-10 09:00", 60300), ("2026-11-10 15:00", 61250), ("2026-11-11 09:00", 59800),
            ("2026-11-12 12:00", 58600), ("2026-11-14 00:00", 59400), ("2026-11-18 00:00", 60500), ("2026-11-22 00:00", 61300),
            ("2026-11-25 18:00", 62600), ("2026-11-26 12:00", 62150)],
    "ETH": [("2026-11-07 00:00", 1690), ("2026-11-14 10:00", 1700), ("2026-11-14 13:00", 1712), ("2026-11-15 06:00", 1668),
            ("2026-11-15 09:00", 1662), ("2026-11-20 00:00", 1680), ("2026-11-26 08:00", 1652), ("2026-11-26 12:00", 1648)],
    "SOL": [("2026-11-07 00:00", 66), ("2026-11-20 13:00", 70.2), ("2026-11-20 20:00", 68.4), ("2026-11-21 07:00", 69.0),
            ("2026-11-23 15:00", 72.3), ("2026-11-25 00:00", 71.2), ("2026-11-26 12:00", 71.6)],
}

# messaggi inventati, nello stile del canale (stessa struttura dei messaggi veri: id, data, testo, foto, risposta_a)
MESSAGGI = [
    (101, "2026-11-10T09:12:00Z", "BTC: se torna sui 61,2k cerco short al retest della resistenza. Stop sopra 62.000, target 59,8k e 58.500. Grafico 4h.", "telethon"),
    (102, "2026-11-10T16:20:00Z", "Short aperto su BTC a 61.150", "telethon"),
    (103, "2026-11-11T09:40:00Z", "Chiuso metà al primo target, stop a pareggio", "telethon"),
    (104, "2026-11-12T12:30:00Z", "Chiuso il resto a 58.600, operazione conclusa", "telethon"),
    (105, "2026-11-13T19:00:00Z", "Settimana con il dato sull'inflazione mercoledì, riduco l'esposizione.", "telethon"),
    (106, "2026-11-14T10:05:00Z", "Long ETH aperto a 1.701, stop 1.670, target 1.780", "telethon"),
    (107, "2026-11-15T08:30:00Z", "Stoppato su ETH, fa parte del gioco", "telethon"),
    (108, "2026-11-20T13:00:00Z", "Ordine long al limite su SOL a 68,5, stop 66,8, target 73,5 e 76", "telethon"),
    (109, "2026-11-21T07:10:00Z", "Long SOL eseguito a 68,5", "telethon"),
    (110, "2026-11-23T15:00:00Z", "SOL: chiuso un terzo a 72, stop a pareggio", "telethon"),
    (111, "2026-11-25T18:30:00Z", "BTC: possibile short se risale a 63,4k. Invalidazione sopra 64.200, obiettivi 61k e 59,5k.", "telethon"),
    (112, "2026-11-26T08:00:00Z", "ETH: ordine long al limite a 1.630, stop 1.600", "telethon"),
]
# un messaggio in piu', solo per l'esempio di avviso "non copiare" (non entra nel registro d'esempio)
EXTRA = (113, "2026-11-24T09:00:00Z", "Short BTC preso a 61.900", "telethon")


def _prezzo(asset: str, t) -> float:
    pts = PERCORSI[asset]
    x = pd.to_datetime([p[0] for p in pts]).as_unit("ns").asi8.astype(float)
    return float(np.interp(float(A._ts(t).as_unit("ns").value), x, [p[1] for p in pts]))


def prezzi_finti(fino=ADESSO) -> dict:
    """Candele orarie sintetiche: apertura e chiusura sul percorso, massimo e minimo 0,1% oltre."""
    out = {}
    fine = A._ts(fino).floor("h")
    for asset, pts in PERCORSI.items():
        t = pd.to_datetime([p[0] for p in pts])
        idx = pd.date_range(t[0], fine, freq="h").as_unit("ns")
        mid = np.interp(idx.asi8.astype(float), t.as_unit("ns").asi8.astype(float), [p[1] for p in pts])
        df = pd.DataFrame({"open": mid, "close": np.append(mid[1:], mid[-1])}, index=idx)
        df["high"] = df[["open", "close"]].max(axis=1) * 1.001
        df["low"] = df[["open", "close"]].min(axis=1) * 0.999
        out[asset] = df[["open", "high", "low", "close"]]
    return out


def candele_minuto_finte(asset: str, fino) -> pd.DataFrame:
    """Ultime 200 candele da 1 minuto fino a `fino`, sul percorso sintetico."""
    fine = A._ts(fino).floor("min")
    idx = pd.date_range(fine - pd.Timedelta(minutes=199), fine, freq="min").as_unit("ns")
    pts = PERCORSI[asset]
    mid = np.interp(idx.asi8.astype(float), pd.to_datetime([p[0] for p in pts]).as_unit("ns").asi8.astype(float), [p[1] for p in pts])
    df = pd.DataFrame({"open": mid, "close": np.append(mid[1:], mid[-1])}, index=idx)
    df["high"] = df[["open", "close"]].max(axis=1) * 1.0003
    df["low"] = df[["open", "close"]].min(axis=1) * 0.9997
    return df[["open", "high", "low", "close"]]


def messaggi_esempio(fino=None, extra=False) -> list[dict]:
    lim = A._dt(fino) if fino else None
    righe = MESSAGGI + ([EXTRA] if extra else [])
    return sorted([A.messaggio(i, d, t, origine=o) for i, d, t, o in righe if lim is None or A._dt(d) <= lim], key=lambda m: m["data"])


def stato_esempio(fino=ADESSO, capitale=10_000.0):
    """Registro, operazioni e uscita di build() con i dati inventati (solo carta, senza servizio)."""
    prezzi = A.Prezzi(dati=prezzi_finti(fino))
    msgs = messaggi_esempio(fino)
    reg, _ = A.elabora(msgs, A.registro_vuoto(), prezzi, adesso=fino, usa_modello=False)
    copia = S.Config().copia()
    ops = A.ricostruisci(reg, prezzi, fino, capitale, B.Contratti(dati=CONTRATTI), copia)
    return msgs, reg, ops, A.build(reg, ops, fino, msgs, copia=copia)


class BotFinto:
    """Client Telegram finto: registra cosa verrebbe inviato."""

    def __init__(self):
        self.inviati, self.risposte, self.chiusi = [], [], []

    def invia(self, testo, pulsanti=None, silenzioso=False):
        self.inviati.append({"testo": testo, "pulsanti": pulsanti, "silenzioso": silenzioso})
        return 1000 + len(self.inviati)

    def rispondi_pulsante(self, callback_id, testo):
        self.risposte.append(testo)

    def chiudi_avviso(self, message_id, testo):
        self.chiusi.append((message_id, testo))

    def aggiornamenti(self, offset, timeout=30):
        return []


class Orologio:
    def __init__(self, t):
        self.t = A._dt(t)

    def __call__(self):
        return self.t


def servizio_esempio(cartella, orologio: Orologio, cfg: S.Config | None = None, bot=None) -> S.Servizio:
    cfg = cfg or S.Config(dati=Path(cartella), chat_id="42", bot_token="finto", bot_dedicato=True, avvisi_attivi=True)
    get_vietato = lambda url: (_ for _ in ()).throw(AssertionError("nessuna rete negli esempi"))
    return S.Servizio(cfg, bot or BotFinto(), contratti=B.Contratti(dati=CONTRATTI, get=get_vietato),
                      prezzo_ora=lambda a: _prezzo(a, orologio()), candele_1m=lambda a: candele_minuto_finte(a, orologio()),
                      prezzi=A.Prezzi(dati=prezzi_finti(ADESSO), get=get_vietato), orologio=orologio)


def gira_esempio(cartella, extra=True, ritardo_s=20, fatto_su=("101.1",)):
    """Fa passare i messaggi d'esempio dal servizio come se arrivassero in tempo reale (avviso `ritardo_s` dopo il messaggio)
    e preme "Fatto" sugli avvisi indicati subito dopo averli ricevuti."""
    ora = Orologio(MESSAGGI[0][1])
    s = servizio_esempio(cartella, ora)
    for m in messaggi_esempio(extra=extra):
        ora.t = A._dt(m["data"]) + pd.Timedelta(seconds=ritardo_s)
        for av in s.su_messaggio(m, ricevuto=A._dt(m["data"]) + pd.Timedelta(seconds=2)):
            if av["id"] in fatto_su:
                s.su_pulsante({"id": "cb", "data": f"aldo:f:{av['id']}", "message": {"message_id": av["telegram_id"], "chat": {"id": 42}}})
    return s


def _md(testo: str) -> str:
    t = testo.replace("<b>", "**").replace("</b>", "**").replace("<i>", "_").replace("</i>", "_")
    return t.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")


def scrivi_esempio_avvisi(s: S.Servizio, file: Path):
    L = ["# Esempi di avvisi Telegram per Aldo (testi proposti, da approvare)", "",
         "Messaggi e prezzi INVENTATI; specifiche dei contratti vere (Bitget USDT-M). Modalità predefinita: importo 1.000 € per",
         "operazione, leva 5x, cambio EUR/USDT 1,08. Gli avvisi con i pulsanti «Fatto» e «Salto» sono quelli da eseguire;",
         "gli altri sono informativi. Ogni avviso arriva circa 20 secondi dopo il messaggio di Aldo (latenza misurata e salvata).", ""]
    scelti = ("piano", "apertura", "chiusura_parziale", "stop_pareggio", "chiusura_totale", "stop_preso", "ordine_non_eseguito")
    visti = set()
    for av in s.avvisi:
        chiave = re.sub(r"<[^>]+>", "", av["testo"].splitlines()[0]).strip()
        if av["tipo"] not in scelti or chiave in visti:
            continue
        visti.add(chiave)
        L += [f"## {chiave}{'' if av['azionabile'] else ' (informativo)'}", "",
              f"Messaggio di Aldo alle {A._dt(av['data_msg']):%d/%m %H:%M} UTC · avviso dopo {A._fmt(av['latenza_s'], 0)} s", "", "```"]
        L += _md(av["testo"]).splitlines()
        if av["azionabile"]:
            L += ["", "[ ✅ Fatto ]  [ ⏭️ Salto ]"]
        L += ["```", ""]
    L += ["Dopo «Fatto» o «Salto» il messaggio perde i pulsanti e riceve la riga \"Registrato: fatto, 10/11 09:12 UTC\".", "",
          "Un futuro pulsante «Esegui su Bitget» è previsto solo come punto d'aggancio (spento, non implementato)."]
    file.write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as d:
        scrivi_esempio_avvisi(gira_esempio(d, extra=True), QUI / "esempio_avvisi.md")
    with tempfile.TemporaryDirectory() as d:
        s = gira_esempio(d, extra=False)
        sez = s.aggiorna_carta(A._dt(ADESSO))
        ops = A.carica_json(Path(d) / "operazioni.json", {})
        testo, _ = A.riepilogo_settimanale(s.registro, ops, "2026-11-26", None, s.messaggi)
    sez["capitale_esempio"] = True
    (QUI / "esempio_sezione.json").write_text(json.dumps(sez, ensure_ascii=False, indent=1), encoding="utf-8")
    (QUI / "esempio_riepilogo.md").write_text(testo, encoding="utf-8")
    vuoto = A.build(A.registro_vuoto(), {}, ADESSO, [])
    html = QUI / "riferimento_sezione.html"
    h = html.read_text(encoding="utf-8")
    dati = json.dumps({"attiva": sez, "vuota": vuoto}, ensure_ascii=False).replace("</", "<\\/")
    h = re.sub(r"const STATI = .*?;\n", lambda m: f"const STATI = {dati};\n", h, count=1, flags=re.S)
    html.write_text(h, encoding="utf-8")
    print(sez["stato"], sez["titolo"], sez["reale"], sez["latenza"])
