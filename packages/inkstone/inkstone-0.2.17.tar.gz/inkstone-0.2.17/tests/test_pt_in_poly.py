# -*- coding: utf-8 -*-

from typing import List, Tuple, Union
import numpy as np
from inkstone.helpers.pt_in_poly import pt_in_poly

if __name__ == "__main__":

    vts = [(0., 0.), (1., 0.), (2., 1.), (2., 2.), (0., 2.), (-0.5, 1.5), (0.5, 1.), (0.5, 0.5)]
    pts = [(0.5, 0.5), (1., 1.), (0.8, 0.), (0.5, 1.), (1., 2.), (2., 1.), (-1., 2.), (-0.5, 1.)]

    for pt in pts:
        print(pt_in_poly(vts, pt))
