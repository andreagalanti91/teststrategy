"""Test di aldo_bitget.py e aldostream.py, tutti offline: client Telegram finto, specifiche Bitget dal file d'esempio
(bitget_contratti_esempio.json, scaricato da api.bitget.com), messaggi e prezzi inventati (esempio.py)."""
import json
import sys
import threading
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import pytest

import aldo as A
import aldo_bitget as B
import aldostream as S
import esempio as E

UTC = timezone.utc
QUI = Path(__file__).parent
SPEC = B.carica_contratti(QUI / "bitget_contratti_esempio.json")
BTC, ETH, SOL = SPEC["BTCUSDT"], SPEC["ETHUSDT"], SPEC["SOLUSDT"]


@pytest.fixture(autouse=True)
def ambiente_pulito(monkeypatch):
    for k in ("ANTHROPIC_API_KEY", "ALDO_AVVISI", "IMPORTO_EUR", "LEVA", "LEVA_MAX", "MODALITA", "ORE_SILENZIOSE", "ALDO_BOT_TOKEN"):
        monkeypatch.delenv(k, raising=False)


# ---- configurazione --------------------------------------------------------------------------------------------------------

def test_configurazione_predefinita_e_limiti():
    c = S.Config.da_ambiente({})
    assert (c.modalita, c.importo_eur, c.leva, c.leva_max, c.rischio_pct, c.max_minuti, c.max_scostamento_pct, c.ordine_ore) == \
        ("importo", 1000, 5, 10, 2, 10, 0.5, 24)
    assert not c.avvisi_attivi and not c.sezione_pubblica and not c.silenzioso(datetime(2026, 11, 26, 2, tzinfo=UTC))
    c = S.Config.da_ambiente({"IMPORTO_EUR": "3000", "LEVA": "12", "LEVA_MAX": "15", "MODALITA": "boh"})
    assert c.importo_eur == 2000 and c.leva_max == 10 and c.leva == 10 and c.modalita == "importo" and len(c.avvertenze) == 4
    c = S.Config.da_ambiente({"ORE_SILENZIOSE": "23-7", "ALDO_FUSO": "Europe/Rome"})
    assert c.silenzioso(datetime(2026, 11, 26, 1, tzinfo=UTC)) and not c.silenzioso(datetime(2026, 11, 26, 12, tzinfo=UTC))


# ---- Bitget ----------------------------------------------------------------------------------------------------------------

def test_specifiche_vere_nel_file_d_esempio():
    assert set(SPEC) == {"BTCUSDT", "ETHUSDT", "SOLUSDT"}
    assert (BTC["sizeMultiplier"], BTC["minTradeNum"], BTC["pricePlace"]) == ("0.0001", "0.0001", "1")
    assert B.passo_prezzo(ETH) == B.Decimal("0.01")


def test_arrotondamenti():
    assert B.arrotonda_prezzo(BTC, 61234.56) == 61234.6
    assert B.arrotonda_prezzo(BTC, 61234.56, "short", "stop") == 61234.6 and B.arrotonda_prezzo(BTC, 61234.51, "short", "stop") == 61234.6
    assert B.arrotonda_prezzo(BTC, 61234.59, "long", "stop") == 61234.5                       # lo stop si arrotonda verso l'esterno
    assert B.arrotonda_quantita(ETH, 3.178) == 3.17 and B.arrotonda_quantita(SOL, 15.99) == 15.9
    assert B.arrotonda_quantita(BTC, 0.00009) == 0.0                                          # sotto il minimo


def test_ordine_modalita_importo():
    o = B.ordine(BTC, "short", 61200, 62000)
    assert o["quantita"] == 0.0882 and o["contratti"] == 882 and o["lato"] == "vendi"        # 1.000 € x 1,08 x 5 / 61.200
    assert o["leva"] == pytest.approx(5, abs=0.01) and o["perdita_stop_eur"] == pytest.approx(0.0882 * 800 / 1.08, abs=0.01)
    assert o["perdita_stop_pct_importo"] == pytest.approx(6.5, abs=0.1) and o["note"] == []
    lontano = B.ordine(BTC, "long", 60000, 52000)                                             # 13% di stop a leva 5 = 67% del margine
    assert "stop troppo lontano per questa leva: riduci la leva" in lontano["note"]
    s = B.ordine(SOL, "long", 68.5, None)
    assert s["stop_stimato"] and s["stop"] == pytest.approx(67.13) and s["quantita"] == 78.8
    assert B.ordine(BTC, "long", 60000, 61000).get("errore")                                  # stop dalla parte sbagliata


