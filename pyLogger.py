#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import functions, settings

for kraina in settings.swiat: 
    print kraina.nazwa + "."

    # Sciaganie obrazu z kamer.
    for kamera in kraina.listaKamer : 
		print kamera.nazwa + "."
		# Jezeli nie pobrano obrazu z kamery
		if (not kamera.pobrano):
			for obraz in kamera.fetchData():
				functions.saveFile(settings.photosFolder + kamera.folder + settings.actualDate + kamera.rozszerzenie, obraz)

    kraina.kolazKamer()


