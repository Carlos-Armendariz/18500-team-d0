#!/usr/bin/env python3

from gpiozero import DigitalInputDevice as IN
from gpiozero import DigitalOutputDevice as OUT
import time
from keycodes import Keycodes

NULL_CHAR = chr(0)

KEYBOARD_DEVICE_NUM = 0
KEYBOARD_REPORT_LEN = 8

MOUSE_DEVICE_NUM = 1
MOUSE_REPORT_LEN = 3

CURR_DEVICE = KEYBOARD_DEVICE_NUM

def write_report(device, report):
    filepath = '/dev/hidg{}'.format(device)
    # print("Writing report")
    try:
        with open(filepath, 'rb+') as fd:
            fd.write(report.encode())
    except:
        print("Failed to open ", filepath)

# clear UDC to unbind
# need to save name of UDC so that new device can have it written to UDC file
def send_report(device, seen, prevSeen):
    max_len = 0
    if (device == MOUSE_DEVICE_NUM):
        max_len = MOUSE_REPORT_LEN
    elif (device == KEYBOARD_DEVICE_NUM):
        max_len = KEYBOARD_REPORT_LEN

    char_dict = create_chardict()

    if (device == MOUSE_DEVICE_NUM):
        curr_report = chr(32) + NULL_CHAR
    else:
        curr_report = chr(0) + NULL_CHAR
        
    for pair in seen:
        prevSeen.add(pair)
        if (len(curr_report) < max_len):
            curr_report += chr(char_dict[pair])

    while len(curr_report) < max_len:
        curr_report += NULL_CHAR
     
    write_report(device, curr_report)


def release_key():
    write_report(KEYBOARD_DEVICE_NUM, NULL_CHAR*KEYBOARD_REPORT_LEN)

def release_mouse():
    write_report(MOUSE_DEVICE_NUM, NULL_CHAR*MOUSE_REPORT_LEN)

"""
Matrix Scanning: set cols to low and see if each row if low
if row low, key in (row,col) is pressed
"""
def scan_matrix(rows, cols):
 
    for col in cols:
        col.on()

    print("Running matrix scanning")
    keyboard_prevSeen = set()
    mouse_prevSeen = set()
    while True:
        #time.sleep(0.001)
        keyboard_seen = set()
        mouse_seen = set()
        for i, col in enumerate(cols):
            col.off()
            for j, row in enumerate(rows): 
                if (row.value):
                    keyboard_seen.add((j,i))
                    # print("SAW KEY")
                elif (j,i) in keyboard_prevSeen:
                    keyboard_prevSeen.remove((j,i))
                    release_key()

            col.on()
            time.sleep(0.001)
   
        if len(keyboard_seen) > 0:
            send_report(KEYBOARD_DEVICE_NUM, keyboard_seen, keyboard_prevSeen)
        
        # if len(mouse_seen) > 0:
        #     send_report(MOUSE_DEVICE_NUM, mouse_seen, mouse_prevSeen)

def main():

    rows = [IN(2, pull_up=True), IN(3, pull_up=True), IN(4, pull_up=True), 
            IN(17, pull_up=True),  IN(27, pull_up=True),  IN(22, pull_up=True)]
    
    cols = [OUT(9), OUT(11), OUT(0), OUT(5),
            OUT(6), OUT(13), OUT(19), OUT(26)]

    scan_matrix(rows, cols)


def create_chardict():
    char_dict = dict()
    char_dict[(0,0)] = Keycodes.NULL #does not exist
    char_dict[(0,1)] = Keycodes.NULL # left click
    char_dict[(0,2)] = Keycodes.C
    char_dict[(0,3)] = Keycodes.D
    char_dict[(0,4)] = Keycodes.E
    char_dict[(0,5)] = Keycodes.F
    char_dict[(0,6)] = Keycodes.G
    char_dict[(0,7)] = Keycodes.H # ESCAPE KEY

    char_dict[(1,0)] = Keycodes.I
    char_dict[(1,1)] = Keycodes.J
    char_dict[(1,2)] = Keycodes.K
    char_dict[(1,3)] = Keycodes.L
    char_dict[(1,4)] = Keycodes.M
    char_dict[(1,5)] = Keycodes.N
    char_dict[(1,6)] = Keycodes.O
    char_dict[(1,7)] = Keycodes.P

    char_dict[(2,0)] = Keycodes.Q
    char_dict[(2,1)] = Keycodes.R
    char_dict[(2,2)] = Keycodes.S
    char_dict[(2,3)] = Keycodes.T
    char_dict[(2,4)] = Keycodes.U
    char_dict[(2,5)] = Keycodes.V
    char_dict[(2,6)] = Keycodes.W
    char_dict[(2,7)] = Keycodes.X

    char_dict[(3,0)] = Keycodes.Y
    char_dict[(3,1)] = Keycodes.Z
    char_dict[(3,2)] = Keycodes.ONE
    char_dict[(3,3)] = Keycodes.TWO
    char_dict[(3,4)] = Keycodes.THREE
    char_dict[(3,5)] = Keycodes.FOUR
    char_dict[(3,6)] = Keycodes.FIVE
    char_dict[(3,7)] = Keycodes.SIX

    char_dict[(4,0)] = Keycodes.SEVEN
    char_dict[(4,1)] = Keycodes.EIGHT
    char_dict[(4,2)] = Keycodes.NINE
    char_dict[(4,3)] = Keycodes.ZERO
    char_dict[(4,4)] = Keycodes.ENTER
    char_dict[(4,5)] = Keycodes.ESC
    char_dict[(4,6)] = Keycodes.BKSPC
    char_dict[(4,7)] = Keycodes.TAB

    char_dict[(5,0)] = Keycodes.SPACE
    char_dict[(5,1)] = Keycodes.NULL   # does not exist
    char_dict[(5,2)] = Keycodes.NULL   # does not exist
    char_dict[(5,3)] = Keycodes.NULL   # does not exist
    char_dict[(5,4)] = Keycodes.NULL   # does not exist
    char_dict[(5,5)] = Keycodes.E   # does not exist
    char_dict[(5,6)] = Keycodes.F
    char_dict[(5,7)] = Keycodes.G # TOGGLE KEY

    return char_dict


if __name__ == "__main__":
    main()
