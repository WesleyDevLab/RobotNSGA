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
	else:
		print('Unrecognized command')
