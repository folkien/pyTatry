#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2, datetime, sqlite3, os, argparse
import xlsxwriter, functions
from xml.dom import minidom


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

# Create an new Excel file and add a worksheet.
workbook = xlsxwriter.Workbook(dataFolder + functions.createFileName('.xlsx'))
# Add an Excel date format.
date_format = workbook.add_format({'num_format': 'mmmm d yyyy hh:mm'})

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
#   0A  |    1B        	  2C          3D        4E       5F 		 6G			7H
#       | Morskie Oko |         | 5 Stawów |        | Goryczkowa |        | Zagrożenie lawinowe
# Czas  | Temp        | Wiatr   | Temp     | Wiatr  | Temp       | Wiatr  |
#
#pierwszy rzad nagłówka
worksheet.write(0, 1, u"Morskie oko")
worksheet.write(0, 3, u"Goryczkowa")
worksheet.write(0, 5, u"5 Stawów")
worksheet.write(0, 7, u"Zagrożenie lawinowe")
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
			worksheet.write_datetime(row, 0, datetime.datetime.strptime(record[1], '%Y-%m-%d %H:%M:%S'), date_format)
    
    worksheet.write(row, locPos+atrPos, record[3])

#Dodajemy wykres temperatur dla wszystkich miejsc
lastRow = str(row)
chart = workbook.add_chart({'type' : 'line'})
chart.add_series({
	'name':		  '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$3:$A$' + lastRow,
    'values':     '=Sheet1!$B$3:$B$' + lastRow,
})
chart.add_series({
	'name':		  '=Sheet1!$D$1',
    'categories': '=Sheet1!$A$3:$A$' + lastRow,
    'values':     '=Sheet1!$D$3:$D$' + lastRow,
})
chart.add_series({
	'name':		  '=Sheet1!$F$1',
    'categories': '=Sheet1!$A$3:$A$' + lastRow,
    'values':     '=Sheet1!$F$3:$F$' + lastRow,
})
chart.set_title({
    'name': 'Temperatury [C]',
    'name_font': {
        'name': 'Calibri',
        'color': 'blue',
    },
})
worksheet.insert_chart('J4',chart)


#Zamykamy zapisany arkusz
workbook.close()

#Zapis danych i zamknięcie bazydanych.
conn.commit()
conn.close()
print "Baza danych zapisana i zamknięta."
