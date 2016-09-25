'''Defines class NSGA'''

class NSGA:
	'''Multi-objective genetic algorithm'''

	def __init__(self, problem):
		'''Creates a genetic algorithm that will work on the provided problem'''
		self.problem = problem
		self.population = None
		self.children = None
