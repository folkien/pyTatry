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
conn = sqlite3.connect(databaseFile)
for row in conn.execute("SELECT * FROM pomiary WHERE desc = 'wiatr' AND localization = ''"):
    print row[3]


#Zapis danych i zamknięcie bazydanych.
conn.commit()
conn.close()
print "Baza danych zapisana i zamknięta."
