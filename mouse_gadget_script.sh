#!/bin/bash
# mouse
# SOURCE: https://forums.raspberrypi.com/viewtopic.php?t=234495
# Create gadget
mkdir /sys/kernel/config/usb_gadget/mymouse
cd /sys/kernel/config/usb_gadget/mymouse

echo 0x0100 > bcdDevice # v1.0.0
echo 0x0200 > bcdUSB # USB2
echo 0x00 > bDeviceClass
echo 0x00 > bDeviceProtocol
echo 0x00 > bDeviceSubClass
echo 0x08 > bMaxPacketSize0
echo 0x0104 > idProduct # Multifunction Composite Gadget
echo 0x1d6b > idVendor # Linux Foundation


mkdir strings/0x409

echo "18500_TEAM_D0" > strings/0x409/manufacturer
echo "Accessibility Mouse" > strings/0x409/product
echo "fedcba9876543210" > strings/0x409/serialnumber

# Add functions here
mkdir functions/hid.usb0

echo 1 > functions/hid.usb0/protocol
echo 3 > functions/hid.usb0/report_length
echo 1 > functions/hid.usb0/subclass

# Write report descriptor
echo -ne \\x05\\x01\\x09\\x02\\xa1\\x01\\x09\\x01\\xa1\\x00\\x05\\x09\\x19\\x01\\x29\\x03\\x15\\x00\\x25\\x01\\x95\\x03\\x75\\x01\\x81\\x02\\x95\\x01\\x75\\x05\\x81\\x03\\x05\\x01\\x09\\x30\\x09\\x31\\x15\\x81\\x25\\x7f\\x75\\x08\\x95\\x02\\x81\\x06\\xc0\\xc0 > functions/hid.usb0/report_desc

# Create configuration
mkdir configs/c.1
mkdir configs/c.1/strings/0x409
echo "Mouse Configuration" > configs/c.1/strings/0x409/configuration
echo 200 > configs/c.1/MaxPower

ln -s functions/hid.usb0 configs/c.1/

#ls /sys/class/udc > UDC
