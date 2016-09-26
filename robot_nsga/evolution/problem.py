'''Defines the Problem interface'''


class Problem:
	'''Interface for building problem classes, suitable for consumption by NSGA'''

	def generate_individual(self):
		'''Must return an individual object with a randomly generated chromosome'''
		raise NotImplementedError('A problem class must implement generate_individual method')
