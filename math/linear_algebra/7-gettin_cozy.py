#!/usr/bin/env python3

"""Function to concatenate matrices."""


def cat_matrices2D(mat1, mat2, axis=0):
    """
    Concatenates two matrices along a specific axis.
    """
    if axis == 0 and len(mat1[0]) != len(mat2[0]):
        return None
    if axis == 1 and len(mat1) != len(mat2):
        return None

    if axis == 0:
        return mat1 + mat2
    else:
        return [row1 + row2 for row1, row2 in zip(mat1, mat2)]
