# -*- coding: utf-8 -*-

import numpy as np
import numpy.linalg as la
# from scipy import sparse as sps
# import scipy.fft as fft
from typing import Tuple, List, Union, Optional, Set
# import time
from warnings import warn
from inkstone.recipro import recipro
from inkstone.g_pts import g_pts
from inkstone.g_pts_1d import g_pts_1d
from inkstone.max_idx_diff import max_idx_diff
from inkstone.conv_mtx_idx import conv_mtx_idx_2d
from inkstone.params import Params

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    lv = ((1., 0), (0.5, 1))
    num_g = 100
    omega = 0.5
    theta = 30.
    phi = 40.
    pr = Params(latt_vec=lv, num_g=num_g, omega=omega, theta=theta, phi=phi)
