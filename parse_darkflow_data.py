#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import json


if __name__ == "__main__":
    # Get the data from the "Tracking with Darkflow" Output
    with open("/data/DVS/DVS_F102_20190423/deepTracking/Tracking-with-darkflow/dvs_record.celex_04.dvs.avi.csv") as nn_data:
        r = csv.reader(nn_data, delimiter=",")
        for row in r:
            #print(", ".join(row))