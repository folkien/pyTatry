#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import functions, settings

for kraina in settings.swiat: 
    print kraina.nazwa + "."

    # Sciaganie obrazu z kamer.
    for kamera in kraina.listaKamer : 
        print kamera.nazwa + "."
        functions.saveFile(settings.photosFolder + kamera.folder + settings.actualDate + kamera.rozszerzenie, kamera.fetchData())

    kraina.kolazKamer()


