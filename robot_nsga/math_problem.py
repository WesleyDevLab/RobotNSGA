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
MUTATION_PROB = 0.01


class MathProblem(evolution.Problem):
	'''Problem class for this module'''

	def __init__(self):
		'''Initializes parameters for the problem'''
		self.n_params = 0
		trainx_path = os.path.abspath(pkg_resources.resource_filename('resources.math', 'train_x.txt'))
		trainy_path = os.path.abspath(pkg_resources.resource_filename('resources.math', 'train_y.txt'))
		self.train_x = np.loadtxt(trainx_path, delimiter=',')[:, None]
		self.train_y = np.loadtxt(trainy_path, delimiter=',').T
		self.neuron_lengths = []
		for i in range(1, len(ARCHITECTURE)):
			self.neuron_lengths += [ARCHITECTURE[i - 1] + 1] * ARCHITECTURE[i]
		self.n_params = sum(self.neuron_lengths)

	def _create_network(self, chromosome=None):
		'''Creates a neural network for this problem'''
		network = neuralnet.NeuralNetwork()
		for i in range(len(ARCHITECTURE) - 1):
			network.add_layer(neuralnet.FullyConnectedLayer(ARCHITECTURE[i], ARCHITECTURE[i + 1]))
		network.compile()
		if chromosome is not None:
			network.set_params(chromosome)
		return network

	def crossover(self, parent1, parent2):
		'''Creates a new individual with genes from both parents'''
		total = 0
		child_chromosome = []
		for i in self.neuron_lengths:
			if random.random() < 0.5:
				child_chromosome += parent1.chromosome[total : total + i]
			else:
				child_chromosome += parent2.chromosome[total : total + i]
			total += i
		return evolution.Individual(child_chromosome)

	def evaluate(self, population):
		'''Tests each individual's performance in imitating the cos and sinc functions'''
		network = self._create_network()
		print('Evaluating')
		progress_bar = utils.ProgressBar()
		i = 1
		for individual in population:
			progress_bar.update(i / population.size())
			if not individual.fitness:
				network.set_params(individual.chromosome)
				output = network.predict(self.train_x)
				individual.fitness = np.mean(np.square(np.array(output) - self.train_y), axis=0).tolist()
			i += 1
		progress_bar = 0

	def generate_individual(self):
		'''Returns a new individual with a random chromosome'''
		chromosome = [random.gauss(0, 1) for _ in range(self.n_params)]
		return evolution.Individual(chromosome)

	def mutate(self, individual):
		'''Performs random mutations in the given individual'''
		for i in range(len(individual.chromosome)):
			if random.random() < MUTATION_PROB:
				individual.chromosome[i] = random.gauss(0, 1)


def main(args):
	'''Module main method'''
	if args.database is None:
		args.database = 'MathDatabase'
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
		database.set_property('no_objectives', 2)
	else:
		database.select()

	generation = database.properties['highest_population']
	population_size = database.properties['population_size']
	genetic_algorithm = evolution.NSGA(problem, population_size)
	if generation > 0:
		parents, children = utils.load_data(database)
		genetic_algorithm.set_population(parents)
		genetic_algorithm.set_children(children)
	for _ in range(args.iterations):
		generation += 1
		print('Starting generation ' + str(generation))
		genetic_algorithm.iterate()
		utils.save_data(genetic_algorithm, database)
