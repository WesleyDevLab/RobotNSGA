'''Defines class NSGA'''

class NSGA:
	'''Multi-objective genetic algorithm'''

	def __init__(self, problem, population_size, generation=1):
		'''Creates a genetic algorithm that will work on the provided problem'''
		self.problem = problem
		self.population = None
		self.children = None
		self.pop_size = population_size
		self.generation = generation

	def iterate(self):
		'''Perform a single iteration of the genetic algorithm'''
		pass
