"""Test di aldo.py, tutti offline. Messaggi e prezzi sono INVENTATI (esempio.py): nessun testo del canale."""
import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import pandas as pd
import pytest

import aldo as A
import esempio as E

PREZZI = E.prezzi_finti()


@pytest.fixture(autouse=True)
def ambiente_pulito(monkeypatch):
    for k in ("ANTHROPIC_API_KEY", "RADAR_ALDO_AVVISI", "RADAR_ALDO_TELETHON", "RADAR_ALDO_CAPITALE", "RADAR_ALDO_MODELLO"):
        monkeypatch.delenv(k, raising=False)


def msg(testo, i=1, data="2026-11-20T10:00:00Z", **kw):
    return A.messaggio(i, data, testo, **kw)


# ---- numeri e asset --------------------------------------------------------------------------------------------------------

@pytest.mark.parametrize("raw,k,asset,rif,atteso", [
    ("27.6", True, "BTC", None, 27600), ("27,6", True, "BTC", None, 27600), ("25.300", False, "BTC", None, 25300),
    ("0,686", False, "ARB", None, 0.686), ("27,187.9", False, "BTC", None, 27187.9), ("8.472", False, "INJ", None, 8.472),
    ("27,4", False, "BTC", 27000, 27400), ("25.300", False, "XYZ", 25.1, 25.3), ("2", False, "BTC", None, None),
    ("14", False, "BTC", 60000, None),
])
def test_numeri(raw, k, asset, rif, atteso):
    assert A.leggi_numero(raw, k, asset, rif) == atteso


def test_asset():
    assert A.trova_asset("Long INJ, FET e WOO da qui") == ["INJ", "FET", "WOO"]
    assert A.trova_asset("ci sono sei livelli sui grafici") == []          # 'sei' e 'sui' sono parole italiane
    assert A.trova_asset("SUI e $SEI, poi ethereum e TAO/USDT") == ["SUI", "SEI", "ETH", "TAO"]


# ---- estrattore a regole ---------------------------------------------------------------------------------------------------

def test_regole_piano_con_livelli():
    r = A.estrai_regole(msg("Piano su BTC: se torna a 61,2k cerco short al retest. Stop sopra 62.000, target 59,8k e 58.500"))
    assert r["eventi"] == []
    p = r["piani"][0]
    assert (p["asset"], p["verso"], p["livello_innesco"], p["stop"], p["target"]) == ("BTC", "short", 61200, 62000, [59800, 58500])
    assert p["affidabilita"] >= A.AFFIDABILE


def test_regole_eventi():
    e = A.estrai_regole(msg("Short aperto su BTC a 61.150"))["eventi"]
    assert [(x["tipo"], x["verso"], x["prezzo"]) for x in e] == [("apertura", "short", 61150)]
    e = A.estrai_regole(msg("Chiuso metà al primo target, stop a pareggio"))["eventi"]
    assert [(x["tipo"], x["quota"]) for x in e] == [("chiusura_parziale", 0.5), ("stop_pareggio", None)]
    e = A.estrai_regole(msg("Chiuso l'80% di INJ"))["eventi"]
    assert [(x["tipo"], x["asset"], x["quota"]) for x in e] == [("chiusura_parziale", "INJ", 0.8)]
    e = A.estrai_regole(msg("Long INJ, FET e WOO da qui"))["eventi"]
    assert [(x["tipo"], x["asset"], x["verso"]) for x in e] == [("apertura", a, "long") for a in ("INJ", "FET", "WOO")]
    e = A.estrai_regole(msg("Stoppato su ETH, fa parte del gioco"))["eventi"]
    assert [x["tipo"] for x in e] == ["stop_preso"]
    e = A.estrai_regole(msg("Settimana con dati macro, riduco l'esposizione."))
    assert e["eventi"] == [] and e["piani"] == []


