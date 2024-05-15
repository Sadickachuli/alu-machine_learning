#!/usr/bin/env python3

"""This function will return the transpose of a matrix."""


def matrix_transpose(matrix):
    """
    Returns the transpose of a 2D matrix.
    """

    rows = len(matrix)
    cols = len(matrix[0])
    transpose_matrix = []

    for j in range(cols):
        new_row = []
        for i in range(rows):
            new_row.append(matrix[i][j])
        transpose_matrix.append(new_row)

    return transpose_matrix
