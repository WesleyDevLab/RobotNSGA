'''Defines Database class'''

import os
import json


POPULATION_PREFIX = 'Population'
PROPERTIES_FILE = 'Properties.json'


class Database:
	'''Manages persistence of the genetic algorithm's state.'''

	def __init__(self, directory):
		'''Creates or loads a database in the given directory

		The directory should not contain any other data than the database, as it may be deleted.
		'''
		self.directory = os.path.abspath(directory)
		self.properties = {}
		self.selected = 0
		if not os.path.exists(self.directory):
			os.mkdir(self.directory)
			self._set_defaults()
			self._save_properties()
		else:
			self._load_properties()

	def _save_properties(self):
		'''Saves the database properties to the PROPERTIES_FILE'''
		with open(os.path.join(self.directory, PROPERTIES_FILE), 'wt') as out_file:
			json.dump(self.properties, out_file, indent='\t', sort_keys=True)

	def _set_defaults(self):
		'''Sets the default properties for the database'''
		self.properties = {}
		self.properties['binary_length'] = 0
		self.properties['highest_population'] = 0

	def _load_properties(self):
		'''Loads the database properties stored in the PROPERTIES_FILE'''
		with open(os.path.join(self.directory, PROPERTIES_FILE), 'rt') as in_file:
			self.properties = json.load(in_file)

	def create_population(self):
		'''Creates a new population after the last one and sets it as selected'''
		self.properties['highest_population'] += 1
		self.select()

	def select(self, index=-1):
		'''Sets the given population as the one to load from and save to

		If given a -1, selects the highest population.
		'''
		if index > self.properties['highest_population']:
			raise IndexError('Given index is higher than max population.')
		if index < 0:
			index = self.properties['highest_population']
		self.selected = index
