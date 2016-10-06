'''Entry point for the application'''

import argparse

import graph_module
import math_problem


def main():
	'''Application main function'''
	global_parser = argparse.ArgumentParser()
	global_parser.add_argument('-d', '--database', help='the directory to be used as database')
	subparsers = global_parser.add_subparsers(title='subcommands')

	# Graph module parser
	graph_parser = subparsers.add_parser('graph',
		description='Display graphs of performance metrics from a database',
		help='Display performance graphs')
	graph_parser.add_argument('-o', '--objectives', type=int, nargs='+',
		help='indexes of the relevant objectives')
	graph_parser.add_argument('types', nargs='+', help='types of graphs to generate', choices=[
		'fitness',
		'pareto'
	])
	graph_parser.set_defaults(
		func=graph_module.main
		)

	# Evolution super-parser
	evolution_parser = argparse.ArgumentParser(add_help=False)
	evolution_parser.add_argument('--reset',
		action='store_true',
		help='delete data and start from generation 1')
	evolution_parser.add_argument('-i', '--iterations', type=int, help='number of iterations to perform')
	evolution_parser.add_argument('-s', '--size', type=int, help='population size')
	evolution_parser.set_defaults(iterations=1)

	# Math problem
	math_parser = subparsers.add_parser('math',
		description='Train neural networks to perform simple mathematical functions',
		help='Execute the math test',
		parents=[evolution_parser])
	math_parser.set_defaults(
		func=math_problem.main
		)

	args = global_parser.parse_args()
	args.func(args)


if __name__ == '__main__':
	main()
