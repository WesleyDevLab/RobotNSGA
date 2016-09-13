'''Evolution of a neural network to perform simple math functions.'''

import theano.tensor as T
import theano.printing

import neuralnet


def main(args):
	'''Module main method'''
	nn = neuralnet.NeuralNetwork()
	nn.add_layer(neuralnet.FullyConnectedLayer(3, 3, T.nnet.sigmoid))
	theano.printing.debugprint(nn.output)
	nn.add_layer(neuralnet.FullyConnectedLayer(3, 2, T.nnet.sigmoid))
	theano.printing.debugprint(nn.output)
	nn.compile()
	print(nn.predict([[-1], [0], [1]]))
