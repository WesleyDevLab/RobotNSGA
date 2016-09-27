'''Defines the Population class'''


class Population:
	'''Group of Individuals for use in an iteration of a genetic algorithm'''

	def __init__(self):
		'''Creates an empty population'''
		self.individuals = []
		self.fronts = []

	def __iter__(self):
		'''Returns an iterable through the individuals'''
		return self.individuals.__iter__()

	def add(self, new_individual):
		'''Appends the given individual to the population'''
		self.individuals.append(new_individual)

	def size(self):
		'''Returns the number of individuals in the population'''
		return len(self.individuals)
