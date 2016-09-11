'''Entry point for the application'''

import sys

def main():
	'''Application main function'''
	module = sys.argv[1]
	args = sys.argv[2:]
	if module == 'math':
		import math_problem
		math_problem.main(args)
	else:
		print('Module not found')

if __name__ == '__main__':
	main()
