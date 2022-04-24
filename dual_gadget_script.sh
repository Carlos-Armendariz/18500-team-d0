#!/bin/bash
# SOURCE: https://forums.raspberrypi.com/viewtopic.php?t=234495

GADGET_PATH=/sys/kernel/config/usb_gadget/my_keyboard

mkdir $GADGET_PATH

# Add basic information
echo 0x0100 > $GADGET_PATH/bcdDevice # Version 1.0.0
echo 0x0200 > $GADGET_PATH/bcdUSB # USB 2.0
echo 0x00 > $GADGET_PATH/bDeviceClass
echo 0x00 > $GADGET_PATH/bDeviceProtocol
echo 0x00 > $GADGET_PATH/bDeviceSubClass
echo 0x08 > $GADGET_PATH/bMaxPacketSize0
echo 0x0104 > $GADGET_PATH/idProduct # Multifunction Composite Gadget
echo 0x1d6b > $GADGET_PATH/idVendor # Linux Foundation

# Create English locale
# STRINGS_DIR=$GADGET_PATH/strings/0x409
mkdir $GADGET_PATH/strings/0x409

echo "18500_TEAM_D0" > $STRINGS_DIR/manufacturer
echo "Accessibility Keyboard & Mouse" > $STRINGS_DIR/product
echo "0123456789" > $STRINGS_DIR/serialnumber

###############################################################################
# KEYBOARD
###############################################################################

# Create HID function
mkdir $GADGET_PATH/functions/hid.usb0

echo 1 > $GADGET_PATH/functions/hid.usb0/protocol
echo 8 > $GADGET_PATH/functions/hid.usb0/report_length # 8-byte reports
echo 1 > $GADGET_PATH/functions/hid.usb0/subclass

# Write report descriptor
echo "05010906a101050719e029e71500250175019508810275089501810175019503050819012903910275019505910175089506150026ff00050719002aff008100c0" | xxd -r -ps > $GADGET_PATH/functions/hid.usb0/report_desc

###############################################################################
# MOUSE
###############################################################################
# Add functions here
mkdir $GADGET_PATH/functions/hid.usb1

echo 1 > $GADGET_PATH/functions/hid.usb1/protocol
echo 3 > $GADGET_PATH/functions/hid.usb1/report_length
echo 1 > $GADGET_PATH/functions/hid.usb1/subclass

# Write report descriptor
echo -ne \\x05\\x01\\x09\\x02\\xa1\\x01\\x09\\x01\\xa1\\x00\\x05\\x09\\x19\\x01\\x29\\x03\\x15\\x00\\x25\\x01\\x95\\x03\\x75\\x01\\x81\\x02\\x95\\x01\\x75\\x05\\x81\\x03\\x05\\x01\\x09\\x30\\x09\\x31\\x15\\x81\\x25\\x7f\\x75\\x08\\x95\\x02\\x81\\x06\\xc0\\xc0 > $GADGET_PATH/functions/hid.usb1/report_desc

###############################################################################

# Create configuration
CONFIGS_DIR=$GADGET_PATH/configs/c.1
mkdir $GADGET_PATH/configs/c.1
mkdir $GADGET_PATH/configs/c.1/strings/0x409

echo 0x80 > $GADGET_PATH/configs/c.1/bmAttributes
echo 200 > $GADGET_PATH/configs/c.1/MaxPower # 200 mA
echo "Keyboard configuration" > $GADGET_PATH/configs/c.1/strings/0x409/configuration

# Link HID functions to configuration
#ln -s $MOUSE_FUNCTIONS_DIR $CONFIGS_DIR
ln -s $GADGET_PATH/functions/hid.usb0 $GADGET_PATH/configs/c.1
ln -s $GADGET_PATH/functions/hid.usb1 $GADGET_PATH/configs/c.1

ls /sys/class/udc > $GADGET_PATH/UDC