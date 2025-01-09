#!/usr/bin/env python3
"""
Defines class NST that performs tasks for neural style transfer
"""

import numpy as np
import tensorflow as tf


class NST:
    """
    Performs tasks for Neural Style Transfer
    """
    style_layers = ['block1_conv1', 'block2_conv1', 'block3_conv1',
                    'block4_conv1', 'block5_conv1']
    content_layer = 'block5_conv2'

    def __init__(self, style_image, content_image, alpha=1e4, beta=1):
        if not isinstance(style_image, np.ndarray) or len(style_image.shape) != 3:
            raise TypeError("style_image must be a numpy.ndarray with shape (h, w, 3)")
        if not isinstance(content_image, np.ndarray) or len(content_image.shape) != 3:
            raise TypeError("content_image must be a numpy.ndarray with shape (h, w, 3)")

        style_h, style_w, style_c = style_image.shape
        content_h, content_w, content_c = content_image.shape

        if style_h <= 0 or style_w <= 0 or style_c != 3:
            raise TypeError("style_image must have valid dimensions")
        if content_h <= 0 or content_w <= 0 or content_c != 3:
            raise TypeError("content_image must have valid dimensions")

        if not (isinstance(alpha, (float, int)) and alpha >= 0):
            raise TypeError("alpha must be a non-negative number")
        if not (isinstance(beta, (float, int)) and beta >= 0):
            raise TypeError("beta must be a non-negative number")

        self.style_image = self.scale_image(style_image)
        self.content_image = self.scale_image(content_image)
        self.alpha = alpha
        self.beta = beta
        self.load_model()
        self.generate_features()

    @staticmethod
    def scale_image(image):
        if not isinstance(image, np.ndarray) or len(image.shape) != 3:
            raise TypeError("image must be a numpy.ndarray with shape (h, w, 3)")

        h, w, c = image.shape
        if h > w:
            h_new, w_new = 512, int(w * (512 / h))
        else:
            h_new, w_new = int(h * (512 / w)), 512

        image_resized = tf.image.resize(image, (h_new, w_new), method='bicubic')
        image_rescaled = image_resized / 255.0
        return tf.clip_by_value(image_rescaled, 0.0, 1.0)[tf.newaxis, ...]

    def load_model(self):
        vgg = tf.keras.applications.VGG19(include_top=False, weights='imagenet')
        vgg.trainable = False

        style_outputs = [vgg.get_layer(name).output for name in self.style_layers]
        content_output = vgg.get_layer(self.content_layer).output
        model_outputs = style_outputs + [content_output]

        self.model = tf.keras.models.Model(vgg.input, model_outputs)

    @staticmethod
    def gram_matrix(input_layer):
        if len(input_layer.shape) != 4:
            raise TypeError("input_layer must be a tensor of rank 4")

        _, h, w, c = input_layer.shape
        features = tf.reshape(input_layer, (-1, c))
        gram = tf.matmul(features, features, transpose_a=True)
        return gram / tf.cast(h * w, tf.float32)

    def generate_features(self):
        vgg19 = tf.keras.applications.vgg19
        preprocess_style = vgg19.preprocess_input(self.style_image * 255)
        preprocess_content = vgg19.preprocess_input(self.content_image * 255)

        style_features = self.model(preprocess_style)[:-1]
        content_feature = self.model(preprocess_content)[-1]

        self.gram_style_features = [self.gram_matrix(style) for style in style_features]
        self.content_feature = content_feature

    def content_cost(self, content_output):
        if not isinstance(content_output, (tf.Tensor, tf.Variable)):
            raise TypeError("content_output must be a tensor")

        return tf.reduce_mean(tf.square(self.content_feature - content_output))
