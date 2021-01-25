#!/bin/sh

set -e

FB_SYSFS_IMX=/sys/class/graphics/fb0
FB_SYSFS_MODELF=/sys/devices/platform/modelffb/graphics/fb0

IMG_ROOT=/boot/uboot

display_type="$1"

[ -z "display_type" ] && {
    echo "Error: no directory specified"
    exit 1
}

dir="$IMG_ROOT/$display_type/img"

[ -d "$dir" ] || {
    echo "Invalid directory: $dir"
    exit 1
}

echo "Slideshow directory: $dir"

rm -f /var/tmp/slideshow
ln -s "$dir" /var/tmp/slideshow
sync

exit 0
