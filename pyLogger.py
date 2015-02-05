#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import functions, settings

for kraina in settings.swiat: 
    print kraina.nazwa + "."

    # Sciaganie obrazu z kamer.
    for kamera in kraina.listaKamer : 
		print kamera.nazwa + "."
		numer = 0
		for obraz in kamera.fetchData():
				functions.saveFile(settings.photosFolder + kamera.folder + settings.actualDate + str(numer) + kamera.rozszerzenie, obraz)
				numer+=1

    kraina.kolazKamer()