def test_ordine_modalita_rischio():
    o = B.ordine(BTC, "short", 61200, 62000, modalita="rischio", capitale_usdt=10_000, rischio_pct=2)
    assert o["quantita"] == 0.25 and o["perdita_stop_usdt"] == pytest.approx(200) and o["leva"] == pytest.approx(1.53, abs=0.01)
    stretto = B.ordine(BTC, "short", 61200, 61210, modalita="rischio", capitale_usdt=10_000, rischio_pct=2, leva_max=10)
    assert stretto["leva"] <= 10 and any("quantità ridotta" in n for n in stretto["note"])
    assert B.ordine(BTC, "long", 60000, 59000, modalita="rischio", capitale_usdt=50, rischio_pct=0.01).get("errore")   # sotto il minimo


def test_contratti_cache(tmp_path):
    chiamate = []

    def get(url):
        chiamate.append(url)
        return {"code": "00000", "data": json.loads((QUI / "bitget_contratti_esempio.json").read_text())["data"]}

    c = B.Contratti(tmp_path / "c.json", get=get)
    assert c.spec("BTC")["symbol"] == "BTCUSDT" and len(chiamate) == 1 and "productType=USDT-FUTURES" in chiamate[0]
    c2 = B.Contratti(tmp_path / "c.json", get=lambda u: (_ for _ in ()).throw(OSError()))
    assert c2.spec("ETH")["symbol"] == "ETHUSDT"                                               # dalla cache, senza rete
    assert c2.spec("XYZ") is None


def test_prezzi_bitget_finti():
    tick = json.loads((QUI / "bitget_ticker_esempio.json").read_text())
    get = lambda url: {"code": "00000", "data": [d for d in tick["data"] if d["symbol"] in url]}
    assert B.ticker("BTC", get) == float(next(d["lastPr"] for d in tick["data"] if d["symbol"] == "BTCUSDT"))
    ms = lambda h: str(int(pd.Timestamp(f"2026-11-24 {h:02d}:00", tz="UTC").timestamp() * 1000))
    pagine = [[[ms(10), "1", "2", "0.5", "1.5", "0", "0"], [ms(11), "1.5", "2", "1", "1.8", "0", "0"]],
              [[ms(8), "1", "1", "1", "1", "0", "0"], [ms(9), "1", "1", "1", "1", "0", "0"]], []]
    df = B.candele_ora("BTC", pd.Timestamp("2026-11-24 08:00"), pd.Timestamp("2026-11-24 11:00"), lambda u: {"code": "00000", "data": pagine.pop(0)})
    assert len(df) == 4 and df.index.is_monotonic_increasing
    with pytest.raises(RuntimeError):
        B.ticker("BTC", lambda u: {"code": "40034", "msg": "errore"})


def test_minuti_dal_prezzo():
    c = E.candele_minuto_finte("ETH", "2026-11-14T10:05:00Z")
    assert B.minuti_dal_prezzo(c, 1700.2, pd.Timestamp("2026-11-14 10:05")) < 3
    assert B.minuti_dal_prezzo(c, 1800, pd.Timestamp("2026-11-14 10:05")) is None


def test_esegui_su_bitget_e_solo_un_aggancio():
    with pytest.raises(NotImplementedError):
        B.esegui_su_bitget({})
    assert len(S.pulsanti("1.1")) == 1 and S.pulsanti("1.1", esegui_bitget=True)[1][0]["callback_data"] == "aldo:b:1.1"


# ---- servizio --------------------------------------------------------------------------------------------------------------

def test_avvisi_in_tempo_reale(tmp_path):
    s = E.gira_esempio(tmp_path, extra=True)
    bot = s.bot
    testi = [x["testo"] for x in bot.inviati]
    assert len(bot.inviati) == len(s.avvisi) == 14 and len({a["id"] for a in s.avvisi}) == 14
    primo = bot.inviati[0]
    assert "ORDINE LIMITE" in primo["testo"] and "0,0882 BTC" in primo["testo"] and "Allo stop perdi" in primo["testo"]
    assert primo["pulsanti"][0][0] == {"text": "Fatto", "callback_data": "aldo:f:101.1"} and not primo["silenzioso"]
    assert any("A MERCATO" in t and "ETH" in t for t in testi)                                     # ingresso rapido: si copia
    assert any("NON COPIARE" in t for t in testi)                                                   # entrato da molto: no
    parz = next(t for t in testi if "Chiudi il 50%" in t)
    assert "0,0441 BTC della tua posizione" in parz and "Risulta copiata da te" in parz
    assert any("Sposta lo stop a prezzo d'ingresso" in t for t in testi) and any("Chiudi il resto a mercato" in t for t in testi)
    assert all(a["latenza_s"] == 20 for a in s.avvisi)
    lat = s.latenze()
    assert len(lat) == 13 and S.latenza(lat)["mediana_s"] == 20                                      # 13 messaggi, uno senza eventi
    for t in testi:                                                                                  # nessun testo del canale negli avvisi
        assert "retest della resistenza" not in t and "fa parte del gioco" not in t
    assert (tmp_path / "avvisi.json").exists() and (tmp_path / "reale.json").exists() and (tmp_path / "sezione.json").exists()


