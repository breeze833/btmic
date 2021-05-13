#!/bin/bash
cd /sys/kernel/config/usb_gadget/
mkdir -p pi
cd pi
echo 0x1d6b > idVendor
echo 0x0101 > idProduct
echo 0x0100 > bcdDevice
echo 0x0200 > bcdUSB
mkdir -p strings/0x409
echo "RPI00001" > strings/0x409/serialnumber
echo "Raspberry Pi Zero" > strings/0x409/manufacturer
echo "Linux USB Audio Gadget" > strings/0x409/product
mkdir -p configs/c.1/strings/0x409
echo "UAC1 Audio" > configs/c.1/strings/0x409/configuration
echo 250 > configs/c.1/MaxPower

N="uac1.usb0"
mkdir -p functions/$N
echo 1 > functions/$N/c_chmask
echo 8000 > functions/$N/c_srate
echo 2 > functions/$N/c_ssize
echo 1 > functions/$N/p_chmask
echo 8000 > functions/$N/p_srate
echo 2 > functions/$N/p_ssize
echo 2 > functions/$N/req_number

ln -s functions/$N configs/c.1

ls /sys/class/udc > UDC
