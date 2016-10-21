'''Defines the Mindstorms robot class'''


import bluetooth

import numpy as np

from . import robot

HEADER = b'\x01\x00\x81\x9E'
PORT = 1

class Mindstorms(robot.Robot):
	'''Robot class for LEGO Mindstorms(TM) robots'''

	def __init__(self):
		self.dof = 3
		self.server_socket = None
		self.client_socket = None

	def _receive_message(self):
		'''Waits for an incoming message and returns the title and the content of the received message'''
		data = self.client_socket.recv(1024)
		data = data[6:]
		title_length = np.fromstring(data, count=1, dtype=np.int8)[0]
		title = data[1 : title_length].decode('ascii')
		data = data[title_length + 1:]
		message_length = np.fromstring(data, count=1, dtype=np.int16)[0]
		message = data[2 : message_length + 1].decode('ascii')
		return title, message

	def _send_message(self, command, value):
		'''Sends a command to the robot'''
		message = HEADER + np.int8(len(command) + 1).tobytes() + \
			bytes(command, 'ascii') + b'\x00'
		if isinstance(value, bool):
			message += np.int16(1).tobytes()
			if value:
				message += b'\x01'
			else:
				message += b'\x00'
		elif isinstance(value, int) or isinstance(value, float):
			message += np.int16(4).tobytes() + np.float32(value).tobytes()
		elif isinstance(value, str):
			message += np.int16(len(value) + 1).tobytes() + bytes(value, 'ascii') + b'\x00'
		message = np.int16(len(message)).tobytes() + message
		self.client_socket.send(message)

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
		self._send_message('END', True)
		self.client_socket.close()
		self.server_socket.close()
		print('EV3 disconnected')

	def home(self):
		'''Returns the robot to the home position'''
		self._send_message('HOME', True)

	def set_motor(self, motor_number, power):
		'''Sends a 'M' command to the robot'''
		if 0 < motor_number <= self.dof:
			self._send_message('M' + str(motor_number), np.clip(power, -100, 100))
