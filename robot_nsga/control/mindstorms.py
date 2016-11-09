'''Defines the Mindstorms robot class'''

# pylint: disable = C0103

import math
from math import sin, cos

import bluetooth
import numpy as np

from . import robot

HEADER = b'\x01\x00\x81\x9E'
JOINT_LIMITS = [180, 120, 120]
PORT = 1
STALL_THRESHOLD = 1

class Mindstorms(robot.Robot):
	'''Robot class for LEGO Mindstorms(TM) robots'''

	def __init__(self):
		self.dof = 3
		self.server_socket = None
		self.client_socket = None
		self.joints = None
		self.last_joints = None

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

	def detect_soft_limits(self, signal):
		'''
		Returns a logical array indicating which joints are software limited, depending on the current
		robot position and the control signal provided.
		'''
		lower_bound = (np.asarray(self.joints) <= 0) & (signal < 0)
		upper_bound = (np.asarray(self.joints) >= np.array(JOINT_LIMITS)) & (signal > 0)
		return lower_bound | upper_bound

	def detect_stall(self):
		'''Returns True if the robot did not move since the last call'''
		if self.last_joints is None:
			self.last_joints = self.joints
			return False
		stall = True
		for last, curr in zip(self.last_joints, self.joints):
			if abs(last - curr) > STALL_THRESHOLD:
				stall = False
		self.last_joints = self.joints
		return stall

	def direct_kinematics(self):
		'''Returns the position of the robot's end effector'''
		q = [math.radians(x) for x in self.joints]
		r = -104 * cos(q[1]) + 123 * cos(q[1] - q[2]) + 8 * (7 + 5 * sin(q[1]) + 4 * sin(q[1] - q[2]))
		posx = cos(q[0]) * r
		posy = sin(q[0]) * r
		posz = 100 + 40 * cos(q[1]) + 32 * cos(q[1] - q[2]) + 104 * sin(q[1]) - 123 * sin(q[1] - q[2])
		return posx, posy, posz

	def disconnect(self):
		'''Disconnects the EV3 brick'''
		self._send_message('END', True)
		self.client_socket.close()
		self.server_socket.close()
		print('EV3 disconnected')

	def home(self):
		'''Returns the robot to the home position'''
		self._send_message('HOME', True)
		self._receive_message()

	def read_joints(self):
		'''Returns the positions of all joints'''
		self._send_message('READ', True)
		_, answer = self._receive_message()
		self.joints = [int(val) for val in answer.split(',')]
		return self.joints

	def reset(self):
		'''Resets the joint measurements to zero'''
		self._send_message('RESET', True)

	def set_motor(self, motor_number, power):
		'''Sends a 'M' command to the robot'''
		if 0 < motor_number <= self.dof:
			self._send_message('M' + str(motor_number), np.clip(power, -100, 100))