def test_regole_ordine_limite_e_immagine():
    r = A.estrai_regole(msg("Ordine long al limite su ARB a 0,686, stop 0,66"))
    assert r["eventi"] == [] and r["piani"][0]["livello_innesco"] == 0.686 and r["piani"][0]["stop"] == 0.66
    r = A.estrai_regole(msg("Ordine long al limite su ARB a 0,65"), asset_aperti={"ARB"})       # posizione aperta: e' un aumento
    assert [x["tipo"] for x in r["eventi"]] == ["ordine_limite"] and r["piani"] == []
    e = A.estrai_regole(msg("Short", foto="card.jpg"))["eventi"][0]                             # dati solo nell'immagine
    assert e["tipo"] == "apertura" and e["affidabilita"] < A.AFFIDABILE


def test_regole_usano_il_prezzo_di_riferimento():
    e = A.estrai_regole(msg("Long ETH aperto a 2.105, stop 2.060"), rif=lambda a: 2100.0)["eventi"][0]
    assert (e["prezzo"], e["stop"]) == (2105, 2060)


# ---- ingresso dei messaggi -------------------------------------------------------------------------------------------------

def test_export_desktop(tmp_path):
    d = {"name": "Canale d'esempio", "type": "private_supergroup", "messages": [
        {"id": 1, "type": "service", "date": "2026-11-01T10:00:00", "date_unixtime": "1793527200", "action": "join_group_by_link", "text": ""},
        {"id": 2, "type": "message", "date": "2026-11-01T12:00:00", "date_unixtime": "1793530800", "from": "Trader", "text": "Short aperto",
         "text_entities": [{"type": "plain", "text": "Short aperto"}], "photo": "photos/photo_1.jpg"},
        {"id": 3, "type": "message", "date": "2026-11-01T12:00:00", "date_unixtime": "1793534400", "from": "Trader",
         "text": ["Livello ", {"type": "bold", "text": "61,2k"}], "reply_to_message_id": 2, "edited_unixtime": "1793534500"}]}
    m = A.da_export_desktop(d, cartella_foto=tmp_path)
    assert [x["id"] for x in m] == ["2", "3"]
    assert m[0]["data"] == "2026-11-01T11:00:00Z"                         # da date_unixtime (UTC), non dall'ora locale di 'date'
    assert m[0]["foto"] == str(tmp_path / "photos/photo_1.jpg") and m[1]["testo"] == "Livello 61,2k" and m[1]["risposta_a"] == "2"
    f = tmp_path / "result.json"
    f.write_text(json.dumps(d), encoding="utf-8")
    assert len(A.da_export_desktop(f, autori=["Altro"])) == 0


def test_inoltri_al_bot():
    chat = 555
    base = {"message_id": 9, "date": 1793600000, "chat": {"id": chat}}
    u_user = {"update_id": 10, "message": dict(base, text="Short aperto", forward_origin={"type": "user", "date": 1793530800, "sender_user": {"first_name": "Aldo"}})}
    u_hidden = {"update_id": 11, "message": dict(base, caption="Chiuso metà", photo=[{"file_id": "a"}, {"file_id": "b"}],
                                                 forward_origin={"type": "hidden_user", "date": 1793534400, "sender_user_name": "Aldo Q"})}
    u_canale = {"update_id": 12, "message": dict(base, text="Piano", forward_origin={"type": "channel", "date": 1793538000, "message_id": 4321, "chat": {"title": "Aldo Qefalia - Trading"}})}
    u_vecchio = {"update_id": 13, "message": dict(base, text="Long", forward_date=1793541600, forward_sender_name="Aldo Q")}
    u_normale = {"update_id": 14, "message": dict(base, text="/stato")}
    u_estraneo = {"update_id": 15, "message": dict(base, chat={"id": 999}, text="x", forward_origin={"type": "user", "date": 1, "sender_user": {"first_name": "Aldo"}})}
    u_altro = {"update_id": 16, "message": dict(base, text="y", forward_origin={"type": "user", "date": 1, "sender_user": {"first_name": "Marco"}})}
    chiamate = []

    def chiama_bot(metodo, par):
        chiamate.append((metodo, par))
        return [u_user, u_hidden, u_canale, u_vecchio, u_normale, u_estraneo, u_altro]

    m, offset, scartati = A.leggi_inoltri(chiama_bot, 7, [chat], origini=["aldo"])
    assert chiamate[0] == ("getUpdates", {"timeout": 0, "allowed_updates": ["message"], "offset": 7})
    assert offset == 17 and scartati == 3 and len(m) == 4
    assert m[0]["data"] == "2026-11-01T11:00:00Z" and m[0]["origine"] == "bot"     # data del post originale
    assert m[1]["testo"] == "Chiuso metà" and m[1]["foto_id"] == "b"
    assert m[2]["id"] == "4321" and m[3]["data"] == "2026-11-01T14:00:00Z"


