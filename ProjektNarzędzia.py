import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# Początkowe wartości parametrów
init_alpha, init_beta = 20, 20
init_h, init_mma = 1.25, 1.4
init_x1, init_x2 = 0.4, 1.1
init_x4, init_x5 = 2.0, 2.6
init_xmax = 3.6

fig, ax = plt.subplots(figsize=(9, 6))
plt.subplots_adjust(left=0.35, bottom=0.1)

def draw_geometry(alpha, beta, h, mma, x1, x2, x4, x5, xmax):
    ax.clear()
    
    x3 = x2 + h * np.tan(np.radians(alpha))
    x6 = x4 - h * np.tan(np.radians(beta))
    
    beam1 = np.array([[x1, h], [x2, h], [x3, 0], [x1 + (x3 - x2), 0]])
    beam2 = np.array([[x4, h], [x5, h], [x5 - (x4 - x6), 0], [x6, 0]])
    
    # Pas PMMA
    ax.add_patch(plt.Rectangle((0, mma), xmax, 0.15, facecolor=(0.7, 0.75, 0.8), edgecolor=(0.4, 0.4, 0.4)))
    # Podłoże
    ax.plot([0, xmax], [0, 0], color='black', linewidth=2)
    # Snopy
    ax.add_patch(plt.Polygon(beam1, facecolor=(0.85, 0.1, 0.5), alpha=0.85))
    ax.add_patch(plt.Polygon(beam2, facecolor=(0.85, 0.1, 0.5), alpha=0.85))
    
    # Pionowe linie
    ax.plot([x2, x2], [h, 0], color='black', lw=1)
    ax.plot([x4, x4], [h, 0], color='black', lw=1)
    
    # Łuki kątów
    t = np.linspace(np.radians(-90), np.radians(-90 + alpha), 30)
    ax.plot(x2 + 0.35 * np.cos(t), h + 0.35 * np.sin(t), color='black')
    ax.text(x2 + 0.18, h - 0.22, r'$\alpha$', fontsize=12)
    
    t_b = np.linspace(np.radians(-90 - beta), np.radians(-90), 30)
    ax.plot(x4 + 0.35 * np.cos(t_b), h + 0.35 * np.sin(t_b), color='black')
    ax.text(x4 - 0.18, h - 0.22, r'$\beta$', fontsize=12)
    
    # Etykiety
    ax.text((x1 + x2)/2, mma + 0.07, 'open1', ha='center')
    ax.text((x2 + x4)/2, mma + 0.07, 'gap', ha='center')
    ax.text((x4 + x5)/2, mma + 0.07, 'open2', ha='center')
    
    # Przerywane linie wymiarowe
    ax.plot([x2, x2], [0, -0.25], 'k--', lw=1)
    ax.plot([x3, x3], [0, -0.45], 'k--', lw=1)
    ax.plot([x6, x6], [0, -0.45], 'k--', lw=1)
    ax.plot([x4, x4], [0, -0.25], 'k--', lw=1)
    
    ax.text((x2 + x3)/2, -0.15, 'a', fontstyle='italic', ha='center')
    ax.text((x3 + x6)/2, -0.35, 'b', fontstyle='italic', ha='center')
    ax.text((x2 + x6)/2, -0.55, 'w', fontstyle='italic', ha='center')
    
    ax.set_xlim(-0.2, xmax + 0.4)
    ax.set_ylim(-0.8, h + 0.25)
    ax.set_ylabel(r'$\mu$m')
    ax.grid(True, linestyle=':', alpha=0.4)

draw_geometry(init_alpha, init_beta, init_h, init_mma, init_x1, init_x2, init_x4, init_x5, init_xmax)

# Definicje suwaków po lewej stronie
ax_alpha = plt.axes([0.05, 0.85, 0.2, 0.03])
ax_beta  = plt.axes([0.05, 0.80, 0.2, 0.03])
ax_h     = plt.axes([0.05, 0.75, 0.2, 0.03])
ax_mma   = plt.axes([0.05, 0.70, 0.2, 0.03])
ax_x1    = plt.axes([0.05, 0.60, 0.2, 0.03])
ax_x2    = plt.axes([0.05, 0.55, 0.2, 0.03])
ax_x4    = plt.axes([0.05, 0.50, 0.2, 0.03])
ax_x5    = plt.axes([0.05, 0.45, 0.2, 0.03])
ax_xmax  = plt.axes([0.05, 0.35, 0.2, 0.03])

s_alpha = Slider(ax_alpha, 'α (°)', 0, 45, valinit=init_alpha, valstep=1)
s_beta  = Slider(ax_beta, 'β (°)', 0, 45, valinit=init_beta, valstep=1)
s_h     = Slider(ax_h, 'h (µm)', 0.5, 2.5, valinit=init_h, valstep=0.05)
s_mma   = Slider(ax_mma, 'MMA (µm)', 0.2, 2.0, valinit=init_mma, valstep=0.05)
s_x1    = Slider(ax_x1, 'x1', 0.0, 1.2, valinit=init_x1, valstep=0.02)
s_x2    = Slider(ax_x2, 'x2', 0.5, 1.8, valinit=init_x2, valstep=0.02)
s_x4    = Slider(ax_x4, 'x4', 1.2, 2.7, valinit=init_x4, valstep=0.02)
s_x5    = Slider(ax_x5, 'x5', 2.0, 3.5, valinit=init_x5, valstep=0.02)
s_xmax  = Slider(ax_xmax, 'xmax', 2.5, 5.0, valinit=init_xmax, valstep=0.1)

def update(val):
    draw_geometry(s_alpha.val, s_beta.val, s_h.val, s_mma.val, 
                  s_x1.val, s_x2.val, s_x4.val, s_x5.val, s_xmax.val)
    fig.canvas.draw_idle()

for s in [s_alpha, s_beta, s_h, s_mma, s_x1, s_x2, s_x4, s_x5, s_xmax]:
    s.on_changed(update)

plt.show()