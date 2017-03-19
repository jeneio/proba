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
x = input('Mettől vizsgáljam? ')
x = str(x)
print (x)
y = input('Meddig vizsgáljam? ')
y = str(y)

import pprint as pp
# pp.pprint(t)

#a kezdő időpont sorszáma a listában (ez kell majd ahhoz, hogy tudjam melyik sor tartozik hőmérsékleti adatsorból az időponthoz)
t1 = t.index(x)
t2 = t.index(y)

print(t1, t2)

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
print(time.mktime(datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S").timetuple()))
#t listában szereplő időpontok konvertálása számmá
t_szammal = [time.mktime(datetime.datetime.strptime(y, "%Y-%m-%d %H:%M:%S").timetuple()) for x in t]
print (t_szammal[2])
#megtalálni x-hez (számformátumban) legközelebbi időpontot (számformátumban)