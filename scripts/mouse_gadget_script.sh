#!/bin/bash
# mouse
# SOURCE: https://forums.raspberrypi.com/viewtopic.php?t=234495
# Create gadget
GADG_PATH=/sys/kernel/config/usb_gadget/mymouse

mkdir $GADG_PATH 
#cd /sys/kernel/config/usb_gadget/mymouse

echo 0x0100 > $GADG_PATH/bcdDevice # v1.0.0
echo 0x0200 > $GADG_PATH/bcdUSB # USB2
echo 0x00 > $GADG_PATH/bDeviceClass
echo 0x00 > $GADG_PATH/bDeviceProtocol
echo 0x00 > $GADG_PATH/bDeviceSubClass
echo 0x08 > $GADG_PATH/bMaxPacketSize0
echo 0x0104 > $GADG_PATH/idProduct # Multifunction Composite Gadget
echo 0x1d6b > $GADG_PATH/idVendor # Linux Foundation


mkdir $GADG_PATH/strings/0x409

echo "18500_TEAM_D0" > $GADG_PATH/strings/0x409/manufacturer
echo "Accessibility Mouse" > $GADG_PATH/strings/0x409/product
echo "fedcba9876543210" > $GADG_PATH/strings/0x409/serialnumber

# Add functions here
mkdir $GADG_PATH/functions/hid.usb0

echo 1 > $GADG_PATH/functions/hid.usb0/protocol
echo 3 > $GADG_PATH/functions/hid.usb0/report_length
echo 1 > $GADG_PATH/functions/hid.usb0/subclass

# Write report descriptor
echo -ne \\x05\\x01\\x09\\x02\\xa1\\x01\\x09\\x01\\xa1\\x00\\x05\\x09\\x19\\x01\\x29\\x03\\x15\\x00\\x25\\x01\\x95\\x03\\x75\\x01\\x81\\x02\\x95\\x01\\x75\\x05\\x81\\x03\\x05\\x01\\x09\\x30\\x09\\x31\\x15\\x81\\x25\\x7f\\x75\\x08\\x95\\x02\\x81\\x06\\xc0\\xc0 > $GADG_PATH/functions/hid.usb0/report_desc

# Create configuration
mkdir $GADG_PATH/configs/c.1
mkdir $GADG_PATH/configs/c.1/strings/0x409
echo "Mouse Configuration" > $GADG_PATH/configs/c.1/strings/0x409/configuration
echo 200 > $GADG_PATH/configs/c.1/MaxPower

ln -s $GADG_PATH/functions/hid.usb0 $GADG_PATH/configs/c.1/

# ls /sys/class/udc > $GADG_PATH/UDC
# cat $GADG_PATH/UDC 
