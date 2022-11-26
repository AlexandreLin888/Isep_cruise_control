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


def main() :

    left_motor.run_direct()
    right_motor.run_direct()

    left_motor.duty_cycle_sp = power
    right_motor.duty_cycle_sp = power
    sleep(20)
    
    left_motor.stop()
    right_motor.stop()

main()

