##!/bin/bash

# Reset
Color_Off='\033[0m' 	# Text Reset

# Regular Colors
Black='\033[0;30m'  	# Black
Red='\033[0;31m'    	# Red
Green='\033[0;32m'  	# Green
Yellow='\033[0;33m' 	# Yellow
Blue='\033[0;34m'   	# Blue
Purple='\033[0;35m' 	# Purple
Cyan='\033[0;36m'   	# Cyan
White='\033[0;97m'  	# White

# Additional colors
LGrey='\033[0;37m'  	# Ligth Gray
DGrey='\033[0;90m'  	# Dark Gray
LRed='\033[0;91m'   	# Ligth Red
LGreen='\033[0;92m' 	# Ligth Green
LYellow='\033[0;93m'	# Ligth Yellow
LBlue='\033[0;94m'  	# Ligth Blue
LPurple='\033[0;95m'	# Light Purple
LCyan='\033[0;96m'  	# Ligth Cyan


# Bold
BBlack='\033[1;30m' 	# Black
BRed='\033[1;31m'   	# Red
BGreen='\033[1;32m' 	# Green
BYellow='\033[1;33m'	# Yellow
BBlue='\033[1;34m'  	# Blue
BPurple='\033[1;35m'	# Purple
BCyan='\033[1;36m'  	# Cyan
BWhite='\033[1;37m' 	# White

# Underline
UBlack='\033[4;30m' 	# Black
URed='\033[4;31m'   	# Red
UGreen='\033[4;32m' 	# Green
UYellow='\033[4;33m'	# Yellow
UBlue='\033[4;34m'  	# Blue
UPurple='\033[4;35m'	# Purple
UCyan='\033[4;36m'  	# Cyan
UWhite='\033[4;37m' 	# White

# Background
On_Black='\033[40m' 	# Black
On_Red='\033[41m'   	# Red
On_Green='\033[42m' 	# Green
On_Yellow='\033[43m'	# Yellow
On_Blue='\033[44m'  	# Blue
On_Purple='\033[45m'	# Purple
On_Cyan='\033[46m'  	# Cyan
On_White='\033[47m' 	# White

NUMBER_OF_DISPLAYS="0"

ONE_WIRE_BUS_PATH="/sys/bus/w1/drivers/w1_master_driver/w1_bus_master1"
ONE_WIRE_DEV_PATH="/sys/bus/w1/drivers/w1_slave_driver"

IMAGE_CONT_TEMP_FOLDER="/tmp/img_cont"
PRE_IMAGE_NAME_FILE="$IMAGE_CONT_TEMP_FOLDER/pre_img"
CLEAR_IMAGE_FILE="$IMAGE_CONT_TEMP_FOLDER/clear.raw"
PRE_IMAGE_WHITE="__CLEAR_FILL_GL15__"

COLOR_PALETTE="/boot/uboot/pl_color_palette.png"
DITHER_METHOD_EDD="-dither FloydSteinberg"
DITHER_METHOD_OD="-ordered-dither 2x2"
CFA_FILTER=wgrb
#brgw -> 180
#gbwr -> -90
ROTATE="180"
#-90

CLEAR_NUM_DSP=3
SHUFFLE="n"
VERSION="1.4.0"

################################################################################
# ONE WIRE

SWITCH_ON="0f"
SWITCH_OFF="f0"
MAX_SW_TRIES=10000

function set_switch()
{
	readarray -d $'\0' sw_folders < <(find $ONE_WIRE_DEV_PATH -name '3a-*' -print0 | sort -z)

	local sw_num=$1
	local sw_state=$2
	local switch_path=${sw_folders[$sw_num]}

	if [[ -d $switch_path && -e "$switch_path/output" ]]; then
		local sw_tries=0
		while [[ "$(xxd -p $switch_path/state)" != $sw_state \
			 || $sw_tries -ge $MAX_SW_TRIES ]]
		do
			echo "$sw_state" | xxd -p -r > $switch_path/output
			sw_tries=$(( $sw_tries + 1 ))
		done
		return 0
	else
		return 1
	fi
}

