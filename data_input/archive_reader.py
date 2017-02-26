# -*- coding: utf-8 -*-

import csv
import pprint as pp

# fájlnév változatlan rész
path = 'C:\\Users\\X250-User\\Downloads\\ho\\M0_ho_20130901'

# mérési adatok beolvasása
with open('.'.join([path, 'ret'])) as f:
    reader = csv.reader(f, delimiter="\t")
    d = list(reader)
ds = [list(x) for x in zip(*d)]  # transzponálás;http://stackoverflow.com/questions/21444338/transpose-nested-list-in-python
# konverzió string -> float
_ds = []
for d in ds:
    _ds.append([float(x) for x in d])
#alternatíva, for-for
# _ds = []
# for d in ds:
#     _ = []
#     for x in d:
#         _.append(float(x))
#     _ds.append(_)
#

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

# megjelenítés: matplotlib, py

# http://stackoverflow.com/questions/13728392/moving-average-or-running-mean
# http://www.excel-easy.com/examples/moving-average.html
def running_mean(l, N):
    sum = 0
    result = list( 0 for x in l)

    for i in range( 0, N ):
        sum = sum + l[i]
        result[i] = sum / (i+1)

    for i in range( N, len(l) ):
        sum = sum - l[i-N] + l[i]
        result[i] = sum / N

    return result

for d in _ds:
    _ret = running_mean(d, 100)
    pp.pprint(_ret)
    print(len(_ret))

    mi
