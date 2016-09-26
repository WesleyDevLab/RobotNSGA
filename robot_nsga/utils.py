'''Utility functions'''

import numpy as np

def save_data(genetic_algorithm, database):
	'''Saves relevant data after each iteration'''
	database.create_population()
	save_dict = {val.name: np.asarray(val).tobytes() for val in genetic_algorithm.population}
	database.save(save_dict)
