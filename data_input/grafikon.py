import csv

# fájlnév változatlan rész
# path = 'C:\\Users\\X250-User\\Downloads\\ho\\M0_ho_20130901'
path = 'C:\\Users\\Oszi\\Desktop\\adatok\\eredeti\\hő\\M0_ho_20130901'

# mérési adatok beolvasása
with open('.'.join([path, 'ret'])) as f:
    reader = csv.reader(f, delimiter="\t")
    d = list(reader)

ds = [list(x) for x in zip(*d)]  # transzponálás;http://stackoverflow.com/questions/21444338/transpose-nested-list-in-python

szenzor_1 = []
szenzor_1.append(ds[0])

print (ds[0])

#listaátalakítás
#import itertools
#ds = list(itertools.chain.from_iterable(ds))
#kiválasztani minden 4. elemet, ezáltal létre
#l = range(len[ds])
#sz_1 = l[0::3]

#szenzor_1 = []
#szenzor_1.append(sz_1)

#print (sz_1)
