# -*- coding: utf-8 -*-

import numpy as np
from inkstone.params import Params
from inkstone.mtr import Mtr
from inkstone.layer import Layer

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    lv = ((5., 0), (1., 4))
    num_g = 300
    omega = 0.5
    theta = 0.
    phi = 0.
    pr = Params(latt_vec=lv, num_g=num_g, omega=omega, theta=theta, phi=phi)

    vac = Mtr(epsi=1., mu=1., name='vacuum')
    di = Mtr(epsi=12., mu=1., name='di')
    materials = {'di': di, 'vacuum': vac}
    t = 0.4

    ly = Layer('my layer', t, 'vacuum', materials, pr)

    a = b = 0.5
    ly.add_box('di', 'rectangle', box_name='sq', side_lengths=(a, b), center=(0., 0.2), factor=0.5)
    a = 1.5
    b = 1.2
    in_angle = 120
    angle = 10
    ly.add_box('vacuum', 'parallelogram', box_name='para', side_lengths=(a,b), shear_angle=in_angle, angle=angle)
    radius = 1.5
    ly.add_box('di', 'disk', box_name='disk', radius=radius, factor=0.5)

    ly._calc_ep_mu_fs_3d()
    # ly.solve()

    x = np.linspace(-3, 3, 101)
    y = np.linspace(-3, 3, 101)
    xx, yy = np.meshgrid(x, y)
    s = ly.epsi_fs[:, :, 0, 0]  # epsi_xx

    xxx, yyy, ep, mu = ly.reconstruct()
    fig, ax = plt.subplots()
    pcm = ax.pcolormesh(xxx, yyy, ep[:, :, 0, 0].real)
    ax.set_aspect('equal')
    plt.colorbar(pcm)

    m = pr.mmax
    n = pr.nmax
    k1i = np.arange(-m, m + 1)
    k2i = np.arange(-n, n + 1)
    kk1i, kk2i = np.meshgrid(k1i, k2i)
    b1, b2 = pr.recipr_vec
    b1 = np.array(b1)
    b2 = np.array(b2)

    recon = np.sum(s[:, :, None, None] * np.exp(1j * ((kk1i * b1[0] + kk2i * b2[0])[:, :, None, None] * xx[None, None, :, :] + (kk1i * b1[1] + kk2i * b2[1])[:, :, None, None] * yy[None, None, :, :])), axis=(0, 1))

    plt.figure()
    plt.pcolormesh(xx, yy, recon.real)
    plt.colorbar()

    s1 = ly.epsi_fs_used
    idx = ly.pr.idx_g_ep_mu_used
    s1a = np.array(s1)[:, 0, 0]
    idxa = np.array(idx)
    recon1 = np.sum(s1a[:, None, None] * np.exp(1j * ((idxa[:, 0] * b1[0] + idxa[:, 1] * b2[0])[:, None, None] * xx[None, :, :] + (idxa[:, 0] * b1[1] + idxa[:, 1] * b2[1])[:, None, None] * yy[None, :, :])), axis=0)

    plt.figure()
    plt.pcolormesh(xx, yy, recon1.real)
    plt.colorbar()
