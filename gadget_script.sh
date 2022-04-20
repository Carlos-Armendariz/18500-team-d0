#!/bin/bash

./keyboard_gadget_script.sh > udc.txt
./mouse_gadget_script.sh

python3 matrix_scanning.py