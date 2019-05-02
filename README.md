# labelbox-scripts-etc
Scripts to work with Labelbox (and the data used)

---

## change_labelbox_names.py
Renames in every dataset the Image-Filenames to match the names set in Labelbox!

---

## measure_labeling_time.py
Measures the time it took to label a dataset for estimating the time the others may take!

---

## create_video_from_images.sh
Creates for every dataset a video composed of all the images in its folder!
Mainly for myself to use it in an OpenCV-program I am working on to better find paths in the images!

### Disclaimer:
Takes ages on 60 datasets per 1000 images (768x640px). On my machine: ~5 min

---

## create_montages.sh
Create montages of the clustered and accumulated images for easier labeling in Labelbox!

### Disclaimer:
Takes ages on 60 datasets per 1000 images (768x640px). On my machine: ~3-4 hours

---

## create_montages_darkflow.sh
Create montages of the accumulated grayscale images for labeling in Labelbox using the values of the NNs.

### Disclaimer:
Takes ages on on dataset by ~30.000 images (768x640px). On my machine:

---

## TODO:
1. in **change_labelbox_names.py** darauf achten, nicht alle anderen Dateien neben den Bildern umzubennenen!
2. in **create_montages.sh** ggf alle (60) Montagen parallelisieren, damit es schneller fertig ist!
- dauert derzeit rund 3 Stunden!
3. in **create_montages.sh** ueberpruefen, ob der Plain-Ordner leer ist oder nicht!
4. generell in Python-Dateien ueberpruefen, ob Ordner "leer"