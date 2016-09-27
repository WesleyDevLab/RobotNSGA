'''Defines the NeuralNetwork class'''

import copy

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
		self.size = 0

	def add_layer(self, new_layer):
		'''Adds the given layer to the network'''
		self.layers.append(new_layer)
		self.output = theano.clone(new_layer.output, replace={new_layer.input: self.output})
		self.size += new_layer.size

	def compile(self):
		'''Make the neural network evaluatable'''
		self.function = theano.function([self.input], self.output)

	def predict(self, input_value):
		'''Compute the output of the network to the given input

		The 'compile' method must be called before this one.
		'''
		return self.function(input_value)

	def set_params(self, unrolled_weights):
		'''Replaces the network's weigths with the first elements of the given list

		Returns the number of elements used.
		'''
		params_vector = copy.copy(unrolled_weights)
		total_used = 0
		for layer in self.layers:
			used = layer.set_params(params_vector)
			params_vector = params_vector[used :]
			total_used += used
		return total_used
