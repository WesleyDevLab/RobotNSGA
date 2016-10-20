'''Script for manually controlling the EV3 robot'''

import time

import control

ev3 = control.Mindstorms()
ev3.connect()
time.sleep(1)
ev3.disconnect()
