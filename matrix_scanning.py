#!/usr/bin/env python3

from gpiozero import DigitalInputDevice as IN
from gpiozero import DigitalOutputDevice as OUT

#import usb_hid
#from adafruit_hid.keyboard import Keyboard
#from adafruit_hid.mouse import Mouse

import time
from keycodes import Keycodes

NULL_CHAR = chr(0)
#m = Mouse(usb_hid.devices)
def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())


# clear UDC to unbind
# need to save name of UDC so that new device can have it written to UDC file

def send_mouse_report(seen, prevSeen):

    char_dict = create_chardict()
    curr_report = chr(32) + NULL_CHAR

    for pair in seen:
        if pair not in prevSeen:
            prevSeen.add(pair)
        if (pair) == (0,0):
            curr_report += chr(0x4) # LEFT CLICK

    while len(curr_report) < 3:
        curr_report = NULL_CHAR + curr_report
     
    write_report(curr_report)


def send_keyboard_report(seen, prevSeen):

    char_dict = create_chardict()
    curr_report = chr(32) + NULL_CHAR

    for pair in seen:
        if pair not in prevSeen:
            prevSeen.add(pair)
        
        curr_report += chr(char_dict[pair])

    while len(curr_report) < 8:
        curr_report += NULL_CHAR
     
    write_report(curr_report)


def release_key():
    write_report(NULL_CHAR*8)
    

def create_chardict():
    char_dict = dict()
    char_dict[(0,0)] = Keycodes.W
    char_dict[(0,1)] = Keycodes.A
    char_dict[(1,0)] = Keycodes.S
    char_dict[(1,1)] = Keycodes.D


    return char_dict

"""
Matrix Scanning: set cols to low and see if each row if low
if row low, key in (row,col) is pressed
"""
def scan_matrix(rows, cols):
 
    for col in cols:
        col.on()

    prevSeen = set()
    print("Running matrix scanning")
    while True:
        #time.sleep(0.001)
        seen = set()
        for i, col in enumerate(cols):
            col.off()
            for j, row in enumerate(rows): 
                if (row.value):
                    seen.add((j,i))
                    
                elif (j,i) in prevSeen:
                    prevSeen.remove((j,i))
                    release_key()

            col.on()
            time.sleep(0.001)
   
        if len(seen) > 0:
            print_val = ""
            #send_mouse_report(seen, prevSeen)
            send_keyboard_report(seen, prevSeen)


def main():

    rows = [IN(5, pull_up=True), IN(6, pull_up=True)]
    cols = [OUT(14), OUT(15)]

    scan_matrix(rows, cols)



if __name__ == "__main__":
    main()
