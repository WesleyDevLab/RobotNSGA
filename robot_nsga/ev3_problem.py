'''EV3 position regulation using neural networks'''

# pylint: disable = C0301, R0914

from datetime import datetime
import os
import random

import numpy as np
import pygame
import pkg_resources
import theano.tensor as T

import control
import evolution
import neuralnet
import utils
from database import Database


ARCHITECTURE = [6, 20, 50, 20, 10, 3]
HOME_THRESHOLD = 10
MUTATION_PROB = 0.005
N_GOALS = 5
RANDOM_MU = 0
RANDOM_SIGMA = 0.25
SAMPLING_FREQ = 10
SCREEN_WIDTH = 120
SPEED_CAP = 40
STALL_SECONDS = 0.5
TIMEOUT = 10

database = None
genetic_algorithm = None
goal_positions = None

class EV3Problem(evolution.Problem):
	'''Problem class for EV3 robot'''

	def __init__(self, log_to_file=True):
		self.robot = control.Mindstorms()
		self.robot.connect()
		self.neuron_lengths = []
		for i in range(1, len(ARCHITECTURE)):
			self.neuron_lengths += [ARCHITECTURE[i - 1] + 1] * ARCHITECTURE[i]
		self.n_params = sum(self.neuron_lengths)
		self.network = neuralnet.NeuralNetwork()
		for i in range(len(ARCHITECTURE) - 2):
			self.network.add_layer(neuralnet.FullyConnectedLayer(ARCHITECTURE[i], ARCHITECTURE[i + 1], T.nnet.nnet.relu))
		self.network.add_layer(neuralnet.FullyConnectedLayer(ARCHITECTURE[-2], ARCHITECTURE[-1]))
		self.network.compile()
		self.log_to_file = log_to_file

	def __del__(self):
		self.robot.disconnect()

	def run_test(self, goal_position, chromosome):
		'''Runs a single position regulation test'''
		if self.log_to_file:
			log = database.log
		else:
			log = print
		self.network.set_params(chromosome)
		clock = pygame.time.Clock()
		inputs = np.expand_dims(np.append(goal_position, [0] * 3), axis=0)
		last_outputs = np.zeros((1, 3))
		integral = np.zeros((1, 3))
		finish = False
		# timeout = False
		stall_counter = 0
		start_time = pygame.time.get_ticks()
		while not finish:
			inputs[0, 3:] = self.robot.read_joints()
			outputs = np.clip(self.network.predict(inputs), -SPEED_CAP, SPEED_CAP)
			for idx, speed in np.ndenumerate(outputs):
				self.robot.set_motor(idx[1] + 1, float(speed))
			integral += (np.absolute(outputs) + np.absolute(last_outputs)) * 1000 / (2 * SAMPLING_FREQ)
			last_outputs = outputs
			# Stall stop criterion
			if self.robot.detect_stall():
				stall_counter += 1
			else:
				stall_counter = 0
			if stall_counter >= STALL_SECONDS * SAMPLING_FREQ:
				# if self.robot.detect_soft_limits(outputs.flatten()).any():
				# 	timeout = True
				finish = True
			# Timeout stop criterion
			if pygame.time.get_ticks() - start_time > TIMEOUT * 1000:
				# timeout = True
				finish = True
			log(str(inputs[0, 3:]) + '\t' +
				str(np.around(outputs, 2)) + '\t' +
				str(clock.get_rawtime()) + '\n')
			clock.tick_busy_loop(SAMPLING_FREQ)
		results = np.zeros(5)
		results[0] = pygame.time.get_ticks() - start_time
		results[1 : 4] = np.absolute(np.array(self.robot.direct_kinematics()) - np.array(goal_position))
		results[4] = np.sum(integral) / results[0]
		# if timeout:
		# 	total_time = float('inf')
		# error = np.linalg.norm(np.array(self.robot.direct_kinematics()) - np.array(goal_position))
		log('Test finished. Total time: {}\tFinal position: ({:.2f}, {:.2f}, {:.2f})\tEnergy avg: {:.2f}'.format(
			results[0], *self.robot.direct_kinematics(), results[4]))
		return results

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
		if self.log_to_file:
			log = database.log
			p_bar = utils.ProgressBar(SCREEN_WIDTH - 1)
		else:
			log = print
		log(('{:=^' + str(SCREEN_WIDTH - 1) + '}\n').format('MINDSTORMS ROBOT TESTING LOG'))
		log(('{:^' + str(SCREEN_WIDTH - 1) + '}\n').format('Created on ' + str(datetime.now())))
		increment = 100.0 / (population.size() * goal_positions.shape[0])
		k = 0
		for individual in population:
			if individual.fitness:
				k += increment * goal_positions.shape[0]
				continue
			log('\n\nTesting individual: ' + individual.name + '\n')
			self.robot.home()
			attempts = 1
			while not (np.array(self.robot.read_joints()) < HOME_THRESHOLD).all():
				attempts += 1
				self.robot.home()
			self.robot.reset()
			log('Attempted homing ' + str(attempts) + ' times.')
			results = np.zeros((goal_positions.shape[0], 5))
			for i, goal in enumerate(np.random.permutation(goal_positions)):
				log('\n\nGoal no. ' + str(i + 1) + ': ' + str(goal) + '\n')
				log('Robot pos.\t\tControl signal\t\tBusy time\n' + ('-' * (SCREEN_WIDTH - 1)) + '\n')
				results[i, :] = self.run_test(goal, individual.chromosome)
				k += increment
				if self.log_to_file:
					p_bar.update(k)
			individual.fitness = np.mean(results, 0).tolist()
			log('\n\nFitness calculated for {}: {}\n'.format(individual.name, individual.fitness))

	def generate_individual(self):
		chromosome = [random.gauss(RANDOM_MU, RANDOM_SIGMA) for _ in range(self.n_params)]
		return evolution.Individual(chromosome)

	def mutate(self, individual):
		for i in range(len(individual.chromosome)):
			if random.random() < MUTATION_PROB:
				individual.chromosome[i] = random.gauss(RANDOM_MU, RANDOM_SIGMA)


def test(args):
	'''Runs a single test, using a prevously generated individual'''
	global database
	global goal_positions
	pygame.init()
	random.seed()
	np.random.seed()
	if args.database is None:
		args.database = 'RobotTrainingData'
	database = Database(args.database)
	problem = EV3Problem(log_to_file=False)

	res_path = os.path.abspath(pkg_resources.resource_filename('resources.ev3', 'test_set.txt'))
	goal_positions = np.loadtxt(res_path)

	database.select(args.generation)
	chromosome = np.fromstring(database.load()['I' + str(args.individual)]).tolist()
	problem.robot.home()
	for goal in goal_positions:
		problem.run_test(goal, chromosome)


def main(args):
	'''Module main function'''
	global database
	global genetic_algorithm
	global goal_positions
	pygame.init()
	random.seed()
	database = utils.initialize_database(args, 'RobotTrainingData')
	database.set_objective_names(['Tiempo', 'Error en X', 'Error en Y', 'Error en Z', 'Energía'])
	problem = EV3Problem()
	generation = database.properties['highest_population']
	population_size = database.properties['population_size']
	genetic_algorithm = evolution.NSGA(problem, population_size)

	res_path = os.path.abspath(pkg_resources.resource_filename('resources.ev3', 'training_set.txt'))
	batch_start = (generation % 10) * N_GOALS
	goal_positions = np.loadtxt(res_path)[batch_start : batch_start + N_GOALS, :]

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
