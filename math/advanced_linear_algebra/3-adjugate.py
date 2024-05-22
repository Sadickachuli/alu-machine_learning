#!/usr/bin/env python3
"""

This calculates the adjugate of a matrix
"""


determinant = __import__('0-determinant').determinant


def transpose(matrix):
    """
    To find the transpose of a  matrix first
      Args:
       matrix

    returns:
        the transpose of matrix
    """
    matrix_size = len(matrix)
    transpose_matrix = []
    for i in range(matrix_size):
        t_row = []
        for row in range(matrix_size):
            for column in range(matrix_size):
                if column == i:
                    t_row.append(matrix[row][column])
        transpose_matrix.append(t_row)
    return transpose_matrix


def adjugate(matrix):
    """
    Calculate the adjugate of a matrix

    Args:
         matrix

    returns:
        the adjugate of the matrix
    """
    if type(matrix) is not list:
        raise TypeError("matrix must be a list of lists")

    matrix_size = len(matrix)
    if matrix_size == 0:
        raise TypeError("matrix must be a list of lists")
    for row in matrix:
        if type(row) is not list:
            raise TypeError("matrix must be a list of lists")
        if len(row) != matrix_size:
            raise ValueError("matrix must be a non-empty square matrix")
    if matrix_size == 1:
        return [[1]]
    multiplier = 1
    cofactor_matrix = []
    for row_idx in range(matrix_size):
        cofactor_row = []
        for column_idx in range(matrix_size):
            sub_matrix = []
            for row in range(matrix_size):
                if row == row_idx:
                    continue
                new_row = []
                for column in range(matrix_size):
                    if column == column_idx:
                        continue
                    new_row.append(matrix[row][column])
                sub_matrix.append(new_row)
            cofactor_row.append(multiplier * determinant(sub_matrix))
            multiplier *= -1
        cofactor_matrix.append(cofactor_row)
        if matrix_size % 2 == 0:
            multiplier *= -1
    adjugate_matrix = transpose(cofactor_matrix)
    return adjugate_matrix
