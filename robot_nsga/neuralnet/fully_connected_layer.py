'''Defines the FullyConnectedLayer class'''

import numpy as np
import theano
import theano.tensor as T


class FullyConnectedLayer:
	'''Layer in which all input neurons connect to all outputs'''

	def __init__(self, n_in, n_out, activation=None):
		'''Constructs a layer with n_in inputs, n_out outputs and the given activation function.

		If the activation is None, it acts as a linear activation.
		'''
		self.input = T.dmatrix('x')
		self.n_in = n_in
		self.n_out = n_out
		self.weights = theano.shared(np.zeros((n_in, n_out)), name='w')
		self.bias = theano.shared(np.zeros((1, n_out)), name='b', broadcastable=[True, False])
		self.size = self.weights.get_value().size + self.bias.get_value().size
		if activation is None:
			self.output = T.dot(self.input, self.weights) + self.bias
		else:
			self.output = activation(T.dot(self.input, self.weights) + self.bias)

	def set_params(self, unrolled_weights):
		'''Replaces the layer's weigths with the first elements of the given list

		Returns the number of elements used.
		'''
		new_weigths = np.zeros((self.n_in, self.n_out))
		new_bias = np.zeros((1, self.n_out))
		acc = 0
		for i in range(self.n_out):
			new_weigths[:, i] = unrolled_weights[acc: acc + self.n_out]
			acc += self.n_out
			new_bias[:, i] = unrolled_weights[acc]
			acc += 1
		self.weights.set_value(new_weigths)
		self.bias.set_value(new_bias)
		return self.size
