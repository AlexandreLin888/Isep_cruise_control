from time import sleep

from ev3dev.auto import *
#BUTTON Init
btn = Button()

#SENSORS Init
col_left = ColorSensor(INPUT_2)
col_center = ColorSensor(INPUT_3)
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
    val_center = col_center.value()

    print('LEFT : ' + str(val_left)+'CENTER'+str(val_center) + ' RIGHT : '+str(val_right))
    if (val_left > 55) & (val_right > 55) & (val_center > 55):
        speaker.speak("Interruption")
    sleep(1)