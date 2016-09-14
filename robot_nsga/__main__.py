'''Entry point for the application'''

import argparse

import math_problem


def main():
	'''Application main function'''
	global_parser = argparse.ArgumentParser()
	global_parser.add_argument('-d', '--database', help='The directory to be used as database')
	subparsers = global_parser.add_subparsers(title='subcommands')

	# Math problem
	math_parser = subparsers.add_parser('math',
		description='Train neural networks to perform simple mathematical functions',
		help='Execute the math test')
	math_parser.set_defaults(
		database='MathDatabase',
		func=math_problem.main
		)

	args = global_parser.parse_args()
	args.func(args)


if __name__ == '__main__':
	main()
