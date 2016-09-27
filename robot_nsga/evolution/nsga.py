'''Defines class NSGA'''

from . import population


class NSGA:
	'''Multi-objective genetic algorithm'''

	def __init__(self, problem, population_size):
		'''Creates a genetic algorithm that will work on the provided problem'''
		self.problem = problem
		self.population = None
		self.children = None
		self.pop_size = population_size

	def _create_offspring(self):
		'''Creates a population of children'''
		pass

	def _crowding_distance(self):
		'''Assings each individual in the population its crowding distance'''
		pass

	def _nondominated_sort(self):
		'''Evaluates and groups individuals into nondomination fronts'''
		self.problem.evaluate(self.population)
		self.population.fronts = [[]]
		for individual in self.population:
			individual.domination_count = 0
			individual.dominated_solutions = []
			for ind in self.population:
				if individual.dominates(ind):
					individual.dominated_solutions.append(ind)
				elif ind.dominates(individual):
					individual.domination_count += 1
			if individual.domination_count == 0:
				individual.rank = 1
				self.population.fronts[0].append(individual)
		i = 0
		while self.population.fronts[i]:
			next_front = []
			for individual in self.population.fronts[i]:
				for ind in individual.dominated_solutions:
					ind.domination_count -= 1
					if ind.domination_count == 0:
						ind.rank = i + 1
						next_front.append(ind)
			i += 1
			self.population.fronts.append(next_front)
		self.population.fronts = self.population.fronts[:-1]

	def iterate(self):
		'''Perform a single iteration of the genetic algorithm'''
		if self.population is None:
			self.population = population.Population()
			for i in range(self.pop_size):
				new_individual = self.problem.generate_individual()
				new_individual.name = 'I' + str(i)
				self.population.add(new_individual)
			self._nondominated_sort()
			self._crowding_distance()
			self._create_offspring()
