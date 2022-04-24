#!/usr/bin/env python3

from turtle import begin_fill
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

L_CLICK_IDX = (2,0)
R_CLICK_IDX = (1,0)
SHIFT_KEY_IDX = (3,7)

def write_report(device, report):
    filepath = '/dev/hidg{}'.format(device)
    try:
        with open(filepath, 'rb+') as fd:
            fd.write(report.encode())
    except:
        print("Failed to open ", filepath)

def send_report(seen, prevSeen, shiftPressed):
    char_dict = create_chardict()
    if (shiftPressed):
        eyboard_report = chr(32) + NULL_CHAR
    else:
        keyboard_report = chr(0) + NULL_CHAR

    l_click_pressed = False
    r_click_pressed = False
    for pair in seen:
        prevSeen.add(pair)
        curr_char = char_dict[pair]
        if (pair == L_CLICK_IDX):
            l_click_pressed = True
        elif (pair == R_CLICK_IDX):
            r_click_pressed = True
        else:
            if (len(keyboard_report) < KEYBOARD_REPORT_LEN and curr_char != Keycodes.NULL):
                keyboard_report += chr(curr_char)

    while len(keyboard_report) < KEYBOARD_REPORT_LEN:
        keyboard_report += NULL_CHAR

    write_report(KEYBOARD_DEVICE_NUM, keyboard_report)

    if (l_click_pressed and r_click_pressed):
        mouse_report = chr(0x3) + (NULL_CHAR*2)
    elif (l_click_pressed):
        mouse_report = chr(0x1) + (NULL_CHAR*2)
    elif (r_click_pressed):
        mouse_report = chr(0x2) + (NULL_CHAR*2)
    else:
        mouse_report = NULL_CHAR * MOUSE_REPORT_LEN

    write_report(MOUSE_DEVICE_NUM, mouse_report)


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
    prevSeen = set()
    while True:
        #time.sleep(0.001)
        seen = set()
        shiftPressed = False
        for i, col in enumerate(cols):
            col.off()
            for j, row in enumerate(rows):
                if (row.value):
                    if (j,i) == SHIFT_KEY_IDX:
                        shiftPressed = True
                    else:
                        seen.add((j,i))
                elif (j,i) in prevSeen:
                    prevSeen.remove((j,i))
                    if (j,i) == R_CLICK_IDX or (j,i) == L_CLICK_IDX:
                        release_mouse()
                    else:
                        release_key()

            col.on()
            time.sleep(0.001)
   
        if len(seen) > 0:
            send_report(seen, prevSeen, shiftPressed)


def create_chardict():
    char_dict = dict()
    char_dict[(0,0)] = Keycodes.NULL #does not exist
    char_dict[(0,1)] = Keycodes.Q
    char_dict[(0,2)] = Keycodes.J
    char_dict[(0,3)] = Keycodes.L
    char_dict[(0,4)] = Keycodes.M
    char_dict[(0,5)] = Keycodes.F
    char_dict[(0,6)] = Keycodes.P
    char_dict[(0,7)] = Keycodes.ESC

    char_dict[R_CLICK_IDX] = Keycodes.NULL # RIGHT CLICK
    char_dict[(1,1)] = Keycodes.Z
    char_dict[(1,2)] = Keycodes.O
    char_dict[(1,3)] = Keycodes.R
    char_dict[(1,4)] = Keycodes.S # 7
    char_dict[(1,5)] = Keycodes.U # 8
    char_dict[(1,6)] = Keycodes.Y # 9
    char_dict[(1,7)] = Keycodes.BKSPC

    char_dict[L_CLICK_IDX] = Keycodes.NULL # LEFT CLICK
    char_dict[(2,1)] = Keycodes.A
    char_dict[(2,2)] = Keycodes.E
    char_dict[(2,3)] = Keycodes.H
    char_dict[(2,4)] = Keycodes.T #4
    char_dict[(2,5)] = Keycodes.D #5
    char_dict[(2,6)] = Keycodes.B #5
    char_dict[(2,7)] = Keycodes.ENTER

    char_dict[(3,0)] = Keycodes.SPACE
    char_dict[(3,1)] = Keycodes.X
    char_dict[(3,2)] = Keycodes.I
    char_dict[(3,3)] = Keycodes.N
    char_dict[(3,4)] = Keycodes.C # 1
    char_dict[(3,5)] = Keycodes.K # 2
    char_dict[(3,6)] = Keycodes.G # 3
    char_dict[(3,7)] = Keycodes.NULL # SHIFT

    char_dict[(4,0)] = Keycodes.PERIOD
    char_dict[(4,1)] = Keycodes.NULL # ! and ? are shift+1 and shift+/
    char_dict[(4,2)] = Keycodes.L_BRACK
    char_dict[(4,3)] = Keycodes.R_BRACK
    char_dict[(4,4)] = Keycodes.SEMICOLON # SEMICOLON
    char_dict[(4,5)] = Keycodes.W # 0
    char_dict[(4,6)] = Keycodes.V
    char_dict[(4,7)] = Keycodes.NULL # NUM LOCK

    char_dict[(5,0)] = Keycodes.APOSTROPHE   # APOSTROPHE/QUOTES
    char_dict[(5,1)] = Keycodes.J   # does not exist
    char_dict[(5,2)] = Keycodes.K   # does not exist
    char_dict[(5,3)] = Keycodes.L   # does not exist
    char_dict[(5,4)] = Keycodes.M   # does not exist
    char_dict[(5,5)] = Keycodes.N   # alt
    char_dict[(5,6)] = Keycodes.ONE   # CTRL
    char_dict[(5,7)] = Keycodes.P # TOGGLE KEY

    return char_dict



def main():

    rows = [IN(2, pull_up=True), IN(3, pull_up=True), IN(4, pull_up=True), 
            IN(17, pull_up=True),  IN(27, pull_up=True),  IN(22, pull_up=True)]
    
    cols = [OUT(9), OUT(11), OUT(0), OUT(5),
            OUT(6), OUT(13), OUT(19), OUT(26)]

    scan_matrix(rows, cols)

if __name__ == "__main__":
    main()
