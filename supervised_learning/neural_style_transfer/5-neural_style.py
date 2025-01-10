#!/usr/bin/env python3
"""
Defines class NST that performs tasks for neural style transfer
"""

import numpy as np
import tensorflow as tf


class NST:
    """
    Performs tasks for Neural Style Transfer

    public class attributes:
        style_layers = ['block1_conv1', 'block2_conv1', 'block3_conv1',
                        'block4_conv1', 'block5_conv1']
        content_layer = 'block5_conv2'

    instance attributes:
        style_image: preprocessed style image
        content_image: preprocessed content image
        alpha: weight for content cost
        beta: weight for style cost

    class constructor:
        def __init__(self, style_image, content_image, alpha=1e4, beta=1)

    static methods:
        def scale_image(image):
            rescales an image so the pixel values are between 0 and 1
                and the largest side is 512 pixels
    """
    style_layers = ['block1_conv1', 'block2_conv1', 'block3_conv1',
                    'block4_conv1', 'block5_conv1']
    content_layer = 'block5_conv2'

    def __init__(self, style_image, content_image, alpha=1e4, beta=1):
        """
        Class constructor for Neural Style Transfer class
        """
        if type(style_image) is not np.ndarray or len(style_image.shape) != 3:
            raise TypeError(
                "style_image must be a numpy.ndarray with shape (h, w, 3)")
        if type(content_image) is not np.ndarray or len(content_image.shape) != 3:
            raise TypeError(
                "content_image must be a numpy.ndarray with shape (h, w, 3)")

        self.style_image = self.scale_image(style_image)
        self.content_image = self.scale_image(content_image)
        self.alpha = alpha
        self.beta = beta

        self.load_model()
        self.generate_features()

    @staticmethod
    def scale_image(image):
        """
        Rescales an image such that its pixels values are between 0 and 1
            and its largest side is 512 pixels
        """
        if type(image) is not np.ndarray or len(image.shape) != 3:
            raise TypeError(
                "image must be a numpy.ndarray with shape (h, w, 3)")
        h, w, c = image.shape
        if h <= 0 or w <= 0 or c != 3:
            raise TypeError(
                "image must be a numpy.ndarray with shape (h, w, 3)")

        if h > w:
            new_h = 512
            new_w = int(w * 512 / h)
        else:
            new_w = 512
            new_h = int(h * 512 / w)

        image = tf.image.resize(image, (new_h, new_w), method='bicubic')
        image = image / 255.0
        return tf.expand_dims(image, axis=0)

    def load_model(self):
        """
        Creates the model used to calculate cost
        """
        vgg = tf.keras.applications.VGG19(include_top=False, weights='imagenet')
        vgg.trainable = False
        outputs = [vgg.get_layer(name).output for name in self.style_layers]
        outputs.append(vgg.get_layer(self.content_layer).output)
        self.model = tf.keras.models.Model(vgg.input, outputs)

    @staticmethod
    def gram_matrix(input_layer):
        """
        Calculates the gram matrix of a tensor
        """
        if not isinstance(input_layer, (tf.Tensor, tf.Variable)) or len(input_layer.shape) != 4:
            raise TypeError("input_layer must be a tensor of rank 4")
        _, h, w, c = input_layer.shape
        features = tf.reshape(input_layer, (-1, c))
        gram = tf.matmul(features, features, transpose_a=True)
        return gram / tf.cast(h * w, tf.float32)

    def generate_features(self):
        """
        Extracts the features used to calculate neural style cost
        """
        preprocessed_style = tf.keras.applications.vgg19.preprocess_input(
            self.style_image * 255)
        preprocessed_content = tf.keras.applications.vgg19.preprocess_input(
            self.content_image * 255)

        outputs_style = self.model(preprocessed_style)
        outputs_content = self.model(preprocessed_content)

        self.gram_style_features = [self.gram_matrix(output)
                                    for output in outputs_style[:-1]]
        self.content_feature = outputs_content[-1]

    def layer_style_cost(self, style_output, gram_target):
        """
        Calculates the style cost for a single layer
        """
        if not isinstance(style_output, (tf.Tensor, tf.Variable)) or len(style_output.shape) != 4:
            raise TypeError("style_output must be a tensor of rank 4")
        if not isinstance(gram_target, (tf.Tensor, tf.Variable)) or len(gram_target.shape) != 2:
            raise TypeError("gram_target must be a tensor of rank 2")
        gram_style = self.gram_matrix(style_output)
        return tf.reduce_mean(tf.square(gram_style - gram_target))

    def style_cost(self, style_outputs):
        """
        Calculates the style cost for the generated image

        parameters:
            style_outputs [list]: list of tf.Tensor containing the outputs
            of the style layers

        returns:
            style_cost [float]: calculated style cost
        """
        if not isinstance(style_outputs, list) or len(style_outputs) != len(self.style_layers):
            raise TypeError(
                "style_outputs must be a list with a length of {}".format(len(self.style_layers))
            )

        weight = 1 / len(self.style_layers)
        style_cost = 0.0
        for i in range(len(self.style_layers)):
            style_cost += weight * self.layer_style_cost(
                style_outputs[i], self.gram_style_features[i])
        return style_cost
