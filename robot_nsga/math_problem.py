'''Evolution of a neural network to perform simple math functions.'''

import sys

import evolution
import neuralnet
import utils

from database import Database


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
	database = Database(args.database)
	problem = MathProblem()

	if args.reset:
		database.reset()
	if database.properties['highest_population'] == 0:
		if args.size is None:
			print('ERROR: Population size must be specified when starting a new run.')
			sys.exit()
		database.set_property('population_size', args.size)
	else:
		database.select()

	generation = database.properties['highest_population']
	population_size = database.properties['population_size']
	genetic_algorithm = evolution.NSGA(problem, population_size)
	for _ in range(args.iterations):
		generation += 1
		print('Starting generation ' + str(generation))
		genetic_algorithm.iterate()
		utils.save_data(genetic_algorithm, database)
