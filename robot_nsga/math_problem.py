'''Evolution of a neural network to perform simple math functions.'''

# pylint: disable = E1101

import os
import random
import sys

import pkg_resources
import numpy as np

import evolution
import neuralnet
import utils
from database import Database


ARCHITECTURE = [1, 10, 10, 2]


class MathProblem(evolution.Problem):
	'''Problem class for this module'''

	def __init__(self):
		'''Initializes parameters for the problem'''
		self.n_params = 0
		for i in range(len(ARCHITECTURE) - 1):
			self.n_params += ARCHITECTURE[i] * ARCHITECTURE[i + 1] + ARCHITECTURE[i + 1]
		trainx_path = os.path.abspath(pkg_resources.resource_filename('resources.math', 'train_x.txt'))
		trainy_path = os.path.abspath(pkg_resources.resource_filename('resources.math', 'train_y.txt'))
		self.train_x = np.loadtxt(trainx_path, delimiter=',')[:, None]
		self.train_y = np.loadtxt(trainy_path, delimiter=',').T

	def _create_network(self, chromosome=None):
		'''Creates a neural network for this problem'''
		network = neuralnet.NeuralNetwork()
		for i in range(len(ARCHITECTURE) - 1):
			network.add_layer(neuralnet.FullyConnectedLayer(ARCHITECTURE[i], ARCHITECTURE[i + 1]))
		network.compile()
		if chromosome is not None:
			network.set_params(chromosome)
		return network

	def evaluate(self, population):
		'''Tests each individual's performance in imitating the cos and sinc functions'''
		network = self._create_network()
		i = 1
		for individual in population:
			print('\rEvaluating [' + str(i) + '/' + str(population.size()) + ']', end='', flush=True)
			network.set_params(individual.chromosome)
			output = network.predict(self.train_x)
			individual.fitness = np.mean(np.square(np.array(output) - self.train_y), axis=0).tolist()
			i += 1

	def generate_individual(self):
		'''Returns a new individual with a random chromosome'''
		chromosome = [random.gauss(0, 1) for _ in range(self.n_params)]
		return evolution.Individual(chromosome)


def main(args):
	'''Module main method'''
	database = Database(args.database)
	problem = MathProblem()
	random.seed()

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
