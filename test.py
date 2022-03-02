#!/usr/bin/env python3

from gpiozero import DigitalInputDevice as IN
from gpiozero import DigitalOutputDevice as OUT
#from signal import pause
import time

rows = [IN(13, pull_up=True)]
cols = [OUT(26)]
#buttons = [Button(26), Button(19), Button(6), Button(5)]
NULL_CHAR = chr(0)

def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())


def handle_press():

    write_report(chr(32)+NULL_CHAR+chr(11)+NULL_CHAR*5)
    # Release all keys
    write_report(NULL_CHAR*8)
    

"""
button.when_pressed = handle_press

pause()



Matrix Scanning: set cols to low and see if each row if low
if row low, key in row,col is pressed
"""

cols[0].on()
time.sleep(1)
cols
while True:

    
    cols[0].off()
    #print(rows[0].is_pressed)
    #time.sleep(1)

    #cols[0].off()
    print(rows[0].value)
    #time.sleep(1)

    

    #print("Value: ", rows[0].is_pressed)
    #print("\n")
    #print("-")