def test_unisci_senza_doppioni():
    a = [A.messaggio(1, "2026-11-01T10:00:00Z", "Short aperto", origine="export")]
    b = [A.messaggio("i1793527200-abc", "2026-11-01T10:00:00Z", "Short  aperto", origine="bot"), A.messaggio(2, "2026-11-01T11:00:00Z", "Altro")]
    arch, n = A.unisci(a, b)
    assert n == 1 and [m["id"] for m in arch] == ["1", "2"]


def test_telethon_non_installato(monkeypatch):
    monkeypatch.setitem(sys.modules, "telethon", None)
    monkeypatch.setitem(sys.modules, "telethon.sync", None)
    with pytest.raises(RuntimeError, match="telethon"):
        A.scarica_telethon(1, "x", "/tmp/nessuna", -100)


# ---- ricostruzione ---------------------------------------------------------------------------------------------------------

def test_ricostruzione_tre_modi():
    msgs, reg, ops, sez = E.stato_esempio()
    t = {o["trade"]: o for o in ops["operazioni"]}
    btc, eth, sol = t["L-261110-BTC-S"], t["L-261114-ETH-L"], t["L-261121-SOL-L"]
    assert btc["trader"]["prezzo_medio"] == 61150 and btc["limite"]["prezzo_medio"] == 61200 and btc.get("ingresso_limite")
    assert btc["mercato"]["prezzo_medio"] < btc["trader"]["prezzo_medio"]          # short: chi entrava dopo il messaggio, peggio
    assert btc["limite"]["rendimento_pct"] > btc["trader"]["rendimento_pct"] > btc["mercato"]["rendimento_pct"] > 0
    assert btc["stop"] == 62000                                                       # stop ereditato dal piano
    assert eth["trader"]["rendimento_pct"] == pytest.approx((1670 / 1701 - 1 - 2 * A.COSTO) * 100, abs=0.01)   # allo stop dichiarato
    assert sol["aperta"] and sol["quota_aperta"] == pytest.approx(2 / 3, abs=0.01)
    s = ops["statistiche"]
    assert s["trader"]["operazioni"] == 2 and s["trader"]["in_guadagno_pct"] == 50 and s["limite_entrate_con_ordine"] == 2
    assert s["limite"]["capitale_rischio_2"] > s["mercato"]["capitale_rischio_2"]
    assert ops["ritardo"]["prezzi_dichiarati"] == 3 and ops["ritardo"]["toccati_pct"] == 100 and ops["ritardo"]["mediana_ore"] >= 0


def test_residuo_chiuso_a_pareggio():
    idx = pd.date_range("2026-11-01", "2026-11-06", freq="h")
    v = [100 + min(i, 24) * 0.25 - max(0, i - 48) * 0.2 for i in range(len(idx))]     # sale a 106, poi torna sotto 100
    df = pd.DataFrame({"open": v, "close": v[1:] + v[-1:]}, index=idx)
    df["high"], df["low"] = df[["open", "close"]].max(axis=1), df[["open", "close"]].min(axis=1)
    prezzi = A.Prezzi(dati={"SOL": df})
    msgs = [A.messaggio(1, "2026-11-01T00:30:00Z", "Long SOL aperto a 100, stop 97"),
            A.messaggio(2, "2026-11-02T01:00:00Z", "SOL: chiuso metà a 106, stop a pareggio")]
    reg, _ = A.elabora(msgs, A.registro_vuoto(), prezzi, adesso="2026-11-06T00:00:00Z", usa_modello=False)
    ops = A.ricostruisci(reg, prezzi, "2026-11-06T00:00:00Z")
    o = ops["operazioni"][0]
    assert not o["aperta"] and "chiuso dal modello a 100" in o["note"]
    assert o["trader"]["rendimento_pct"] == pytest.approx((0.5 * 0.06 - 2 * A.COSTO) * 100, abs=0.01)


