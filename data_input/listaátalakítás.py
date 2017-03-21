import csv
import itertools

def darabolo(be,nagydb,kisdb,kezdet):
    """eznegy fuggveny"""
    lista =[]
    z = kezdet*4
    while z < len(be):
        a = kisdb
        l2 = []
        for x in range(0, kisdb):
            l2.append(float(be[z + x]))
        z = z + nagydb
        lista.append(l2)
    return lista

def homersekleteldonto (km,deltat):
    igazhamis=[]
    for x in range(0,len(km)):
        igazhamis2=[]
        for y in range (0,len(km[x])):
            x1 = abs(max(km[x][y])-min(km[x][y]))  # ABS!!!
    # eldönteni, hogy azonos-e a hőmérséklet a vizsgált km 4 pontján
            if x1 <= deltat:
                igazhamis2.append(True)
            else:
                igazhamis2.append(False)
        igazhamis.append(igazhamis2)
    return igazhamis




# fájlnév változatlan rész
# path = 'C:\\Users\\X250-User\\Downloads\\ho\\M0_ho_20130901'
path = 'C:\\Users\\Oszi\\Desktop\\adatok\\eredeti\\hő\\M0_ho_20130901'

# mérési adatok beolvasása
with open('.'.join([path, 'ret'])) as f:
    reader = csv.reader(f, delimiter="\t")
    d = list(reader)

ds = [list(x) for x in zip(*d)]  # transzponálás;http://stackoverflow.com/questions/21444338/transpose-nested-list-in-python


d_km = list(itertools.chain.from_iterable(d))

keresztmetszetlista=[]
for keresztmetszet in range(0,21):
    km=darabolo(d_km,85,4,keresztmetszet)
    list_1=[km[0],km[1],km[2]]
    for y in range(0,10):
        print(km[y])
    print(len(km))
    keresztmetszetlista.append(km)
# keresztmetszetlista [keresztmetszet] [időpont(4érték)] [szenzorérték]
print(keresztmetszetlista[0][0][0])

igazhamis=homersekleteldonto(keresztmetszetlista,1)
szamlalo=0
for h in igazhamis[0]:
    if h==True:
        szamlalo=szamlalo+1
print(szamlalo)