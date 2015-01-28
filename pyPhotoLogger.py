#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2, datetime, os

photosFolder = os.getenv("HOME") + "/python/pyTatry/data/photos/"

def saveFile(filename,data):
		f = open(filename,'w')
		f.write(data)
		f.close()

def createFileName(sufix):
		now = datetime.datetime.now()
		return format(now.year,'02') + "." + \
					format(now.month,'02') + "." + \
					format(now.day,'02') + "_" + \
					format(now.hour,'02') + ":" + \
					format(now.minute,'02') + sufix


print "Morskie oko 1."
response = urllib2.urlopen('http://kamery.topr.pl/moko/moko_01.jpg')
saveFile(photosFolder + "moko1/" + createFileName('.jpg'), response.read())

print "Morskie oko 2."
response = urllib2.urlopen('http://kamery.topr.pl/moko_TPN/moko_02.jpg')
saveFile(photosFolder + "moko2/" +createFileName('.jpg'), response.read())

print "Dolina 5 stawów."
response = urllib2.urlopen('http://kamery.topr.pl/stawy2/stawy2.jpg')
saveFile(photosFolder + "5stawow/" +createFileName('.jpg'), response.read())

print "Buczynowa dolinka."
response = urllib2.urlopen('http://kamery.topr.pl/stawy1/stawy1.jpg')
saveFile(photosFolder + "buczynowa/" +createFileName('.jpg'), response.read())

print "Gąsienicowa dolina."
response = urllib2.urlopen('http://kamery.topr.pl/gasienicowa/gasie.jpg')
saveFile(photosFolder + "gasienicowa/" +createFileName('.jpg'), response.read())

print "Goryczkowa dolina."
response = urllib2.urlopen('http://kamery.topr.pl/goryczkowa/gorycz.jpg')
saveFile(photosFolder + "goryczkowa/" +createFileName('.jpg'), response.read())

print "Chochołowska dolina."
response = urllib2.urlopen('http://kamery.topr.pl/chocholowska/chocholow.jpg')
saveFile(photosFolder + "chocholowska/" +createFileName('.jpg'), response.read())

print "Meteogram."
response = urllib2.urlopen('http://new.meteo.pl/um/metco/mgram_pict.php?ntype=0u&fdate=2015012806&row=487&col=232&lang=pl')
saveFile(photosFolder + "meteo/" +createFileName('.png'), response.read())


