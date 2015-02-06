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

class zdjecieWyszukiwane(kameraInternetowa):
		
		def __init__(self,n,l,f, ext = ".jpg", pattern = ""):
				self.nazwa 	= n
				self.link  	= l
				self.folder = f
				self.rozszerzenie = ext
				self.wzorzec = pattern
		
		def fetchData(self):
				# lista z obrazami
				listaObrazow = []

				#odczytujemy stronę www z zagrożeniem lawinowym
				response 			= urllib2.urlopen(self.link)
				analizowanaTresc	= response.read()
				element  			= re.search(self.wzorzec, analizowanaTresc)
				#wystawy  			= re.search('images\/kierunki\/[nesw]*\.jpg', analizowanaTresc)

				#sciagamy obrazek zagrozenia ze strony TOPR'u
				if (element != None):
					response = urllib2.urlopen("http://www.topr.pl/" + element.group(0))
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
kameryTatry.append( kameraInternetowa("Meteogram Zakopane", "http://new.meteo.pl/um/metco/mgram_pict.php?ntype=0u&row=487&col=232&lang=pl", "pogoda-zakopane/", ".png" ) )
kameryTatry.append( zdjecieWyszukiwane( "Stopień zagrożenia lawinowego", "http://www.topr.pl/wwt/warunki-w-tatrach-2", 	"lawiny/", "stopien.jpg",  "images/stopnie.*jpg") )
kameryTatry.append( zdjecieWyszukiwane( "Wystawy niebezpieczne", "http://www.topr.pl/wwt/warunki-w-tatrach-2", 	"lawiny/", "wystawy.jpg", "images\/kierunki\/[nesw]*\.jpg") )

#kamery w Karkonoszach
kameryKarkonosze = []
kameryKarkonosze.append( kameraInternetowa("Meteogram Karpacz", "http://new.meteo.pl/um/metco/mgram_pict.php?ntype=0u&row=444&col=158&lang=pl", "pogoda-karpacz/", ".png" ) )
kameryKarkonosze.append( kameraInternetowa("Meteogram Szklarska poręba", "http://new.meteo.pl/um/metco/mgram_pict.php?ntype=0u&row=443&col=154&lang=pl", "pogoda-szklarska/", ".png" ) )

# tworzymy krainy geograficzne
tatry = krainaGeograficzna("Tatry","tatry/",kameryTatry)
karkonosze = krainaGeograficzna("Karkonosze","karkonosze/",kameryKarkonosze)

# tworzymy swiat
swiat = []
swiat.append(tatry)
swiat.append(karkonosze)