function turn_off_all_switches()
{
	readarray -d $'\0' sw_folders < <(find $ONE_WIRE_DEV_PATH -name '3a-*' -print0 | sort -z)

	for ((i = 0; i < ${#sw_folders[@]}; i++)); do
		set_switch $i $SWITCH_OFF
	done
	return 0
}

################################################################################
# EPDC APP

function init_epdc()
{
	epdc-app -start_epdc 0 0 > /dev/null
	return 0
}

function send_post_image()
{
	epdc-app -override_post_buffer $1 1 > /dev/null
	return 0
}

function set_temperature()
{
	readarray -d $'\0' temp_sensor_path < <(find $ONE_WIRE_DEV_PATH -name '28-*' | sort -z)

	if [[ -e ${temp_sensor_path[0]} ]]; then
		local temp_sensor_ret="$(cat ${temp_sensor_path[0]}/w1_slave)"
		local temp_sensor="${temp_sensor_ret##*=}"
		local temp=$(( "$temp_sensor" / 1000 ))
		epdc-app -set_temperature "$temp" > /dev/null
	else
		return 1
	fi
	return 0
}

function trigger_update()
{
	epdc-app -load_buffer $1 2 2 0,0,1280,960 > /dev/null
	return 0
}

function trigger_clear_update()
{
	epdc-app -fill GL15 0 > /dev/null
	return 0
}

################################################################################
# IMAGE CONVERSION + IMAGE BUFFERING

##
# png_to_raw [input_image] [output_image]
function png_to_raw()
{
	local input_image=$1
	local output_image=$2

	local w=$(identify -format "%[fx:w]" $input_image)
	local h=$(identify -format "%[fx:h]" $input_image)

	convert $input_image \
		-rotate $ROTATE \
		$DITHER_METHOD_EDD \
		-remap $COLOR_PALETTE \
		ppm:- | tail -c $((w * h * 3)) > $output_image

	if rgb2cfa $output_image $w $CFA_FILTER; then
		return 0
	else
		return 1
	fi
}

##
# all_png2raw [image_folder] [target_folder]
function all_png2raw()
{
	readarray -d $'\0' images < <(find $1 -type f -print0 | sort -z)

	local target_folder=$2

	for png_image in ${images[@]}; do
		local height=$(identify -format "%[fx:h]" "$png_image")
		local width=$(identify -format "%[fx:w]" "$png_image")
		local raw_image="$(basename $png_image)"
		raw_image=${raw_image%.*}.raw

		png_to_raw $png_image $target_folder/$raw_image
	done
	return 0
}

################################################################################
# SCRIPT FUNCTIONS -> CALL FUNCTIONS

##
# init
function init()
{
	init_epdc

	# remove all actual switches
	for old_1w_dev in $(find $ONE_WIRE_DEV_PATH -name '*-*'); do
		echo "${old_1w_dev##*/}" > "$ONE_WIRE_BUS_PATH/w1_master_remove"
	done

	# search for new devs
	echo "5" > $ONE_WIRE_BUS_PATH/w1_master_search
	local bus_search_timeout="$(cat $ONE_WIRE_BUS_PATH/w1_master_timeout)"
	while [[ "$(cat $ONE_WIRE_BUS_PATH/w1_master_search)" != "0" ]]; do
		sleep 2 # $bus_search_timeout
	done

	set_temperature
	turn_off_all_switches

	readarray -d $'\0' devices < <(find $ONE_WIRE_DEV_PATH -name '3a-*')

	if [[ ${#devices[@]} -lt $NUMBER_OF_DISPLAYS ]]; then
		pr_err "Found too few displays"
		return 1
	fi

	if [[ ! -e $IMAGE_CONT_TEMP_FOLDER ]]; then
		mkdir $IMAGE_CONT_TEMP_FOLDER
	fi

	return 0
}

##
# clear
function clear()
{
	readarray -d $'\0' sw_folders < <(find $ONE_WIRE_DEV_PATH -name '3a-*' -print0 | sort -z)

	turn_off_all_switches
	set_temperature

	if [[ ! -e $CLEAR_IMAGE_FILE ]]; then
		png_to_raw "/boot/uboot/D107_T3.1/img/09_white_1280x960.png" \
			   $CLEAR_IMAGE_FILE
	fi

	for (( i = 0 ; i < ${#sw_folders[@]}; i+=$CLEAR_NUM_DSP )); do
		for ((sw = 0; sw < $CLEAR_NUM_DSP; sw++)); do
			set_switch $((i + sw)) $SWITCH_ON
		done

		trigger_clear_update

		for ((sw = 0; sw < $CLEAR_NUM_DSP; sw++)); do
			set_switch $((i + sw)) $SWITCH_OFF
		done
	done

	echo $PRE_IMAGE_FILE > $PRE_IMAGE_NAME_FILE
	return 0
}

##
# pre_load_image [image_folder]
function pre_load_all()
{
	# check if [image_folder] is really a folder
	if [[ ! -d $1 ]]; then
		pr_err "'$1' is not a valid folder"
		return 1
	fi

	local image_name="$(basename $1)"

	# check if content folder exists
	if [[ ! -e  $IMAGE_CONT_TEMP_FOLDER ]]; then
		mkdir $IMAGE_CONT_TEMP_FOLDER
	fi

	# check if a buffered version of this image already exists
	if [[ -e "$IMAGE_CONT_TEMP_FOLDER/$image_name" ]]; then
		return 0
	fi

	mkdir $IMAGE_CONT_TEMP_FOLDER/$image_name

	# convert images
	if all_png2raw $1 $IMAGE_CONT_TEMP_FOLDER/$image_name; then
		return 0
	else
		return 1
	fi
}

##
# update_all [image_folder | image_name]
function update_all()
{
	local image_name="$(basename $1)"

	pre_load_all $1

	readarray -d $'\0' images < <(find "$IMAGE_CONT_TEMP_FOLDER/$image_name" -type f -print0 | sort -z)
	local num_of_displays=${#images[@]}
	declare -a update_seq

	turn_off_all_switches
	set_temperature

	update_seq=( $(seq 0 1 $((num_of_displays - 1))) )

	if [[ $SHUFFLE == "y" ]]; then
		update_seq=( $(shuf -e "${update_seq[@]}"))
	fi

	# if pre image file info file does not exist yet -> make it
	if [[ ! -e $PRE_IMAGE_NAME_FILE ]]; then
		echo $image_name > $PRE_IMAGE_NAME_FILE
	fi

	local pre_image="$(cat $PRE_IMAGE_NAME_FILE)"
	readarray -d $'\0' pre_images < <(find $IMAGE_CONT_TEMP_FOLDER/$pre_image -type f -print0 | sort -z)

	for i in "${update_seq[@]}"; do
		if set_switch $i $SWITCH_ON; then
			send_post_image ${pre_images[i]}
			trigger_update ${images[i]}
			set_switch $i $SWITCH_OFF
		fi
	done

	# set new pre image
	echo $image_name > $PRE_IMAGE_NAME_FILE
	return 0
}

################################################################################
# SCRIPT FUNCTIONS -> INTERNAL FUNCTIONS

function pr_warn()
{
	echo -e "${Yellow}$1${Color_Off}"
}

function pr_err()
{
	echo -e "${Red}$1${Color_Off}"
}

function print_version()
{
	printf "pl_panel.sh script v%s\n" $VERSION
	return 0
}

function usage()
{
	echo "Usage: $0 -i (-n [number of displays])"
	echo "Usage: $0 -c"
	echo "Usage: $0 -[a|ra] [content folder | image name]"
	echo "Usage: $0 -p [content folder]"
	echo "Usage: $0 -d"
	echo "Usage: $0 -h"
	echo "Usage: $0 -v"
	echo "Updates a multi-display PL Germany panel."
	echo ""
	echo -e "-i\tInitiates the EPDC and prepares the panel"
	echo -e "-c\tTriggers a clear update"
	echo -e "-h\tPrints this message"
	echo -e "-v\tPrints the version number"
	echo -e "-a\tUpdates the whole panel"
	echo -e "-p\tPre-load Panel image"
	echo -e "-d\tDelete all pre-loaded content"
	return 1
}

while getopts "n:rica:p:hvd" options; do
	case "${options}" in
		r)
			SHUFFLE="y"
			;;
		n)
			NUMBER_OF_DISPLAYS=${OPTARG}
			;;
		i)
			if init; then
				exit 0
			else
				pr_err "Init failed!"
				exit 1
			fi
			;;
		c)
			if clear; then
				exit 0
			else
				pr_err "Clear update failed!"
				exit 1
			fi
			;;
		a)
			if update_all ${OPTARG}; then
				exit 0
			else
				pr_err "Update failed!"
				exit 1
			fi
			;;
		p)
			if pre_load_all ${OPTARG}; then
				exit 0
			else
				pr_err "Pre-loading failed!"
				exit 1
			fi
			;;
		h)
			usage
			exit 0
			;;
		v)
			print_version
			exit 0
			;;
		d)
			if [[ -e $IMAGE_CONT_TEMP_FOLDER ]];then
				rm -r $IMAGE_CONT_TEMP_FOLDER
			fi
			exit 0
			;;
	esac
done
