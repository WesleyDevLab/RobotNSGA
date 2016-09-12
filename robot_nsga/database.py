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
		self._save_properties()

	def _set_property(self, key, value):
		self.properties[key] = value
		self._save_properties()

	def _load_properties(self):
		'''Loads the database properties stored in the PROPERTIES_FILE'''
		with open(os.path.join(self.directory, PROPERTIES_FILE), 'rt') as in_file:
			self.properties = json.load(in_file)

	def create_population(self):
		'''Creates a new population after the last one and sets it as selected'''
		self._set_property('highest_population', self.properties['highest_population'] + 1)
		self.select()

	def load(self):
		'''Returns a list of all elements in the selected population as binary strings'''
		with open(os.path.join(self.directory, POPULATION_PREFIX + str(self.selected)), 'rb') as in_file:
			elements = []
			bstring = in_file.read(self.properties['binary_length'])
			while len(bstring) == self.properties['binary_length']:
				elements.append(bstring)
				bstring = in_file.read(self.properties['binary_length'])
		return elements

	def save(self, elements):
		'''Saves the given list of elements to the selected population file

		This operation overwrites any previous data in the file. All the elements in the list must be
		binary strings of the same length.
		'''
		self._set_property('binary_length', len(elements[0]))
		with open(os.path.join(self.directory, POPULATION_PREFIX + str(self.selected)), 'wb') as out_file:
			for row in elements:
				if len(row) != self.properties['binary_length']:
					raise RuntimeError('Attempting to save elements of different length.')
				else:
					out_file.write(row)

	def select(self, index=-1):
		'''Sets the given population as the one to load from and save to

		If given a -1, selects the highest population.
		'''
		if index > self.properties['highest_population']:
			raise IndexError('Given index is higher than max population.')
		if index < 0:
			index = self.properties['highest_population']
		self.selected = index
