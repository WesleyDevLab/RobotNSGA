'''Defines the Robot parent class'''


class Robot:
	'''Parent class for all robot classes to be used'''

	def connect(self):
		'''Must set the connection to the physical robot'''
		raise NotImplementedError("A robot class must implement the 'connect' method")

	def disconnect(self):
		'''Must end the connection established by the connect method'''
		raise NotImplementedError("A robot class must implement the 'disconnect' method")
