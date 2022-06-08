#!/bin/bash
set -e
#comment out for use with Falcon
#echo BB-PL-SPIDEV0 > /sys/devices/bone_capemgr.*/slots
#echo BB-PL-SPIDEV1 > /sys/devices/bone_capemgr.*/slots
#export PATH=/boot/uboot/epdc/bin:$PATH
export PATH=$PATH:/boot/uboot/epdc/bin
#sleep 3
#start-epdc.sh 1 1
#epdc-app -update_image /var/www/pl_dsp_ctl/images/qr_code.png
#sleep 3
#manual_slideshow.sh --first
#slideshow-start.sh
exit 0

