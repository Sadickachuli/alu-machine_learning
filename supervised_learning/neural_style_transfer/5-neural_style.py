#!/usr/bin/env python3
"""
Defines class NST that performs tasks for neural style transfer.
"""

import numpy as np
import tensorflow as tf


class NST:
    """
    Performs tasks for Neural Style Transfer.

    Public class attributes:
        style_layers: List of VGG19 layers used for style extraction.
        content_layer: VGG19 layer used for content extraction.
    """

    style_layers = ['block1_conv1', 'block2_conv1', 'block3_conv1',
                    'block4_conv1', 'block5_conv1']
    content_layer = 'block5_conv2'

    def __init__(self, style_image, content_image, alpha=1e4, beta=1):
        """
        Class constructor for Neural Style Transfer class.

        Parameters:
            style_image (numpy.ndarray): Image used as the style reference.
            content_image (numpy.ndarray): Image used as the content reference.
            alpha (float): Weight for content cost.
            beta (float): Weight for style cost.
        """
        if not isinstance(style_image, np.ndarray) or len(style_image.shape) != 3:
            raise TypeError("style_image must be a numpy.ndarray with shape (h, w, 3)")
        if not isinstance(content_image, np.ndarray) or len(content_image.shape) != 3:
            raise TypeError("content_image must be a numpy.ndarray with shape (h, w, 3)")
        if style_image.shape[2] != 3 or content_image.shape[2] != 3:
            raise TypeError("Both images must have 3 channels.")
        if not isinstance(alpha, (int, float)) or alpha < 0:
            raise TypeError("alpha must be a non-negative number.")
        if not isinstance(beta, (int, float)) or beta < 0:
            raise TypeError("beta must be a non-negative number.")

        self.style_image = self.scale_image(style_image)
        self.content_image = self.scale_image(content_image)
        self.alpha = alpha
        self.beta = beta

        self.load_model()
        self.generate_features()

    @staticmethod
    def scale_image(image):
        """
        Rescales an image such that its pixel values are between 0 and 1
        and its largest side is 512 pixels.

        Parameters:
            image (numpy.ndarray): Image to be rescaled.

        Returns:
            tf.Tensor: Rescaled image tensor.
        """
        if not isinstance(image, np.ndarray) or len(image.shape) != 3:
            raise TypeError("image must be a numpy.ndarray with shape (h, w, 3)")
        h, w, _ = image.shape
        if h > w:
            new_h, new_w = 512, int(512 * w / h)
        else:
            new_h, new_w = int(512 * h / w), 512

        resized = tf.image.resize(image, (new_h, new_w), method='bicubic')
        scaled = tf.clip_by_value(resized / 255.0, 0.0, 1.0)
        return tf.expand_dims(scaled, axis=0)

    def load_model(self):
        """
        Creates the model used to calculate cost.
        Uses the VGG19 Keras model as a base and sets the outputs to
        the layers defined in style_layers and content_layer.
        """
        vgg = tf.keras.applications.VGG19(include_top=False, weights='imagenet')
        vgg.trainable = False

        outputs = [vgg.get_layer(layer).output for layer in self.style_layers]
        outputs.append(vgg.get_layer(self.content_layer).output)

        self.model = tf.keras.Model(inputs=vgg.input, outputs=outputs)

    @staticmethod
    def gram_matrix(input_layer):
        """
        Calculates the Gram matrix for a given layer output.

        Parameters:
            input_layer (tf.Tensor): Layer output to calculate the Gram matrix.

        Returns:
            tf.Tensor: Gram matrix.
        """
        if len(input_layer.shape) != 4:
            raise ValueError("input_layer must be a tensor of rank 4.")

        _, h, w, c = input_layer.shape
        features = tf.reshape(input_layer, (-1, c))
        gram = tf.matmul(features, features, transpose_a=True)
        return gram / tf.cast(h * w, tf.float32)

    def generate_features(self):
        """
        Extracts the style and content features from the preprocessed images.
        """
        preprocess_input = tf.keras.applications.vgg19.preprocess_input

        style_preprocessed = preprocess_input(self.style_image * 255.0)
        content_preprocessed = preprocess_input(self.content_image * 255.0)

        outputs = self.model(style_preprocessed)
        self.gram_style_features = [self.gram_matrix(out) for out in outputs[:-1]]
        self.content_feature = outputs[-1]

    def layer_style_cost(self, style_output, gram_target):
        """
        Calculates the style cost for a single layer.

        Parameters:
            style_output (tf.Tensor): Style layer output from the generated image.
            gram_target (tf.Tensor): Gram matrix of the target style layer.

        Returns:
            tf.Tensor: Style cost for the layer.
        """
        if len(style_output.shape) != 4:
            raise ValueError("style_output must be a tensor of rank 4.")
        gram_style = self.gram_matrix(style_output)
        return tf.reduce_mean(tf.square(gram_style - gram_target))

    def style_cost(self, style_outputs):
        """
        Calculates the style cost for the generated image.

        Parameters:
            style_outputs (list): Outputs of the style layers for the generated image.

        Returns:
            tf.Tensor: Total style cost.
        """
        weight_per_layer = 1.0 / len(self.style_layers)
        total_style_cost = 0.0

        for style_output, gram_target in zip(style_outputs, self.gram_style_features):
            total_style_cost += weight_per_layer * self.layer_style_cost(style_output, gram_target)

        return total_style_cost
