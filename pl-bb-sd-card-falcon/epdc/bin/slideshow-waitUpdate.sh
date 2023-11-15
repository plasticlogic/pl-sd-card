#!/bin/bash

set -e
#i=0
# do not run the slideshow if it is disabled
if [ -e /var/tmp/slideshow-disabled ]; then
    echo "Slideshow disabled"
    exit 1
fi

# remove the file which is used to stop the slideshow
rm -f /var/tmp/slideshow-stop

#set liveSlideshow Path
spath=/root/liveSlideshow

# persist cached changes of file system
sync

#use inotify package (suoda apt-get install inotify-tools) to monitor changes in given folder
inotifywait --monitor $spath -e close_write -e moved_to |
    while read spath action file; do
        if [ -e /var/tmp/slideshow-stop ]; then
            echo "Stopping slideshow"
            exit 1
        fi
        if [[ $file = *.png ]]; then # Does the file end with .png?
            #echo "The file '$file' appeared in directory '$spath' via '$action'"
            #sleep 2
            echo "The file '$file' will be updated to the Display"
            #epdc-app -fill GL15 >/dev/null
            epdc-app -update_image $spath$file >/dev/null
            sleep 1
            echo "Deleting '$spath$file'"
            rm -f $spath$file
        fi
    done
