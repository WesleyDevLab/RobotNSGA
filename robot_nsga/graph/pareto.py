'''Defines the pareto graph'''

import matplotlib.pyplot as plt


FRONT_COUNT = 10

def pareto_graph(database, objectives=None):
	'''Constructs a visualization of the movement of the best front over generations

	The argument 'objectives' must be a list indicating the indices of the fitness values to be used.
	The first two will be consumed. If the list has less than two elements, or if is not given, the
	graph will be produced using the first two fitness values.
	'''
	if objectives is None or len(objectives) < 2:
		objectives = [0, 1]

	generations = []
	if database.properties['highest_population'] < FRONT_COUNT:
		generations = list(range(1, database.properties['highest_population'] + 1))
	else:
		step = database.properties['highest_population'] / FRONT_COUNT
		generations = [round(i * step) for i in range(1, FRONT_COUNT + 1)]

	for i, gen in enumerate(generations, start=1):
		database.select(gen)
		individual_data = [val for key, val in database.load_report().items()
			if key.startswith('I') and val['rank'] == 1]
		x_values = [val['fitness'][objectives[0]] for val in individual_data]
		y_values = [val['fitness'][objectives[1]] for val in individual_data]
		plt.plot(x_values, y_values,
			color=str((FRONT_COUNT - i) / FRONT_COUNT),
			linestyle='None',
			marker='o',
			markeredgecolor='white')

	plt.title('Movement of best front')
	plt.xscale('log')
	plt.yscale('log')
	plt.xlabel(database.properties['objective_names'][objectives[0]])
	plt.ylabel(database.properties['objective_names'][objectives[1]])
	plt.show()