def test_pulsanti_fatto_salto(tmp_path):
    s = E.gira_esempio(tmp_path, extra=False, fatto_su=())
    av = s.avvisi[0]
    cb = lambda dati, chat=42: {"id": "x", "data": dati, "message": {"message_id": av["telegram_id"], "chat": {"id": chat}}}
    assert s.su_pulsante(cb(f"aldo:f:{av['id']}", chat=7)) is None                                  # chat estranea: ignorata
    assert s.su_pulsante(cb(f"aldo:s:{av['id']}")) == "salto"
    assert s.su_pulsante(cb(f"aldo:f:{av['id']}")) == "salto" and s.bot.risposte[-1] == "Già registrato: salto"
    assert s.su_pulsante(cb(f"aldo:b:{av['id']}")) is None and "non attiva" in s.bot.risposte[-1]
    assert s.bot.chiusi and "Registrato: salto" in s.bot.chiusi[-1][1]
    assert s.reale["scelte"][-1]["scelta"] == "salto"
    ops = A.ricostruisci(s.registro, s.prezzi, E.ADESSO)
    r = S.statistiche_reali(s.avvisi, s.registro, ops)
    assert r["saltati"] == 1 and r["operazioni_saltate"] == 1 and r["operazioni_copiate"] == 0


def test_statistiche_reali_copia_contro_carta(tmp_path):
    s = E.gira_esempio(tmp_path, extra=False, fatto_su=("101.1",))
    ops = A.carica_json(tmp_path / "operazioni.json", {})
    r = S.statistiche_reali(s.avvisi, s.registro, ops)
    btc = next(o for o in ops["operazioni"] if o["trade"] == "L-261110-BTC-S")
    assert r["operazioni_copiate"] == 1 and r["copiate_chiuse"] == 1 and r["medio_pct"] == btc["limite"]["rendimento_pct"]


def test_avvisi_spenti_finche_non_approvati(tmp_path):
    ora = E.Orologio("2026-11-10T09:12:20Z")
    bot = E.BotFinto()
    s = E.servizio_esempio(tmp_path, ora, S.Config(dati=tmp_path, chat_id="42", bot_token="x", bot_dedicato=True, avvisi_attivi=False), bot)
    av = s.su_messaggio(E.messaggi_esempio()[0])
    assert av and av[0]["stato"] == "proposto" and bot.inviati == []


def test_senza_bot_dedicato_niente_pulsanti(tmp_path):
    ora = E.Orologio("2026-11-10T09:12:20Z")
    bot = E.BotFinto()
    s = E.servizio_esempio(tmp_path, ora, S.Config(dati=tmp_path, chat_id="42", bot_token="x", bot_dedicato=False, avvisi_attivi=True), bot)
    s.su_messaggio(E.messaggi_esempio()[0])
    assert bot.inviati[0]["pulsanti"] is None


def test_regola_a_mercato(tmp_path):
    msg = A.messaggio(200, "2026-11-14T10:05:00Z", "Long ETH aperto a 1.701, stop 1.670")
    for prezzo_mult, ritardo_min, atteso in ((1.0, 0.3, "A MERCATO"), (1.01, 0.3, "NON COPIARE"), (1.0, 15, "NON COPIARE")):
        d = tmp_path / f"{prezzo_mult}-{ritardo_min}"
        ora = E.Orologio(A._dt(msg["data"]) + timedelta(minutes=ritardo_min))
        s = E.servizio_esempio(d, ora)
        s.prezzo_ora = lambda a, m=prezzo_mult: E._prezzo(a, ora()) * m
        av = s.su_messaggio(dict(msg))
        assert atteso in av[0]["testo"] and av[0]["azionabile"] == (atteso == "A MERCATO")
    vecchio = tmp_path / "vecchio"
    ora = E.Orologio(A._dt(msg["data"]) + timedelta(hours=30))                                    # recupero dopo 30 ore: nessun avviso
    assert E.servizio_esempio(vecchio, ora).su_messaggio(dict(msg)) == []


def test_errore_di_rete_bitget_non_ferma(tmp_path):
    ora = E.Orologio("2026-11-10T09:12:20Z")
    s = E.servizio_esempio(tmp_path, ora)
    s.prezzo_ora = lambda a: (_ for _ in ()).throw(OSError("rete giù"))
    av = s.su_messaggio(E.messaggi_esempio()[0])
    assert av and "ORDINE LIMITE" in av[0]["testo"] and "Prezzo ora" not in av[0]["testo"]


