#!/usr/bin/env python3
"""This function performs pooling on images"""

import numpy as np


def pool(images, kernel_shape, stride, mode='max'):
    """Performs a convolution on images using multiple kernels
    Args:
        images: array with shape (m, h, w)
            containing multiple grayscale images
            m: the number of images
            h: the height in pixels of the images
            w: the width in pixels of the images
            c: the number of channels in the image
        kernel_shape is a tuple of (kh, kw) containing
            the kernel shape for the pooling
            kh: the height of the kernel
            kw: the width of the kernel
        stride is a `tuple` of (sh, sw)
            sh: the stride for the height of the image
            sw: the stride for the width of the image
        mode: `str`, indicates the type of pooling
            max: indicates max pooling
            avg: indicates average pooling
    Returns:
        output: array containing the convolved images
    """
    c = images.shape[3]
    m, h, w = images.shape[0], images.shape[1], images.shape[2]
    kh, kw = kernel_shape[0], kernel_shape[1]
    sh, sw = stride[0], stride[1]
    nw = int(((w - kw) / stride[1]) + 1)
    nh = int(((h - kh) / stride[0]) + 1)
    pooled = np.zeros((m, nh, nw, c))
    for i in range(nh):
        x = i * stride[0]
        for j in range(nw):
            y = j * stride[1]
            image = images[:, x:x + kh, y:y + kw, :]
            if mode == 'max':
                pooled[:, i, j, :] = np.max(image, axis=(1, 2))
            else:
                pooled[:, i, j, :] = np.average(image, axis=(1, 2))
    return pooled
