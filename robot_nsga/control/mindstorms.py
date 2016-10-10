'''Defines the Mindstorms robot class'''


import bluetooth

from . import robot

PORT = 1

class Mindstorms(robot.Robot):
	'''Robot class for LEGO Mindstorms(TM) robots'''

	def __init__(self):
		self.server_socket = None
		self.client_socket = None

	def connect(self):
		'''Connects to an EV3 brick via Bluetooth'''
		self.server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		self.server_socket.bind(('', PORT))
		self.server_socket.listen(1)
		print('Waiting for EV3 to connect')
		self.client_socket, _ = self.server_socket.accept()
		print('EV3 connected')

	def disconnect(self):
		'''Disconnects the EV3 brick'''
		self.client_socket.close()
		self.server_socket.close()
