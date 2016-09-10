'''
Package metadata.
'''

from setuptools import setup
from setuptools import find_packages

setup(
	name='robot_nsga',
	description='Using genetic algorithms to evolve a neural network controller for a robot arm',
	author='Luis Lara',
	author_email='luislarap@outlook.com',
	packages=find_packages()
)