def test_modifiche(tmp_path):
    ora = E.Orologio("2026-11-10T16:21:00Z")
    s = E.servizio_esempio(tmp_path, ora)
    vuoto = A.messaggio(300, "2026-11-10T16:20:00Z", "Guardate questo grafico")
    assert s.su_messaggio(vuoto) == []
    av = s.su_modifica(A.messaggio(300, "2026-11-10T16:20:00Z", "Short aperto su BTC a 61.150"))   # prima non diceva nulla: si rilegge
    assert av and av[0]["tipo"] == "apertura"
    av = s.su_modifica(A.messaggio(300, "2026-11-10T16:20:00Z", "Short aperto su BTC a 61.250"))   # gia' estratto: solo avviso
    assert av[0]["tipo"] == "modifica" and not av[0]["azionabile"] and s.registro["da_rivedere"][-1]["msg_id"] == "300"


def test_ore_silenziose(tmp_path):
    ora = E.Orologio("2026-11-10T09:12:20Z")                                                       # 10:12 a Roma
    bot = E.BotFinto()
    cfg = S.Config(dati=tmp_path, chat_id="42", bot_token="x", bot_dedicato=True, avvisi_attivi=True, ore_silenziose="9-11")
    E.servizio_esempio(tmp_path, ora, cfg, bot).su_messaggio(E.messaggi_esempio()[0])
    assert bot.inviati[0]["silenzioso"] is True


def test_riepilogo_del_lunedi(tmp_path):
    s = E.gira_esempio(tmp_path, extra=False)
    lunedi = datetime(2026, 11, 23, 7, 30, tzinfo=UTC)
    n = len(s.bot.inviati)
    s.ogni_ora(lunedi)
    assert (tmp_path / "riepilogo_2026-11-22.md").exists() and len(s.bot.inviati) == n + 1
    assert "riepilogo fino al 22/11" in s.bot.inviati[-1]["testo"]
    s.ogni_ora(lunedi + timedelta(hours=1))
    assert len(s.bot.inviati) == n + 1                                                               # una volta sola


def test_bot_telegram_finto(capsys, monkeypatch):
    chiamate = []
    risposte = [{"ok": False, "description": "Too Many Requests", "parameters": {"retry_after": 1}}, {"ok": True, "result": {"message_id": 5}}]

    def post(metodo, dati):
        chiamate.append((metodo, dati))
        return risposte.pop(0)

    monkeypatch.setattr(S.time, "sleep", lambda s: None)
    bot = S.BotTelegram("123:SEGRETO", "42", post=post)
    assert bot.invia("<b>prova</b>", S.pulsanti("1.1"), silenzioso=True) == 5 and len(chiamate) == 2
    m, d = chiamate[0]
    assert m == "sendMessage" and d["chat_id"] == "42" and d["parse_mode"] == "HTML" and d["disable_notification"] is True
    assert d["reply_markup"]["inline_keyboard"][0][1]["callback_data"] == "aldo:s:1.1"
    bot2 = S.BotTelegram("123:SEGRETO", "42", post=lambda m, d: {"ok": False, "description": "Bad Request"})
    assert bot2.invia("x") is None
    assert "SEGRETO" not in capsys.readouterr().out


def test_ascolto_pulsanti(tmp_path):
    s = E.gira_esempio(tmp_path, extra=False, fatto_su=())
    fermo = threading.Event()
    av = s.avvisi[0]

    class BotCoda(E.BotFinto):
        def aggiornamenti(self, offset, timeout=30):
            fermo.set()
            return [{"update_id": 77, "callback_query": {"id": "c", "data": f"aldo:f:{av['id']}", "message": {"message_id": 1, "chat": {"id": 42}}}}]

    s.bot = BotCoda()
    s.ascolta_pulsanti(fermo)
    assert av["scelta"] == "fatto" and s.reale["offset"] == 78


def test_sezione_privata_di_default(tmp_path):
    s = E.gira_esempio(tmp_path, extra=False)
    sez = json.loads((tmp_path / "sezione.json").read_text(encoding="utf-8"))
    assert sez["copia"]["modalita"] == "importo" and sez["reale"]["fatti"] == 1 and sez["latenza"]["n"] == 11
    assert not A.sezione_pubblica() and "a pagamento" not in sez["avvertenza"] and "canale privato" in sez["avvertenza"]


def test_file_di_deploy():
    unit = (QUI / "deploy" / "aldostream.service").read_text(encoding="utf-8")
    assert "EnvironmentFile=/etc/aldostream.env" in unit and "Restart=always" in unit and "radar.aldostream" in unit
    guida = (QUI / "deploy" / "ALDOSTREAM.md").read_text(encoding="utf-8")
    for k in ("my.telegram.org", "TELEGRAM_API_ID", "TELEGRAM_API_HASH", "ALDO_CANALE_ID", "ANTHROPIC_API_KEY", "chmod 600", "accedi"):
        assert k in guida
