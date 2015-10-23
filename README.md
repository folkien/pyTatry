# pyTatry

Logger historii i pogody w polskich tatrach. Za pomocą tego zestawu skryptów
napisanych w Pythonie oraz zadań cron'a, możemy rejestrować obraz z kamer
topr na dysku, tworzyć z nich mozaikę oraz tworzyć własną bazę danych temperatur
podawanych przez TOPR oraz zagrożenia lawinowego. Taka baza jest przechowywana
za pomocą sqlite3 i może być bezpośrednio exportowana do .xlsx oraz .csv.

# TODO

- Dodać analizę godziny wschodu i zachodu, tak aby nie robić photo w nocy
- Postawić skrypt na linuxowym serwerze ze stałym dostępem do netu, uruchomionym
24h/dobę,
- Stworzyć aplikację webową do wyświetlania danych i przeglądania zdjęć,
- Poprawić export do XLS,
- Dodać Ślęże,
- Dodać Śnieżnik,
- Dodać analizę zdjęć i na tej podstawie oceniać widzialność i zapisywać w bazie
- Schronisko górskie orzeł http://www.orzel.info.pl/okno.php?file=kamera/stacja.jpg&title=Orze%C5%82&desc=Obraz

# Wymagania
- python 2.7
- python-xlsxwriter
- ImageMagick - przede wszystkim polecenie Convert.
- Cron, jeżeli chcemy zautomatyzować wywoływanie skryptów.

# Opis poleceń

# Uruchamianie z Cron'em

Aby uruchamiać skrypt co pół godziny należy dodać do crontab

0,30 * * * * /usr/bin/python scieżkaDoPobranegoRepozytorium/pyLogger.py 

Aby uruchamiać skrypt o każdej pełnej godzinie(np 10:00, 11:00 etc) należy dodać

0 * * * * /usr/bin/python scieżkaDoPobranegoRepozytorium/pyLogger.py 
