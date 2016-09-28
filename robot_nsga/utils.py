'''Utility functions and classes'''

import numpy as np


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
