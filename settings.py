#!/usr/bin/python
# -*- coding: utf-8 -*-
import functions, os, urllib2, re

class cameraLocalization:
		
		def __init__(self,n,l,f, ext = ".jpg", k = "tatry"):
				self.nazwa 	= n
				self.link  	= l
				self.folder = f
				self.rozszerzenie = ext
				self.kraina = k

		def fetchData(self):
				response = urllib2.urlopen(self.link)
				return response.read()

class stopienZagrozenia(cameraLocalization):
		
		def fetchData(self):
				#odczytujemy stronę www z zagrożeniem lawinowym
				response = urllib2.urlopen(self.link)
				stopien  = re.search('images/stopnie.*jpg',response.read()).group(0)
				#sciagamy obrazek ze strony TOPR'u
				response = urllib2.urlopen("http://www.topr.pl/" + stopien)
				return response.read()


# ścieżki i foldery w programie				
scriptFolder = os.path.dirname(os.path.realpath(__file__))
photosFolder = scriptFolder + "/data/photos/"

# Tworzymy nazwe pliku zgodnie z aktualna data
actualDate = functions.createFileName('')
allFileName= photosFolder + "tatry/" + actualDate

kamery = []
kamery.append( cameraLocalization("Morskie Oko 1", "http://kamery.topr.pl/moko/moko_01.jpg", 				"moko1/" ) )
kamery.append( cameraLocalization("Morskie Oko 2", "http://kamery.topr.pl/moko_TPN/moko_02.jpg", 			"moko2/" ) )
kamery.append( cameraLocalization("Dol 5 stawów", "http://kamery.topr.pl/stawy2/stawy2.jpg", 				"5stawow/" ) )
kamery.append( cameraLocalization("Buczynowa dolinka", "http://kamery.topr.pl/stawy1/stawy1.jpg", 			"buczynowa/" ) )
kamery.append( cameraLocalization("Hala gąsienicowa", "http://kamery.topr.pl/gasienicowa/gasie.jpg", 		"gasienicowa/" ) )
kamery.append( cameraLocalization("Goryczkowa", "http://kamery.topr.pl/goryczkowa/gorycz.jpg", 				"goryczkowa/" ) )
kamery.append( cameraLocalization("Dol Chochołowska", "http://kamery.topr.pl/chocholowska/chocholow.jpg", 	"chocholowska/" ) )
kamery.append( cameraLocalization("Meteogram", "http://new.meteo.pl/um/metco/mgram_pict.php?ntype=0u&row=487&col=232&lang=pl", "meteo/", ".png" ) )
kamery.append( stopienZagrozenia( "Stopień zagrożenia lawinowego", "http://www.topr.pl/wwt/warunki-w-tatrach-2", 	"lawiny/" ) )


