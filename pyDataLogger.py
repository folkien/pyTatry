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
conn = sqlite3.connect('./data/database.db')
#Tworzymy tabele jeżeli nie istnieje
conn.execute("create table if not exists pomiary ( localization text, \
						   moment DATETIME, desc text,    \
						   value real)")
conn.commit()

# Łączenie się ze stroną xml poprzez HTTP.
thisMoment = str( datetime.datetime.now() )[:19] # Zapamiętujemy czas połączenia, bez milisekund.
response = urllib2.urlopen('http://www.test.tatrynet.pl/pogoda/weatherMiddleware_v1.0/xml/lokalizacje1.xml')
xmldoc = minidom.parseString(response.read())

for node in xmldoc.getElementsByTagName('lokalizacja'):  # visit every node
        nazwa = str(node.getElementsByTagName("nazwa")[0].childNodes[0].toxml())
        print nazwa

        #Zapis temperatury do bazy
        try :
            args = (nazwa,                                                                                                          \
                    thisMoment,                                                                                                     \
                    "temperatura",                                                                                                  \
                    float(node.getElementsByTagName("temperatura")[0].getElementsByTagName("aktualna")[0].childNodes[0].toxml()),   \
                    )
            # Zapisujemy dane do bazy danych
            conn.execute('INSERT INTO pomiary VALUES (?,?,?,?)', args);
            print "-Zapis danych temperatury."
        except: 
            print "-Brakuje temperatury, coś się zepsuło!"
        
        #Zapis wiatru do bazy
        try :
            args = (nazwa,                                                                                                          \
                    thisMoment,                                                                                                     \
                    "wiatr",                                                                                                        \
                    float(node.getElementsByTagName("wiatr")[0].getElementsByTagName("silaAvg")[0] .childNodes[0].toxml()),   \
                    )
            # Zapisujemy dane do bazy danych
            conn.execute('INSERT INTO pomiary VALUES (?,?,?,?)', args);
            print "-Zapis danych wiatru."
        except: 
            print "-Brakuje wiatru, coś się zepsuło!"

#Zapis danych i zamknięcie bazydanych.
conn.commit()
conn.close()
print "Baza danych zapisana i zamknięta."
