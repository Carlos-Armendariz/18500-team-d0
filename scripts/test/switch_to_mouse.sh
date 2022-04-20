#!/bin/bash

KEYBRD_PATH=/sys/kernel/config/usb_gadget/mykeyboard
MOUSE_PATH=/sys/kernel/config/usb_gadget/mymouse

# disable keyboard
echo "" | tee $KEYBRD_PATH/UDC
cat udc.txt > $MOUSE_PATH/UDC

