'''Defines class NSGA'''

class NSGA:
	'''Multi-objective genetic algorithm'''

	def __init__(self, problem, population_size):
		'''Creates a genetic algorithm that will work on the provided problem'''
		self.problem = problem
		self.population = None
		self.children = None
		self.pop_size = population_size

	def iterate(self, n_iterations=1, callback=None):
		'''Perform n iterations of the genetic algorithm

		After each iteration, the provided callback function will be called.
		'''
		pass
