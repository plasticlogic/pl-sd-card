#!/bin/bash

set -e

declare count
declare area
declare folderPath

#Ansi Colors
Yellow='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# do not run the slideshow if it is disabled
if [ -e /var/tmp/slideshow-disabled ]; then
    echo "Slideshow disabled"
    exit 1
fi

# remove the file which is used to stop the slideshow
rm -f /var/tmp/slideshow-stop

if [ -n "$1" ]
    then
        if [ "$1" == "-h" ]; then
            echo "Usage: `basename $0` [pathToFolder] [AnimationCycleCount] [startpos_x,startpos_y,anim_height,anim_width]"
            exit 0
        else
            folderPath=$1
        fi
    else
        printf "${Yellow}No folder path specified, aborting !${NC}\n"
        exit
fi

if [ -n "$2" ]
    then
	    count=$2
    else
        printf "${Yellow}No animation cycle count specified, using 1 as default !${NC}\n"
        count=1
fi

if [ -n "$3" ]
    then
	    area=$3
    else
        printf "${RED}No area specified, buffer loading needs size Information ! (top,left,sizex,sizey)${NC}\n"
        exit
fi

epdc-app -slideshow $folderPath 4 $count 1 $area

exit



