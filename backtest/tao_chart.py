"""Grafico di TAO (Bitget spot, settimanale): zona di supporto, massimi decrescenti dei rimbalzi, livelli della proposta."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
INK, MUTED, GRID, SURF, BLUE, ORANGE, AQUA, RED = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb", "#2a78d6", "#eb6834", "#1baf7a", "#d03b3b"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED,
                     "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "savefig.facecolor": SURF})
d = pd.read_csv(ROOT / "data" / "tao" / "bitget_TAOUSDT_spot_1d.csv", parse_dates=["ts"]).set_index("ts")
w = d.resample("W-SUN").agg({"high": "max", "low": "min", "close": "last"}).loc["2023-10-01":]
fig, ax = plt.subplots(figsize=(10, 5.6))
ax.axhspan(150, 190, color=AQUA, alpha=0.16, lw=0)
ax.vlines(w.index, w.low, w.high, color=BLUE, lw=0.8, alpha=0.45)
ax.plot(w.index, w.close, color=BLUE, lw=2)
peaks = [("2024-04-01", "2024-04-30"), ("2024-12-01", "2024-12-31"), ("2025-10-20", "2025-11-15"), ("2026-03-15", "2026-04-10"), ("2026-09-15", "2026-10-10")]
pts = []
for a, b in peaks:
    seg = d.loc[a:b, "high"]
    pts.append((seg.idxmax(), float(seg.max())))
ax.plot([p[0] for p in pts], [p[1] for p in pts], color=ORANGE, lw=1.6, ls=(0, (5, 3)), marker="o", ms=7, mec=SURF, mew=1.5, zorder=3)
for t, v in pts:
    ax.annotate(f"{v:.0f}", (t, v), xytext=(0, 9), textcoords="offset points", ha="center", fontsize=9, color=INK)
ax.axhline(126, color=RED, lw=1.4, ls=(0, (2, 2)))
end = w.index[-1]
ax.annotate("stop: chiusura sotto 126", (end, 126), xytext=(8, -4), textcoords="offset points", fontsize=9, color=INK, va="top")
ax.annotate("zona d'acquisto 150–190", (end, 170), xytext=(8, 0), textcoords="offset points", fontsize=9, color=INK, va="center")
ax.annotate("massimi dei rimbalzi", (pts[2][0], pts[2][1]), xytext=(30, 34), textcoords="offset points", fontsize=9, color=INK)
ax.annotate(f"prezzo {w.close.iloc[-1]:.0f}", (end, w.close.iloc[-1]), xytext=(8, 14), textcoords="offset points", fontsize=9, color=INK)
ax.set_xlim(w.index[0], end + pd.Timedelta(days=200))
ax.set_ylim(0, 820)
ax.grid(axis="y", color=GRID, lw=0.8)
ax.set_ylabel("USDT")
ax.set_title("TAO settimanale (Bitget spot): supporto piatto, rimbalzi sempre più bassi", loc="left", color=INK, fontsize=12, fontweight="bold")
fig.savefig(ROOT / "results" / "tao" / "tao.png", dpi=160, bbox_inches="tight")
print(pts)
