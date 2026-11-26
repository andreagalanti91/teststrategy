"""Idea di Aldo applicata a W3.2: stesso segnale, ingresso migliore con ordini sul livello o dopo una presa di liquidita'.

Per ogni operazione di W3.2 (segnale settimanale, ingresso all'apertura del lunedi'), tre modi di entrare nella prima settimana:
- lunedi': come W3.2 (riferimento);
- limite: ordine limite al minimo (long) / massimo (short) delle 48 ore prima del lunedi'; se non viene eseguito entro 7 giorni
  si entra a mercato alla fine della settimana;
- sweep & reclaim: prima discesa sotto il minimo delle 24 ore precedenti con rientro entro un'ora (15 minuti, come Eliz), nel
  verso del segnale; se non succede entro 7 giorni, ingresso a fine settimana.
Uscita uguale a W3.2 (stesso giorno e prezzo). Se W3.2 esce prima che l'ordine venga eseguito, l'operazione salta.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import intraday as I

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "results" / "intraday_combo"
pct = lambda x, d=1: "n/d" if x is None or not np.isfinite(x) else f"{x * 100:+.{d}f}%".replace(".", ",")
num = lambda x, d=2: f"{x:.{d}f}".replace(".", ",")


def main():
    b = I.load("binance")
    O, H, L, C = (b[k].to_numpy() for k in ("open", "high", "low", "close"))
    idx = b.index
    tr = pd.read_csv(ROOT / "results" / "w32" / "movimenti_w32.csv")
    rows = []
    for t in tr.itertuples():
        sg = 1 if t.verso == "long" else -1
        t0 = pd.Timestamp(t.entra)
        t_exit = pd.Timestamp(t.esce) if isinstance(t.esce, str) else idx[-1]
        i0 = idx.searchsorted(t0)
        iw = min(idx.searchsorted(t0 + pd.Timedelta(days=7)), len(idx) - 1)
        base = float(t.prezzo_in)
        res = {"verso": t.verso, "entra": t.entra, "lunedi": base}
        # limite al minimo/massimo delle 48 ore prima
        lev = (L[i0 - 192:i0].min() if sg > 0 else H[i0 - 192:i0].max())
        hit = np.where((L[i0:iw] <= lev) if sg > 0 else (H[i0:iw] >= lev))[0]
        res["limite"] = (min(O[i0 + hit[0]], lev) if sg > 0 else max(O[i0 + hit[0]], lev)) if len(hit) else O[iw]
        res["limite_t"] = idx[i0 + hit[0]] if len(hit) else idx[iw]
        # sweep & reclaim sulle 24 ore precedenti
        px, tt = O[iw], idx[iw]
        for i in range(i0, iw):
            ref = L[i - 96:i - 4].min() if sg > 0 else H[i - 96:i - 4].max()
            if (sg > 0 and L[i] < ref * 0.999) or (sg < 0 and H[i] > ref * 1.001):
                for k in range(i, min(i + 4, iw)):
                    if (sg > 0 and C[k] > ref) or (sg < 0 and C[k] < ref):
                        px, tt = O[k + 1], idx[k + 1]
                        break
                else:
                    continue
                break
        res["sweep"], res["sweep_t"] = px, tt
        out = float(t.prezzo_out)
        for k in ("lunedi", "limite", "sweep"):
            tk = t0 if k == "lunedi" else res[f"{k}_t"]
            res[f"mossa_{k}"] = sg * (out / res[k] - 1) if tk < t_exit else np.nan   # se W3.2 e' gia' uscita, l'operazione salta
        res["esposizione"] = t.esposizione
        res["sul_capitale"] = t.sul_capitale
        rows.append(res)
    d = pd.DataFrame(rows)
    T = ["## E1 esecuzione\n", "Le 23 operazioni di W3.2 dal 2018, stesso segnale e stessa uscita, tre modi di entrare. Risultato sul capitale = esposizione di W3.2 × movimento.\n",
         "| Ingresso | Operazioni eseguite | Prezzo d'ingresso migliore del lunedì | Miglioramento medio del prezzo | 10.000 $ → | Operazioni saltate |",
         "|---|---|---|---|---|---|"]
    for k, lab in (("lunedi", "Apertura del lunedì (W3.2)"), ("limite", "Ordine limite al minimo/massimo delle 48 ore prima (Aldo)"), ("sweep", "Presa di liquidità e rientro a 15 minuti (Eliz)")):
        m = d[f"mossa_{k}"]
        better = (d[k] < d.lunedi) if True else None
        imp = np.where(d.verso == "long", d.lunedi / d[k] - 1, d[k] / d.lunedi - 1)
        r = (d.esposizione * m).fillna(0.0) - np.where(m.notna(), 0.002, 0.0) * d.esposizione
        T.append(f"| {lab} | {int(m.notna().sum())} | {int((imp > 0.0005).sum())} su {len(d)} | {pct(float(np.mean(imp)), 2)} | {f'{10000 * np.prod(1 + r):,.0f}'.replace(',', '.')} | {int(m.isna().sum())} |")
    d.to_csv(OUT / "w32_esecuzione.csv", index=False)
    (OUT / "tables_esecuzione.md").write_text("\n".join(T) + "\n")
    print("\n".join(T))
    print(d[["verso", "entra", "lunedi", "limite", "sweep", "mossa_lunedi", "mossa_limite", "mossa_sweep"]].round(3).to_string())


if __name__ == "__main__":
    main()
