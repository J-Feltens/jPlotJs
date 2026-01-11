import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation
from math import sin, cos, tan, exp, pi, degrees, radians

from port import calc_port_mode

plt.rcParams.update({
    "text.color": "white",
    "axes.labelcolor": "white",
    "axes.titlecolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "axes.edgecolor": "white",
})
fig = plt.figure(figsize=(10, 5))
ax_e = fig.add_subplot(2, 2, 1)
ax_h = fig.add_subplot(2, 2, 2)
ax_e_contour = fig.add_subplot(2, 2, 3)
ax_h_contour = fig.add_subplot(2, 2, 4)

mu = 1.25663706127e-6
c = 299792458

res_x = 30
res_y = 15

f = 70e9

m = 1
n = 1

a = 3.1e-3
b = a / 2

phi = 0.0001

phis = np.linspace(0, 2 * pi, 100)

e_mag_max_global = 0
h_mag_max_global = 0


def calc_frame(frame):
    global e_mag_max_global, h_mag_max_global
    phi = phis[frame]
    X, Y, Ex, Ey, E_mag, Hx, Hy, H_mag = calc_port_mode(a, b, f, m, n, phi, res_x, res_y)

    e_mag_min = np.min(E_mag)
    e_mag_max = np.max(E_mag)
    h_mag_min = np.min(H_mag)
    h_mag_max = np.max(H_mag)
    print(f"Min E_mag: {e_mag_min:10.6f}, Max E_mag: {e_mag_max:10.6f}")
    print(f"Min H_mag: {h_mag_min:10.6f}, Max H_mag: {h_mag_max:10.6f}")

    if e_mag_max > e_mag_max_global:
        e_mag_max_global = e_mag_max
    if h_mag_max > h_mag_max_global:
        h_mag_max_global = h_mag_max

    e_mag_max = e_mag_max_global
    h_mag_max = h_mag_max_global

    e_norm = mpl.colors.Normalize(vmin=0.0, vmax=e_mag_max)
    h_norm = mpl.colors.Normalize(vmin=0.0, vmax=h_mag_max)

    # normalize vectors for quiver plot
    Ex_normalized = Ex.real / np.sqrt(Ex.real ** 2 + Ey.real ** 2)
    Ey_normalized = Ey.real / np.sqrt(Ex.real ** 2 + Ey.real ** 2)
    Hx_normalized = Hx.real / np.sqrt(Ex.real ** 2 + Ey.real ** 2)
    Hy_normalized = Hy.real / np.sqrt(Ex.real ** 2 + Ey.real ** 2)

    cbar_e = ax_e.quiver(X, Y, Ex_normalized, Ey_normalized, E_mag,
                         cmap="plasma", norm=e_norm, pivot="mid")
    cbar_h = ax_h.quiver(X, Y, Hx_normalized, Hy_normalized, H_mag,
                         cmap="plasma", norm=h_norm, pivot="mid")
    cbar_e_contour = ax_e_contour.contourf(X, Y, E_mag, cmap="plasma", levels=100, norm=e_norm)
    cbar_h_contour = ax_h_contour.contourf(X, Y, H_mag, cmap="plasma", levels=100, norm=h_norm)

    return cbar_e, cbar_h, cbar_e_contour, cbar_h_contour


fig.set_facecolor("black")
ax_e.set_facecolor("#555")
ax_h.set_facecolor("#555")
ax_e_contour.set_facecolor("#555")
ax_h_contour.set_facecolor("#555")

# plt.colorbar(cbar_e, ax=ax_e)
# plt.colorbar(cbar_h, ax=ax_h)
ax_e.set_xticks([], [])
ax_e.set_yticks([], [])
ax_h.set_xticks([], [])
ax_h.set_yticks([], [])
ax_e_contour.set_xticks([], [])
ax_e_contour.set_yticks([], [])
ax_h_contour.set_xticks([], [])
ax_h_contour.set_yticks([], [])
ax_e.set_title("e-field")
ax_h.set_title("h-field")
ax_e.set_aspect("equal")
ax_h.set_aspect("equal")
ax_e_contour.set_aspect("equal")
ax_h_contour.set_aspect("equal")

ani = FuncAnimation(
    fig,
    calc_frame,
    frames=len(phis),
    interval=10,
    blit=True,
    repeat=True
)

plt.show()
