#!/usr/bin/python
# coding: utf-8

import threading
from time import sleep
from smbus import SMBus
from ev3dev2.port import LegoPort
from ev3dev.auto import *

class LineFollower:
    def _init_(self):
        # ------Input--------
        self.power = 30
        self.target = 43
        self.kp = float(0.47) # Proportional gain, Start value 1
        self.kd = 0.46          # Derivative gain, Start value 0
        self.ki = float(0.07) # Integral gain, Start value 0
        self.self.self.direction = -1
        self.minRef = 11 # Sensor min value 
        self.maxRef = 89 # Sensor max value 
        # -------------------
        #Motors
        self.left_motor = LargeMotor(OUTPUT_B);  assert left_motor.connected
        self.right_motor = LargeMotor(OUTPUT_A); assert right_motor.connected

        # Sensors
        self.col= ColorSensor(INPUT_3);		assert col.connected
        self.col_left = ColorSensor(INPUT_2); assert col_left.connected
        self.col_right = ColorSensor(INPUT_4); assert col_right.connected
        self.ul = UltrasonicSensor(INPUT_1); #assert ul.connected

        # Change color sensor mode
        self.col.mode = 'COL-REFLECT'
        self.col_left.mode = 'COL-REFLECT'
        self.col_right.mode = 'COL-REFLECT'

        #Global values
        self.ulCorrection = 0
        self.turnRight = False
        self.turnLeft = False

        print("Hi ... \n")       


     #Function for ultrasonic sensor
    def readingSensors():
        distance = ul.value()/10
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

    def run(power, target, kp, kd, ki, direction, minRef, maxRef):
        lastError = error = integral = 0
        left_motor.run_direct()
        right_motor.run_direct()
    
	    #PID computing
        ulCorrection = readingSensors()
        refRead = col.value()
        error = target - (100 * ( refRead - minRef ) / ( maxRef - minRef ))
        derivative = error - lastError
        lastError = error
        integral = float(0.5) * integral + error
        course = (kp * error + kd * derivative +ki * integral) * direction
		

        for (motor, pow) in zip((left_motor, right_motor), steering(course, power,ulCorrection)):
            motor.duty_cycle_sp = pow
            sleep(0.01) # Aprox 100 Hz

def goStraight(self):
    run(self.power, self.target, self.kp, self.kd, self.ki, self.direction, self.minRef, self.maxRef)

def turnRight(self):
    return 0

def turnLeft(self):
    return 0

def stop():   
    # Stop the motors before exiting.
    print ('Stopping motors')
    left_motor.stop()
    right_motor.stop()