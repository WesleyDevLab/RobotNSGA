'''Defines the main function of the graph module'''

import os
import sys

import database
import graph


def main(args):
	'''Graph module's main function'''
	abs_path = ''
	if args.database is None:
		abs_path = os.getcwd()
	else:
		abs_path = os.path.abspath(args.database)
	if not database.is_database(abs_path, verbose=True):
		sys.exit()

	db = database.Database(abs_path)

	for graph_type in args.types:
		if graph_type == 'fitness':
			graph.fitness_graph(db, args.objectives)
