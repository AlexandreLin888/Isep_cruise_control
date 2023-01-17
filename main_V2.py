#!/usr/bin/python
# coding: utf-8

import threading
from time import sleep

from pixy2 import (
    Pixy2,
    MainFeatures,
    STOP,
    SLOW_DOWN,
	FORBIDDEN,
	GOTTA_GO_FAST
    )

from robot import *
from ev3dev.auto import *

# ------Input--------
power = 30
target = 43
kp = float(0.85) # Proportional gain, Start value 1
kd = float(0.46)          # Derivative gain, Start value 0
ki = float(0.15) # Integral gain, Start value 0
direction = 1 # Direction (-1 for black line on the left or 1 for black line on the right)
minRef = 11 # Sensor min value 
maxRef = 89 # Sensor max value 
# -------------------

EV3 = robot()

#Main function
def lineFollowing():

    EV3.Start()
    while not EV3.btn.any():
        if EV3.btn.down:
            print("Breaking loop")
            break
        EV3.run(power, target, kp, kd, ki, direction, minRef, maxRef)

    EV3.Stop()


lineFollowing()