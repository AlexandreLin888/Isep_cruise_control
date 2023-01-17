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

from ev3dev.auto import *


#SOUND init
speaker = Sound()
speaker.speak("Hellow")

#CAMERA Init
pixy2 = Pixy2()
data = MainFeatures()

btn = Button()

while not btn.any() :
		if btn.down: # User pressed the touch sensor
			print('Breaking loop')
			break

		data = pixy2.getdata()
		if data.error:
			speaker.beep()
		else:
			if data.number_of_barcodes > 0:
				for i in range(0, data.number_of_barcodes):
					if data.barcodes[i].code == STOP:
						speaker.speak("STOP SIGN")
					elif data.barcodes[i].code == SLOW_DOWN:
						speaker.speak("SLOW_DOWN")
					elif data.barcodes[i].code == FORBIDDEN:
						speaker.speak("FORBIDDEN")
					elif data.barcodes[i].code == GOTTA_GO_FAST:
						speaker.speak("GOTTA GO FAST")