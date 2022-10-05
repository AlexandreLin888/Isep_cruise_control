#!/usr/bin/ python3

from time   import sleep
from random import choice, randint

from ev3dev2.motor import LargeMotor,OUTPUT_B, OUTPUT_A
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.button import Button
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
import time

ts = TouchSensor(INPUT_1)
mRight = LargeMotor(OUTPUT_A)
mLeft = LargeMotor(OUTPUT_B)

print("Started")

while True:
    if ts.is_pressed:
        mRight.run_timed(time_sp=3000, speed_sp=500)
        mLeft.run_timed(time_sp=3000, speed_sp=500)