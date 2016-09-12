'''Defines Database class'''

import os
import json


PROPERTIES_FILE = 'Properties.json'


class Database:
	'''Manages persistence of the genetic algorithm's state.'''

	def __init__(self, directory):
		'''Creates or loads a database in the given directory

		The directory should not contain any other data than the database, as it may be deleted.
		'''
		self.directory = os.path.abspath(directory)
		self.properties = {}
		if not os.path.exists(self.directory):
			os.mkdir(self.directory)
		else:
			self._load_properties()

	def _save_properties(self):
		'''Saves the database properties to the PROPERTIES_FILE'''
		with open(os.path.join(self.directory, PROPERTIES_FILE), 'wt') as out_file:
			json.dump(self.properties, out_file, indent='\t')

	def _load_properties(self):
		'''Loads the database properties stored in the PROPERTIES_FILE'''
		with open(os.path.join(self.directory, PROPERTIES_FILE), 'rt') as in_file:
			self.properties = json.load(in_file)
