import csv
import pprint as pp

# fájlnév változatlan rész
path = 'C:\\Users\\Oszi\\Desktop\\adatok\\eredeti\\hő\\M0_ho_20130901'
#path = 'C:\\Users\\X250-User\\Downloads\\ho\\M0_ho_20130901'

with open('.'.join([path, 'tim'])) as f:
    reader = csv.reader(f, delimiter="\t")
    t = list(reader)

# t egy nested list (-> google it!) ezert elotte ki kell bontani, hogy egy sima ("flat" list legyen)
import itertools
t = list(itertools.chain.from_iterable(t))

print(t[1])  # ez mar egy string



#a vizsgált időszak bevitele
xb = input('Mettől vizsgáljam? ')
xb = str(xb)

yb = input('Meddig vizsgáljam? ')
yb = str(yb)

import pprint as pp
# pp.pprint(t)

#a kezdő időpont sorszáma a listában (ez kell majd ahhoz, hogy tudjam melyik sor tartozik hőmérsékleti adatsorból az időponthoz)
#t1 = t.index(x)
#t2 = t.index(y)

#print(t1, t2)

# mi van ha nincs ilyen idopont?

# pelda:
# 2013-09-01 00:00:11
# Mettől vizsgáljam? 2013-09-01 00:00:11
# 2013-09-01 00:00:11
# Meddig vizsgáljam? 2013-09-01 00:03:02
# 1 18


#nincs a keresett időpont, ezért a legközelebbi megkeresése
# # http://stackoverflow.com/questions/9637838/convert-string-date-to-timestamp-in-python
import time
import datetime
#kezdő és végidőpontok számmá konvertálása
x_szammal = time.mktime(datetime.datetime.strptime(xb, "%Y-%m-%d %H:%M:%S").timetuple())
y_szammal = time.mktime(datetime.datetime.strptime(yb, "%Y-%m-%d %H:%M:%S").timetuple())
#t listában szereplő időpontok konvertálása számmá
t_szammal = [time.mktime(datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S").timetuple()) for x in t]
#megtalálni x-hez, y-hoz (számformátumban) legközelebbi időpontot (számformátumban)
x1 = min(t_szammal, key=lambda x:abs(x-x_szammal)) #http://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value
y1 = min(t_szammal, key=lambda x:abs(x-y_szammal))

#sorszámuk a listában
t1 = t_szammal.index(x1)
t2 = t_szammal.index(y1)

print(t1, t2)
#erre a két értékre lesz szükségünk szerintem, ezt kell majd felhasználnunk a többi fájlban


#adott dátum milyen napra esett
#http://stackoverflow.com/questions/9847213/which-day-of-week-given-a-date-python
def weekDay(year, month, day):
    offset = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    week   = ['Sunday',
              'Monday',
              'Tuesday',
              'Wednesday',
              'Thursday',
              'Friday',
              'Saturday']
    afterFeb = 1
    if month > 2: afterFeb = 0
    aux = year - 1700 - afterFeb
    # dayOfWeek for 1700/1/1 = 5, Friday
    dayOfWeek  = 5
    # partial sum of days betweem current date and 1700/1/1
    dayOfWeek += (aux + afterFeb) * 365
    # leap year correction
    dayOfWeek += aux / 4 - aux / 100 + (aux + 100) / 400
    # sum monthly and day offsets
    dayOfWeek += offset[month - 1] + (day - 1)
    dayOfWeek %= 7
    dayOfWeek = int(dayOfWeek) #ezt én raktam hozzá, mert float-nak érzékelte. a problémája így megoldódott
    return dayOfWeek, week[dayOfWeek]

print (weekDay(2013, 9, 1))
