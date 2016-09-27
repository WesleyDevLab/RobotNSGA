'''Defines the Individual class'''


class Individual:
	'''Represents one individual in the genetic algorithm'''

	def __init__(self, chromosome):
		'''Creates a basic individual, with no metadata'''
		self.name = None
		self.chromosome = chromosome
		self.fitness = []
		self.rank = 0
		self.crowding_distance = 0
		self.domination_count = 0
		self.dominated_solutions = []

	def __repr__(self):
		fitness_repr = ['{:0.2f}'.format(a) for a in self.fitness]
		return self.name + '(' + str(fitness_repr) + ', ' + str(self.rank) + \
			str(self.crowding_distance) + ')'

	def __str__(self):
		return self.name

	def dominates(self, other):
		'''Returns true if this individual dominates the other one'''
		better = False
		for i in range(len(self.fitness)):
			if self.fitness[i] > other.fitness[i]:
				break
			elif self.fitness[i] < other.fitness[i]:
				better = True
		else:
			return better
		return False
