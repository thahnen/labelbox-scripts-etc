#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json


def measure_time(path: str):
    key :str = "Seconds to Label"
    all_times = []

    files = [
        path+n for n in os.listdir(path) if (
            os.path.isfile(os.path.join(path, n)) and n.endswith(".json")
        )
    ]

    for file in files:
        seconds :float = 0

        try:
            data = json.load(open(file))

            # Überprüfen, ob Liste vorliegt (so normal von Labelbox) und gefüllt
            assert(type(data) == list and len(data) > 0)

            assert(
                key in [
                    k for k in data[0]
                ]
            )
        except Exception as e:
            return -1
        
        for i in range(len(data)):
            if key in data[i]:
                seconds += data[i][key]
            else:
                print(f"Es fehlte das '{key}' Label!")
                return -1
        
        all_times.append(seconds)
    
    return [sum(all_times)/len(all_times), len(all_times)]
    

if __name__ == "__main__":
    if len(sys.argv) == 2:
        path :str = sys.argv[1]
        if os.path.isdir(path):
            times = measure_time(path)

            if type(times) != int:
                # Wenn man sich ueber die Berechnungen wundert: da genau 60 Datasets kuerzen sich die Minuten raus!
                print(f"\nDurchschnittliche Zeit fuer ein Dataset: {round(times[0]/60, 2)} min")
                print(f"Veranschlagte Zeit fuer alle 60 Datasets: {round(times[0]/60, 2)} h")
                print(f"Bereits bearbeitete {times[1]} Datasets, hat gedauert: {round(times[0]*times[1]/60/60, 2)} h")
                print(f"Es fehlen noch {60-times[1]} Datasets, das dauert: {round(times[0]*(60-times[1])/60/60, 2)} h \n")
            else:
                print("Es ist ein Fehler bei der Berechnung aufgetreten!")
                exit(1)
            pass
        else:
            print("Bei dem angegebenen Pfad handelt es sich nicht um ein Verzeichnis!\n")
    else:
        print("Nur den Ordner mit den exportierten (unbearbeiteten) Labelbox-JSONs angeben!")
        exit(1)