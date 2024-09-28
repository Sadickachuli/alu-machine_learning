#!/usr/bin/env python3
''' Creates Training using RMSProp '''


import tensorflow as tf


def create_RMSProp_op(loss, alpha, beta2, epsilon):
    '''
    Creates Training op using RMSProp algorithm

    Args:
    loss -> loss of the network
    alpha -> learning rate
    beta2 -> RMSProp weight
    epsilon -> small number to avoid zero division

    Returns:
    RMSProp optimization operation
    '''

    return tf.train.RMSPropOptimizer(
        alpha, beta2, epsilon=epsilon).minimize(loss)
