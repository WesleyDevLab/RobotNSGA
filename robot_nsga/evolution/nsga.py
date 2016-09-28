'''Defines class NSGA'''

import random

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
		self.children = population.Population()
		for i in range(self.pop_size):
			participants = random.sample(self.population.individuals, 4)
			winner1 = max(participants[:2])
			winner2 = max(participants[-2:])
			new_child = self.problem.crossover(winner1, winner2)
			new_child.name = 'C' + str(i)
			self.problem.mutate(new_child)
			self.children.add(new_child)

	def _crowding_distance(self):
		'''Assings each individual in the population its crowding distance'''
		n_objectives = len(self.population.individuals[0].fitness)
		f_max = [float('-inf') for _ in range(n_objectives)]
		f_min = [float('inf') for _ in range(n_objectives)]
		for individual in self.population:
			individual.crowding_distance = 0
			for i in range(n_objectives):
				if individual.fitness[i] > f_max[i]:
					f_max[i] = individual.fitness[i]
				if individual.fitness[i] < f_min[i]:
					f_min[i] = individual.fitness[i]
		for front in self.population.fronts:
			for i in range(n_objectives):
				sorted_front = sorted(front, key=lambda a: a.fitness[i])
				sorted_front[0].crowding_distance = float('inf')
				sorted_front[-1].crowding_distance = float('inf')
				for j in range(1, len(sorted_front) - 1):
					sorted_front[j].crowding_distance += \
						sorted_front[j + 1].fitness[i] - sorted_front[j - 1].fitness[i]
					sorted_front[j].crowding_distance /= f_max[i] - f_min[i]

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
						ind.rank = i + 2
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
		else:
			self.population.join(self.children)
			self._nondominated_sort()
			self._crowding_distance()
			new_population = population.Population()
			i = 0
			while new_population.size() + len(self.population.fronts[i]) <= self.pop_size:
				for individual in self.population.fronts[i]:
					new_population.add(individual)
				i += 1
			sorted_front = sorted(self.population.fronts[i], reverse=True)
			for individual in sorted_front[:self.pop_size - self.population.size]:
				new_population.add(individual)
			self.population = new_population
			self._create_offspring()

	def set_children(self, new_children):
		'''Sets the children population to be used'''
		self.children = new_children

	def set_population(self, new_population):
		'''Sets the population to work with'''
		self.population = new_population
		self.pop_size = new_population.size()
