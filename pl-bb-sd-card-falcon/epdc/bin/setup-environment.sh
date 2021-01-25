#!/bin/bash
set -e
#comment out for use with Falcon
#echo BB-PL-SPIDEV0 > /sys/devices/bone_capemgr.*/slots
echo BB-PL-SPIDEV1 > /sys/devices/bone_capemgr.*/slots
export PATH=/boot/uboot/epdc/bin:$PATH
sleep 3
epdc-app -start_epdc 0 1
sleep 3
slideshow-start.sh
exit 0
