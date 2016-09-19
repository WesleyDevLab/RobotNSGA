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
		w_size = self.weights.get_value().size
		b_size = self.bias.get_value().size
		self.weights.set_value(np.reshape(unrolled_weights[: w_size], (self.n_in, self.n_out)))
		self.bias.set_value(np.reshape(unrolled_weights[w_size : w_size + b_size], (1, self.n_out)))
		return self.size
