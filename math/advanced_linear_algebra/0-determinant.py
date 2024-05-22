#!/usr/bin/env python3

def determinant(matrix):
    # Check if matrix is a list of lists
    if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
        raise TypeError("matrix must be a list of lists")
    
    # Handle the special case of an empty matrix
    if matrix == []:
        raise TypeError("matrix must be a list of lists")
    
    # Handle the special case of a 0x0 matrix
    if matrix == [[]]:
        return 1
    
    # Check if matrix is square
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ValueError("matrix must be a square matrix")
    
    # Base case for 1x1 matrix
    if n == 1:
        return matrix[0][0]
    
    # Base case for 2x2 matrix
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    # Recursive case for larger matrices
    det = 0
    for c in range(n):
        submatrix = [row[:c] + row[c+1:] for row in matrix[1:]]
        sign = (-1) ** c
        det += sign * matrix[0][c] * determinant(submatrix)
    
    return det
