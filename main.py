#!/usr/bin/python
# coding: utf-8

import threading
from time import sleep

from ev3dev.auto import *

# ------Input--------
power = 30
target = 43
kp = float(0.8) # Proportional gain, Start value 1
kd = float(0.46)          # Derivative gain, Start value 0
ki = float(0.07) # Integral gain, Start value 0
direction = 1
minRef = 11 # Sensor min value 
maxRef = 89 # Sensor max value 
# -------------------

#SOUND init
speaker = Sound()
speaker.speak("Hellow")

HOLE = False

#MUX Init
muxC1port = LegoPort("in1:i2c80:mux1")
muxC1port.set_device="lego-ev3-us"
sleep(1) # need to wait for sensors to be loaded. 0.5 seconds is not enough.

ul = UltrasonicSensor("in1:i2c80:mux1"); assert ul.connected

# Sensors
col= ColorSensor(INPUT_3);		assert col.connected
col_left = ColorSensor(INPUT_2)
col_right = ColorSensor(INPUT_4)

# Change color sensor mode
col.mode = 'COL-REFLECT'

btn = Button()

#Global values
ulCorrection = 0
turnRight = False
turnLeft = False

#Motors
left_motor = LargeMotor(OUTPUT_D);  assert left_motor.connected
right_motor = LargeMotor(OUTPUT_A); assert right_motor.connected



#Function for ultrasonic sensor
def readingSensors():
	distance = ul.value()/10
	#Computing a correction depending on the measured distance
	if distance < 20 and distance > 10 :
		correction = -100 / distance
	elif distance <= 10 :
		correction = - power
	else :
		correction = 0
	return correction

#Function called to compute power for each motors
def steering(course, power,correction):
	power_left = power_right = power + correction
	s = (50 - abs(float(course))) / 50

	if course >= 0:
		power_right *= s
		if course > 100:
			power_right = - power
	else:
		power_left *= s
		if course < -100:
			power_left = - power

	return (int(power_left), int(power_right))

#Main function
def run(power, target, kp, kd, ki, direction, minRef, maxRef):
	lastError = error = integral = 0
	left_motor.run_direct()
	right_motor.run_direct()

	#thread = threading(readingSensors)


	while not btn.any() :
		if btn.down: # User pressed the touch sensor
			print('Breaking loop')
			break

		
		ulCorrection = readingSensors()
		#Reading sensors for crossroad & interruption detection
		refRead = col.value()
		val_left = col_left.value()
		val_right = col_right.value()

			

		print('LEFT : ' + str(val_left) + ' RIGHT : '+str(val_right))
		if (val_left < 20) & (val_right < 20):
			if kp == float(1.2) :
				kp = float(0.8)
			elif kp == float(0.8) :
				kp = float(1.2)
			turnLeft(kp)

		#PID computing
		if (val_left > 55) & (val_right > 55) & (refRead > 55):
			straightForward(pow)
		else:
			error = target - (100 * ( refRead - minRef ) / ( maxRef - minRef ))
			derivative = error - lastError
			lastError = error
			integral = float(0.5) * integral + error
			course = (kp * error + kd * derivative +ki * integral) * direction
			
			for (motor, pow) in zip((left_motor, right_motor), steering(course, power,ulCorrection)):
				motor.duty_cycle_sp = pow

		sleep(0.01) # Aprox 100 Hz

def turnLeft(kp):
	speaker.speak("CROSSROAD " + str(kp))
	left_motor.duty_cycle_sp = 60
	right_motor.duty_cycle_sp = 0
	sleep(1)

def turnRight():
	speaker.speak("CROSSROAD!")
	left_motor.duty_cycle_sp = 0
	right_motor.duty_cycle_sp = 60
	sleep(1)

def straightForward(pow):
	left_motor.duty_cycle_sp = pow
	right_motor.duty_cycle_sp = pow
	sleep(1)


run(power, target, kp, kd, ki, direction, minRef, maxRef)

# Stop the motors before exiting.
print ('Stopping motors')
left_motor.stop()
right_motor.stop()
