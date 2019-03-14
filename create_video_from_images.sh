#!/usr/bin/env bash

## For working with /data/ user must be root!
if [[ "$( id -u )" != "0" ]]; then
	echo "Be root to use me!" 1>&2
	exit 1
fi


PLAIN_PATH=/data/DVS/DVS_HGH/plain

## Test if Plain folder exists
if [[ ! -d $PLAIN_PATH ]]; then
    echo "Plain folder does not exist, cannot create Videos!"
fi


BEGIN=$(date +%s)

## For all datasets do
for DIR in $PLAIN_PATH/*/; do
    cd $DIR

    DIR=${DIR%*/}       ## Strips following "/"
    DIR=${DIR##*/}      ## Strips everything before last "/"

    VIDEO_NAME="$DIR.mp4"

    ## Test if video already exists
    if [ -f $VIDEO_NAME ]; then
        echo "Video $VIDEO_NAME already exists, gets redone!"
        rm $VIDEO_NAME
    fi

    ffmpeg -r 30 -f image2 -s 720x640 -pattern_type glob -i '*.png' -vcodec libx264 -crf 15 $VIDEO_NAME &>/dev/null
    if [ $? -ne 0 ]; then
        echo "An error with FFMPEG occured!"
        rm $VIDEO_NAME
        exit 1
    fi

    echo "Video in $DIR created!"
done

ENDING=$(date +%s)
DIFF=$(echo "$ENDING-$START" | bc)
echo "All videos done! Time: $DIFF sec"
