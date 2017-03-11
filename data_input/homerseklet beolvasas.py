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


elsokm = []

for d in ds:
    elsokm.append([ds[0],ds[1],ds[2],ds[3]])

print ('1.km: ',elsokm)