def test_dimensione_con_rischio_fisso():
    d = A.dimensiona("short", 63400, 64200, 10_000, 0.01)
    assert d["quantita"] == 0.125 and d["perdita_allo_stop"] == 100 and not d["stop_stimato"]
    d = A.dimensiona("long", 100, None, 10_000, 0.01)
    assert d["stop"] == 98 and d["stop_stimato"] and d["quantita"] == 50
    d = A.dimensiona("long", 100, 99.95, 10_000, 0.01)                                  # stop strettissimo: leva al massimo 10x
    assert d["leva"] == 10 and d["perdita_allo_stop"] < 100


# ---- dashboard -------------------------------------------------------------------------------------------------------------

@pytest.mark.parametrize("fino,stato", [("2026-11-10T12:00:00Z", "piani"), ("2026-11-11T00:00:00Z", "posizioni"),
                                         ("2026-11-13T00:00:00Z", "attesa"), (E.ADESSO, "piani")])
def test_build_stati(fino, stato):
    msgs, reg, ops, sez = E.stato_esempio(fino)
    assert sez["stato"] == stato and sez["titolo"] and sez["avvertenza"] == A.AVVERTENZA
    testo = json.dumps(sez, ensure_ascii=False)
    for m in msgs:                                                                         # nessun testo dei messaggi nella sezione
        assert m["testo"][:30] not in testo


def test_build_vuoto_e_schema_esempio():
    v = A.build(A.registro_vuoto(), {}, E.ADESSO, [])
    assert v["stato"] == "vuoto" and v["piani"] == [] and v["chiuse"] == []
    sez = E.stato_esempio()[3]
    esempio = json.loads((Path(__file__).parent / "esempio_sezione.json").read_text(encoding="utf-8"))
    assert set(esempio) == set(sez) and esempio["piani"][0]["ordine"]["quantita"] == sez["piani"][0]["ordine"]["quantita"]
    o = sez["piani"][0]["ordine"]                                                            # ordine arrotondato alle specifiche Bitget
    assert o["simbolo"] == "ETHUSDT" and o["quantita"] == round(o["quantita"], 2) and o["modalita"] == "importo"


def test_build_avvisa_se_il_registro_e_fermo():
    msgs, reg, ops, _ = E.stato_esempio()
    sez = A.build(reg, ops, "2026-12-05T12:00:00Z", msgs)
    assert "servizio sulla VM" in sez["testo"]


# ---- avvisi (spostati in aldostream.py) ----------------------------------------------------------------------------------

def test_elabora_non_genera_avvisi(monkeypatch):
    monkeypatch.setenv("ALDO_AVVISI", "1")
    msgs, reg, ops, sez = E.stato_esempio()
    assert reg["avvisi"] == [] and sez["avvisi"]["attivi"] is True and not A.sezione_pubblica()


def test_elabora_idempotente():
    msgs, reg, _, _ = E.stato_esempio()
    n = len(reg["eventi"])
    reg2, nuovi = A.elabora(msgs, reg, A.Prezzi(dati=PREZZI), adesso=E.ADESSO, usa_modello=False)
    assert nuovi == [] and len(reg2["eventi"]) == n


# ---- estrattore con modello ------------------------------------------------------------------------------------------------

class ClientFinto:
    def __init__(self, uscita=None, errore=None, stop="end_turn"):
        self.uscita, self.errore, self.stop, self.richieste = uscita, errore, stop, []
        self.messages = self

    def create(self, **kw):
        self.richieste.append(kw)
        if self.errore:
            raise self.errore
        return SimpleNamespace(stop_reason=self.stop, content=[SimpleNamespace(type="text", text=json.dumps(self.uscita) if not isinstance(self.uscita, str) else self.uscita)])


