#!/usr/bin/python
# coding: utf-8

import threading
from time import sleep

from robot import *
from ev3dev.auto import *
from pixy2 import (
    Pixy2,
    MainFeatures,
    STOP,
    SLOW_DOWN,
	FORBIDDEN,
	GOTTA_GO_FAST
    )

#Speaker
speaker = Sound()
speaker.speak("Hellow")

#Threads
ul_sensor = UltrasonicSensorThread()
camera_Reading = CameraThread();


print("Hi ... \n")


#Main function
def main(power, target, kp, kd, ki, direction, minRef, maxRef):
	lastError = error = integral = 0
	left_motor.run_direct()
	right_motor.run_direct()	

	while not btn.any() :
		if btn.down: # User pressed the touch sensor
			print('Breaking loop')
			break

		val_left = col_left.value()
		val_right = col_right.value()

		#In case of crossroad
		if (val_left < 20) & (val_right < 20):
			turnLeft()
		#In case of interruption
		if (val_left > 70) & (val_right > 70) & (refRead > 70):
			print('Interruption')
			goForward(pow)

		state = camera_Reading.stateIndex

		if (state == 0):
			#Case 0 : PID computing
			refRead = col.value()

			error = target - (100 * ( refRead - minRef ) / ( maxRef - minRef ))
			derivative = error - lastError
			lastError = error
			integral = float(0.5) * integral + error
			course = (kp * error + kd * derivative +ki * integral) * direction

			for (motor, pow) in zip((left_motor, right_motor), steering(course, power,ul_sensor.Correction)):
				motor.duty_cycle_sp = pow
			sleep(0.01) # Aprox 100 Hz
		elif (state==1):
			#Case 1 : Stop sign
			stop()
			state = 0
		elif (state==2):
			#Case 2 : FORBBIDEN SIGN OR CROSSROAD
			turnLeft()
			state = 0
		elif (state==3):
			#Case 3 : FORBBIDEN SIGN OR CROSSROAD
			turnLeft()
			state = 0
		elif (state==4):
			#Case 4 : FORBBIDEN SIGN OR CROSSROAD
			turnRight()
			state = 0
		elif (state == 5):
			#Case 5 : GOTTA GO FAST SIGN
			increasePower()
			state = 0
		elif (state == 6):
			#Case 6 : SLOW DOWN SIGN 
			decreasePower()
			state = 0
			

#Thread starts
ul_sensor.start()
camera_Reading.start()

#Main function start
main(power, target, kp, kd, ki, direction, minRef, maxRef)

# Stop the motors before exiting.
print ('Stopping motors')
left_motor.stop()
right_motor.stop()