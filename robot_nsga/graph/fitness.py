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

	if indexes is None:
		indexes = list(range(database.properties['no_objectives']))

	_, axes = plt.subplots(len(indexes), 1, sharex=True, squeeze=False)
	axes = axes.T[0]

	for j, idx in enumerate(indexes):
		best_fitness = []
		worst_fitness = []
		for i in x_range:
			database.select(i)
			individual_data = [val for key, val in database.load_report().items() if key.startswith('I')]
			gen_fitness = [val['fitness'][idx] for val in individual_data]
			best_fitness.append(min(gen_fitness))
			worst_fitness.append(max(gen_fitness))
		axes[j].semilogy(x_range, best_fitness, 'g', x_range, worst_fitness, 'r')
		axes[j].set_ylabel(database.properties['objective_names'][idx])

	plt.suptitle('Best and worst fitness')
	plt.xlabel('Generation')
	plt.show()
