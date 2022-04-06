#!/bin/bash

set -e

declare firmware_name
declare filetype
declare no_whitespace_filetype

#Ansi Colors
Yellow='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

if [ -n "$1" ]
    then
	    firmware_name=$1
    else
        printf "${RED}Theres no ITE Firmware file specified !${NC}\n"
        exit
fi

if [ "${firmware_name: -4}" == ".bin" ]
    then 
        filetype=$(file $firmware_name)
        no_whitespace_filetype="$(echo -e "${filetype#*:}" | tr -d '[:space:]')"
        if [ "$no_whitespace_filetype" = "data" ]
            then
                printf "${Yellow}Make sure the Flash Jumper is set when using Falcon 4.1.2 or older!${NC}\n"
                read -p "Press Enter to continue or ctrl + c to abort!"
                printf "${NC}Flashing firmware file $firmware_name to ITE\n"
                epdc-app -start_epdc 0 0 1
                epdc-app -pgm_epdc $firmware_name 1
                exit
            else
                printf "${RED}It looks like the specified file is not in the correct format${NC}\n" 
        fi    
    else    
        printf "${RED}Specified File $firmware_name is not of type .bin${NC}\n"
    fi
exit