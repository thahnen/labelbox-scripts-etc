#!/usr/bin/env bash

## This script is used with the newly approached "Tracking with darkflow" method!


## For working with /data/ user must be root!
if [[ "$( id -u )" != "0" ]]; then
	echo "Be root to use me!" 1>&2
	exit 1
fi

## All worked on folders!
## Here not only the Dataset "04" shall be used but is due to it being only 30 min long!
FRAMES_PATH=/data/DVS/DVS_F102_20190423/Frames/04
OUTPUT_PATH=$HOME/LB

## Test if directories exists!
if [[ ! -d $FRAMES_PATH ]]; then
    echo "The Path containing the extracted Frames from the Video does not exist!"
    exit 1
fi

if [[ ! -d $OUTPUT_PATH ]]; then
    echo "Output folder does not exist yet, gets created!"

    mkdir $OUTPUT_PATH
    if [[ $? -ne 0 ]]; then
        echo "Creation of Output folder not possible!"
        echo "Maybe some rights missing?"
        exit 1
    fi
fi


BEGIN=$(date +%s)

## Gets first and last id of images
cd $FRAMES_PATH
START=$(find . -name '*.png' | sort | head -1 | cut -d'/' -f2 | cut -d'_' -f1)
END=$(find . -name '*.png' | sort | tail -1 | cut -d'/' -f2 | cut -d'_' -f1)

## For all images do montage
for i in $(eval echo {$START..$END}); do
    montage $FRAMES_PATH/${i}_accumulated.png $FRAMES_PATH/${i}_accumulated.png -tile 2x1 -geometry +0+0 $OUTPUT_PATH/${i}_montage.png &>/dev/null
    if [[ $? -ne 0 ]]; then
        echo "Montage cannot be done on image: ${i} in $FRAMES_PATH!"
        echo "Maybe 'montage' is not installed?"
        exit 1
    fi
done


## Split the Folder with its 1000s of images into Subfolders!
##IMG_PER_FOLDER=1000
##AMOUNT_IMAGES=$(echo $END | sed 's/^0*//')
##AMOUNT_FOLDERS=$(($AMOUNT_IMAGES / $IMG_PER_FOLDER))
##if [[ $(($AMOUNT_IMAGES % $IMG_PER_FOLDER)) != 0 ]]; then
##    AMOUNT_FOLDERS=$(($AMOUNT_FOLDERS + 1))
##fi
##
##for i in $(eval echo {1..$AMOUNT_FOLDERS}); do
##    echo "Test"
##done


## Giving the owning user its rights to the files back
FOLDER_OWNER=$(stat -c '%U' $OUTPUT_PATH)
chown $FOLDER_OWNER $OUTPUT_PATH/*
if [ $? -ne 0 ]; then
    echo "Owner of the files cannot be set to the folders owner, have to do it manually!"
fi

ENDING=$(date +%s)
echo "Done Directory ... Time: $(echo "$ENDING-$BEGIN" | bc) Sec"