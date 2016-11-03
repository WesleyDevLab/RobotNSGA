'''EV3 position regulation using neural networks'''

import random
import _thread

import pygame
import numpy as np

import control
import evolution
import neuralnet
import utils


ARCHITECTURE = [6, 20, 50, 20, 10, 3]
MUTATION_PROB = 0.005
RANDOM_MU = 0
RANDOM_SIGMA = 0.2
SAMPLING_FREQ = 10
SCREEN_WIDTH = 80
SPEED_CAP = 20
STALL_SECONDS = 1
TIMEOUT = 10

def emergency_stop(var):
	'''Wait for emergency stop keystroke'''
	input()
	var.append(None)

class EV3Problem(evolution.Problem):
	'''Problem class for EV3 robot'''

	def __init__(self):
		self.robot = control.Mindstorms()
		self.robot.connect()
		self.neuron_lengths = []
		for i in range(1, len(ARCHITECTURE)):
			self.neuron_lengths += [ARCHITECTURE[i - 1] + 1] * ARCHITECTURE[i]
		self.n_params = sum(self.neuron_lengths)
		self.network = neuralnet.NeuralNetwork()
		for i in range(len(ARCHITECTURE) - 1):
			self.network.add_layer(neuralnet.FullyConnectedLayer(ARCHITECTURE[i], ARCHITECTURE[i + 1]))
		self.network.compile()

	def __del__(self):
		self.robot.disconnect()

	def _run_test(self, goal_position, chromosome):
		'''Runs a single position regulation test'''
		self.network.set_params(chromosome)
		clock = pygame.time.Clock()
		inputs = np.array([list(goal_position) + [0] * 3])
		finish = False
		dummy_list = []
		_thread.start_new_thread(emergency_stop, (dummy_list,))
		stall_counter = 0
		start_time = pygame.time.get_ticks()
		while not finish:
			inputs[0][3:] = self.robot.read_joints()
			outputs = np.clip(self.network.predict(inputs), -SPEED_CAP, SPEED_CAP)
			for idx, speed in np.ndenumerate(outputs):
				self.robot.set_motor(idx[1] + 1, float(speed))
			# Emergency stop
			if dummy_list:
				finish = True
			# Stall stop criterion
			if self.robot.detect_stall():
				stall_counter += 1
			else:
				stall_counter = 0
			if stall_counter >= STALL_SECONDS * SAMPLING_FREQ:
				finish = True
			# Timeout stop criterion
			if pygame.time.get_ticks() - start_time > TIMEOUT * 1000:
				finish = True
			print(self.robot.joints, outputs, clock.get_rawtime(), sep='\t')
			clock.tick_busy_loop(SAMPLING_FREQ)
		total_time = pygame.time.get_ticks() - start_time
		error = np.linalg.norm(np.array(self.robot.direct_kinematics()) - np.array(goal_position))
		return total_time, error

	def crossover(self, parent1, parent2):
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
		pass

	def generate_individual(self):
		chromosome = [random.gauss(RANDOM_MU, RANDOM_SIGMA) for _ in range(self.n_params)]
		return evolution.Individual(chromosome)

	def mutate(self, individual):
		for i in range(len(individual.chromosome)):
			if random.random() < MUTATION_PROB:
				individual.chromosome[i] = random.gauss(RANDOM_MU, RANDOM_SIGMA)


def main(args):
	'''Module main function'''
	pygame.init()
	random.seed()
	problem = EV3Problem()
	database = utils.initialize_database(args, 'RobotTrainingData')
	database.set_objective_names(['Error de posicion', 'Tiempo'])
	generation = database.properties['highest_population']
	population_size = database.properties['population_size']
	genetic_algorithm = evolution.NSGA(problem, population_size)

	problem.robot.home()
	problem.robot.reset()
	problem._run_test((-90, 90, 220), problem.generate_individual().chromosome)

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
