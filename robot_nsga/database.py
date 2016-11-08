'''Defines Database class'''

import os
import json
import shutil


DATA_DIRECTORY = 'data'
ID_PREFIX = 'id_'
LOG_DIRECTORY = 'logs'
PROPERTIES_FILE = 'Properties.json'
REPORT_DIRECTORY = 'reports'


def is_database(path, verbose=False):
	'''Returns true if the given directory contains a database

	Argument verbose controls logging to the command line about error info.
	'''
	abs_path = os.path.abspath(path)
	if not os.path.isdir(abs_path):
		if verbose:
			print('The directory ' + abs_path + ' does not exist')
		return False
	else:
		prop_file = os.path.join(abs_path, PROPERTIES_FILE)
		if not os.path.exists(prop_file):
			if verbose:
				print('The directory ' + abs_path + ' is not a database')
			return False
	return True


class Database:
	'''Manages persistence of the genetic algorithm's state.'''

	def __init__(self, directory):
		'''Creates or loads a database in the given directory

		The directory should not contain any other data than the database, as it may be deleted.
		'''
		self.directory = os.path.abspath(directory)
		self.log_file = None
		self.properties = {}
		self.selected = 0
		if not os.path.exists(self.directory):
			os.mkdir(self.directory)
			self._set_defaults()
			self._save_properties()
		else:
			self._load_properties()
		if not os.path.exists(os.path.join(self.directory, DATA_DIRECTORY)):
			os.mkdir(os.path.join(self.directory, DATA_DIRECTORY))
		if not os.path.exists(os.path.join(self.directory, LOG_DIRECTORY)):
			os.mkdir(os.path.join(self.directory, LOG_DIRECTORY))
		if not os.path.exists(os.path.join(self.directory, REPORT_DIRECTORY)):
			os.mkdir(os.path.join(self.directory, REPORT_DIRECTORY))

	def __del__(self):
		if self.log_file is not None:
			self.log_file.close()
			self.log_file = None

	def _save_properties(self):
		'''Saves the database properties to the PROPERTIES_FILE'''
		with open(os.path.join(self.directory, PROPERTIES_FILE), 'wt') as out_file:
			json.dump(self.properties, out_file, indent='\t', sort_keys=True)

	def _set_defaults(self):
		'''Sets the default properties for the database'''
		self.properties = {}
		self.properties['binary_length'] = 0
		self.properties['highest_population'] = 0
		self.properties['population_size'] = 0
		self.properties['no_objectives'] = 0
		self.properties['objective_names'] = None
		self._save_properties()

	def set_property(self, key, value):
		'''Sets the given propery, saving it immediately'''
		self.properties[key] = value
		self._save_properties()

	def _load_properties(self):
		'''Loads the database properties stored in the PROPERTIES_FILE'''
		with open(os.path.join(self.directory, PROPERTIES_FILE), 'rt') as in_file:
			self.properties = json.load(in_file)

	def create_population(self):
		'''Creates a new population after the last one and sets it as selected'''
		self.set_property('highest_population', self.properties['highest_population'] + 1)
		self.select()

	def load(self):
		'''Returns a dictionary of all elements in the selected population as binary strings'''
		id_path = os.path.join(self.directory, ID_PREFIX + str(self.selected))
		data_path = os.path.join(self.directory, DATA_DIRECTORY, str(self.selected))
		elements = {}
		with open(id_path, 'rt') as id_file, open(data_path, 'rb') as data_file:
			key_buffer = id_file.read().splitlines()
			for key in key_buffer:
				elements[key] = data_file.read(self.properties['binary_length'])
		return elements

	def load_report(self):
		'''Returns the report corresponding to the selected population'''
		path = os.path.join(self.directory, REPORT_DIRECTORY, str(self.selected) + '.json')
		with open(path, 'rt') as in_file:
			report = json.load(in_file)
		return report

	def log(self, string):
		'''Writes the given string to the current log file'''
		if self.log_file is not None:
			self.log_file = open(os.path.join(self.directory, LOG_DIRECTORY, str(self.selected) + '.log'))
		self.log_file.write(string)

	def reset(self):
		'''Deletes all data in the database and restores the properties to their default values'''
		shutil.rmtree(self.directory)
		os.mkdir(self.directory)
		self._set_defaults()
		self._save_properties()

	def save(self, elements):
		'''Saves the given dictionary of elements to the selected population file

		This operation overwrites any previous data in the file. All the elements in the list must be
		binary strings of the same length.
		'''
		id_path = os.path.join(self.directory, ID_PREFIX + str(self.selected))
		data_path = os.path.join(self.directory, DATA_DIRECTORY, str(self.selected))
		with open(id_path, 'wt') as id_file, open(data_path, 'wb') as data_file:
			for key, value in elements.items():
				self.properties['binary_length'] = len(value)
				id_file.write(key + '\n')
				data_file.write(value)
		self._save_properties()

	def save_report(self, report):
		'''Saves the given report

		The report must be a dictionary of dictionaries, where the keys are the identifiers of each of
		the individuals.
		'''
		path = os.path.join(self.directory, REPORT_DIRECTORY, str(self.selected) + '.json')
		with open(path, 'wt') as out_file:
			json.dump(report, out_file, indent='\t', sort_keys=True)

	def select(self, index=-1):
		'''Sets the given population as the one to load from and save to

		If given a -1, selects the highest population.
		'''
		if index > self.properties['highest_population']:
			raise IndexError('Given index is higher than max population.')
		if index < 0:
			index = self.properties['highest_population']
		self.selected = index
		if self.log_file is not None:
			self.log_file.close()
			self.log_file = None

	def set_objective_names(self, names):
		'''Sets the text to be used in graphs for each objective'''
		self.properties['objective_names'] = names
		self.properties['no_objectives'] = len(names)
		self._save_properties()
