#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2, datetime, sqlite3, os
from xml.dom import minidom

databaseFile = os.getenv("HOME") + "/python/pyTatry/data/database.db"

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


# Łączymy się z bazą danych.
conn = sqlite3.connect('example.db')
#Tworzymy tabele jeżeli nie istnieje
conn.execute("create table if not exists data ( id integer, localization text, \
												moment DATETIMe, desc text,    \
												value real)")
conn.commit()


response = urllib2.urlopen('http://www.test.tatrynet.pl/pogoda/weatherMiddleware_v1.0/xml/lokalizacje1.xml')
xmldoc = minidom.parseString(response.read())
#print xmldoc
for node in xmldoc.getElementsByTagName('lokalizacja'):  # visit every node
	print node.getAttribute("id")
	print node.getElementsByTagName("temperatura")[0].getElementsByTagName("aktualna")[0].childNodes[0].toxml()

#Zapis danych i zamknięcie bazydanych.
conn.commit()
conn.close()
