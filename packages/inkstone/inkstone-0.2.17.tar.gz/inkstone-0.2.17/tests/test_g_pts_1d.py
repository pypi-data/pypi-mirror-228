# -*- coding: utf-8 -*-

import numpy as np
from inkstone.g_pts_1d import g_pts_1d

import matplotlib.pyplot as plt

num_g = 7
b = (0.8, 0.9)

k_pts, idx = g_pts_1d(num_g, b)
ka = np.array(k_pts)
idxa = np.array(idx)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(ka[:, 0], ka[:, 1])
ax.set_aspect('equal')

fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.plot(idxa)
ax1.set_aspect('equal')
