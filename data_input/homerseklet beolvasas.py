import csv
# listát létrehozni meglévő fájlból

# fájlnév változatlan rész
path = 'C:\\Users\\Oszi\\Google Drive\\Diploma\\adatok\\hő\\M0_ho_20130901_p'

# mérési adatok beolvasása
with open('.'.join([path, 'ret'])) as f:
    reader = csv.reader(f, delimiter="\t")
    d = list(reader)
    print(d)
ds = [list(x) for x in zip(*d)]  # transzponálás;http://stackoverflow.com/questions/21444338/transpose-nested-list-in-python
# konverzió string -> float
_ds = []
for d in ds:
    _ds.append([float(x) for x in d])
elsokm = []

for d in _ds:
    elsokm.append([_ds[0],_ds[1],_ds[2],_ds[3]])

print (elsokm)