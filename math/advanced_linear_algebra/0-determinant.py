#!/usr/bin/env python3
"""
    This function calculates the determinant of a matrix
"""


def determinant(matrix):
    """
    Calculate the determinant of a matrix

    Args:
        - matrix: list of lists representing the matrix

    Returns:
        - the determinant of matrix

    """
    if type(matrix) is not list:
        raise TypeError("matrix must be a list of lists")

    matrix_size = len(matrix)
    if matrix_size == 0:
        raise TypeError("matrix must be a list of lists")

    for row in matrix:
        if type(row) is not list:
            raise TypeError("matrix must be a list of lists")
        if matrix == [[]]:
            return 1
        if len(row) != matrix_size:
            raise ValueError("matrix must be a square matrix")

    if matrix_size == 1:
        return matrix[0][0]

    if matrix_size == 2:
        a = matrix[0][0]
        b = matrix[0][1]
        c = matrix[1][0]
        d = matrix[1][1]
        return (a * d) - (b * c)

    # For larger matrices
    multiplier = 1
    det = 0
    for i in range(matrix_size):
        element = matrix[0][i]
        sub_matrix = []
        for row_idx in range(1, matrix_size):
            new_row = []
            for col_idx in range(matrix_size):
                if col_idx != i:
                    new_row.append(matrix[row_idx][col_idx])
            sub_matrix.append(new_row)
        det += (element * multiplier * determinant(sub_matrix))
        multiplier *= -1
    return det
