#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# Just here for legacy!
# Filenames usually looks sth. like this: 0000012345_montage.png

if __name__ == "__main__":
    # The folder with all datasets each in an numbered folder starting with 01
    path :str = "/data/DVS/DVS_HGH/labelbox/"

    folders = [ n for n in os.listdir(path) if os.path.isdir(os.path.join(path, n)) ]

    for folder in folders:
        print(f"\nDataset: {path}{folder}/")

        # Folder number is always one higher (starts at 1 while images at 0)
        data :int = int(folder)-1
        dateien = sorted([ [n, n.split("_")[0][-4:]] for n in os.listdir(path+folder) if os.path.isfile(os.path.join(path+folder, n)) ])
        suffix :str = "_montage.png"

        for datei in dateien:
            if int(datei[1][0]) == 1:
                data += 1

            # For all datasets less than 10 there is another 0 infront
            if data < 10:
                praefix :str = "000000"
            else:
                praefix :str = "00000"

            datei[1] = praefix + str(data) + datei[1][-3:] + suffix
            
            # Decrease because used on every image
            data = int(folder)-1

            full_path :str = os.path.join(path, folder)
            os.rename(os.path.join(full_path, datei[0]), os.path.join(full_path, datei[1]))
