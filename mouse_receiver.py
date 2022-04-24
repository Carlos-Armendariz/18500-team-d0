

from gpiozero import DigitalInputDevice as IN
import time

RIGHT_CLICK=0
LEFT_CLICK=1
NULL_CHAR = chr(0)

def write_report(device, report):
    filepath = '/dev/hidg{}'.format(device)
    # print("Writing report")
    try:
        with open(filepath, 'rb+') as fd:
            fd.write(report.encode())
    except:
        print("Failed to open ", filepath)


def left_click():
    #p rint("left_click")
    write_report(0, chr(32) + NULL_CHAR + NULL_CHAR)

def right_click():
    # print("right_click")
    # write_report(0,))
    pass

def main():
    mouse_buttons = [IN(20), IN(21)]
    mouse_buttons[LEFT_CLICK].when_activated=left_click
    mouse_buttons[RIGHT_CLICK].when_activated=right_click

    print("Starting loop")
    while(True):
        #print(mouse_buttons[LEFT_CLICK].value)
        left_click()
        time.sleep(5)


if __name__ == "__main__":
        main()

