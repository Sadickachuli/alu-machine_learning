#!/usr/bin/env python3

"""This will determine the shape of a matrix."""


def matrix_shape(matrix):
    """Determine the shape of a matrix.

    Args:
        matrix (list): A nested list representing a matrix.

    Returns:
        list: A list containing the dimensions of the matrix.

    """
    dimension = []  # Initialize an empty list to store the dimensions
    while isinstance(matrix, list):  # Loop while 'matrix' is a list
        dimension.append(len(matrix))
        matrix = matrix[0]
    return dimension
