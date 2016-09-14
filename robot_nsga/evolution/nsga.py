'''Defines class NSGA'''

class NSGA:
	'''Multi-objective genetic algorithm'''

	def __init__(self, problem, population, children=None):
		'''Creates a genetic algorithm that will work on the provided population and children.

		If children are not provided, the algorithm will behave as if it was its first iteration.
		'''
		self.problem = problem
		self.population = population
		self.children = children
