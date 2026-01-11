import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from math import sin, cos, tan, exp, pi

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(1, 1, 1)
cmap = cm.get_cmap("viridis")

res_x = 100
res_y = 50

mu = 1.25663706127e-6
c = 299792458

f = 1000e9
l = c / f

m = 1
n = 0

a = 3.1e-3
b = a / 2

omega = 2 * pi * f
k = (2 * pi * f) / c
k_cutoff = np.sqrt(((m * pi) / a) ** 2 + ((n * pi) / b) ** 2)

beta = np.sqrt(k ** 2 - k_cutoff ** 2 + 0j)
l_g = (2 * pi) / beta
z = 0

phi = pi / 2

xs = np.linspace(0, a, res_x)
ys = np.linspace(0, b, res_y)

vectors = []
for y in ys:
    row = []
    for x in xs:
        e_x = ((1j * omega * mu * n * pi) / (k_cutoff ** 2 * b)) * cos((m * pi * x) / a) * sin(
            (n * pi * y) / b) * np.exp(-1j * beta * z)
        e_y = ((-1j * omega * mu * m * pi) / (k_cutoff ** 2 * a)) * sin((m * pi * x) / a) * cos(
            (n * pi * y) / b) * 1 * np.exp(-1j * beta * z)

        e_xt = (e_x * np.exp(1j * phi)).real
        e_yt = (e_y * np.exp(1j * phi)).real

        mag = np.sqrt(abs(e_xt) ** 2 + abs(e_yt) ** 2)

        row.append({
            "x": x,
            "y": y,
            "e_x": abs(e_x),
            "e_y": abs(e_y),
            "mag": mag
        })
    vectors.append(row)

mag_min = 1e12
mag_max = -1e12
for row in vectors:
    for vec in row:
        if vec["mag"] < mag_min:
            mag_min = vec["mag"]
        if vec["mag"] > mag_max:
            mag_max = vec["mag"]

print("magnitude min, max", mag_min, mag_max)

mag_max = 5000

# normalize
for row in vectors:
    for vec in row:
        mag_norm = vec['mag'] / mag_max
        vec['mag_norm'] = mag_norm

xs = []
ys = []
vals = []

for row in vectors:
    for d in row:
        xs.append(d["x"])
        ys.append(d["y"])
        vals.append(d["mag_norm"])

ax.scatter(xs, ys, c=vals)

ax.set_aspect('equal')
ax.grid()

plt.show()
