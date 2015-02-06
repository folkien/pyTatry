#!/usr/bin/python
# -*- coding: utf-8 -*-
import functions, os, urllib2, re, math

class kameraInternetowa:
		
		def __init__(self,n,l,f, ext = ".jpg", isKolage = True ):
				self.nazwa 	= n
				self.link  	= l
				self.folder = f
				self.rozszerzenie = ext
				self.czyKolaz = isKolage
				self.pobrano = False

		def fetchData(self):
				response = urllib2.urlopen(self.link)
				self.pobrano = True
				return [ response.read() ]

class zdjecieWyszukiwane(kameraInternetowa):
		
		def __init__(self,n,l,f, ext = ".jpg", isKolage = True, pattern = ""):
				self.nazwa 	= n
				self.link  	= l
				self.folder = f
				self.rozszerzenie = ext
				self.czyKolaz = isKolage
				self.wzorzec = pattern
				self.pobrano = False
		
		def fetchData(self):
				# lista z obrazami
				listaObrazow = []

				#odczytujemy stronę www z zagrożeniem lawinowym
				response 			= urllib2.urlopen(self.link)
				analizowanaTresc	= response.read()
				element  			= re.search(self.wzorzec, analizowanaTresc)

				#sciagamy obrazek zagrozenia ze strony TOPR'u
				if (element != None):
					response = urllib2.urlopen("http://www.topr.pl/" + element.group(0))
					listaObrazow.append(response.read())
				else:
					self.czyKolaz = False

				# Zaznaczenie ze pobrano dane za kamery
				self.pobrano = True

				return listaObrazow

class generowaneZdjecie(kameraInternetowa):
		

		def fetchData(self):
				os.system("convert -background black -fill '#FFFFFF' -pointsize 72 label:'"+self.nazwa+"' tmp.jpg")
				data = functions.loadFile("tmp.jpg")
				os.unlink("tmp.jpg")
				return [ data ]





class krainaGeograficzna:
		
		def __init__(self,n="beznazwy",f="./",k=[], ext = ".jpg"):
				self.nazwa 			= n
				self.folder 		= f
				self.listaKamer		= k
				self.rozszerzenie 	= ext

		def listaKamerDoKolazu(self):
				kameryDoKolazu = []
				for kamera in self.listaKamer:
						if (kamera.czyKolaz == True):
								kameryDoKolazu.append( kamera )
				return kameryDoKolazu

		def kolazKamer(self):
				print "Zdjęcie całego dnia."
				kameryDoKolazu = self.listaKamerDoKolazu()

				#Mergowanie plikow
				command 	= "convert "
				photosNumber= len(kameryDoKolazu)
				sizex 		= int(math.ceil( math.sqrt( photosNumber ) )) 
				n 			= 0
				row 		= ""
				while (n < photosNumber):
						row += photosFolder + kameryDoKolazu[n].folder + actualDate + kameryDoKolazu[n].rozszerzenie + " "
						n += 1
						# Jezeli trzeba kończyć rząd to kończymy
						if (n%sizex == 0):
								command += "\( " + row + " +append \)  "
								row 	 = ""
				#Sprawdzamy czy nie zostało nam coś do dopisania
				if (len(row)>0):
					command += "\( " + row + " +append \)  "
				#Kończymy polecenie
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
kameryTatry.append( zdjecieWyszukiwane( "Stopień zagrożenia lawinowego", "http://www.topr.pl/wwt/warunki-w-tatrach-2", 	"lawiny/", "_stopien.jpg", True, "images/stopnie.*jpg") )
kameryTatry.append( zdjecieWyszukiwane( "Wystawy niebezpieczne", "http://www.topr.pl/wwt/warunki-w-tatrach-2", 	"lawiny/", "_wystawy.jpg", True, "images\/kierunki\/[nesw]*\.jpg") )

#kamery w Karkonoszach
kameryKarkonosze = []
#kameryKarkonosze.append( kameraInternetowa("Śnieżka 1", "http://kamery.humlnet.cz/images/webcams/snezka1/640x480.jpg?", "sniezka1/", ".jpg") )
kameryKarkonosze.append( kameraInternetowa("Śnieżka 2", "http://kamery.humlnet.cz/images/webcams/snezka2/640x480.jpg?", "sniezka2/", ".jpg") )
kameryKarkonosze.append( kameraInternetowa("Śnieżka 3", "http://kamery.humlnet.cz/images/webcams/snezka3/640x480.jpg?", "sniezka3/", ".jpg") )
kameryKarkonosze.append( kameraInternetowa("Piec pod śnieżką", "http://kamery.humlnet.cz/images/webcams/pecpodsnezkou/640x480.jpg?", "piec-pod-sniezka/", ".jpg") )


# Pogoda jest traktowana jako osobna kraina geograficzna, gdzie pobieramy pogodę z różnych miejsc Kraju
# a następnie łączymy w kolaz
kameryPogoda = []
kameryPogoda.append( kameraInternetowa("Meteogram Zakopane", "http://new.meteo.pl/um/metco/mgram_pict.php?ntype=0u&row=487&col=232&lang=pl", "pogoda-zakopane/", ".png") )
kameryPogoda.append( kameraInternetowa("Meteogram Karpacz", "http://new.meteo.pl/um/metco/mgram_pict.php?ntype=0u&row=444&col=158&lang=pl", "pogoda-karpacz/", ".png" ) )
kameryPogoda.append( kameraInternetowa("Meteogram Szklarska poręba", "http://new.meteo.pl/um/metco/mgram_pict.php?ntype=0u&row=443&col=154&lang=pl", "pogoda-szklarska/", ".png" ) )
kameryPogoda.append( generowaneZdjecie("Zakopane", "", "etykiety/", "_zakopane.jpg" ) )
kameryPogoda.append( generowaneZdjecie("Karpacz", "", "etykiety/", "_karpacz.jpg" ) )
kameryPogoda.append( generowaneZdjecie("Szklarska poręba", "", "etykiety/", "_szklarska.jpg" ) )


# tworzymy krainy geograficzne
tatry 		= krainaGeograficzna("Tatry","tatry/",kameryTatry)
karkonosze 	= krainaGeograficzna("Karkonosze","karkonosze/",kameryKarkonosze)
pogoda		= krainaGeograficzna("Pogoda Polska","pogoda/",kameryPogoda)


# tworzymy swiat
swiat = []
swiat.append(tatry)
swiat.append(karkonosze)
swiat.append(pogoda)


