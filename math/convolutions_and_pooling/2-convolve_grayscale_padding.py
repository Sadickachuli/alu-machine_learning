#!/usr/bin/env python3
"""This function performs a valid convolution
on grayscale images with custom padding"""

import numpy as np


def convolve_grayscale_padding(images, kernel, padding):
    """Performs a convolution on grayscale images custom padding
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
        padding: `tuple` of (ph, pw)
            ph: the padding for the height of the image
            pw: the padding for the width of the image
    Returns:
        output: array containing the convolved images
    """
    m, h, w = images.shape[0], images.shape[1], images.shape[2]
    kh, kw = kernel.shape[0], kernel.shape[1]
    ph, pw = padding[0], padding[1]
    nw = int(w - kw + (2 * pw) + 1)
    nh = int(h - kh + (2 * ph) + 1)
    convolved = np.zeros((m, nh, nw))
    npad = ((0, 0), (ph, ph), (pw, pw))
    imagesp = np.pad(images, pad_width=npad,
                     mode='constant', constant_values=0)
    for i in range(nh):
        for j in range(nw):
            image = imagesp[:, i:i + kh, j:j + kw]
            convolved[:, i, j] = np.sum(np.multiply(image, kernel),
                                        axis=(1, 2))
    return convolved
