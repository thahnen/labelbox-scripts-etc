#!/bin/bash

## Um auf /data/ Veraenderungen vorzunehmen, muss man Root sein!
if [[ "$( id -u )" != "0" ]]; then
	echo "Skript muss als Root ausgeführt werden!" 1>&2
	exit 1
fi


## Alle Ordner, mit denen gearbeitet wird!
PLAIN_PATH=/data/DVS/DVS_HGH/plain
CLUSTERED=$PLAIN_PATH/../cluster
ACCUMULATED=$PLAIN_PATH/../accumulated
LABELBOX=$PLAIN_PATH/../labelbox
    
    
## Hier testen, ob die Verzeichnisse existieren!
if [[ ! -d $PLAIN_PATH ]] || [[ ! -d $CLUSTERED ]] || [[ ! -d $ACCUMULATED ]]; then
    echo "Plain-Ordner oder Clustered-Ordner oder Accumulated-Ordner existiert nicht, Montage nicht moeglich!"
fi

if [[ ! -d $LABELBOX ]]; then
    echo "Labelbox-Ordner existiert nicht, wird erstellt!"

    mkdir $PLAIN_PATH/labelbox
    if [[ $? -ne 0 ]]; then
        echo "Labelbox-Ordner konnte nicht erstellt werden!"
        echo "Moeglicherweise keine Rechte vorhanden?"
        exit 1
    fi
fi


## Hier testen, ob Plain-Ordner auch Daten beinhaltet!
## Kommt noch ...


## Alle Datensaetze durchgehen
for DIR in $PLAIN_PATH/*/; do
    echo "Running Directory: $DIR"
    BEGIN=$(date +%s.%N)
    
    DIR=${DIR%*/}       ## Entfernt hinteren "/"
    DIR=${DIR##*/}      ## Entfernt alles vor letzem "/"

    ## Existiert das DIR auch in jedem der Ordner?
    if [[ ! -d $CLUSTERED/$DIR ]] || [[ ! -d $ACCUMULATED/$DIR ]]; then
        echo "Es gibt keine geclusterten oder akkumulierten Dateien fuer den Ordner $DIR, Montage nicht moeglich"
        exit 1
    fi

    if [[ ! -d $LABELBOX/$DIR ]]; then
        echo "Labelbox-$DIR-Ordner existiert nicht, wird erstellt!"

        mkdir $LABELBOX/$DIR
        if [[ $? -ne 0 ]]; then
            echo "Labelbox-$DIR-Ordner konnte nicht erstellt werden!"
            echo "Moeglicherweise keine Rechte vorhanden?"
            exit 1
        fi
    fi

    ## Die erste und die letzte Bild-Id bekommen
    cd $PLAIN_PATH/$DIR/
    START=$(find . -name '*.png' | sort | head -1 | cut -d'/' -f2 | cut -d'_' -f1)
    END=$(find . -name '*.png' | sort | tail -1 | cut -d'/' -f2 | cut -d'_' -f1)

    ## Fuer jedes Bild Montage durchfuehren
    for i in $(eval echo {$START..$END}); do
        montage $CLUSTERED/$DIR/${i}_clustered.png $ACCUMULATED/$DIR/${i}_accumulated.png -tile 2x1 -geometry +0+0 $LABELBOX/$DIR/${i}_montage.png
        if [[ $? -ne 0 ]]; then
            echo "Montage konnte nicht ausgefuert werden auf Bild: ${i} in $DIR!"
            exit 1
        fi
    done

    ENDING=$(date +%s.%N)
    DIFF=$(echo "$END - $START" | bc)
    echo "Done Directory ... Time: $DIFF"
done