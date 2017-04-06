import csv
import itertools

#ezzel csinálom meg az adatok rendezését
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

#ennek a segítségével döntöm majd el, hogy milyen hőmérséklet állapot van jelen (ez egyelőre az azonos hőmérséklethez tartozó)
def homersekleteldontoazonos (km,deltat):
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

def homersekleteldontofelulalul (km,deltat):
    igazhamis=[]
    for x in range(0,len(km)):
        igazhamis2=[]
        for y in range (0,len(km[x])):
            x1 = abs((km[x][y][0])-(km[x][y][3]))  # ABS!!!
            y1 = abs((km[x][y][1])-(km[x][y][2]))
    # eldönteni, hogy azonos-e a hőmérséklet a vizsgált km felső két pontján
            if x1 and y1 <= deltat:
                igazhamis2.append(True)
            else:
                igazhamis2.append(False)
        igazhamis.append(igazhamis2)
    return igazhamis

#átlagszámítás
def atlagszamito (atllista):
    return (sum(atllista)/len(atllista))

#transzponálás kézileg
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

#ezzel fogom csökkenteni a hőmérsékleti adatokat
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

#a bolvasott fájl rendezése km, időpont és szenzor szerint
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

# azt vizsgálom, hogy egy km-ben hányszor fordul elő, hogy azonosnak tekinthető a hőmérséklet
#igazhamis=homersekleteldontoazonos(keresztmetszetlista,1)
#szamlalo=0
#for h in igazhamis[0]:
#    if h==True:
#        szamlalo=szamlalo+1
#print(szamlalo)

igazhamis=homersekleteldontofelulalul(keresztmetszetlista,1)
szamlalo=0
for h in igazhamis[0]:
    if h==True:
        szamlalo=szamlalo+1
print(szamlalo)

#helyes: 1434
#print(len(dbcsokkento(6,keresztmetszetlista)[0][0]))
#helyes: 86
#print(len(dbcsokkento(100,keresztmetszetlista)[0][0]))

egypercesatlagT=[dbcsokkento(6,keresztmetszetlista)]
egypercesatlag=transzponalo(egypercesatlagT)
#print (egypercesatlagT[0][0])
#print(len(dbcsokkento(6,keresztmetszetlista)))

# azt vizsgálom, hogy egy km-ben hányszor fordul elő, hogy azonosnak tekinthető a hőmérséklet (az átlagolt, 1 perces listán)
#igazhamis=homersekleteldontoazonos(egypercesatlag[0],1)
#szamlalo=0
#for h in igazhamis[0]:
#    if h==False:
#       szamlalo=szamlalo+1
#print(szamlalo)