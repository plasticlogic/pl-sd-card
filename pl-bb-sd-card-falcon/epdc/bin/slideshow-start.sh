#!/bin/bash

set -e
# do not run the slideshow if it is disabled
if [ -e /var/tmp/slideshow-disabled ]; then
    echo "Slideshow disabled"
    exit 1
fi

# remove the file which is used to stop the slideshow
rm -f /var/tmp/slideshow-stop

declare -a slideShowArray
declare slideShowFolder

slideShowFolder=$(cat /boot/uboot/config.txt)
/boot/uboot/epdc/bin/slideshow-select.sh "${slideShowFolder#*=}"

slideShowArray=($(ls /var/tmp/slideshow/*png))

# persist cached changes of file system
sync

# run the slideshow
while true; do
    for f in ${slideShowArray[@]}
    do
        if [ -e /var/tmp/slideshow-stop ]
        then
            echo "Stopping slideshow"
            exit 1
        fi
	if [ "${slideShowFolder#*=}" = "D054_T2.1" ]
	then
            echo "ACEP Clear"
            epdc-app -update_image $f 1 > /dev/null 
	fi
        epdc-app -update_image $f > /dev/null

        sleep 5
    done
done
exit 0
