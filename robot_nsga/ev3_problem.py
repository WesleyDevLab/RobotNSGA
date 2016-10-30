'''EV3 position regulation using neural networks'''

import random

import evolution
import utils


class EV3Problem(evolution.Problem):
	'''Problem class for EV3 robot'''
	pass


def main(args):
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
