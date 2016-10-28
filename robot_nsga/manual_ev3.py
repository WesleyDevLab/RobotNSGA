'''Script for manually controlling the EV3 robot'''

import control

ev3 = control.Mindstorms()
ev3.connect()

while True:
	command, *value = input().split(' ', maxsplit=1)
	command = command.upper()
	if command == 'END':
		ev3.disconnect()
		break
	elif command == 'HOME':
		ev3.home()
	elif command == 'M1':
		ev3.set_motor(1, float(value[0]))
	elif command == 'M2':
		ev3.set_motor(2, float(value[0]))
	elif command == 'M3':
		ev3.set_motor(3, float(value[0]))
	elif command == 'S1':
		ev3._send_message('S1', float(value[0]))
	elif command == 'S2':
		ev3._send_message('S2', float(value[0]))
	elif command == 'S3':
		ev3._send_message('S3', float(value[0]))
	elif command == 'READ':
		print(ev3.read_joints())
	elif command == 'RESET':
		ev3.reset()
	else:
		print('Unrecognized command')
