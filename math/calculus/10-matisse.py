#!/usr/bin/env python3
""" This function calculates the derivative of a polynomial """


def poly_derivative(poly):
    """
    calculates the derivative of polynomial

    Parameters:
        poly (list): list of coefficients representing a polynomial
            the index of the list represents the power of x
            the coefficient belongs to

    Returns:
        a new list of coefficients representing the derivative
        [0], if the derivate is 0
        None, if poly is not valid
    """
    if not isinstance(poly, list) or len(poly) == 0:
        return None
    if not all(isinstance(coef, (int, float)) for coef in poly):
        return None
    derivative = [coef * power for power, coef in enumerate(poly) if power > 0]

    if not derivative:
        return [0]

    return derivative
