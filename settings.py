#!/usr/bin/python
# -*- coding: utf-8 -*-
import functions, os, urllib2, re, math, datetime, sqlite3

# Zmienne developerskie
DEBUG = 0

# Pozbywanie się HTML z tekstu
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class webCamera:
		
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

# Klasa do przechowywania pomiarów                            
class cMeasurement:

		def __init__(self, newLoc, newMoment, newDesc, newPatterns, newValue = ""):
                                self.localization = newLoc
                                self.moment       = newMoment
                                self.desc         = newDesc
                                # Ponieważ pomiar zazwyczaj uzyskujemy za pomocą przeszukiwania treści dokumentu
                                # wyrażeniami regularnymi, dlatego też dodajemy listę wyrażen, których będziemy używać
                                # aby wydobyć pomiar.
                                self.patterns     = newPatterns
                                self.value        = newValue

                def sqlFormat(self):
                                return (self.localization, self.moment, self.desc, self.value)

                def str(sefl):
                                return str(self.localization) +  str(self.moment) + str(self.desc) + str(self.value)



class htmlMeasurments:
		
		def __init__(self, newLink, newMeasurments = [] ):
				self.link  	    = newLink
				self.text           = ""
                                self.measurments    = newMeasurments
                                self.coding         = "utf-8"
		
                "Pobiera dokument o adresie wskazanym przez self.link z internetu."                
		def fetchData(self):
				#odczytujemy stronę www i wyszukujemy pattern
				response 			= urllib2.urlopen(self.link)
				self.text			= response.read().replace("\n","")
                                #Sprawdzamy kodowanie strony www
                                result = re.search("charset=[a-zA-Z0-9\-]*",self.text) # pierwszy filtr
                                if (result != None):
                                    #nadpisujemy kodowanie
                                    self.coding = result.group(0)[8:]

                "Ustawia ręcznie treść dokumentu."                
                def setData(self, newContent):
				self.text			= newContent

            
                "Filtruje treść dokumentu dla każdego zestawu wzorców. Odczytane \
                 wartości zapisuje w słowniku self.results."
		def doFiltering(self):
                                for measurement in self.measurments:
                                    result = self.text
                                    # Przechodzimy przez wszystkie filtry
                                    for filtr in measurement.patterns:
                                        #print "Filtr:" + filtr
                                        result = re.search(filtr, result )
                                        if (result != None):
                                            result = result.group(0)
                                        else:
                                            result = ""
                                        #print "Result:" + result
                                    # Po filtrowaniu mamy w końcu rezultat który zapisujemy jako pomiar
                                    measurement.value = strip_tags(result).decode(self.coding)


		def freeMemory(self):
				self.text	    = ""
				self.results       = {}

class searchedPhoto(webCamera):
		
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

"Zdjęcie generowane z tekstu"
class generatedPhoto(webCamera):
		
		def fetchData(self):
				os.system("convert -background black -fill '#FFFFFF' -pointsize 72 label:'"+self.nazwa+"' tmp.jpg")
				data = functions.loadFile("tmp.jpg")
				os.unlink("tmp.jpg")
				return [ data ]




"Kraina geograficzna"
class geographicRegion:
		
		def __init__(self,n="beznazwy",f="./",k=[],  nowePomiary = [], ext = ".jpg"):
				self.nazwa 	    	= n
				self.folder 		= f
				self.listaKamer		= k
                                self.listaPomiarow      = nowePomiary
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
				#print command
				os.system(command)
						
class cDatabase:
            def __init__(self, newDatabaseFile):
                self.databaseFile = newDatabaseFile
                self.conn         = sqlite3.connect(self.databaseFile)
                self.conn.execute("create table if not exists pomiary ( localization text, \
						                        moment DATETIME, \
                                                desc text, \
                						        value text)")
                self.conn.commit()

            def addMeasurment(self, args):
                self.conn.execute('INSERT INTO pomiary VALUES (?,?,?,?)', args);


            def close(self):
                self.conn.commit()
                self.conn.close()
                print "Baza danych zapisana i zamknięta."


# ŚCIEŻKI I KATALOGI				
################################################################################
scriptFolder = os.path.dirname(os.path.realpath(__file__))
photosFolder = scriptFolder + "/data/photos/"

# ZMIENNE GLOBALNE
################################################################################
actualDate      = functions.createFileName('')
thisMoment      = unicode( str( datetime.datetime.now() )[:19]) # Zapamiętujemy czas połączenia, bez milisekund.
allFileName     = photosFolder + "tatry/" + actualDate
databaseFile 	= os.getenv("HOME") + "/python/pyTatry/data/database.db"

