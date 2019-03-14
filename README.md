# labelbox-scripts-etc
Scripts to work with Labelbox (and the data used)

---

## change_labelbox_names.py
Renames in every dataset the Image-Filenames to match the names set in Labelbox!

---

## create_video_from_images.sh
Creates for every dataset a video composed of all the images in its folder!
Mainly for myself to use it in an OpenCV-program I am working on to better find paths in the images!

---

## create_montages.sh
Create montages of the clustered and accumulated images for easier labeling in Labelbox!

---

## TODO:
1. in **change_labelbox_names.py** darauf achten, nicht alle anderen Dateien neben den Bildern umzubennenen!
2. in **create_montages.sh** ggf alle (60) Montagen parallelisieren, damit es schneller fertig ist!
- dauert derzeit rund 3 Stunden!
3. in **create_montages.sh** ueberpruefen, ob der Plain-Ordner leer ist oder nicht!
