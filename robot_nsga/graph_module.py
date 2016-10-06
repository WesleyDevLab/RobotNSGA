'''Defines the main function of the graph module'''

import os
import sys

import database


def main(args):
	'''Graph module's main function'''
	abs_path = ''
	if args.database is None:
		abs_path = os.getcwd()
	else:
		abs_path = os.path.abspath(args.database)
	if not database.is_database(abs_path, verbose=True):
		sys.exit()
