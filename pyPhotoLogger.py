#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2, datetime

photosFolder = "./data/photos/"


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


#Moko 1
response = urllib2.urlopen('http://kamery.topr.pl/moko/moko_01.jpg')
saveFile(photosFolder + "moko1/" + createFileName('.jpg'), response.read())

#Moko 2
response = urllib2.urlopen('http://kamery.topr.pl/moko_TPN/moko_02.jpg')
saveFile(photosFolder + "moko2/" +createFileName('.jpg'), response.read())

#5 stawów
response = urllib2.urlopen('http://kamery.topr.pl/stawy2/stawy2.jpg')
saveFile(photosFolder + "5stawow/" +createFileName('.jpg'), response.read())

#buczynowa
response = urllib2.urlopen('http://kamery.topr.pl/stawy1/stawy1.jpg')
saveFile(photosFolder + "buczynowa/" +createFileName('.jpg'), response.read())

#gasienicowa
response = urllib2.urlopen('http://kamery.topr.pl/gasienicowa/gasie.jpg')
saveFile(photosFolder + "gasienicowa/" +createFileName('.jpg'), response.read())

#goryczkowa
response = urllib2.urlopen('http://kamery.topr.pl/goryczkowa/gorycz.jpg')
saveFile(photosFolder + "goryczkowa/" +createFileName('.jpg'), response.read())

#chocholowska
response = urllib2.urlopen('http://kamery.topr.pl/chocholowska/chocholow.jpg')
saveFile(photosFolder + "chocholowska/" +createFileName('.jpg'), response.read())

#Meteogram
response = urllib2.urlopen('http://new.meteo.pl/um/metco/mgram_pict.php?ntype=0u&fdate=2015012806&row=487&col=232&lang=pl')
saveFile(photosFolder + "meteo/" +createFileName('.png'), response.read())


