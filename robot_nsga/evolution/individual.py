'''Defines the Individual class'''


class Individual:
	'''Represents one individual in the genetic algorithm'''

	def __init__(self, chromosome):
		'''Creates a basic individual, with no metadata'''
		self.chromosome = chromosome
