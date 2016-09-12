'''Defines the FullyConnectedLayer class'''

import numpy
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
		self.weights = theano.shared(numpy.zeros((n_out, n_in)), name='w')
		self.bias = theano.shared(numpy.zeros((n_out, 1)), name='b')
		if activation == None:
			self.output = T.dot(self.weights, self.input) + self.bias
		else:
			self.output = activation(T.dot(self.weights, self.input) + self.bias)
