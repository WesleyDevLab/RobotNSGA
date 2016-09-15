'''Defines the Population class'''


class Population:
	'''Group of Individuals for use in an iteration of a genetic algorithm'''

	def __init__(self):
		'''Creates an empty population'''
		self.individuals = {}

	def __iter__(self):
		'''Returns an iterable through the individuals'''
		return self.individuals.__iter__()

	def items(self):
		'''Get individuals as (key, value) pairs'''
		return self.individuals.items()

	def size(self):
		'''Returns the number of individuals in the population'''
		return len(self.individuals)
