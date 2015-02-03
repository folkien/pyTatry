#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2, datetime, sqlite3, os, re
import functions
from xml.dom import minidom

databaseFile 	= os.getenv("HOME") + "/python/pyTatry/data/database.db"

# Łączymy się z bazą danych.
conn = sqlite3.connect(databaseFile)
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

#Zapis stopnia zagrożenia lawinowego
print "Stopień zagrożenia lawinowego."
#odczytujemy stronę www z zagrożeniem lawinowym
response = urllib2.urlopen('http://www.topr.pl/wwt/warunki-w-tatrach-2')
stopien  = re.search('[0-9]',re.search('images/stopnie.*jpg',response.read()).group(0) ).group(0)
#zapisujemy dane do bazy
args = ("tatry",                \
	thisMoment,                 \
	"lawiny",                   \
	stopien, 				  	\
	)
# Zapisujemy dane do bazy danych
conn.execute('INSERT INTO pomiary VALUES (?,?,?,?)', args);



#Zapis danych i zamknięcie bazydanych.
conn.commit()
conn.close()
print "Baza danych zapisana i zamknięta."
