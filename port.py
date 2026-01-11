import numpy as np
from numpy import pi

"""
usage:
    
res_x = 30
res_y = 15

f = 1000e9
m = 2
n = 1
a = 3.1e-3
b = a / 2
phi = 2 * pi

X, Y, Ex, Ey, Mag = calc_port_mode(a, b, f, m, n, phi)

ax.contourf(X, Y, Mag, cmap=cmap, levels=100)
ax.quiver(X, Y, Ex, Ey, Mag, cmap="viridis")
"""


def calc_port_mode(a, b, f, m, n, phi, res_x, res_y):
    mu = 1.25663706127e-6
    c = 299792458

    omega = 2 * pi * f
    l = c / f

    k = (2 * pi * f) / c
    k_cutoff = np.sqrt(((m * pi) / a) ** 2 + ((n * pi) / b) ** 2)

    beta = np.sqrt(k ** 2 - k_cutoff ** 2 + 0j)
    l_g = (2 * pi) / beta

    xs = np.linspace(0, a, res_x)
    ys = np.linspace(0, b, res_y)
    X, Y = np.meshgrid(xs, ys)

    # phases
    z = 0
    phase_z = np.exp(-1j * beta * z)
    phase_phi = np.exp(1j * phi)

    # calc e field
    Ex = ((1j * omega * mu * n * pi) / (k_cutoff ** 2 * b)) * np.cos((m * pi * X) / a) * np.sin(
        (n * pi * Y) / b) * phase_z
    Ey = ((-1j * omega * mu * m * pi) / (k_cutoff ** 2 * a)) * np.sin((m * pi * X) / a) * np.cos(
        (n * pi * Y) / b) * phase_z

    # calc h field
    Hx = ((1j * beta * m * pi) / (k_cutoff ** 2 * a)) * np.sin((m * pi * X) / a) * np.cos((n * pi * Y) / b) * phase_z
    Hy = ((1j * beta * n * pi) / (k_cutoff ** 2 * b)) * np.cos((m * pi * X) / a) * np.sin((n * pi * Y) / b) * phase_z

    # add phi phase shift
    Ex_t = np.real(Ex * phase_phi)
    Ey_t = np.real(Ey * phase_phi)
    Hx_t = np.real(Hx * phase_phi)
    Hy_t = np.real(Hy * phase_phi)

    # SUPER SKETCHY
    # add 90deg phase shift for h-field, dont understand why
    # Hx_t = np.real(Hx * phase_phi * np.exp(1j * pi / 2))
    # Hy_t = np.real(Hy * phase_phi * np.exp(1j * pi / 2))

    # phasor magnitudes
    E_mag = np.sqrt(np.abs(Ex) ** 2 + np.abs(Ey) ** 2)
    H_mag = np.sqrt(np.abs(Hx) ** 2 + np.abs(Hy) ** 2)

    # snapshot magnitudes
    E_mag = np.sqrt(Ex_t ** 2 + Ey_t ** 2)
    H_mag = np.sqrt(Hx_t ** 2 + Hy_t ** 2)

    return X, Y, Ex_t, Ey_t, E_mag, Hx_t, Hy_t, H_mag
