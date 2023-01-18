#!/usr/bin/python
# coding: utf-8

import threading
from time import sleep
from smbus import SMBus
from ev3dev2.port import LegoPort
from ev3dev.auto import *
from pixy2 import (
    Pixy2,
    MainFeatures,
    STOP,
    SLOW_DOWN,
	FORBIDDEN,
	GOTTA_GO_FAST
    )
#----------Sensors init----------
#CAMERA Init
pixy2 = Pixy2()
data = MainFeatures()

#Motors
left_motor = LargeMotor(OUTPUT_D);  assert left_motor.connected
right_motor = LargeMotor(OUTPUT_A); assert right_motor.connected

#MUX Init
muxC1port = LegoPort("in1:i2c80:mux1")
muxC2port = LegoPort("in1:i2c81:mux2")
muxC3port = LegoPort("in1:i2c82:mux3")

muxC1port.set_device="lego-ev3-color"
muxC2port.set_device="lego-ev3-color"
muxC3port.set_device="lego-ev3-color"
sleep(1) # need to wait for sensors to be loaded. 0.5 seconds is not enough.

# Sensors
col_right = ColorSensor("in1:i2c80:mux1")
col= ColorSensor("in1:i2c81:mux2");		assert col.connected
col_left = ColorSensor("in1:i2c82:mux3")
ul = UltrasonicSensor(INPUT_3); assert ul.connected

# Change color sensor mode
col_right.mode = 'COL-REFLECT'
col.mode = 'COL-REFLECT'
col_left.mode = 'COL-REFLECT'

btn = Button()

#----------Settings----------
power = 30
movementPower = 55
target = 47
kp = float(0.80) # Proportional gain, Start value 1
ki = float(0.07) # Integral gain, Start value 0
kd = 0.46    # Derivative gain, Start value 0
direction = -1
minRef = 5 # Sensor min value 
maxRef = 70# Sensor max value
state = 0# switch index 
#-----------------------

#Thread function for camera panel (barcodes) reading
class CameraThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.currentPanel = None
        self.panelSaw = False
        self.stateIndex = 0
    
    def run(self):
        while True:
            data = pixy2.getdata()
            if data.error:
                self.currentPanel = ""
            else:
                self.panelSaw = True
                self.currentPanel = ""
                if data.number_of_barcodes > 0:
                    pixy2.lamp_on()
                    for i in range(0, data.number_of_barcodes):
                        if data.barcodes[i].code == STOP:
                            self.currentPanel = "STOP SIGN"
                            self.stateIndex = 1
                        elif data.barcodes[i].code == SLOW_DOWN:
                            self.currentPanel = "SLOW_DOWN"
                            self.stateIndex = 6
                        elif data.barcodes[i].code == FORBIDDEN:
                            self.currentPanel = "FORBIDDEN"
                            self.stateIndex = 2
                        elif data.barcodes[i].code == GOTTA_GO_FAST:
                             self.currentPanel = "GOTTA GO FAST"
                             self.stateIndex = 5
                        else :
                            self.stateIndex = 0
                    sleep(1)
                    pixy2.lamp_off()

                else:
                    self.currentPanel = 0
                    self.stateIndex = 0        
                data.clear()
                self.currentPanel = None


#Thread for ultrasonic sensor reading
class UltrasonicSensorThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.Correction = 0
    
    def run(self):
        while True:
            distance = ul.value()/10
            if distance < 20 and distance > 10 :
                self.Correction = -100 / distance
            elif distance <= 10 :
                self.Correction = - power
            else :
                self.Correction = 0

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


#----------Robot movements functions----------
def turnLeft():
    left_motor.duty_cycle_sp = movementPower
    right_motor.duty_cycle_sp = 0
    print("turnLeft Called")
    sleep(1)

def turnRight():
    left_motor.duty_cycle_sp = 0
    right_motor.duty_cycle_sp = movementPower
    print("turnRight Called")
    sleep(1)

def goForward(power):
    left_motor.duty_cycle_sp = power
    right_motor.duty_cycle_sp = power
    print("goForward Called")
    sleep(1)

def goBack():
    left_motor.duty_cycle_sp = movementPower
    right_motor.duty_cycle_sp = -movementPower
    print("goBack Called")
    sleep(1)

def stop():
    left_motor.duty_cycle_sp = 0
    right_motor.duty_cycle_sp = 0
    print("stop Called")
    sleep(3)

def increasePower():
    print("increasepower called")
    return 35

def decreasePower():
    print("decreasePower called")
    return 15