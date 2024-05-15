#!/usr/bin/env python3

"""Function to add matrices element-wise."""


def add_matrices2D(mat1, mat2):
    """
    Adds two matrices element-wise.
    """
    # Check if matrices have the same shape
    if len(mat1) != len(mat2) or len(mat1[0]) != len(mat2[0]):
        return None

    result = []
    for i in range(len(mat1)):
        row = []
        for j in range(len(mat1[0])):
            row.append(mat1[i][j] + mat2[i][j])
        result.append(row)

    return result
