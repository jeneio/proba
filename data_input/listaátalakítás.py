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

def atlagszamito (atllista):
    return (sum(atllista)/len(atllista))

def transzponalo (bemenolista):
    folista=[]
    l0=[]
    l1=[]
    l2=[]
    l3=[]
    for x in range (0,len(bemenolista)) :
        for y in range (0, len(bemenolista[x])):
            if y==0:
                l0.append(bemenolista[x][y])
            elif y==1:
                l1.append(bemenolista[x][y])
            elif y == 2:
                l2.append(bemenolista[x][y])
            else:
                l3.append(bemenolista[x][y])
    folista.append(l0)
    folista.append(l1)
    folista.append(l2)
    folista.append(l3)
    return folista

def dbcsokkento (idodb,forraslista):
    l0=[]
    for x in range(0,len(forraslista)):
        i = transzponalo(forraslista[x])
        l1=[]
        for y in range (0,len(i)):
            l2=[]
            z=0
            while z < len(i[y]):
                l3=[]
                for w in range(0,idodb):
                    # idodbnak megfelelő elemszám
                    if z+w < len(i[y]):
                        l3.append(i[y][z+w])
                #egy szenzorhoz tartozo átlag számítása és listába rakása
                l2.append(atlagszamito(l3))
                z=z+idodb
            #egy kmhez tartozó szenzorok értéksorát rakjuk egy km listába
            l1.append(l2)
        #összerakjuk a teljes kmlistát
        l0.append(l1)
    return l0

# fájlnév változatlan rész
# path = 'C:\\Users\\X250-User\\Downloads\\ho\\M0_ho_20130901'
path = 'C:\\Users\\Oszi\\Desktop\\adatok\\eredeti\\hő\\M0_ho_20130901'
#path = 'C:\\Users\\szatm\\PycharmProjects\\oszi\\M0_ho_20130901'

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
    #for y in range(0,10):
    #   print(km[y])
        # print(len(km))
    keresztmetszetlista.append(km)
# keresztmetszetlista [keresztmetszet] [időpont(4érték)] [szenzorérték]
# print(keresztmetszetlista[0][0][0])

igazhamis=homersekleteldonto(keresztmetszetlista,1)
szamlalo=0
for h in igazhamis[0]:
    if h==True:
        szamlalo=szamlalo+1
# print(szamlalo)

#helyes: 1434
print(len(dbcsokkento(6,keresztmetszetlista)[0][0]))
#helyes: 86
print(len(dbcsokkento(100,keresztmetszetlista)[0][0]))
print(dbcsokkento(6,keresztmetszetlista))
