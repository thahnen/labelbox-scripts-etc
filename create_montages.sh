#!/usr/bin/env bash

## For working with /data/ user must be root!
if [[ "$( id -u )" != "0" ]]; then
	echo "Be root to use me!" 1>&2
	exit 1
fi


## All worked on folders!
PLAIN_PATH=/data/DVS/DVS_HGH/plain
CLUSTERED=$PLAIN_PATH/../cluster
ACCUMULATED=$PLAIN_PATH/../accumulated
LABELBOX=$PLAIN_PATH/../labelbox
    
## Test if directories exists!
if [[ ! -d $PLAIN_PATH ]] || [[ ! -d $CLUSTERED ]] || [[ ! -d $ACCUMULATED ]]; then
    echo "Plain/ Clustered or Accumulated folder does not exist, cannot create Montages!"
    exit 1
fi

if [[ ! -d $LABELBOX ]]; then
    echo "Labelbox folder does not exist yet, gets ceated!"

    mkdir $PLAIN_PATH/labelbox
    if [[ $? -ne 0 ]]; then
        echo "Creation of Labelbox folder not possible!"
        echo "Maybe some rights missing?"
        exit 1
    fi
fi


BEGIN=$(date +%s)

## For all datasets do
for DIR in $PLAIN_PATH/*/; do
    echo "Running Directory: $DIR"
    
    DIR=${DIR%*/}       ## Strips following "/"
    DIR=${DIR##*/}      ## Strips everything before last "/"

    ## Does DIR exist in every folder?
    if [[ ! -d $CLUSTERED/$DIR ]] || [[ ! -d $ACCUMULATED/$DIR ]]; then
        echo "There is no Clustered or Accumulated folder for $DIR, cannot create Montages"
        exit 1
    fi

    if [[ ! -d $LABELBOX/$DIR ]]; then
        echo "Labelbox $DIR folder does not exist yet, gets created!"

        mkdir $LABELBOX/$DIR
        if [[ $? -ne 0 ]]; then
            echo "Creation of Labelbox $DIR folder not possible!"
            echo "Maybe some rights missing?"
            exit 1
        fi
    fi

    ## Gets first and last id of images
    cd $PLAIN_PATH/$DIR/
    START=$(find . -name '*.png' | sort | head -1 | cut -d'/' -f2 | cut -d'_' -f1)
    END=$(find . -name '*.png' | sort | tail -1 | cut -d'/' -f2 | cut -d'_' -f1)

    ## For all images do montage
    for i in $(eval echo {$START..$END}); do
        montage $CLUSTERED/$DIR/${i}_clustered.png $ACCUMULATED/$DIR/${i}_accumulated.png -tile 2x1 -geometry +0+0 $LABELBOX/$DIR/${i}_montage.png &>/dev/null
        if [[ $? -ne 0 ]]; then
            echo "Montage cannot be done on image: ${i} in $DIR!"
            echo "May 'montage' is not installed?"
            exit 1
        fi
    done

    ## Giving the owning user its rights to the files back
    FOLDER_OWNER=$(stat -c '%U' $PLAIN_PATH)
    chown $FOLDER_OWNER $LABELBOX/*
    if [ $? -ne 0 ]; then
        echo "Owner of the files cannot be set to the folders owner, have to do it manually!"
    fi
done

ENDING=$(date +%s)
echo "Done Directory ... Time: $(echo "$ENDING-$BEGIN" | bc) Sec"