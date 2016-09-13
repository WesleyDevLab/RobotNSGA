'''Evolution of a neural network to perform simple math functions.'''

import theano.tensor as T

import neuralnet


def main(args):
	'''Module main method'''
	nn = neuralnet.NeuralNetwork()
	nn.add_layer(neuralnet.FullyConnectedLayer(3, 3, T.nnet.sigmoid))
	nn.add_layer(neuralnet.FullyConnectedLayer(3, 2, T.nnet.sigmoid))
	nn.compile()
	print(nn.set_params([1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3]))
	print(nn.predict([[-1], [0], [1]]))
