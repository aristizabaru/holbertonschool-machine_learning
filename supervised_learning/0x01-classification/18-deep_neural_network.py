#!/usr/bin/env python3
"""represents a deep neural network performing
binary classification"""

import numpy as np


class DeepNeuralNetwork:
    """represents a deep neural network
    performing binary classification

    Attributes:
        L (int): the number of layers in the neural network.
        cache (dict): hold all intermediary values of the network.
        weights (dict): hold all weights and biased of the network.

    Methods:
        __init__(self, nx, nodes): constructor.
        forward_prop(self, X):
            calculates the forward propagation of the deep NN.

    Static Methods:
        sigmoid(x):
            calculates sigmoid function to 'x' value.
    """

    def __init__(self, nx, layers):
        """defines a deep neural network performing
        binary classification.

        Exp. The layers weights are initialized using He et al. method
        and the bias to 0's. To use He et al. method W1 and b1 must be
        initialized beforehand.

        Numpy implementation He et al. method:
            weight = np.random.randn(layer_size[l],layer_size[l-1])
                    *np.sqrt(2/layer_size[l-1])

        Args:
            nx (int): number of input features.
            layers (list):
                represents the number of nodes in each
                layer of the network

        Raises:
            TypeError: nx must be an integer.
            ValueError: nx must be a positive integer.
            TypeError: layers must be a list of positive integers.
        """
        if not isinstance(nx, int):
            raise TypeError('nx must be an integer')
        if nx < 1:
            raise ValueError('nx must be a positive integer')
        if not isinstance(layers, list) or len(layers) == 0:
            raise TypeError('layers must be a list of positive integers')
        # check if layer[0] in list is integer
        if layers[0] < 1 or not isinstance(layers[0], int):
            raise TypeError('layers must be a list of positive integers')

        self.__L = len(layers)
        self.__cache = dict()
        self.__weights = dict()
        # initialize L1
        # weights (neurons x input features)
        self.__weights['W1'] = np.random.randn(layers[0], nx)*np.sqrt(2/nx)
        # bias (float of zero's x # neurons of the layer)
        self.__weights['b1'] = np.zeros([layers[0], 1], dtype=float)
        # initialize L2 and L3
        for layer in range(1, self.L):
            # check if layer[layer] in list is integer
            if layers[layer] < 1 or not isinstance(layers[layer], int):
                raise TypeError('layers must be a list of positive integers')
            # He et al method
            # weight = np.random.randn(layer_size[l],layer_size[l-1])
            # *np.sqrt(2/layer_size[l-1])
            self.__weights['W{}'.format(
                layer + 1)] = np.random.randn(layers[layer],
                                              layers[layer-1])*np.sqrt(
                2/layers[layer-1])
            # bias (float of zero's x # neurons of the layer)
            self.__weights['b{}'.format(
                layer + 1)] = np.zeros([layers[layer], 1], dtype=float)

    @property
    def L(self):
        """defines public attribute L"""
        return self.__L

    @property
    def cache(self):
        """defines public attribute cache"""
        return self.__cache

    @property
    def weights(self):
        """defines public attribute weights"""
        return self.__weights

    def forward_prop(self, X):
        """calculates the forward propagation of the deep NN

        Formulas:
            Y = Σ (weight * input) + bias → get the input value to
            the sigmoid activation function

        Args:
            X (numpy.ndarray):
                with shape (nx, m), X contains the input data.
                'nx' is the number of input features to the neuron.
                'm' is the number of examples.

        Returns:
            tuple: the output of the neural network and the cache, respectively
        """
        # calculate A0
        self.__cache['A0'] = X
        # calculate An (i == layer)
        for i in range(1, self.L + 1):
            Y = np.dot(self.weights['W{}'.format(i)], self.cache['A{}'.format(
                i - 1)]) + self.weights['b{}'.format(i)]
            self.__cache['A{}'.format(i)] = type(self).sigmoid(Y)
        # (output deep NN, cache all layers)
        return self.cache['A{}'.format(self.L)], self.cache

    @ staticmethod
    def sigmoid(x):
        """calculates sigmoid function to 'x' value

        Formula:
            S(x) = 1 / (1 + e^-x)
            e → 2.7182818285 (Euler's number)

        Args:
            x (numpy.ndarray): contains the dot product
                               of the input data and weights
                               plus the bias

        Returns:
            numpy.ndarray: the activation values
        """
        # S(x) = 1 / (1 + e^-x)
        return 1/(1 + np.exp(-x))
