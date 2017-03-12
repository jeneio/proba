import csv
# listát létrehozni meglévő fájlból

# fájlnév változatlan rész
path = 'C:\\Users\\Oszi\\Google Drive\\Diploma\\adatok\\eredeti\\hő\\M0_ho_20130901'

# mérési adatok beolvasása
with open('.'.join([path, 'ret'])) as f:
    reader = csv.reader(f, delimiter="\t")
    d = list(reader)

ds = [list(x) for x in zip(*d)]  # transzponálás;http://stackoverflow.com/questions/21444338/transpose-nested-list-in-python

#keresztmetszet és szenzor megadása, ahol a hőmérsékletre kíváncsi vagyok
km = input ('melyik km? (1-21: 1-7 jobb ártéri, 8-14 meder, 15-21 bal ártéri)')
szsz = input ('melyik szenzor? (1-4) ')
km=int(km)
szsz=int(szsz)
if km==2:
    _szsz=szsz+(km-1)*4
elif km==3:
    _szsz = szsz + (km - 1) * 4
elif km==4:
    _szsz = szsz + (km - 1) * 4
elif km==5:
    _szsz = szsz + (km - 1) * 4
elif km==6:
    _szsz = szsz + (km - 1) * 4
elif km==7:
    _szsz = szsz + (km - 1) * 4
elif km==8:
    _szsz = szsz + (km - 1) * 4
elif km==9:
    _szsz = szsz + (km - 1) * 4
elif km==10:
    _szsz = szsz + (km - 1) * 4
elif km==11:
    _szsz = szsz + (km - 1) * 4
elif km==12:
    _szsz = szsz + (km - 1) * 4
elif km==13:
    _szsz = szsz + (km - 1) * 4
elif km==14:
    _szsz = szsz + (km - 1) * 4
elif km==15:
    _szsz = szsz + (km - 1) * 4
elif km==16:
    _szsz = szsz + (km - 1) * 4
elif km==17:
    _szsz = szsz + (km - 1) * 4
elif km==18:
    _szsz = szsz + (km - 1) * 4
elif km==19:
    _szsz = szsz + (km - 1) * 4
elif km==20:
    _szsz = szsz + (km - 1) * 4
elif km==21:
    _szsz = szsz + (km - 1) * 4

i = int(_szsz)-1

#ide kéne majd az időpont helyére behozni az idő beolvasósból a megállapított időpontot, és az ahhoz tartozó sorszámot
# (a 136 helyére t2 mondjuk)
print (km,'.km., 1.időpont, ',szsz,'. szenzor: ',ds[i][0])
print (km,'.km., 136.időpont, ',szsz,'. szenzor: ',ds[i][136])




