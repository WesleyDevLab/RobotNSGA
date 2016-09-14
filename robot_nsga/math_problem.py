'''Evolution of a neural network to perform simple math functions.'''

import numpy

import evolution
import neuralnet
from database import Database


ARCHITECTURE = [2, 10, 10, 2]


class MathProblem(evolution.Problem):
	'''Problem class for this module'''

	def __init__(self):
		'''Initializes parameters for the problem'''
		self.n_params = 0
		for i in range(len(ARCHITECTURE) - 1):
			self.n_params += ARCHITECTURE[i] * ARCHITECTURE[i + 1] + ARCHITECTURE[i + 1]
		print(self.n_params)

	def _create_network(self, chromosome=None):
		'''Creates a neural network for this problem'''
		network = neuralnet.NeuralNetwork()
		for i in range(len(ARCHITECTURE) - 1):
			network.add_layer(neuralnet.FullyConnectedLayer(ARCHITECTURE[i], ARCHITECTURE[i + 1]))
		network.compile()
		if chromosome is not None:
			network.set_params(chromosome)

	def generate_population(self, size):
		'''Creates a new random population'''
		new_population = evolution.Population()
		for i in range(size):
			name = 'I' + str(i)
			chromosome = [numpy.random.normal(0, 1) for _ in range(self.n_params)]
			new_individual = evolution.Individual(chromosome)
			new_population.individuals[name] = new_individual
		return new_population


def main(args):
	'''Module main method'''
	numpy.random.seed()
	database = Database(args.database)
	problem = MathProblem()
	database.create_population()
	first_population = problem.generate_population(10)
	to_save = {key: numpy.asarray(val.chromosome).tobytes() for key, val in first_population.individuals.items()}
	database.save(to_save)
	print(database.load())
