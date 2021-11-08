#!/bin/bash

OUT_DIR="/tmp/conv_out"
CFA_FILTER=gbwr

trap 'error' ERR

if [[ ! -d $OUT_DIR ]]; then
	mkdir $OUT_DIR
fi

if [[ -d $1 ]]; then
	cp $1/* $OUT_DIR
fi

images=( $OUT_DIR/* )

for image in ${images[@]}; do
	echo "Converting file: $image"
	height=$(identify -format "%[fx:h]" $image)
	width=$(identify -format "%[fx:w]" $image)
	new_file_path=${image%.*}.raw
	convert $image ppm:- | tail -c $(( height*width*3 )) > $new_file_path
	rgb2cfa $new_file_path $width $CFA_FILTER
done

find $OUT_DIR -type f ! -name '*.raw' -delete

echo "Conversion done"
