#!/usr/bin/ python3

from time   import sleep
from random import choice, randint

from ev3dev2.motor import LargeMotor,OUTPUT_B, OUTPUT_A
from ev3dev2.sensor import INPUT_1,INPUT_2,INPUT_3,INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor
from ev3dev2.button import Button
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
import time

cs = ColorSensor(INPUT_3)

print("Started")

meanValue = cs.reflected_light_intensity

while True:
    meanValue = (meanValue+cs.reflected_light_intensity)/2
    print(meanValue)
    print('\n')
