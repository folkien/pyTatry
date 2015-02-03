#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2, datetime, os
import functions

photosFolder = os.getenv("HOME") + "/python/pyTatry/data/photos/"

# Tworzymy nazwe pliku zgodnie z aktualna data
fileName = functions.createFileName('.jpg')
m1FileName = photosFolder + "moko1/" + fileName
m2FileName = photosFolder + "moko2/" + fileName
psFileName = photosFolder + "5stawow/" + fileName
buFileName = photosFolder + "buczynowa/" + fileName
gaFileName = photosFolder + "gasienicowa/" + fileName
goFileName = photosFolder + "goryczkowa/" + fileName
chFileName = photosFolder + "chocholowska/" + fileName
allFileName= photosFolder + "tatry/" + fileName


print "Morskie oko 1."
response = urllib2.urlopen('http://kamery.topr.pl/moko/moko_01.jpg')
functions.saveFile(m1FileName, response.read())

print "Morskie oko 2."
response = urllib2.urlopen('http://kamery.topr.pl/moko_TPN/moko_02.jpg')
functions.saveFile(m2FileName, response.read())

print "Dolina 5 stawów."
response = urllib2.urlopen('http://kamery.topr.pl/stawy2/stawy2.jpg')
functions.saveFile(psFileName, response.read())

print "Buczynowa dolinka."
response = urllib2.urlopen('http://kamery.topr.pl/stawy1/stawy1.jpg')
functions.saveFile(buFileName, response.read())

print "Gąsienicowa dolina."
response = urllib2.urlopen('http://kamery.topr.pl/gasienicowa/gasie.jpg')
functions.saveFile(gaFileName, response.read())

print "Goryczkowa dolina."
response = urllib2.urlopen('http://kamery.topr.pl/goryczkowa/gorycz.jpg')
functions.saveFile(goFileName, response.read())

print "Chochołowska dolina."
response = urllib2.urlopen('http://kamery.topr.pl/chocholowska/chocholow.jpg')
functions.saveFile(chFileName, response.read())

print "Meteogram."
response = urllib2.urlopen('http://new.meteo.pl/um/metco/mgram_pict.php?ntype=0u&row=487&col=232&lang=pl')
functions.saveFile(photosFolder + "meteo/" +functions.createFileName('.png'), response.read())

#Mergowanie plikow
print "Zdjęcie całego dnia."
command =  "convert \( "+m1FileName+" "+m2FileName+" "+psFileName+" +append \) \
          \( "+buFileName+" "+gaFileName+" "+goFileName+" +append \) \
          \( "+chFileName+" +append \) \
          -background none -append "+allFileName 
os.system(command)

