from inkstone.params import Params
from inkstone.mtr import Mtr
from inkstone.bx import Bx
import time
import numpy as np
import matplotlib.pyplot as plt

mtr = Mtr(2, 3, 'fic')

lv = ((3., 0), (2., 3))
pr = Params(latt_vec=lv)

a = 1.5
b = 0.8
cen = (0.2, 0.3)
angle = 30

bx = Bx(mtr, 'ellipse', center=cen, half_lengths=(a, b), angle=angle)

m = 50
n = 50
k1i = np.arange(-m, m + 1)
k2i = np.arange(-n, n + 1)
kk1i, kk2i = np.meshgrid(k1i, k2i)
b1, b2 = pr.recipr_vec
b1 = np.array(b1)
b2 = np.array(b2)
kk1, kk2 = [kk1i * b1[i] + kk2i * b2[i] for i in range(2)]
ks = list(zip(kk1.ravel(), kk2.ravel()))

t1 = time.process_time()
ep, ei, mu, mi = bx.ft(ks, factor=0.7)
t2 = time.process_time()
s = np.array(ep).reshape((2*n+1, 2*m+1, 3, 3))[:, :, 0, 0]
t3 = time.process_time()
print(t2-t1)
print(t3-t2)

xi = np.linspace(-0.5, 0.5, 101)
yi = np.linspace(-0.5, 0.5, 101)
xxi, yyi = np.meshgrid(xi, yi)
xx, yy = [xxi * lv[0][i] + yyi * lv[1][i] for i in range(2)]
# s = ly.epsi_fs[:, :, 0, 0]  # epsi_xx

poly_recon = 1. / 4 / np.pi ** 2 * np.cross(pr.recipr_vec[0], pr.recipr_vec[1]) * \
             np.sum(s[:, :, None, None] * np.exp(1j * ((kk1i * b1[0] + kk2i * b2[0])[:, :, None, None] * xx[None, None, :, :] + (kk1i * b1[1] + kk2i * b2[1])[:, :, None, None] * yy[None, None, :, :])), axis=(0, 1))

fig, ax = plt.subplots()
pcm = ax.pcolormesh(xx, yy, poly_recon.real)
ax.set_aspect('equal')
plt.colorbar(pcm)

plt.figure()
plt.plot(xxi[21, :], poly_recon.real[:, 21])
