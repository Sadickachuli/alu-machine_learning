#!/usr/bin/env python3
"""This function performs a valid convolution on grayscale images"""

import numpy as np


def convolve_grayscale_same(images, kernel):
    """Performs a valid convolution on grayscale images
    Args:
        images: array with shape (m, h, w)
            containing multiple grayscale images
            m: the number of images
            h: the height in pixels of the images
            w: the width in pixels of the images
        kernel: array with shape (kh, kw)
            containing the kernel for the convolution
            kh: the height of the kernel
            kw: the width of the kernel
    Returns:
         output: array containing the convolved images
    """
    m, h, w = images.shape[0], images.shape[1], images.shape[2]
    kh, kw = kernel.shape[0], kernel.shape[1]
    pw = int(kw / 2)
    ph = int(kh / 2)
    convolved = np.zeros((m, h, w))
    npad = ((0, 0), (ph, ph), (pw, pw))
    imagesp = np.pad(images, pad_width=npad,
                     mode='constant', constant_values=0)
    for i in range(h):
        for j in range(w):
            image = imagesp[:, i:i + kh, j:j + kw]
            convolved[:, i, j] = np.sum(np.multiply(image, kernel),
                                        axis=(1, 2))
    return convolved
