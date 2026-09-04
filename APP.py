import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math
import pandas as pd

st.set_page_config(layout="wide", page_title="Symulacja Napylania z Podcięciem")

col1, col2 = st.columns(2)

with col1:
    alpha = st.slider("alpha [deg]", 0, 45, 25, 1)
    p_mma_maa = st.slider("P(MMA-MAA) [\u03BCm]", 0.1, 2.0, 0.67, 0.01)
    undercut = st.slider("undercut [\u03BCm]", 0.0, 1.0, 0.20, 0.01)
    open_1 = st.slider("open 1 [\u03BCm]", 0.1, 2.0, 0.89, 0.01)
    margin = st.slider("margin [\u03BCm]", 0.1, 2.0, 0.55, 0.01)

with col2:
    beta = st.slider("beta [deg]", 0, 45, 20, 1)
    pmma_h = st.slider("PMMA [\u03BCm]", 0.1, 2.0, 0.28, 0.01)
    gap_pmma_input = st.slider("gap PMMA [\u03BCm]", 0.05, 1.0, 0.16, 0.01)
    open_2 = st.slider("open 2 [\u03BCm]", 0.1, 2.0, 0.75, 0.01)

x1 = margin
x2 = x1 + open_1
x4 = x2 + gap_pmma_input
x5 = x4 + open_2
xmax = x5 + margin

h = p_mma_maa + pmma_h
mma = p_mma_maa

alpha_rad = math.radians(alpha)
beta_rad = math.radians(beta)
b1_L = x1 + h * math.tan(alpha_rad)

b1_R = x2 + mma * math.tan(alpha_rad)

b2_L = x4 - mma * math.tan(beta_rad)
b2_R = x5 - h * math.tan(beta_rad)

overlap_L = max(b1_L, b2_L)
overlap_R = min(b1_R, b2_R)
overlap_val = max(0.0, overlap_R - overlap_L) * 1000

pozostala_szczelina = max(0.0, b2_L - b1_R) * 1000
gap_w_pmma = gap_pmma_input * 1000
gap_w_pmma_maa = max(0.0, gap_pmma_input - 2 * undercut) * 1000

fig, ax = plt.subplots(figsize=(10, 6))

c_pmma = '#D5D8DC'
c_pmma_maa = '#AED6F1'

ax.add_patch(patches.Rectangle((-0.5, -0.2), xmax + 1.0, 0.2, facecolor='#EAEAEA', edgecolor='black'))
ax.plot([-0.5, xmax + 1.0], [0, 0], color='black', linewidth=2)

ax.add_patch(patches.Rectangle((0, 0), x1 - undercut, mma, facecolor=c_pmma_maa, edgecolor='black', linewidth=1))
if gap_w_pmma_maa > 0:
    ax.add_patch(patches.Rectangle((x2 + undercut, 0), gap_w_pmma_maa / 1000, mma, facecolor=c_pmma_maa, edgecolor='black', linewidth=1))
ax.add_patch(patches.Rectangle((x5 + undercut, 0), xmax - x5 + undercut, mma, facecolor=c_pmma_maa, edgecolor='black', linewidth=1))

ax.add_patch(patches.Rectangle((0, mma), x1, pmma_h, facecolor=c_pmma, edgecolor='black', linewidth=1))
ax.add_patch(patches.Rectangle((x2, mma), x4 - x2, pmma_h, facecolor=c_pmma, edgecolor='black', linewidth=1))
ax.add_patch(patches.Rectangle((x5, mma), xmax - x5, pmma_h, facecolor=c_pmma, edgecolor='black', linewidth=1))

ax.text(0.1, mma + pmma_h/2, "PMMA", va='center', fontweight='bold', fontsize=9)
ax.text(0.1, mma/2, "P(MMA-MAA)", va='center', fontweight='bold', fontsize=9)

line_y = h + 0.3

x2_top = x2 - pmma_h * math.tan(alpha_rad)
beam1_poly = np.array([[x1, h], [x2_top, h], [b1_R, 0], [b1_L, 0]])
ax.add_patch(patches.Polygon(beam1_poly, facecolor='#A9CFF0', alpha=0.5))

line1_x1_top = b1_L - line_y * math.tan(alpha_rad)
ax.plot([b1_L, line1_x1_top], [0, line_y], color='#1C4587', linewidth=2)
line1_x2_top = b1_R - line_y * math.tan(alpha_rad)
ax.plot([b1_R, line1_x2_top], [0, line_y], color='#1C4587', linewidth=2)

x4_top = x4 + pmma_h * math.tan(beta_rad)
beam2_poly = np.array([[x4_top, h], [x5, h], [b2_R, 0], [b2_L, 0]])
ax.add_patch(patches.Polygon(beam2_poly, facecolor='#F5CBA7', alpha=0.5))

line2_x4_top = b2_L + line_y * math.tan(beta_rad)
ax.plot([b2_L, line2_x4_top], [0, line_y], color='#D35400', linewidth=2)
line2_x5_top = b2_R + line_y * math.tan(beta_rad)
ax.plot([b2_R, line2_x5_top], [0, line_y], color='#D35400', linewidth=2)

ax.plot([b1_L, b1_R], [0.03, 0.03], color='blue', linewidth=6)
ax.plot([b2_L, b2_R], [0.03, 0.03], color='#D35400', linewidth=6)
if overlap_val > 0:
    ax.plot([overlap_L, overlap_R], [0.06, 0.06], color='magenta', linewidth=8)

ax.plot(x1, h, 'ko', markersize=6)
ax.plot(x2, mma, 'ko', markersize=6)
ax.plot(x4, mma, 'ko', markersize=6)
ax.plot(x5, h, 'ko', markersize=6)

ax.text((x1 + x2)/2, h + 0.05, "open 1", ha='center', fontsize=10)
ax.text((x2 + x4)/2, h + 0.05, "gap PMMA", ha='center', fontsize=10)
ax.text((x4 + x5)/2, h + 0.05, "open 2", ha='center', fontsize=10)

ax.set_xlim(-0.1, xmax + 0.1)
ax.set_ylim(-0.2, h + 0.4)
ax.set_xlabel("{PlotLabel x [\u03BCm], PlotLabel wysokosc [\u03BCm]} \u2192")
ax.grid(False)

if overlap_val > 0:
    status_str = "OVERLAP"
elif pozostala_szczelina > 0:
    status_str = "GAP"
else:
    status_str = "STYK"

dane = {
    "Parametr": [
        "Gap w PMMA", "Gap w P(MMA-MAA)", "Dolne apertury polaczone?",
        "Footprint napylania 1", "Footprint napylania 2",
        "Wewnetrzna granica 1", "Wewnetrzna granica 2",
        "Zewnetrzna granica 1", "Zewnetrzna granica 2",
        "Overlap", "Pozostala szczelina", "STATUS"
    ],
    "Wartość": [
        f"{gap_w_pmma:.1f} nm",
        f"{gap_w_pmma_maa:.0f} nm",
        "TAK" if gap_w_pmma_maa <= 0 else "NIE",
        f"{(b1_R - b1_L)*1000:.1f} nm",
        f"{(b2_R - b2_L)*1000:.1f} nm",
        "PMMA: dolny prawy naroznik",
        "PMMA: dolny lewy naroznik",
        "PMMA: gorny lewy naroznik",
        "PMMA: gorny prawy naroznik",
        f"{overlap_val:.1f} nm",
        f"{pozostala_szczelina:.0f} nm",
        status_str
    ]
}

df = pd.DataFrame(dane)

st.markdown("### Diagnostyka geometrii")
st.dataframe(df, hide_index=True, use_container_width=True)
