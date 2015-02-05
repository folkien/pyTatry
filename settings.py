#!/usr/bin/python
# -*- coding: utf-8 -*-
import functions, os, urllib2, re, math

class kameraInternetowa:
		
		def __init__(self,n,l,f, ext = ".jpg"):
				self.nazwa 	= n
				self.link  	= l
				self.folder = f
				self.rozszerzenie = ext

		def fetchData(self):
				response = urllib2.urlopen(self.link)
				return [ response.read() ]

class stopienZagrozenia(kameraInternetowa):
		
		def fetchData(self):
				# lista z obrazami
				listaObrazow = []

				#odczytujemy stronę www z zagrożeniem lawinowym
				response 			= urllib2.urlopen(self.link)
				analizowanaTresc	= response.read()
				stopien  			= re.search('images/stopnie.*jpg', analizowanaTresc).group(0)
				wystawy  			= re.search('images\/kierunki\/[nesw]*\.jpg', analizowanaTresc).group(0)

				#sciagamy obrazek zagrozenia ze strony TOPR'u
				if (len(stopien)>0):
					response = urllib2.urlopen("http://www.topr.pl/" + stopien)
					listaObrazow.append(response.read())

				#sciagamy wystawy niebezpieczne
				if (len(stopien)>0):
					response = urllib2.urlopen("http://www.topr.pl/" + wystawy)
					listaObrazow.append(response.read())

				return listaObrazow

class krainaGeograficzna:
		
		def __init__(self,n="beznazwy",f="./",k=[], ext = ".jpg"):
				self.nazwa 			= n
				self.folder 		= f
				self.listaKamer		= k
				self.rozszerzenie 	= ext

		def kolazKamer(self):
				print "Zdjęcie całego dnia."
				#Mergowanie plikow
				command 	= "convert "
				photosNumber= len(self.listaKamer)
				sizex 		= math.ceil( math.sqrt( photosNumber ) ) 
				n 			= 0
				row 		= ""
				while (n < photosNumber):
						row += photosFolder + self.listaKamer[n].folder + actualDate + self.listaKamer[n].rozszerzenie + " "
						n += 1
						# Jezeli trzeba kończyć rząd to kończymy
						if (n%sizex == 0):
								command += "\( " + row + " +append \)  "
								row 	 = ""
				command += "-background none -append "+ photosFolder + self.folder + actualDate + self.rozszerzenie 
				print command
				os.system(command)
						


				#command =  "convert \( "+m1FileName+" "+m2FileName+" "+psFileName+" +append \) \
				#		  \( "+buFileName+" "+gaFileName+" "+goFileName+" +append \) \
				#		  \( "+chFileName+" +append \) \
				#		  -background none -append "+allFileName 
				#os.system(command)


# ścieżki i foldery w programie				
scriptFolder = os.path.dirname(os.path.realpath(__file__))
photosFolder = scriptFolder + "/data/photos/"

# Tworzymy nazwe pliku zgodnie z aktualna data
actualDate = functions.createFileName('')
allFileName= photosFolder + "tatry/" + actualDate


# kamery w Tatrach
kameryTatry = []
kameryTatry.append( kameraInternetowa("Morskie Oko 1", "http://kamery.topr.pl/moko/moko_01.jpg", 				"moko1/" ) )
kameryTatry.append( kameraInternetowa("Morskie Oko 2", "http://kamery.topr.pl/moko_TPN/moko_02.jpg", 			"moko2/" ) )
kameryTatry.append( kameraInternetowa("Dol 5 stawów", "http://kamery.topr.pl/stawy2/stawy2.jpg", 				"5stawow/" ) )
kameryTatry.append( kameraInternetowa("Buczynowa dolinka", "http://kamery.topr.pl/stawy1/stawy1.jpg", 			"buczynowa/" ) )
kameryTatry.append( kameraInternetowa("Hala gąsienicowa", "http://kamery.topr.pl/gasienicowa/gasie.jpg", 		"gasienicowa/" ) )
kameryTatry.append( kameraInternetowa("Goryczkowa", "http://kamery.topr.pl/goryczkowa/gorycz.jpg", 				"goryczkowa/" ) )
kameryTatry.append( kameraInternetowa("Dol Chochołowska", "http://kamery.topr.pl/chocholowska/chocholow.jpg", 	"chocholowska/" ) )
kameryTatry.append( kameraInternetowa("Meteogram", "http://new.meteo.pl/um/metco/mgram_pict.php?ntype=0u&row=487&col=232&lang=pl", "meteo/", ".png" ) )
kameryTatry.append( stopienZagrozenia( "Stopień zagrożenia lawinowego", "http://www.topr.pl/wwt/warunki-w-tatrach-2", 	"lawiny/" ) )

# tworzymy krainę tatr
tatry = krainaGeograficzna("Tatry","tatry/",kameryTatry)

# tworzymy swiat
swiat = []
swiat.append(tatry)