if (DEBUG==1):
    testDocument = htmlMeasurments("http://www.test.tatrynet.pl/pogoda/weatherMiddleware_v1.0/xml/lokalizacje1.xml",
                                [
                                cMeasurement("Morskie Oko",actualDate,"temperatura",["MORSKIE OKO.*?</temperatura>", "<aktualna>.*</aktualna>"]),
                                cMeasurement("Pięć Stawów",actualDate,"temperatura",["PIEC STAWOW.*?</temperatura>", "<aktualna>.*</aktualna>"]),
                                cMeasurement("Goryczkowa",actualDate,"temperatura",["GORYCZKOWA.*?</temperatura>", "<aktualna>.*</aktualna>"]),
                                
                                cMeasurement("Morskie Oko",actualDate,"wiatr",["MORSKIE OKO.*?</wiatr>", "<silaAvg>.*</silaAvg>"]),
                                cMeasurement("Pięć Stawów",actualDate,"wiatr",["PIEC STAWOW.*?</wiatr>", "<silaAvg>.*</silaAvg>"]),
                                cMeasurement("Goryczkowa",actualDate,"wiatr",["GORYCZKOWA.*?</wiatr>", "<silaAvg>.*</silaAvg>"])
                                ])
    testDocument.fetchData()
    testDocument.doFiltering()
    for m in testDocument.measurments:
        print m.desc
        print m.localization
        print m.moment
        print m.value
    
    #testDocument = htmlMeasurments("http://www.topr.pl/",
                                #[ cMeasurement("tatry",actualDate,"rozwojZagrozenia",['Przewidywany rozwój.*?Zobacz cały','<p.*?</p'] ) ]
                                #)
    #testDocument.fetchData()
    #testDocument.doFiltering()
    #for m in testDocument.measurments:
        #print m.desc
        #print m.localization
        #print m.moment
        #print m.value
