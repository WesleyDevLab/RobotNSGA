'''Defines the Problem interface'''


class Problem:
	'''Interface for building problem classes, suitable for consumption by NSGA'''

	def evaluate(self, population):
		'''Must assign each individual in the population a fitness for each of the objectives'''
		raise NotImplementedError('A problem class must implement evaluate method')

	def generate_individual(self):
		'''Must return an individual object with a randomly generated chromosome'''
		raise NotImplementedError('A problem class must implement generate_individual method')
