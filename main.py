#!/usr/bin/python
# coding: utf-8

import threading
from time import sleep

from ev3dev.auto import *

# ------Input--------
power = 30
target = 43
kp = float(0.47) # Proportional gain, Start value 1
kd = 0.46          # Derivative gain, Start value 0
ki = float(0.07) # Integral gain, Start value 0
direction = 1
minRef = 11 # Sensor min value 
maxRef = 89 # Sensor max value 
# -------------------

#Motors
left_motor = LargeMotor(OUTPUT_B);  assert left_motor.connected
right_motor = LargeMotor(OUTPUT_A); assert right_motor.connected

# Sensors
ts = TouchSensor();   	assert ts.connected
col= ColorSensor();		assert col.connected
ul = UltrasonicSensor(); assert ul.connected

# Change color sensor mode
col.mode = 'COL-REFLECT'

btn = Button()

#Global values
ulCorrection = 0
turnRight = False
turnLeft = False

print("Hi ... \n")

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
		if ts.value(): # User pressed the touch sensor
			print('Breaking loop')
			break
		
		#thread.start()
		#PID computing
		ulCorrection = readingSensors()
		refRead = col.value()
		#print(refRead)
		#print("\n")
		
		error = target - (100 * ( refRead - minRef ) / ( maxRef - minRef ))
		derivative = error - lastError
		lastError = error
		integral = float(0.5) * integral + error
		course = (kp * error + kd * derivative +ki * integral) * direction
		

		for (motor, pow) in zip((left_motor, right_motor), steering(course, power,ulCorrection)):
			motor.duty_cycle_sp = pow

		sleep(0.01) # Aprox 100 Hz

run(power, target, kp, kd, ki, direction, minRef, maxRef)

# Stop the motors before exiting.
print ('Stopping motors')
left_motor.stop()
right_motor.stop()