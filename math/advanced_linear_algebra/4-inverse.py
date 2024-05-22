#!/usr/bin/env python3
"""
Calculates the inverse of a given matrix
"""

determinant = __import__('0-determinant').determinant
adjugate = __import__('3-adjugate').adjugate


def inverse(matrix):
    """
    Calculates the inverse of a matrix

    Args:
        matrix

    returns:
        the inverse of matrix
    """
    if type(matrix) is not list:
        raise TypeError("matrix must be a list of lists")
    matrix_size = len(matrix)
    for row in matrix:
        if type(row) is not list:
            raise TypeError("matrix must be a list of lists")
        if len(row) != matrix_size or len(row) == 0:
            raise ValueError("matrix must be a non-empty square matrix")
    det = determinant(matrix)
    if det == 0:
        return None
    adjugate_matrix = adjugate(matrix)
    inverse_matrix = []
    for row_idx in range(matrix_size):
        inverse_row = []
        for column_idx in range(matrix_size):
            inverse_row.append(adjugate_matrix[row_idx][column_idx] / det)
        inverse_matrix.append(inverse_row)
    return inverse_matrix
