'''Defines the NeuralNetwork class'''

import theano


class NeuralNetwork:
	'''Modular neural network, built as a stack of layers'''

	def __init__(self):
		'''Creates an empty, unusable neural network'''
		self.layers = []
		self.output = None

	def add_layer(self, new_layer):
		'''Adds the given layer to the network'''
		self.layers.append(new_layer)
		if len(self.layers) == 1:
			self.output = new_layer.output
		else:
			self.output = theano.clone(new_layer.output, replace={new_layer.input: self.output})
