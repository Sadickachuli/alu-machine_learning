#!/usr/bin/env python3
"""This function performs a convolution on images using multiple kernels"""

import numpy as np


def convolve(images, kernels, padding='same', stride=(1, 1)):
    """Performs a convolution on images using multiple kernels
    Args:
        images: array with shape (m, h, w)
            containing multiple grayscale images
            m: the number of images
            h: the height in pixels of the images
            w: the width in pixels of the images
            c: the number of channels in the image
        kernels: array with shape (kh, kw, c, nc)
            containing the kernel for the convolution
            kh: the height of the kernel
            kw: the width of the kernel
            nc: the number of kernels
        padding: `tuple` of (ph, pw), ‘same’, or ‘valid’
            if `tuple`:
                ph: the padding for the height of the image
                pw: the padding for the width of the image
            if ‘same’, performs a same convolution
            if ‘valid’, performs a valid convolution
        stride is a tuple of (sh, sw)
            sh: the stride for the height of the image
            sw: the stride for the width of the image
    Returns:
        output: array containing the convolved images
    """
    m, h, w = images.shape[0], images.shape[1], images.shape[2]
    kh, kw, nc = kernels.shape[0], kernels.shape[1], kernels.shape[3]
    sh, sw = stride[0], stride[1]
    if padding == 'same':
        pw = int(((w - 1) * sw + kw - w) / 2) + 1
        ph = int(((h - 1) * sh + kh - h) / 2) + 1
    elif padding == 'valid':
        ph = 0
        pw = 0
    else:
        pw = padding[1]
        ph = padding[0]
    nw = int(((w - kw + (2 * pw)) / sw) + 1)
    nh = int(((h - kh + (2 * ph)) / sh) + 1)
    convolved = np.zeros((m, nh, nw, nc))
    npad = ((0, 0), (ph, ph), (pw, pw), (0, 0))
    imagesp = np.pad(images, pad_width=npad,
                     mode='constant', constant_values=0)
    for i in range(nh):
        x = i * sh
        for j in range(nw):
            y = j * sw
            for k in range(nc):
                image = imagesp[:, x:x + kh, y:y + kw, :]
                kernel = kernels[:, :, :, k]
                convolved[:, i, j, k] = np.sum(np.multiply(image, kernel),
                                               axis=(1, 2, 3))
    return convolved
