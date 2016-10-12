'''Utility functions and classes'''

import sys

import numpy as np

from database import Database
import evolution


class ProgressBar:
	'''Progress bar to be displayed in a separate line in the terminal'''

	def __init__(self, width=79):
		'''Initializes an empty progress bar, with the given width in characters

		This method should be called when the cursor is in an empty line, as it will be overwritten.
		'''
		self.progress = 0
		self.width = width
		self._print()

	def __del__(self):
		'''Erases the progress bar from the screen'''
		print('\r' + ' ' * self.width + '\r', end='', flush=True)

	def _print(self):
		'''Prints the progress bar to the console'''
		filling = '#' * int(self.progress * (self.width - 7) / 100)
		filling = ('{: <' + str(self.width - 7) + '}').format(filling)
		print('\r{: >3}% [{}]'.format(int(self.progress), filling), end='', flush=True)

	def update(self, progress):
		'''Updates the progress bar to show the given progress'''
		self.progress = progress
		self._print()


def initialize_database(args, default_dir):
	'''Performs the necessary checks and initialization procedures to initialize the database

	Returns the database to be used.
	'''
	if args.database is None:
		args.database = default_dir
	ret_db = Database(args.database)
	if args.reset:
		ret_db.reset()
	if ret_db.properties['highest_population'] == 0:
		if args.size is None:
			print('ERROR: Population size must be specified when starting a new run.')
			sys.exit()
		ret_db.set_property('population_size', args.size)
	else:
		ret_db.select()
	return ret_db

def generate_report(population):
	'''Creates a dictionary containing relevant data from each individual in population'''
	report = {val.name: {
		'fitness': val.fitness,
		'rank': val.rank,
		'crowding_distance': val.crowding_distance
		}
		for val in population}
	return report

def load_data(database):
	'''Returns parent and children populations in the selected population of the database'''
	pop_dict = database.load()
	report = database.load_report()
	parents = []
	children = []
	for name, bstring in pop_dict.items():
		ind = evolution.Individual(np.fromstring(bstring).tolist())
		ind.name = name
		ind.fitness = report[name]['fitness']
		ind.rank = report[name]['rank']
		ind.crowding_distance = report[name]['crowding_distance']
		if name.startswith('I'):
			parents.append(ind)
		elif name.startswith('C'):
			children.append(ind)
	return (parents, children)

def save_data(genetic_algorithm, database):
	'''Saves relevant data after each iteration'''
	database.create_population()
	pop_save = {val.name: np.asarray(val.chromosome).tobytes()
		for val in genetic_algorithm.population}
	if genetic_algorithm.children is not None:
		child_save = {val.name: np.asarray(val.chromosome).tobytes()
			for val in genetic_algorithm.children}
		pop_save.update(child_save)
	database.save(pop_save)
	report = generate_report(genetic_algorithm.population)
	if genetic_algorithm.children is not None:
		report.update(generate_report(genetic_algorithm.children))
	database.save_report(report)
