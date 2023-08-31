# -*- coding: utf-8 -*-

import numpy as np
from warnings import warn
import copy
from typing import List, Union, Tuple, Optional
from inkstone.ft.ft_1d_sq import ft_1d_sq
from inkstone.ft.ft_2d_rct import ft_2d_rct
from inkstone.ft.ft_2d_para import ft_2d_para
from inkstone.ft.ft_2d_ellip import ft_2d_ellip
from inkstone.ft.ft_2d_disk import ft_2d_disk
from inkstone.ft.ft_2d_poly import ft_2d_poly
from inkstone.ft.poly_area import poly_area
from inkstone.ft.gibbs import gibbs_corr
from inkstone.shps import Disk, OneD, Poly, Elli, Rect, Para


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from inkstone.mtr import Mtr
    from inkstone.layer import Layer
    from inkstone.params import Params
    import time

    lv = ((3., 0), (2., 3))
    pr = Params(latt_vec=lv)

    r = 1.
    cen = (0, 0)
    di = Disk(radius=r, center=cen)

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
    s = np.array(di.ft(ks, factor=0.7)).reshape(2 * n + 1, 2 * m + 1)
    t2 = time.process_time()
    print(t2 - t1)

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

