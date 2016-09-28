'''Utility functions and classes'''

import numpy as np

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
		print('\r' + ' ' * self.width + '\r', end=' ', flush=True)

	def _print(self):
		'''Prints the progress bar to the console'''
		filling = '#' * int(self.progress * (self.width - 7) / 100)
		filling = ('{: <' + str(self.width - 7) + '}').format(filling)
		print('\r{: >3}% [{}]'.format(int(self.progress), filling), end='', flush=True)

	def update(self, progress):
		'''Updates the progress bar to show the given progress'''
		self.progress = progress
		self._print()


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
