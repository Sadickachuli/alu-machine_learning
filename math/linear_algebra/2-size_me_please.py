#!/usr/bin/env python3

def matrix_shape(matrix):
    """
    Shape function
    """
    dimension = []
    while isinstance(matrix, list):
        dimension.append(len(matrix))
        matrix = matrix[0]
    return dimension
