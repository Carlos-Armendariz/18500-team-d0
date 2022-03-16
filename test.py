#!/usr/bin/env python3

from gpiozero import DigitalInputDevice as IN
from gpiozero import DigitalOutputDevice as OUT
#from signal import pause
import time

rows = [IN(6, pull_up=True), IN(5, pull_up=True)]
cols = [OUT(26), OUT(19)]
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
if row low, key in (row,col) is pressed
"""

def main():
    for col in cols:
        col.on()
    #time.sleep(1)

    #prev = [[1,1], [1,1]]

    while True:
        time.sleep(0.5)
        for i, col in enumerate(cols):
            col.off()
            #print("col: ", i)
            for j, row in enumerate(rows):
                #print("row: {}, col: {} val: {}".format(j, i, row.value))
                if (row.value):
                    handle_press()

            col.on()

        #print("----------")

main()
