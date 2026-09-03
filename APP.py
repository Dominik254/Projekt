# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 19:06:22 2026

@author: kubak
"""

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math

# Konfiguracja strony Streamlit na szerszą
st.set_page_config(layout="wide", page_title="Symulacja Napylania")

st.title("Symulacja geometrii napylania")

# --- INTERFEJS: SUWAKI (podzielone na kolumny jak na zdjęciu) ---
col1, col2 = st.columns(2)

with col1:
    alpha = st.slider("Kąt \u03B1 [deg]", 0, 45, 20, 1)
    h = st.slider("Grubość h [\u03BCm]", 0.5, 2.5, 1.25, 0.05)
    x1 = st.slider("x1 (open1 lewy) [\u03BCm]", 0.0, 1.2, 0.4, 0.02)
    x4 = st.slider("x4 (open2 lewy) [\u03BCm]", 1.2, 2.7, 2.0, 0.02)
    xmax = st.slider("xmax [\u03BCm]", 2.5, 5.0, 3.6, 0.1)

with col2:
    beta = st.slider("Kąt \u03B2 [deg]", 0, 45, 20, 1)
    mma = st.slider("Poziom MMA [\u03BCm]", 0.2, 2.0, 1.4, 0.05)
    x2 = st.slider("x2 (open1 prawy) [\u03BCm]", 0.5, 1.8, 1.1, 0.02)
    x5 = st.slider("x5 (open2 prawy) [\u03BCm]", 2.0, 3.5, 2.6, 0.02)

# --- OBLICZENIA FIZYCZNE ---
# Przeliczenie stopni na radiany do funkcji trygonometrycznych
alpha_rad = math.radians(alpha)
beta_rad = math.radians(beta)

# Wyliczenie przemieszczenia krawędzi snopów
x3 = x2 + h * math.tan(alpha_rad)
x6 = x4 - h * math.tan(beta_rad)

# Współrzędne wierzchołków dla trapezów (snopów)
beam1_pts = np.array([[x1, h], [x2, h], [x3, 0], [x1 + (x3 - x2), 0]])
beam2_pts = np.array([[x4, h], [x5, h], [x5 - (x4 - x6), 0], [x6, 0]])

# --- RYSOWANIE WYKRESU (Matplotlib) ---
fig, ax = plt.subplots(figsize=(10, 6))

# 1. Szaroniebieski pas PMMA
pmma_rect = patches.Rectangle((0, mma), xmax, 0.15, facecolor='#B3BFCB', edgecolor='gray', linewidth=1)
ax.add_patch(pmma_rect)

# 2. Podłoże krzemowe
ax.plot([0, xmax], [0, 0], color='black', linewidth=3)

# 3. Różowe/pomarańczowe snopy napylania (zależne od kątów)
beam1 = patches.Polygon(beam1_pts, closed=True, facecolor='#D91A80', alpha=0.85)
beam2 = patches.Polygon(beam2_pts, closed=True, facecolor='#D91A80', alpha=0.85)
ax.add_patch(beam1)
ax.add_patch(beam2)

# 4. Linie pionowe z otworów
ax.plot([x2, x2], [0, h], color='black', linestyle='-')
ax.plot([x4, x4], [0, h], color='black', linestyle='-')

# 5. Łuki kątów alpha i beta
arc1 = patches.Arc((x2, h), 0.7, 0.7, angle=0, theta1=-90, theta2=-90+alpha, color='black')
arc2 = patches.Arc((x4, h), 0.7, 0.7, angle=0, theta1=-90-beta, theta2=-90, color='black')
ax.add_patch(arc1)
ax.add_patch(arc2)

# Tekst kątów
ax.text(x2 + 0.1, h - 0.25, r'$\alpha$', fontsize=12, style='italic')
ax.text(x4 - 0.2, h - 0.25, r'$\beta$', fontsize=12, style='italic')

# 6. Etykiety otworów
ax.text((x1 + x2)/2, mma + 0.07, "open1", fontsize=10, ha='center')
ax.text((x2 + x4)/2, mma + 0.07, "gap", fontsize=10, ha='center')
ax.text((x4 + x5)/2, mma + 0.07, "open2", fontsize=10, ha='center')

# 7. Wysokość h po prawej
ax.plot([xmax + 0.1, xmax + 0.1], [0, h], color='black')
ax.text(xmax + 0.2, h/2, 'h', fontsize=12, style='italic')

# 8. Linie wymiarowe na dole
ax.plot([x2, x2], [0, -0.25], 'k--')
ax.plot([x3, x3], [0, -0.45], 'k--')
ax.plot([x6, x6], [0, -0.45], 'k--')
ax.plot([x4, x4], [0, -0.65], 'k--')

ax.text((x2 + x3)/2, -0.15, 'a', fontsize=10, style='italic', ha='center')
ax.text((x3 + x6)/2, -0.35, 'b', fontsize=10, style='italic', ha='center')
ax.text((x2 + x6)/2, -0.55, 'w', fontsize=10, style='italic', ha='center')

# Ustawienia osi i limitów wykresu
ax.set_xlim(-0.2, xmax + 0.4)
ax.set_ylim(-0.8, h + 0.25)
ax.set_xlabel(r"$\mu m$")
ax.grid(False)

# Wyświetlenie wykresu w Streamlit
st.pyplot(fig)