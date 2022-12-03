from time import sleep

from ev3dev.auto import *
#BUTTON Init
btn = Button()

#SENSORS Init
col_left = ColorSensor(INPUT_2)
col_right = ColorSensor(INPUT_4)

#SOUND Init
speaker = Sound()

while not btn.any() :
    if btn.down: # User pressed the touch sensor
        print('Breaking loop')
        break
    
    #Reading sensors for crossroad detection
    val_left = col_left.value()
    val_right = col_right.value()

    print('LEFT : ' + str(val_left) + ' RIGHT : '+str(val_right))
    if (val_left < 10) & (val_right < 10):
        speaker.speak("Crossroad")
    sleep(1)