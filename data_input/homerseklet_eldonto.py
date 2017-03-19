import csv

# fájlnév változatlan rész
# path = 'C:\\Users\\X250-User\\Downloads\\ho\\M0_ho_20130901'
path = 'C:\\Users\\Oszi\\Desktop\\adatok\\eredeti\\hő\\M0_ho_20130901'

# mérési adatok beolvasása
with open('.'.join([path, 'ret'])) as f:
    reader = csv.reader(f, delimiter="\t")
    d = list(reader)

ds = [list(x) for x in zip(*d)]  # transzponálás;http://stackoverflow.com/questions/21444338/transpose-nested-list-in-python
import itertools

d_km = list(itertools.chain.from_iterable(d))
print(len(d_km))
print(d_km[0])
#az első km-re vonatkozó hömérséklet adatok listába rendezése
i = []
i0 = 0
while i0 < 731000:
    i.append(i0)
    i0 = i0 + 85
j = []
j0 = 4
while j0 < 731000:
    j.append(j0)
    j0 = j0 + 85

elsokm = []
elsokm.append(d_km[i:j])

print(elsokm)

# megadni, hogy mekkora hőmérsékleteltérést tekintünk azonos hőmérsékletnek
y = 1

#x = abs(max(elsokm)-min(elsokm))  # ABS!!!
# eldönteni, hogy azonos-e a hőmérséklet a vizsgált km 4 pontján
#if x <= y:
#    print('a vizsgált km minden pontja egyenlő hőmérsékletűnek tekinthető')
#    print('a max. hőm. kül. = ', x)
    #ide kéne behozni majd az átlagszámítást
#else:
#    print('a vizsgált km pontjai nem egyenlő hőmérsékletűek','a max. hőm. kül. = ', x)

