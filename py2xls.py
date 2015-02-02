#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2, datetime, sqlite3, os, argparse
from xml.dom import minidom
import xlsxwriter


lokalizacje = { "MORSKIE OKO": 0,
                "GORYCZKOWA" : 2,
                "PIEC STAWOW" : 4,
				"tatry"		  : 6
}

atrybuty = { "temperatura": 1,
             "wiatr" 	  : 2,
			 "lawiny" 	  : 3,
}


#parser = argparse.ArgumentParser()
#parser.add_argument("-i", "--inputfile", 	type=str, 		 		required=False)
#parser.add_argument("-o", "--outputfile", 	type=str, 		 		required=False)
#parser.add_argument("-k", "--keyfile", 		type=str, 		 		required=False)
#parser.add_argument("-c", "--crypt", 		action='store_true', 	required=False)
#parser.add_argument("-n", "--newkey", 		type=int, 				required=False)
#args = parser.parse_args()

databaseFile = os.getenv("HOME") + "/python/pyTatry/data/database.db"
dataFolder = "./data/"

def saveFile(filename,data):
		f = open(filename,'w')
		f.write(data)
		f.close()

def createFileName(sufix):
		now = datetime.datetime.now()
		return  format(now.year,'02') + "." + \
                        format(now.month,'02') + "." + \
                        format(now.day,'02') + "_" + \
                        format(now.hour,'02')  + \
                        format(now.minute,'02') +  sufix

# Create an new Excel file and add a worksheet.
workbook = xlsxwriter.Workbook(dataFolder + createFileName('.xlsx'))
worksheet = workbook.add_worksheet()

# Widen the first column to make the text clearer.
#worksheet.set_column('A:A', 20)

# Add a bold format to use to highlight cells.
#bold = workbook.add_format({'bold': True})

# Write some simple text.
#worksheet.write('A1', 'Hello')

# Text with formatting.
#worksheet.write('A2', 'World', bold)

# Write some numbers, with row/column notation.
#worksheet.write(2, 0, 123)
#worksheet.write(3, 0, 123.456)

# Insert an image.
#worksheet.insert_image('B5', 'logo.png')


# Zapis nagłówka, jak poniżej.
# 
#   0  |    1        2           3           4       5
#      | Morskie Oko |         | 5 Stawów |        | Goryczkowa |
# Czas | Temp        | Wiatr   | Temp     | Wiatr  | Temp       | Wiatr  
#
#pierwszy rzad nagłówka
worksheet.write(0, 1, u"Morskie oko")
worksheet.write(0, 3, u"Goryczkowa")
worksheet.write(0, 5, u"5 Stawów")
#drugi rząd nagłówka
worksheet.write(1, 0, u"Czas[data]")
worksheet.write(1, 1, u"Temperatura[C]")
worksheet.write(1, 3, u"Temperatura[C]")
worksheet.write(1, 5, u"Temperatura[C]")
worksheet.write(1, 2, u"Wiatr[m/s]")
worksheet.write(1, 4, u"Wiatr[m/s]")
worksheet.write(1, 6, u"Wiatr[m/s]")

# Łączymy się z bazą danych.
row = 1
lastTime = ""
conn = sqlite3.connect(databaseFile)
for record in conn.execute("SELECT * FROM pomiary ORDER BY moment ASC"):
    print record

    locPos = lokalizacje[record[0]]
    atrPos = atrybuty[record[2]]
    # Dla nowego czasu zwiększamy rząd i zapisujemy czas.
    if (lastTime != record[1]):
			lastTime = record[1]
			row +=1
			worksheet.write_datetime(row, 0, datetime.datetime.strptime(record[1], '%Y-%m-%d %H:%M:%S'))
    
    worksheet.write(row, locPos+atrPos, record[3])


    #worksheet.write(2, 0, 123)

#Zamykamy zapisany arkusz
workbook.close()

#Zapis danych i zamknięcie bazydanych.
conn.commit()
conn.close()
print "Baza danych zapisana i zamknięta."
