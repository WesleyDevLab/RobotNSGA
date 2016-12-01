'''Train a neural network to perform inverse kinematics'''

# pylint: disable = C0301

import os
import random

import numpy as np
import pkg_resources
import theano.tensor as T

import evolution
import neuralnet
import utils


ARCHITECTURE = [3, 10, 3]
MUTATION_PROB = 0.01
RANDOM_MU = 0
RANDOM_SIGMA = 5
SCREEN_WIDTH = 120

x_train = None
y_train = None

class IKProblem(evolution.Problem):
	'''Problem class for inverse kinematics'''

	def __init__(self):
		self.neuron_lengths = []
		for i in range(1, len(ARCHITECTURE)):
			self.neuron_lengths += [ARCHITECTURE[i - 1] + 1] * ARCHITECTURE[i]
		self.n_params = sum(self.neuron_lengths)
		self.network = neuralnet.NeuralNetwork()
		for i in range(len(ARCHITECTURE) - 2):
			self.network.add_layer(neuralnet.FullyConnectedLayer(ARCHITECTURE[i], ARCHITECTURE[i + 1], T.nnet.nnet.sigmoid))
		self.network.add_layer(neuralnet.FullyConnectedLayer(ARCHITECTURE[-2], ARCHITECTURE[-1]))
		self.network.compile()

	def crossover(self, parent1, parent2):
		child_chromosome = []
		counter = 0
		for i in range(len(ARCHITECTURE) - 1):
			positions = np.random.randint(ARCHITECTURE[i + 1], size=ARCHITECTURE[i + 1])
			for pos in positions:
				start = counter + (ARCHITECTURE[i] + 1) * pos
				parent_from = random.choice([parent1, parent2])
				child_chromosome += parent_from.chromosome[start : start + ARCHITECTURE[i] + 1]
			counter += (ARCHITECTURE[i] + 1) * ARCHITECTURE[i + 1]
		return evolution.Individual(child_chromosome)

	def evaluate(self, population):
		print('Evaluating')
		for individual in population:
			if individual.fitness:
				continue
			self.network.set_params(individual.chromosome)
			results = self.network.predict(x_train)
			individual.fitness = np.mean(np.square(results - y_train), axis=0).tolist()

	def generate_individual(self):
		chromosome = [random.gauss(RANDOM_MU, RANDOM_SIGMA) for _ in range(self.n_params)]
		return evolution.Individual(chromosome)

	def mutate(self, individual):
		for i in range(len(individual.chromosome)):
			if random.random() < MUTATION_PROB:
				individual.chromosome[i] = random.gauss(RANDOM_MU, RANDOM_SIGMA)


def main(args):
	'''Module main function'''
	global x_train
	global y_train
	random.seed()
	database = utils.initialize_database(args, 'IKTrainingData')
	database.set_objective_names(['Error en x', 'Error en y', 'Error en z'])
	problem = IKProblem()
	generation = database.properties['highest_population']
	population_size = database.properties['population_size']
	genetic_algorithm = evolution.NSGA(problem, population_size)

	x_path = os.path.abspath(pkg_resources.resource_filename('resources.ev3', 'x_train.txt'))
	y_path = os.path.abspath(pkg_resources.resource_filename('resources.ev3', 'y_train.txt'))
	x_train = np.loadtxt(y_path)
	y_train = np.loadtxt(x_path)

	if generation > 0:
		parents, children = utils.load_data(database)
		genetic_algorithm.set_population(parents)
		genetic_algorithm.set_children(children)
	for _ in range(args.iterations):
		generation += 1
		print('Starting generation ' + str(generation))
		genetic_algorithm.iterate()
		database.create_population()
		utils.save_data(genetic_algorithm, database)
		print('=' * (SCREEN_WIDTH - 1))
