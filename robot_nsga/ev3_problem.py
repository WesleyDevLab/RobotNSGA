'''EV3 position regulation using neural networks'''

import random

import control
import evolution
import utils


ARCHITECTURE = [6, 20, 50, 20, 10, 3]
MUTATION_PROB = 0.005
SCREEN_WIDTH = 80

class EV3Problem(evolution.Problem):
	'''Problem class for EV3 robot'''

	def __init__(self):
		self.robot = control.Mindstorms()
		self.robot.connect()
		self.neuron_lengths = []
		for i in range(1, len(ARCHITECTURE)):
			self.neuron_lengths += [ARCHITECTURE[i - 1] + 1] * ARCHITECTURE[i]
		self.n_params = sum(self.neuron_lengths)

	def __del__(self):
		self.robot.disconnect()

	def crossover(self, parent1, parent2):
		pass

	def evaluate(self, population):
		pass

	def generate_individual(self):
		pass

	def mutate(self, individual):
		pass


def main(args):
	'''Module main function'''
	random.seed()
	problem = EV3Problem()
	database = utils.initialize_database(args, 'RobotTrainingData')
	database.set_objective_names(['Error de posicion', 'Tiempo'])
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
		database.create_population()
		utils.save_data(genetic_algorithm, database)
		print('=' * (SCREEN_WIDTH - 1))
