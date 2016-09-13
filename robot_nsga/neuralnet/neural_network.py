'''Defines the NeuralNetwork class'''

import theano
import theano.tensor as T


class NeuralNetwork:
	'''Modular neural network, built as a stack of layers'''

	def __init__(self):
		'''Creates an empty, unusable neural network'''
		self.layers = []
		self.input = T.dmatrix('x')
		self.output = self.input
		self.function = None

	def add_layer(self, new_layer):
		'''Adds the given layer to the network'''
		self.layers.append(new_layer)
		self.output = theano.clone(new_layer.output, replace={new_layer.input: self.output})

	def compile(self):
		'''Make the neural network evaluatable'''
		self.function = theano.function([self.input], self.output)

	def predict(self, input_value):
		'''Compute the output of the network to the given input

		The 'compile' method must be called before this one.
		'''
		return self.function(input_value)
