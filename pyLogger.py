#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import functions, settings

# Sciaganie obrazu z kamer.
for kamera in settings.kamery : 
    print kamera.nazwa
    functions.saveFile(settings.photosFolder + kamera.folder + settings.actualDate + kamera.rozszerzenie, kamera.fetchData())

#Mergowanie plikow
#print "Zdjęcie całego dnia."
#command =  "convert \( "+m1FileName+" "+m2FileName+" "+psFileName+" +append \) \
#          \( "+buFileName+" "+gaFileName+" "+goFileName+" +append \) \
#          \( "+chFileName+" +append \) \
#          -background none -append "+allFileName 
#os.system(command)

