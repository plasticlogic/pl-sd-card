PANEL_IMG_FOLDER=/boot/uboot/Panel_5x2/img
PANEL_SCRIPT=/boot/uboot/pl_panel.sh

IMG_FOLDER_LIST=($(ls -d $PANEL_IMG_FOLDER/*))

while true
do
	for img_folder in ${IMG_FOLDER_LIST[@]}
	do
		printf "Updating '%s'\n" $img_folder
		$PANEL_SCRIPT --all_shuffle $img_folder/*
		echo "Update done. Waiting for the next..."
		sleep 1m
	done
done

