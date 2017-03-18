import csv
import math

# listát létrehozni meglévő fájlból

# fájlnév változatlan rész
path = 'C:\\Users\\Oszi\\Google Drive\\Diploma\\adatok\\eredeti\\hő\\M0_ho_20130901'

# mérési adatok beolvasása
with open('.'.join([path, 'ret'])) as f:
    reader = csv.reader(f, delimiter="\t")
    d = list(reader)

ds = [list(x) for x in zip(*d)]  # transzponálás;http://stackoverflow.com/questions/21444338/transpose-nested-list-in-python
#átlag előállítása
import statistics as st
#átlag megadása
#x = input ('Mekkora átlagot vegyek? (db adat) ')
#x = int(x)
#for i in range (0,(x-1)):
#    y = (sum(ds[i]))/x
#print('átlag=',y)
#a listában szereplő allisták elemeinek számmá konvertálása
for y in ds:
    for z in y:
        float()
#ellenőrzés, hogy szám-e?
add = ds[0][0] + ds[0][1]
print(add)

#valamiért még mindig nem jó.. és szerintem ez a probémája amiért az átlagszámítás se fut.

#átlag számítása - Jakab Gábor
ATLAGOLT_HOSSZ = 2

#l = [1, 2, 3, 4, 5, 6]
_ret = (zip(*[iter(ds)]*ATLAGOLT_HOSSZ))

# a kapott listabol:
atl = [sum(x) / ATLAGOLT_HOSSZ for x in _ret]
print(atl)