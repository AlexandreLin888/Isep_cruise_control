#!/usr/bin/ python3

from time   import sleep
from random import choice, randint

from ev3dev.auto import *

import time

muxC2port = LegoPort("in1:i2c81:mux2")
muxC2port.set_device="lego-ev3-color"
sleep(1) # need to wait for sensors to be loaded. 0.5 seconds is not enough.

cs= ColorSensor("in1:i2c81:mux2");		assert cs.connected

cs.mode = 'COL-REFLECT'


print("Started")

meanValue = cs.value()

while True:
    meanValue = (meanValue+cs.value())/2
    print(meanValue)
    print('\n')
    print(cs.value())
    sleep(1)
