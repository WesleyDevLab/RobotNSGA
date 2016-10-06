'''Defines the fitness graph'''

import matplotlib.pyplot as plt


def fitness_graph(database, indexes=None):
	'''Constructs the fitness evolution graph for the given database

	The 'indexes' argument specifies the objectives for which graphs will be produced. If not present,
	graphs will be produced for all objectives.
	'''
	generations = database.properties['highest_population']
	best_fitness = []
	worst_fitness = []
	x_range = range(1, generations + 1)

	for i in x_range:
		database.select(i)
		individual_data = [val for key, val in database.load_report().items() if key.startswith('I')]
		gen_fitness = [val['fitness'][0] for val in individual_data]
		best_fitness.append(min(gen_fitness))
		worst_fitness.append(max(gen_fitness))

	plt.semilogy(x_range, best_fitness, 'g', x_range, worst_fitness, 'r')
	plt.show()
