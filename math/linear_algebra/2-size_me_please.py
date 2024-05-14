#!/usr/bin/env python3

def matrix_shape(matrix):
    """
    This function computes the shape of a matrix by iterating
    over its nested lists and appending the length of each dimension
    to a list called dimension. It then returns this list, which contains
    the dimensions of the matrix.
    """
    dimension = []
    while isinstance(matrix, list):
        dimension.append(len(matrix))
        matrix = matrix[0]
    return dimension
