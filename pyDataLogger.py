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
					format(now.day,'02') + " " + \
					format(now.hour,'02') + " " + \
					format(now.minute,'02') + " " + sufix

# Temperatury pobieramy stąd
# 


from xml.dom import minidom
response = urllib2.urlopen('http://www.test.tatrynet.pl/pogoda/weatherMiddleware_v1.0/xml/lokalizacje1.xml')
xmldoc = minidom.parseString(response.read())
print xmldoc
#itemlist = xmldoc.getElementsByTagName('item') 
#print len(itemlist)
#print itemlist[0].attributes['name'].value
#for s in itemlist :
#    print s.attributes['name'].value
