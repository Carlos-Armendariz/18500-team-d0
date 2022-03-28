#!/usr/bin/env python3

from gpiozero import DigitalInputDevice as IN
from gpiozero import DigitalOutputDevice as OUT

import time
from keycodes import Keycodes



def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())


def send_key(key):
    NULL_CHAR = chr(0)

    write_report(chr(32)+NULL_CHAR+chr(key)+NULL_CHAR*5)
    # Release all keys
    write_report(NULL_CHAR*8)
    

def create_chardict():
    char_dict = dict()
    char_dict[(0,0)] = Keycodes.A
    char_dict[(0,1)] = Keycodes.B
    char_dict[(1,0)] = Keycodes.C
    char_dict[(1,1)] = Keycodes.D


    return char_dict

"""
Matrix Scanning: set cols to low and see if each row if low
if row low, key in (row,col) is pressed
"""

def scan_matrix(rows, cols):
 
    for col in cols:
        col.on()

    char_dict = create_chardict()
    prevSeen = set()
    print("Running matrix scanning")
    while True:
        time.sleep(0.001)
        seen = set()
        for i, col in enumerate(cols):
            col.off()
            for j, row in enumerate(rows):
                if (row.value):
                    seen.add((j,i))
                elif (j,i) in prevSeen:
                    prevSeen.remove((j,i))
            col.on()
            time.sleep(0.001)
   
        if len(seen) > 0:
            print_val = ""
            for pair in seen:
                if pair not in prevSeen:
                    print(prevSeen, pair)
                    prevSeen.add(pair)
                    #print_val += str(char_dict[pair])
                    send_key(char_dict[pair])
 
            # print(print_val)
            # print("----------")

def main():

    rows = [IN(5, pull_up=True), IN(6, pull_up=True)]
    cols = [OUT(20), OUT(21)]

    scan_matrix(rows, cols)



if __name__ == "__main__":
    main()
