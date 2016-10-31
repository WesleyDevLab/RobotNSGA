'''Defines the Robot parent class'''


class Robot:
	'''Parent class for all robot classes to be used'''

	def connect(self):
		'''Must set the connection to the physical robot'''
		raise NotImplementedError("A robot class must implement the 'connect' method")

	def direct_kinematics(self):
		'''Must return a tuple containing the position of the robot's end effector'''
		raise NotImplementedError("A robot class must implement the 'direct_kinematics' method")

	def disconnect(self):
		'''Must end the connection established by the connect method'''
		raise NotImplementedError("A robot class must implement the 'disconnect' method")

	def home(self):
		'''Must return the physical robot to its home position'''
		raise NotImplementedError("A robot class must implement the 'home' method")

	def read_joints(self):
		'''Must return an array with the current joint positions'''
		raise NotImplementedError("A robot class must implement the 'read_joints' method")

	def set_motor(self, motor_number, power):
		'''Must move the specified motor with the given power in the physical robot'''
		raise NotImplementedError("A robot class must implement the 'set_motor' method")