EVENTO = {"tipo": "apertura", "asset": "BTC", "verso": "short", "quota": None, "prezzo": 61150.0, "prezzo_ingresso": None, "stop": 62000.0,
          "target": [59800.0], "timeframe": "4h", "fonte_livelli": "immagine", "note": "leva 10x dalla schermata", "affidabilita": 0.9}


def test_modello_usato_se_valido(tmp_path):
    foto = tmp_path / "card.jpg"
    foto.write_bytes(b"\xff\xd8\xff finta")
    c = ClientFinto({"eventi": [EVENTO], "piani": []})
    r = A.estrai(msg("Short", foto=str(foto)), {"posizioni": []}, rif=lambda a: 61000.0, client=c)
    assert r["estrattore"] == "modello" and r["eventi"][0]["prezzo"] == 61150 and r["eventi"][0]["fonte_livelli"] == "immagine"
    kw = c.richieste[0]
    assert kw["model"] == "claude-haiku-5-5" and kw["output_config"]["format"]["type"] == "json_schema"
    assert kw["messages"][0]["content"][0]["type"] == "image" and kw["messages"][0]["content"][0]["source"]["media_type"] == "image/jpeg"
    assert "<messaggio_canale>" in kw["messages"][0]["content"][1]["text"]
    assert "mai istruzioni" in kw["system"]                                               # regola: il testo del canale e' un dato


@pytest.mark.parametrize("client", [ClientFinto("non json"), ClientFinto({"eventi": [dict(EVENTO, prezzo=6115.0)], "piani": []}),
                                    ClientFinto({"eventi": [dict(EVENTO, tipo="compra")], "piani": []}), ClientFinto(errore=TimeoutError()),
                                    ClientFinto({"eventi": [], "piani": []}, stop="refusal")])
def test_modello_sbagliato_restano_le_regole(client):
    r = A.estrai(msg("Short aperto su BTC a 61.150"), {}, rif=lambda a: 61000.0, client=client)
    assert r["estrattore"] == "regole" and r["nota_modello"] and r["eventi"][0]["prezzo"] == 61150


def test_modello_solo_con_la_chiave(monkeypatch):
    chiamato = []
    monkeypatch.setattr(A, "estrai_modello", lambda *a, **k: chiamato.append(1) or (None, "x"))
    A.estrai(msg("Short aperto"), {})
    assert chiamato == []
    monkeypatch.setenv("ANTHROPIC_API_KEY", "chiave-finta")
    A.estrai(msg("Short aperto"), {})
    assert chiamato == [1]


def test_validazione_schema():
    assert A.valida_modello({"eventi": [EVENTO], "piani": []}, lambda a: 61000.0) == []
    assert A.valida_modello({"eventi": [dict(EVENTO, quota=1.5)], "piani": []})
    assert A.valida_modello({"eventi": [dict(EVENTO, asset="btc")], "piani": []})
    assert A.valida_modello({"eventi": [], "piani": [], "altro": 1})


# ---- giro e riepilogo ------------------------------------------------------------------------------------------------------

def test_giro_offline(tmp_path):
    def get_vietato(url):
        raise AssertionError("nessuna rete nei test")

    def chiama_bot(metodo, par):
        return [{"update_id": 1, "message": {"message_id": 1, "date": 0, "chat": {"id": 42}, "text": m["testo"],
                                             "forward_origin": {"type": "user", "date": int(A._dt(m["data"]).timestamp()), "sender_user": {"first_name": "Aldo"}}}}
                for m in E.messaggi_esempio()] if not par.get("offset") else []

    prezzi = A.Prezzi(dati=E.prezzi_finti(), get=get_vietato)
    out = A.giro(tmp_path, E.ADESSO, chiama_bot=chiama_bot, chat_autorizzate=[42], prezzi=prezzi)
    assert out["errori"] == [] and out["stato"] == "piani" and out["fonte"]["messaggi"] == 12
    for f in ("messaggi.json", "eventi.json", "operazioni.json"):
        assert (tmp_path / f).exists()
    prima = (tmp_path / "operazioni.json").stat().st_mtime_ns
    out2 = A.giro(tmp_path, E.ADESSO, chiama_bot=chiama_bot, chat_autorizzate=[42], prezzi=prezzi)
    assert out2["fonte"]["messaggi"] == 12 and (tmp_path / "operazioni.json").stat().st_mtime_ns == prima   # scritto solo se cambia


