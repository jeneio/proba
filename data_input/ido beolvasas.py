import csv
import pprint as pp

# fájlnév változatlan rész
path = 'C:\\Users\\Oszi\\Google Drive\\Diploma\\adatok\\eredeti\\hő\\M0_ho_20130901'


with open('.'.join([path, 'tim'])) as f:
    reader = csv.reader(f, delimiter="\t")
    t = list(reader)

# http://stackoverflow.com/questions/9637838/convert-string-date-to-timestamp-in-python
import time
import datetime
s = '2013-09-01 00:00:01'
print(time.mktime(datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S").timetuple()))
s = '2013-09-01 00:00:11'
print(time.mktime(datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S").timetuple()))


#a vizsgált időszak bevitele
x = input('Mettől vizsgáljam? ')

y = input('Meddig vizsgáljam? ')

k = t.FindIndex(x)
