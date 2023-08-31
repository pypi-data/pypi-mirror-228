# -*- coding: utf-8 -*-

import numpy as np
from inkstone.g_pts import g_pts

import matplotlib.pyplot as plt

num_g = 50
b1 = (1., 0.)
b2 = (0.8, 0.9)

k_pts, idx = g_pts(num_g, b1, b2)
ka = np.array(k_pts)
idxa = np.array(idx)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(ka[:, 0], ka[:, 1])
ax.set_aspect('equal')

fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.scatter(idxa[:, 0], idxa[:, 1])
ax1.set_aspect('equal')
