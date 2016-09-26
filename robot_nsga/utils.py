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

	def _print(self):
		'''Prints the progress bar to the console'''
		filling = '#' * int(self.progress * (self.width - 7) / 100)
		filling = ('{: <' + str(self.width - 7) + '}').format(filling)
		print('\r{: >3}% [{}]'.format(int(self.progress), filling))


def save_data(genetic_algorithm, database):
	'''Saves relevant data after each iteration'''
	database.create_population()
	save_dict = {val.name: np.asarray(val.chromosome).tobytes()
		for val in genetic_algorithm.population}
	database.save(save_dict)
