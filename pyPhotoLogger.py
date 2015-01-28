#!/usr/bin/python
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
					format(now.day,'02') + " " + \
					format(now.hour,'02') + " " + \
					format(now.minute,'02') + " " + sufix


response = urllib2.urlopen('http://kamery.topr.pl/moko/moko_01.jpg')
saveFile(photosFolder + createFileName('moko.jpg'), response.read())


