"""TAO: regola a fascia 'compra in zona supporto, vendi a target' sui dati giornalieri Binance TAOUSDT (dal 04/2024).
Acquisto con ordine limite al prezzo `buy`, vendita con ordine limite a `sell`; costi 0,1% per lato. Una posizione alla volta."""
import pandas as pd

d = pd.read_csv("data/tao/binance_TAOUSDT_1d.csv", parse_dates=["ts"]).set_index("ts")
FEE = 0.001


def run(buy, sell):
    pos, out, entry, t0, low = False, [], None, None, None
    for t, r in d.iterrows():
        if not pos and r.low <= buy:
            pos, entry, t0, low = True, min(r.open, buy), t, r.low
            continue                                   # il target non conta nel giorno d'ingresso
        if pos:
            low = min(low, r.low)
            if r.high >= sell:
                out.append((t0.date(), t.date(), entry, sell, sell / entry * (1 - FEE) ** 2 - 1, (t - t0).days, low / entry - 1))
                pos = False
    last = d.close.iloc[-1]
    op = (t0.date(), None, entry, last, last / entry - 1, (d.index[-1] - t0).days, low / entry - 1) if pos else None
    return out, op


if __name__ == "__main__":
    print("| Compra a | Vendi a | Cicli chiusi | Guadagno per ciclo | Giorni medi in posizione | Peggior calo dopo l'acquisto | Capitale composto | Posizione aperta ora |")
    print("|---|---|---|---|---|---|---|---|")
    for buy in (170, 190, 210):
        for sell in (300, 350, 400, 500):
            tr, op = run(buy, sell)
            comp = 1.0
            for x in tr:
                comp *= 1 + x[4]
            mae = min([x[6] for x in tr] + ([op[6]] if op else [0]))
            days = sum(x[5] for x in tr) / len(tr) if tr else 0
            g = f"{tr[0][4] * 100:+.0f}%" if tr else "–"
            o = f"dal {op[0]} a {op[2]:.0f} $, ora {op[4] * 100:+.0f}%" if op else "no"
            print(f"| {buy} | {sell} | {len(tr)} | {g} | {days:.0f} | {mae * 100:.0f}% | x{comp:.1f} | {o} |")
    tr, op = run(170, 300)
    print("\ncicli 170->300:", [(str(a), str(b), n) for a, b, _, _, _, n, _ in tr], op)
    tr, op = run(170, 500)
    print("cicli 170->500:", [(str(a), str(b), n) for a, b, _, _, _, n, _ in tr], op)
    # massimo raggiunto dopo ogni visita alla zona <=170 (prima della visita successiva)
    w = d.resample("W-SUN").agg({"high": "max", "low": "min", "close": "last"})
    print("\nsettimane con chiusura <= 200:", int((w.close <= 200).sum()), "di", len(w), "| con minimo <= 170:", int((w.low <= 170).sum()))
    print("chiusure settimanali sotto 170:", int((w.close < 170).sum()), "| minimo assoluto:", d.low.min(), d.low.idxmin().date())
