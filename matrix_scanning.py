#!/usr/bin/env python3

from ssl import ALERT_DESCRIPTION_PROTOCOL_VERSION
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

R_CLICK_IDX = (1,0)
L_CLICK_IDX = (2,0)
SHIFT_KEY_IDX = (3,7)
NUM_LOCK_IDX = (4,7)
ALT_IDX = (5,5)
CTRL_IDX = (5,6)
TOGGLE_IDX = (5,7)


#TOGGLE VALUES
NUM_LOCK = False

def write_report(device, report):
    filepath = '/dev/hidg{}'.format(device)
    try:
        with open(filepath, 'rb+') as fd:
            fd.write(report.encode())
    except:
        print("Failed to open ", filepath)

def send_report(char_dict, alt_char_dict, alt_num_dict, seen, prevSeen, shiftPressed, ctrlPressed, altPressed):

    modifier_byte = get_modifer_byte(shiftPressed, ctrlPressed, altPressed)
    keyboard_report = modifier_byte + NULL_CHAR

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
                if shiftPressed and pair in alt_char_dict.keys(): # shift is pressed
                    keyboard_report += chr(alt_char_dict[pair])
                elif NUM_LOCK and pair in alt_num_dict.keys():
                    keyboard_report += chr(alt_num_dict[pair])
                else:
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

def get_modifer_byte(shiftPressed, ctrlPressed, altPressed):
    modifier_byte = 0x0
    if (shiftPressed):
        modifier_byte |= 0x2
    if (ctrlPressed):
        modifier_byte |= 0x1
    if (altPressed):
        modifier_byte |= 0x4
    return chr(modifier_byte)

"""
Matrix Scanning: set cols to low and see if each row if low
if row low, key in (row,col) is pressed
"""
def scan_matrix(rows, cols):
    
    for col in cols:
        col.on()

    print("Running matrix scanning")
    char_dict = create_chardict()
    alt_char_dict = create_alt_chardict()
    alt_num_dict = create_alt_numdict()
    prevSeen = set()
    while True:
        #time.sleep(0.001)
        seen = set()
        shiftPressed = False
        ctrlPressed = False
        altPressed = False
        for i, col in enumerate(cols):
            col.off()
            for j, row in enumerate(rows):
                if (row.value):
                    if (j,i) == SHIFT_KEY_IDX:
                        shiftPressed = True
                    elif (j,i) == CTRL_IDX:
                        ctrlPressed = True
                    elif (j,i) == ALT_IDX:
                        altPressed = True
                    seen.add((j,i))

                elif (j,i) in prevSeen:
                    prevSeen.remove((j,i))
                    if (j,i) == R_CLICK_IDX or (j,i) == L_CLICK_IDX:
                        release_mouse()
                    else:
                        if (j,i) == NUM_LOCK_IDX:
                            global NUM_LOCK
                            NUM_LOCK = not NUM_LOCK # toggle NUM_LOCK on key release
                        
                        release_key()

            col.on()
            time.sleep(0.001)

        # modifier_byte = get_modifer_byte(shiftPressed, ctrlPressed, altPressed)
        if len(seen) > 0:
            send_report(char_dict, alt_char_dict, alt_num_dict, seen, prevSeen, shiftPressed, ctrlPressed, altPressed)


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
    char_dict[(2,6)] = Keycodes.B #6
    char_dict[(2,7)] = Keycodes.ENTER

    char_dict[(3,0)] = Keycodes.SPACE
    char_dict[(3,1)] = Keycodes.X
    char_dict[(3,2)] = Keycodes.I
    char_dict[(3,3)] = Keycodes.N
    char_dict[(3,4)] = Keycodes.C # 1
    char_dict[(3,5)] = Keycodes.K # 2
    char_dict[(3,6)] = Keycodes.G # 3
    char_dict[SHIFT_KEY_IDX] = Keycodes.L_SHIFT # SHIFT

    char_dict[(4,0)] = Keycodes.PERIOD
    char_dict[(4,1)] = Keycodes.NULL # ! and ? are shift+1 and shift+/
    char_dict[(4,2)] = Keycodes.L_BRACK
    char_dict[(4,3)] = Keycodes.R_BRACK
    char_dict[(4,4)] = Keycodes.SEMICOLON
    char_dict[(4,5)] = Keycodes.W # 0
    char_dict[(4,6)] = Keycodes.V
    char_dict[NUM_LOCK_IDX] = Keycodes.NULL # NUM LOCK

    char_dict[(5,0)] = Keycodes.APOSTROPHE   # APOSTROPHE/QUOTES
    char_dict[(5,1)] = Keycodes.J   # does not exist
    char_dict[(5,2)] = Keycodes.K   # does not exist
    char_dict[(5,3)] = Keycodes.L   # does not exist
    char_dict[(5,4)] = Keycodes.M   # does not exist
    char_dict[ALT_IDX] = Keycodes.L_ALT   # alt
    char_dict[CTRL_IDX] = Keycodes.L_CTRL   # CTRL
    char_dict[TOGGLE_IDX] = Keycodes.NULL # TOGGLE KEY

    return char_dict

def create_alt_chardict():
    alt_char_dict = dict()

    alt_char_dict[(4,0)] = Keycodes.COMMA # PERIOD
    alt_char_dict[(4,2)] = Keycodes.NINE # Left square bracket
    alt_char_dict[(4,3)] = Keycodes.ZERO # right square bracket

    return alt_char_dict

def create_alt_numdict():
    alt_num_dict = dict()

    alt_num_dict[(1,4)] = Keycodes.SEVEN # S
    alt_num_dict[(1,5)] = Keycodes.EIGHT # U
    alt_num_dict[(1,6)] = Keycodes.NINE # Y

    alt_num_dict[(2,4)] = Keycodes.FOUR #T
    alt_num_dict[(2,5)] = Keycodes.FIVE #D
    alt_num_dict[(2,6)] = Keycodes.SIX #B

    alt_num_dict[(3,4)] = Keycodes.ONE # C
    alt_num_dict[(3,5)] = Keycodes.TWO # K
    alt_num_dict[(3,6)] = Keycodes.THREE # G

    alt_num_dict[(4,5)] = Keycodes.ZERO # W

    return alt_num_dict



def main():

    rows = [IN(2, pull_up=True), IN(3, pull_up=True), IN(4, pull_up=True), 
            IN(17, pull_up=True),  IN(27, pull_up=True),  IN(22, pull_up=True)]
    
    cols = [OUT(9), OUT(11), OUT(0), OUT(5),
            OUT(6), OUT(13), OUT(19), OUT(26)]

    scan_matrix(rows, cols)

if __name__ == "__main__":
    main()
