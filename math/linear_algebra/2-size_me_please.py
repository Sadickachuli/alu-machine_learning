#!/usr/bin/env python3

def matrix_shape(matrix):
    """
    Calculates the shape of a matrix.

    Args:
        matrix (list): The matrix whose shape needs to be calculated.

    Returns:
        list: A list containing the dimensions of the matrix.
    """
    dimension = []  # Initialize an empty list to store the dimensions of the matrix
    while isinstance(matrix, list):  # Loop while 'matrix' is a list
        dimension.append(len(matrix))
        matrix = matrix[0]
    return dimension
