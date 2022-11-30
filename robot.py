#!/usr/bin/python
# coding: utf-8

import threading
from time import sleep
from smbus import SMBus
from ev3dev2.port import LegoPort
from ev3dev.auto import *

class LineFollower:

    #Initialisation of the differents sensors and actuator
    def init(self):
        # ------Input--------
        self.power = 30
        self.target = 43
        self.kp = float(0.80) # Proportional gain, Start value 1
        self.kd = 0.46          # Derivative gain, Start value 0
        self.ki = float(0.07) # Integral gain, Start value 0
        self.direction = -1
        self.minRef = 11 # Sensor min value 
        self.maxRef = 89 # Sensor max value 
        # -------------------
        
        #Motors
        self.left_motor = LargeMotor(OUTPUT_D);  assert self.left_motor.connected
        self.right_motor = LargeMotor(OUTPUT_A); assert self.right_motor.connected

        # Sensors
        #MUX Init
        muxC1port = LegoPort("in1:i2c80:mux1")
        muxC1port.set_device="lego-ev3-us"
        sleep(1) # need to wait for sensors to be loaded. 0.5 seconds is not enough.

        ul = UltrasonicSensor("in1:i2c80:mux1"); assert ul.connected
        self.col= ColorSensor(INPUT_3);		assert self.col.connected
        self.col_left = ColorSensor(INPUT_2); assert self.col_left.connected
        self.col_right = ColorSensor(INPUT_4); assert self.col_right.connected
        self.ul = UltrasonicSensor(INPUT_1); assert ul.connected

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
    def readingSensors(self):
        distance = self.ul.value()/10
        if distance < 20 and distance > 10 :
            correction = -100 / distance
        elif distance <= 10 :
            correction = - self.power
        else :
            correction = 0
        
        correction = 0

        return correction

     #Function called to compute power for each motors
    def steering(self,course, power,correction):
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

    def run(self,power, target, kp, kd, ki, direction, minRef, maxRef,lastError,error,integral):

	    #PID computing
        self.ulCorrection = self.readingSensors()
        self.refRead = self.col.value()
        self.error = target - (100 * ( self.refRead - minRef ) / ( maxRef - minRef ))
        self.derivative = self.error - self.lastError
        self.lastError = self.error
        self.integral = float(0.5) * self.integral + self.error
        self.course = (kp * self.error + self.kd * self.derivative +self.ki * self.integral) * self.direction
        print(self.course)

        for (motor, pow) in zip((self.left_motor, self.right_motor), self.steering(self.course, self.power,self.ulCorrection)):
            motor.duty_cycle_sp = pow
            sleep(0.01) # Aprox 100 Hz

    #Simple line following
    def goStraight(self):
        self.run( self.power,self.target, self.kp, self.kd, self.ki, self.direction, self.minRef, self.maxRef,0,0,0)

    #Turn to the right
    def turnRight(self):
        self.run(self.power, self.target, self.kp, self.kd, self.ki, self.direction, self.minRef, self.maxRef,0,0,0)
    
        return 0

    #Turn to the right
    def turnLeft(self):
        return 0

    #Start the engine
    def Start(self):
        self.lastError = 0
        self.error = 0
        self.integral = 0
        self.left_motor.run_direct()
        self.right_motor.run_direct()
    
    #Stop the robot
    def Stop(self):   
        # Stop the motors before exiting.
        print ('Stopping motors')
        self.left_motor.stop()
        self.right_motor.stop()