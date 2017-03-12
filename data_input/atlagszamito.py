import csv
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
x = input ('Mekkora átlagot vegyek? (db adat) ')
x = int(x)
for i in range (0,(x-1)):
    y = (sum(ds[i]))/x

print('átlag=',y)

