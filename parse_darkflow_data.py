#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import csv
import json
import time


if __name__ == "__main__":
    begin = time.time()

    # Hier eigentlich mit sys.argv auf den zweiten Parameter achten, der sollte den Link zur CSV-Datei beinhalten!

    # Hier werden die einzelnen Frame-Objekte mit ihren Informationen reingespeichert
    data = []

    # Get the data from the "Tracking with Darkflow" Output
    with open("/data/DVS/DVS_F102_20190423/deepTracking/Tracking-with-darkflow/dvs_record.celex_04.dvs.avi.csv") as nn_data:
        r = csv.reader(nn_data, delimiter=",")
        for row in r:
            # Noch schnell die erste Reihe ueberspringen!
            if row[0] == "frame_id":
                continue
            
            elem = None
            found = False
            for i in range(len(data)):
                if data[i]["frame_nr"] == int(row[0]):
                    # dann wird das gefundene Objekt einfach angehangen
                    elem = i
                    found = True
                    break
            
            if found:
                # Objekt hinten anhaengen an bestehenden Frame!
                label_id = row[1]

                # Die Punkte liegen im Uhrzeigersinn vor!
                p1 = {"x" : row[2], "y" : row[3]}
                p2 = {"x" : row[2]+row[4], "y" : row[3]}
                p3 = {"x" : row[2]+row[4], "y" : row[3]+row[5]}
                p4 = {"x" : row[2], "y" : row[3]+row[5]}

                obj = {
                    "label_id" : label_id,
                    "geometry" : [
                        p1, p2, p3, p4
                    ]
                }

                data[elem]["prediction_label"]["object"].append(obj)
            else:
                # Neuen Frame erstellen mit dem ersten Objekt!
                frame_nr = int(row[0])

                # Zahlen immer 10 stellig -> %010d
                image_url = "https://127.0.0.1:8000/%010d_montage.png" % frame_nr

                external_id = image_url.split("/")[-1:][0]
                label_id = row[1]

                # Die Punkte liegen im Uhrzeigersinn vor!
                p1 = {"x" : row[2], "y" : row[3]}
                p2 = {"x" : row[2]+row[4], "y" : row[3]}
                p3 = {"x" : row[2]+row[4], "y" : row[3]+row[5]}
                p4 = {"x" : row[2], "y" : row[3]+row[5]}

                frame = {
                    "frame_nr" : frame_nr,
                    "image_url" : image_url,
                    "external_id" : external_id,
                    "prediction_label" : {
                        "object" : [
                            {
                                "label_id" : label_id,
                                "geometry" : [
                                    p1, p2, p3, p4
                                ]
                            }
                        ]
                    }
                }

                data.append(frame)
    
    with open("darkflow_parsed.json", "w") as output:
        json.dump(data, output)
    
    print("ALLE Informationen aus der CSV-Datei wurden geparsed!")
    print(f"Gedauert hat das Parsen {time.time()-begin} sec!")