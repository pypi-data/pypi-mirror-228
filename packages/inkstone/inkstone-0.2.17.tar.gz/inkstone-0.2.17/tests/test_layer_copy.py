# -*- coding: utf-8 -*-

from typing import Tuple, Optional
import time
import numpy as np
from inkstone.layer import Layer
from inkstone.sm import s_1l, s_1l_in, s_1l_out
from inkstone.layer_copy import layer_copy


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from inkstone.params import Params
    from inkstone.mtr import Mtr

    lv = ((3., 0), (2., 4))
    num_g = 300
    omega = 0.5
    theta = 0.
    phi = 0.
    pr = Params(latt_vec=lv, num_g=num_g, omega=omega, theta=theta, phi=phi)

    vac = Mtr(epsi=1., mu=1., name='vacuum')
    di = Mtr(epsi=12., mu=1., name='di')
    materials = {'di': di, 'vacuum': vac}
    t = 0.4

    layer = Layer('my layer', t, 'vacuum', materials, pr)

    layer_copy = LayerCopy('copy', layer, 0.)

    layer.thickness = 0.6
    print(layer_copy.thickness)

