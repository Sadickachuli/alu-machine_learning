#!/usr/bin/env python3

"""Function to concatenate matrices along an  axis with numpy"""


import numpy as np


def np_cat(mat1, mat2, axis=0):
    """
    Concatenates two matrices along an  axis using numpy.
    """
    return np.concatenate((mat1, mat2), axis=axis)
