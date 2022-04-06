#!/bin/bash

sudo ./keyboard_gadget_script.sh
sudo ./mouse_gadget_script.sh

# Enable gadgets
ls /sys/class/udc > UDC
