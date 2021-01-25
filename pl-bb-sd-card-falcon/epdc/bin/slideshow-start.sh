#!/bin/sh

set -e

# do not run the slideshow if it is disabled
if [ -e /var/tmp/slideshow-disabled ]; then
    echo "Slideshow disabled"
    exit 1
fi

# remove the file which is used to stop the slideshow
rm -f /var/tmp/slideshow-stop

# persist cached changes of file system
sync

# run the slideshow
while true; do
for f in /var/tmp/slideshow/*.png; do
if [ -e /var/tmp/slideshow-stop ]
then
echo "Stopping slideshow"
exit 1
fi
epdc-app -update_image $f > /dev/null
#epview -i 2 -r auto -b black "$f"
#epview -i 2 "$f"        
sleep 3
done
done
exit 0
