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
    # eldönteni, hogy azonos-e a hőmérséklet a vizsgált km felső és alsó két pontján
            if x1 and y1 <= deltat:
                igazhamis2.append(True)
            else:
                igazhamis2.append(False)
        igazhamis.append(igazhamis2)
    return igazhamis

def homersekleteldontobeki (km,deltat):
    igazhamis=[]
    for x in range(0,len(km)):
        igazhamis2=[]
        for y in range (0,len(km[x])):
            x1 = abs((km[x][y][0])-(km[x][y][1]))  # ABS!!!
            y1 = abs((km[x][y][2])-(km[x][y][3]))
    # eldönteni, hogy azonos-e a hőmérséklet a vizsgált km be és kifolyási két pontján
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
    for x in range (0,len(bemenolista[0])):
        folista.append([])
    for x in range (0,len(bemenolista)) :
        for y in range (0, len(bemenolista[x])):
            folista[y].append(bemenolista[x][y])
    return folista

def transzponalonagy (nagylista):
    transzponalt=[]
    for i in range (0,len(nagylista)):
        folista=[]
        for x in range (0,len(nagylista[0][0])):
            folista.append([])
        for x in range (0,len(nagylista[0])) :
            for y in range (0, len(nagylista[i][x])):
                folista[y].append(nagylista[i][x][y])
        transzponalt.append(folista)
    return transzponalt

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

def napvizsgalo (path):
    # mérési adatok beolvasása
    with open('.'.join([path, 'ret'])) as f:
        reader = csv.reader(f, delimiter="\t")
        d = list(reader)

    ds = [list(x) for x in
          zip(*d)]  # transzponálás;http://stackoverflow.com/questions/21444338/transpose-nested-list-in-python

    d_km = list(itertools.chain.from_iterable(d))

    # a bolvasott fájl rendezése km, időpont és szenzor szerint
    keresztmetszetlista = []
    for keresztmetszet in range(0, 21):
        km = darabolo(d_km, 85, 4, keresztmetszet)
        list_1 = [km[0], km[1], km[2]]
        keresztmetszetlista.append(km)
    # keresztmetszetlista [keresztmetszet] [időpont(4érték)] [szenzorérték]

    egypercesatlagT = dbcsokkento(6, keresztmetszetlista)
    egypercesatlag = transzponalonagy(egypercesatlagT)

    # azt vizsgálom, hogy egy km-ben hányszor fordul elő, hogy azonosnak tekinthető a hőmérséklet (az átlagolt, 1 perces listán)
    igazhamis = homersekleteldontoazonos(egypercesatlag, 1)
    napieredmeny=[]
    for g in range(0, len(igazhamis)):
        szamlalo = 0
        for h in igazhamis[g]:
            if h == True:
                szamlalo = szamlalo + 1
        napieredmeny.append(szamlalo)

    return napieredmeny


f=open('adat.csv','a')


for x in range (1,31):
    # fájlnév változatlan rész
    # path = 'C:\\Users\\X250-User\\Downloads\\ho\\M0_ho_201309' + str(x)

    if x < 10:
        file_nev = "0" + str(x)
    else:
        file_nev= str(x)
    path = 'C:\\Users\\Oszi\\Desktop\\adatok\\eredeti\\hő\\M0_ho_201309' + file_nev
    # path = 'C:\\Users\\szatm\\PycharmProjects\\oszi\\M0_ho_201309' + str(x)
    eredmeny=napvizsgalo(path)
    string=",".join(map(str,eredmeny))+"\n"
    f.write(string)

f.close()