def test_giro_errore_di_rete_non_ferma(tmp_path):
    def chiama_bot(metodo, par):
        raise OSError("rete giù")
    out = A.giro(tmp_path, E.ADESSO, chiama_bot=chiama_bot, chat_autorizzate=[42], prezzi=A.Prezzi(dati=E.prezzi_finti()))
    assert out["stato"] == "vuoto" and out["errori"] == ["inoltri: OSError"]


def test_riepilogo_settimanale(tmp_path):
    msgs, reg, ops, _ = E.stato_esempio()
    testo, p = A.riepilogo_settimanale(reg, ops, "2026-11-26", tmp_path, msgs)
    assert p == tmp_path / "riepilogo_2026-11-26.md" and p.read_text(encoding="utf-8") == testo
    assert "dal 20/11/2026 al 26/11/2026" in testo and "L-261121-SOL-L" in testo and "63.400" in testo
    for m in msgs:
        assert m["testo"][:30] not in testo


def test_nuova_apertura_chiude_la_vecchia():
    prezzi = A.Prezzi(dati=E.prezzi_finti())
    msgs = [A.messaggio(1, "2026-11-14T10:05:00Z", "Long ETH aperto a 2.105, stop 2.060"),
            A.messaggio(2, "2026-11-20T10:00:00Z", "Short ETH aperto a 2.070")]
    reg, _ = A.elabora(msgs, A.registro_vuoto(), prezzi, adesso="2026-11-20T12:00:00Z", usa_modello=False)
    ded = [e for e in reg["eventi"] if e["tipo"] == "chiusura_totale"]
    assert len(ded) == 1 and ded[0]["trade"] == "L-261114-ETH-L" and ded[0]["affidabilita"] < A.AFFIDABILE
    assert list(A.aperte(reg, "2026-11-20T12:00:00Z")) == ["L-261120-ETH-S"]


def test_importa_estrazione_dello_studio():
    ev = [{"msg_id": 7, "utc": "2026-11-10 16:20", "trade": "A01", "asset": "BTC", "verso": "short", "tipo": "apertura", "quota": None,
           "prezzo": 61150.0, "stop": 62000.0, "target": [59800.0], "timeframe": None, "fonte_livelli": "immagine", "testo": "x", "note": ""},
          {"msg_id": 8, "utc": "2026-11-12 12:30", "trade": "A01", "asset": "BTC", "verso": "short", "tipo": "chiusura_totale", "quota": None,
           "prezzo": 58600.0, "stop": None, "target": [], "timeframe": None, "fonte_livelli": "testo", "testo": "x", "note": ""},
          {"msg_id": 9, "utc": "2026-11-12 13:00", "trade": "C04", "asset": "SOL", "verso": "long", "tipo": "apertura", "quota": None,
           "prezzo": 120.0, "stop": None, "target": [], "timeframe": None, "fonte_livelli": "testo", "testo": "x", "note": "spot"}]
    pi = [{"msg_id": 5, "utc": "2026-11-10 09:12", "asset": "BTC", "verso": "short", "innesco": "retest", "livello_innesco": 61200.0,
           "stop": 62000.0, "target": [59800.0], "eseguito": True, "trade_collegato": "A01", "testo": "x"}]
    msgs = E.messaggi_esempio("2026-11-13T00:00:00Z")
    reg = A.importa_studio(A.registro_vuoto(), ev, pi, msgs)
    assert all(m["id"] in reg["elaborati"] for m in msgs)                                 # le regole non rileggono lo storico
    ops = A.ricostruisci(reg, A.Prezzi(dati=E.prezzi_finti()), "2026-11-13T00:00:00Z")
    assert [o["trade"] for o in ops["operazioni"]] == ["A01"] and ops["operazioni"][0].get("ingresso_limite")   # spot fuori