else:

    # kamery w Tatrach
    kameryTatry = []
    kameryTatry.append( webCamera("Morskie Oko 1", "http://kamery.topr.pl/moko/moko_01.jpg", 				"moko1/" ) )
    kameryTatry.append( webCamera("Morskie Oko 2", "http://kamery.topr.pl/moko_TPN/moko_02.jpg", 			"moko2/" ) )
    kameryTatry.append( webCamera("Dol 5 stawów", "http://kamery.topr.pl/stawy2/stawy2.jpg", 				"5stawow/" ) )
    kameryTatry.append( webCamera("Buczynowa dolinka", "http://kamery.topr.pl/stawy1/stawy1.jpg", 			"buczynowa/" ) )
    kameryTatry.append( webCamera("Hala gąsienicowa", "http://kamery.topr.pl/gasienicowa/gasie.jpg", 		"gasienicowa/" ) )
    kameryTatry.append( webCamera("Goryczkowa", "http://kamery.topr.pl/goryczkowa/gorycz.jpg", 				"goryczkowa/" ) )
    kameryTatry.append( webCamera("Dol Chochołowska", "http://kamery.topr.pl/chocholowska/chocholow.jpg", 	"chocholowska/" ) )
    kameryTatry.append( searchedPhoto( "Stopień zagrożenia lawinowego", "http://www.topr.pl/wwt/warunki-w-tatrach-2", 	"lawiny/", "_stopien.jpg", True, "images/stopnie.*jpg") )
    kameryTatry.append( searchedPhoto( "Wystawy niebezpieczne", "http://www.topr.pl/wwt/warunki-w-tatrach-2", 	"lawiny/", "_wystawy.jpg", True, "images\/kierunki\/[nesw]*\.jpg") )

    #pomiary w Tatrach
    pomiaryTatry = []
    pomiaryTatry.append( htmlMeasurments("http://www.topr.pl/wwt/warunki-w-tatrach-2",
                                [cMeasurement(u"tatry",thisMoment,u"stopien",['images/stopnie.*?jpg','[0-9]']),
                                 cMeasurement(u"tatry",thisMoment,u"informacjeDodatkowe",["Informacje dodatkowe.*?/span"])
                                ]) 
                        )
    pomiaryTatry.append( htmlMeasurments("http://www.topr.pl/",
                                [ cMeasurement(u"tatry",thisMoment,"rozwojZagrozenia",['Przewidywany rozwój.*?Zobacz cały','<p.*?</p'] ) ]
                                )
                        )
    pomiaryTatry.append( htmlMeasurments("http://www.test.tatrynet.pl/pogoda/weatherMiddleware_v1.0/xml/lokalizacje1.xml",
                                [
                                cMeasurement(u"Morskie Oko",thisMoment,u"temperatura",["MORSKIE OKO.*?</temperatura>", "<aktualna>.*</aktualna>"]),
                                cMeasurement(u"Pięć Stawów",thisMoment,u"temperatura",["PIEC STAWOW.*?</temperatura>", "<aktualna>.*</aktualna>"]),
                                cMeasurement(u"Goryczkowa",thisMoment,u"temperatura",["GORYCZKOWA.*?</temperatura>", "<aktualna>.*</aktualna>"]),
                                cMeasurement(u"Morskie Oko",thisMoment,u"wiatr",["MORSKIE OKO.*?</wiatr>", "<silaAvg>.*</silaAvg>"]),
                                cMeasurement(u"Pięć Stawów",thisMoment,u"wiatr",["PIEC STAWOW.*?</wiatr>", "<silaAvg>.*</silaAvg>"]),
                                cMeasurement(u"Goryczkowa",thisMoment,u"wiatr",["GORYCZKOWA.*?</wiatr>", "<silaAvg>.*</silaAvg>"])
                                ])
                        )

    #kamery w Karkonoszach
    kameryKarkonosze = []
    #kameryKarkonosze.append( webCamera("Śnieżka 1", "http://kamery.humlnet.cz/images/webcams/snezka1/640x480.jpg?", "sniezka1/", ".jpg") )
    kameryKarkonosze.append( webCamera("Śnieżka 2", "http://kamery.humlnet.cz/images/webcams/snezka2/640x480.jpg?", "sniezka2/", ".jpg") )
    kameryKarkonosze.append( webCamera("Śnieżka 3", "http://kamery.humlnet.cz/images/webcams/snezka3/640x480.jpg?", "sniezka3/", ".jpg") )
    kameryKarkonosze.append( webCamera("Piec pod śnieżką", "http://kamery.humlnet.cz/images/webcams/pecpodsnezkou/640x480.jpg?", "piec-pod-sniezka/", ".jpg") )
    kameryKarkonosze.append( webCamera("Karpacz stok lodowiec", "http://www.kamera.karpacz.pl/lodowiec.jpg", "karpacz-lodowiec/", ".jpg") )
    kameryKarkonosze.append( webCamera("Schronisko Lucni Buda", "http://portal.chmi.cz/files/portal/docs/meteo/kam/lucnibouda.jpg", "lucni-buda/", ".jpg") )
    kameryKarkonosze.append( webCamera("Szpindlerove", "http://kamery.humlnet.cz/images/webcams/medvedin/640x480.jpg?", "spindlerove/", ".jpg") )

    # Pogoda jest traktowana jako osobna kraina geograficzna, gdzie pobieramy pogodę z różnych miejsc Kraju
    # a następnie łączymy w kolaz
    kameryPogoda = []
    kameryPogoda.append( webCamera("Meteogram Zakopane", "http://new.meteo.pl/um/metco/mgram_pict.php?ntype=0u&row=487&col=232&lang=pl", "pogoda-zakopane/", ".png") )
    kameryPogoda.append( webCamera("Meteogram Karpacz", "http://new.meteo.pl/um/metco/mgram_pict.php?ntype=0u&row=444&col=158&lang=pl", "pogoda-karpacz/", ".png" ) )
    kameryPogoda.append( webCamera("Meteogram Szklarska poręba", "http://new.meteo.pl/um/metco/mgram_pict.php?ntype=0u&row=443&col=154&lang=pl", "pogoda-szklarska/", ".png" ) )
    kameryPogoda.append( generatedPhoto("Zakopane", "", "etykiety/", "_zakopane.jpg" ) )
    kameryPogoda.append( generatedPhoto("Karpacz", "", "etykiety/", "_karpacz.jpg" ) )
    kameryPogoda.append( generatedPhoto("Szklarska poręba", "", "etykiety/", "_szklarska.jpg" ) )

    # tworzymy krainy geograficzne
    tatry 		= geographicRegion("Tatry","tatry/",kameryTatry,pomiaryTatry)
    karkonosze 	        = geographicRegion("Karkonosze","karkonosze/",kameryKarkonosze)
    pogoda		= geographicRegion("Pogoda Polska","pogoda/",kameryPogoda)

    # tworzymy swiat
    swiat = []
    swiat.append(tatry)
    swiat.append(karkonosze)
    swiat.append(pogoda)

