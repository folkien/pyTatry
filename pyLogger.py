#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, functions, settings

# STARTUP BAZY DANYCH
################################################################################
database = settings.cDatabase(settings.databaseFile)

for kraina in settings.swiat: 
    print kraina.nazwa + "."

    # KAMERY
	################################################################################
    for kamera in kraina.listaKamer: 
		print "->"+kamera.nazwa + "."
		# Jezeli nie pobrano obrazu z kamery
		if (not kamera.pobrano):
			for obraz in kamera.fetchData():
				functions.saveFile(settings.photosFolder + kamera.folder + settings.actualDate + kamera.rozszerzenie, obraz)

    kraina.kolazKamer()
	
	# POMIARY
	################################################################################
    for dokumentPomiarowy in kraina.listaPomiarow:
			dokumentPomiarowy.fetchData()
			dokumentPomiarowy.doFiltering()
			for pomiar in dokumentPomiarowy.measurments:
					database.addMeasurment(pomiar.sqlFormat())
					print "Dodano " + pomiar.desc + pomiar.localization


# ZAKOŃCZENIE BAZY DANYCH
################################################################################
database.close()
