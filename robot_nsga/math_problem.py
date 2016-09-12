'''Evolution of a neural network to perform simple math functions.'''

from database import Database


def main(args):
	'''Module main method'''
	database = Database('MathDatabase')
	print(database.properties)
	database.create_population()
	database.save([b'abc', b'def', b'ghi'])
	print(database.properties)
