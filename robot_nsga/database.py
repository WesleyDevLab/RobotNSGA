'''Defines Database class'''

import os


PROPERTIES_FILE = 'Properties.json'


class Database:
	'''Manages persistence of the genetic algorithm's state.'''

	def __init__(self, directory):
		'''Creates or loads a database in the given directory

		The directory should not contain any other data than the database, as it may be deleted.
		'''
		self.directory = os.path.abspath(directory)
		if not os.path.exists(self.directory):
			os.mkdir(self.directory)
