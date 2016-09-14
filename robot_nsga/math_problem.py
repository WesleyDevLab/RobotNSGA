'''Evolution of a neural network to perform simple math functions.'''

import evolution
from database import Database


class MathProblem(evolution.Problem):
	'''Problem class for this module'''
	pass


def main(args):
	'''Module main method'''
	database = Database(args.database)
	problem = MathProblem()
