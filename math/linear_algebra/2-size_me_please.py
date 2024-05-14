#!/usr/bin/env python3

# Calculates the shape of a matrix.
def matrix_shape(matrix):
    dimension = []  # Initialize an empty list to store the dimensions
    while isinstance(matrix, list):  # Loop while 'matrix' is a list
        dimension.append(len(matrix))
        matrix = matrix[0]
    return dimension
