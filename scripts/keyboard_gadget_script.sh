#!/bin/bash

#SOURCE: https://gist.github.com/rmed/0d11b7225b3b772bb0dd89108ee93df0

# Create gadget

GADG_PATH=/sys/kernel/config/usb_gadget/mykeyboard

mkdir $GADG_PATH

# Add basic information
echo 0x0100 > $GADG_PATH/bcdDevice # Version 1.0.0
echo 0x0200 > $GADG_PATH/bcdUSB # USB 2.0
echo 0x00 > $GADG_PATH/bDeviceClass
echo 0x00 > $GADG_PATH/bDeviceProtocol
echo 0x00 > $GADG_PATH/bDeviceSubClass
echo 0x08 > $GADG_PATH/bMaxPacketSize0
echo 0x0104 > $GADG_PATH/idProduct # Multifunction Composite Gadget
echo 0x1d6b > $GADG_PATH/idVendor # Linux Foundation

# Create English locale
mkdir $GADG_PATH/strings/0x409

echo "18500_TEAM_D0" > $GADG_PATH/strings/0x409/manufacturer
echo "Accessibility Keyboard" > $GADG_PATH/strings/0x409/product
echo "0123456789" > $GADG_PATH/strings/0x409/serialnumber

# Create HID function
mkdir $GADG_PATH/functions/hid.usb0

echo 1 > $GADG_PATH/functions/hid.usb0/protocol
echo 8 > $GADG_PATH/functions/hid.usb0/report_length # 8-byte reports
echo 1 > $GADG_PATH/functions/hid.usb0/subclass

# Write report descriptor
echo "05010906a101050719e029e71500250175019508810275089501810175019503050819012903910275019505910175089506150026ff00050719002aff008100c0" | xxd -r -ps > $GADG_PATH/functions/hid.usb0/report_desc

# Create configuration
mkdir $GADG_PATH/configs/c.1
mkdir $GADG_PATH/configs/c.1/strings/0x409

echo 0x80 > $GADG_PATH/configs/c.1/bmAttributes
echo 200 > $GADG_PATH/configs/c.1/MaxPower # 200 mA
echo "Keyboard configuration" > $GADG_PATH/configs/c.1/strings/0x409/configuration

# Link HID function to configuration
ln -s $GADG_PATH/functions/hid.usb0 $GADG_PATH/configs/c.1

# Enable gadget
#ls /sys/class/udc > UDC.txt
ls /sys/class/udc > $GADG_PATH/UDC
# cat $GADG_PATH/UDC 
