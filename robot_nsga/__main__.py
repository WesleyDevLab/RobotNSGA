'''Entry point for the application'''

import sys

def main():
	'''Application main function'''
	module = sys.argv[1]
	args = sys.argv[2:]
	if module == 'dev':
		import devtest
	else:
		print('Module not found')

if __name__ == '__main__':
	main()
