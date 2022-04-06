#!/bin/bash

###############################################################################
#sudo ./keyboard_gadget_script.sh
#SOURCE: https://gist.github.com/rmed/0d11b7225b3b772bb0dd89108ee93df0

# Create gadget
mkdir /sys/kernel/config/usb_gadget/mykeyboard
cd /sys/kernel/config/usb_gadget/mykeyboard

# Add basic information
echo 0x0100 > bcdDevice # Version 1.0.0
echo 0x0200 > bcdUSB # USB 2.0
echo 0x00 > bDeviceClass
echo 0x00 > bDeviceProtocol
echo 0x00 > bDeviceSubClass
echo 0x08 > bMaxPacketSize0
echo 0x0104 > idProduct # Multifunction Composite Gadget
echo 0x1d6b > idVendor # Linux Foundation

# Create English locale
mkdir strings/0x409

echo "18500_TEAM_D0" > strings/0x409/manufacturer
echo "Accessibility Keyboard" > strings/0x409/product
echo "0123456789" > strings/0x409/serialnumber

# Create HID function
mkdir functions/hid.usb1

echo 1 > functions/hid.usb1/protocol
echo 8 > functions/hid.usb1/report_length # 8-byte reports
echo 1 > functions/hid.usb1/subclass

# Write report descriptor
echo "05010906a101050719e029e71500250175019508810275089501810175019503050819012903910275019505910175089506150026ff00050719002aff008100c0" | xxd -r -ps > functions/hid.usb1/report_desc

# Create configuration
mkdir configs/c.1
mkdir configs/c.1/strings/0x409

echo 0x80 > configs/c.1/bmAttributes
echo 200 > configs/c.1/MaxPower # 200 mA
echo "Keyboard configuration" > configs/c.1/strings/0x409/configuration

# Link HID function to configuration
ln -s functions/hid.usb1 configs/c.1

# Enable gadget
#ls /sys/class/udc > UDC
###############################################################################

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

echo 2 > functions/hid.usb0/protocol
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
###############################################################################

# Enable gadgets
#touch UDC
#touch /sys/kernel/config/usb_gadget/mykeyboard/UDC

#ls /sys/class/udc > UDC 
#ls /sys/class/udc | sudo tee /sys/kernel/config/usb_gadget/UDC > UDC

