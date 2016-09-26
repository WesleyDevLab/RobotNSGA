'''Defines class NSGA'''

import population


class NSGA:
	'''Multi-objective genetic algorithm'''

	def __init__(self, problem, population_size):
		'''Creates a genetic algorithm that will work on the provided problem'''
		self.problem = problem
		self.population = None
		self.children = None
		self.pop_size = population_size

	def iterate(self):
		'''Perform a single iteration of the genetic algorithm'''
		if self.population is None:
			self.population = population.Population()
			for i in range(self.pop_size):
				new_individual = self.problem.generate_individual()
				new_individual.name = 'I' + str(i)
				self.population.add(new_individual)
