'''Evolution of a neural network to perform simple math functions.'''

import evolution
import neuralnet


ARCHITECTURE = [2, 10, 10, 2]


class MathProblem(evolution.Problem):
	'''Problem class for this module'''

	def __init__(self):
		'''Initializes parameters for the problem'''
		self.n_params = 0
		for i in range(len(ARCHITECTURE) - 1):
			self.n_params += ARCHITECTURE[i] * ARCHITECTURE[i + 1] + ARCHITECTURE[i + 1]

	def _create_network(self, chromosome=None):
		'''Creates a neural network for this problem'''
		network = neuralnet.NeuralNetwork()
		for i in range(len(ARCHITECTURE) - 1):
			network.add_layer(neuralnet.FullyConnectedLayer(ARCHITECTURE[i], ARCHITECTURE[i + 1]))
		network.compile()
		if chromosome is not None:
			network.set_params(chromosome)


def main(args):
	'''Module main method'''
	pass
