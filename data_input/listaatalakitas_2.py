# -*- coding: utf-8 -*-

import csv
import itertools
from data_input import PATH_HO
import pickle


# ezzel csinálom meg az adatok rendezését
def darabolo(be, nagydb, kisdb, kezdet):
    """eznegy fuggveny"""
    lista = []
    z = kezdet * 4
    while z < len(be):
        l2 = []
        for x in range(0, kisdb):
            l2.append(float(be[z + x]))
        z = z + nagydb
        lista.append(l2)
    return lista


# ennek a segítségével döntöm majd el, hogy milyen hőmérséklet állapot van jelen (ez egyelőre az azonos hőmérséklethez tartozó)
def homersekleteldontoazonos(km, deltat):
    igazhamis = []
    for x in range(0, len(km)):

        igazhamis_2 = [abs(max(km[x][y]) - min(km[x][y])) <= deltat for y in range(0, len(km[x]))]
        igazhamis.append(igazhamis_2)

    return igazhamis


def homersekleteldontofelulalul(km, deltatazonos, deltatkulonbseg):
    igazhamis = []
    for x in range(0, len(km)):
        igazhamis2 = []
        for y in range(0, len(km[x])):
            x1 = abs((km[x][y][0]) - (km[x][y][3]))  # ABS!!!
            y1 = abs((km[x][y][1]) - (km[x][y][2]))
            z1 = abs(x1 - y1)
            # eldönteni, hogy azonos-e a hőmérséklet a vizsgált km felső és alsó két pontján
            if x1 and y1 <= deltatazonos and z1 > deltatkulonbseg:
                igazhamis2.append(True)
                # ide bele kéne még rakni hogy x1 és y1 abs különbsége legyen nagyobb mint egy érték, mondjuk 1 fok
                # működik is szerintem
            else:
                igazhamis2.append(False)
        igazhamis.append(igazhamis2)
    return igazhamis


def homersekleteldontobeki(km, deltatazonos, deltatkulonbseg):
    igazhamis = []
    for x in range(0, len(km)):
        igazhamis2 = []
        for y in range(0, len(km[x])):
            x1 = abs((km[x][y][0]) - (km[x][y][1]))  # ABS!!!
            y1 = abs((km[x][y][2]) - (km[x][y][3]))
            z1 = abs(x1 - y1)
            # eldönteni, hogy azonos-e a hőmérséklet a vizsgált km be és kifolyási két pontján
            if x1 and y1 <= deltatazonos and z1 > deltatkulonbseg:
                igazhamis2.append(True)
            else:
                igazhamis2.append(False)
        igazhamis.append(igazhamis2)
    return igazhamis


# átlagszámítás
def atlagszamito(atllista):
    return sum(atllista) / len(atllista)


# transzponálás kézileg
def transzponalo(bemenolista):
    folista = []
    for x in range(0, len(bemenolista[0])):
        folista.append([])
    for x in range(0, len(bemenolista)):
        for y in range(0, len(bemenolista[x])):
            folista[y].append(bemenolista[x][y])
    return folista


def transzponalonagy(nagylista):
    transzponalt = []
    for i in range(0, len(nagylista)):
        folista = []
        for x in range(0, len(nagylista[0][0])):
            folista.append([])
        for x in range(0, len(nagylista[0])):
            for y in range(0, len(nagylista[i][x])):
                folista[y].append(nagylista[i][x][y])
        transzponalt.append(folista)
    return transzponalt


# ezzel fogom csökkenteni a hőmérsékleti adatokat
def dbcsokkento(idodb, forraslista):
    l0 = []
    for x in range(0, len(forraslista)):
        i = transzponalo(forraslista[x])
        l1 = []
        for y in range(0, len(i)):
            l2 = []
            z = 0
            while z < len(i[y]):
                l3 = []
                for w in range(0, idodb):
                    # idodbnak megfelelő elemszám
                    if z + w < len(i[y]):
                        l3.append(i[y][z + w])
                # egy szenzorhoz tartozo átlag számítása és listába rakása
                l2.append(atlagszamito(l3))
                z = z + idodb
            # egy kmhez tartozó szenzorok értéksorát rakjuk egy km listába
            l1.append(l2)
        # összerakjuk a teljes kmlistát
        l0.append(l1)
    return l0


def valami_beolvaso(path):

    try:
        with open('egypercesatlag_%s.adat' % path[-8:], 'rb') as f:
            egypercesatlag = pickle.load(f)
        # print('%s: oke be tudtam olvasni' % path[-8:])
    except FileNotFoundError:
        print('%s: meg nem volt kiirva' % path[-8:])
        pass

        # mérési adatok beolvasása
        with open('.'.join([path, 'ret'])) as f:
            reader = csv.reader(f, delimiter="\t")
            d = list(reader)

        d_km = list(itertools.chain.from_iterable(d))

        # a bolvasott fájl rendezése km, időpont és szenzor szerint
        keresztmetszetlista = []
        for keresztmetszet in range(0, 21):
            km = darabolo(d_km, 85, 4, keresztmetszet)
            # list_1 = [km[0], km[1], km[2]]
            keresztmetszetlista.append(km)
        # keresztmetszetlista [keresztmetszet] [időpont(4érték)] [szenzorérték]

        egypercesatlagT = dbcsokkento(6, keresztmetszetlista)
        egypercesatlag = transzponalonagy(egypercesatlagT)

        with open('egypercesatlag_%s.adat' % path[-8:], 'wb') as f:
            pickle.dump(egypercesatlag, f)

    return egypercesatlag


def napvizsgalo(path):
    # azt vizsgálom, hogy egy km-ben hányszor fordul elő, hogy azonosnak tekinthető a hőmérséklet (az átlagolt, 1 perces listán)
    igazhamis = homersekleteldontoazonos(valami_beolvaso(path), 1)
    return [igazhamis[g].count(True) for g in range(len(igazhamis))]


def napvizsgalofelulalul(path):

    igazhamis = homersekleteldontofelulalul(valami_beolvaso(path), 1, 0.5)
    return [igazhamis[g].count(True) for g in range(len(igazhamis))]


def napvizsgalobeki(path):

    igazhamis = homersekleteldontobeki(valami_beolvaso(path), 1, 0.5)
    return [igazhamis[g].count(True) for g in range(len(igazhamis))]


def run():

    with open('adat.csv', 'w+') as f:

        for x in range(1, 31):
            # fájlnév változatlan rész
            # path = 'C:\\Users\\X250-User\\Downloads\\ho\\M0_ho_201309' + str(x)

            if x < 10:
                file_nev = "0" + str(x)
            else:
                file_nev = str(x)
            path = PATH_HO + file_nev
            # path = 'C:\\Users\\szatm\\PycharmProjects\\oszi\\M0_ho_201309' + str(x)
            eredmeny = napvizsgalo(path)
            string = ",".join(map(str, eredmeny)) + "\n"
            f.write(string)

    with open('adatfelulalul.csv', 'a') as f:

        for x in range(1, 31):
            # fájlnév változatlan rész
            # path = 'C:\\Users\\X250-User\\Downloads\\ho\\M0_ho_201309' + str(x)

            if x < 10:
                file_nev = "0" + str(x)
            else:
                file_nev = str(x)
            path = PATH_HO + file_nev
            # path = 'C:\\Users\\szatm\\PycharmProjects\\oszi\\M0_ho_201309' + str(x)
            eredmeny = napvizsgalofelulalul(path)
            string = ",".join(map(str, eredmeny)) + "\n"
            f.write(string)

    with open('adatbeki.csv', 'a') as f:

        for x in range(1, 31):
            # fájlnév változatlan rész
            # path = 'C:\\Users\\X250-User\\Downloads\\ho\\M0_ho_201309' + str(x)

            if x < 10:
                file_nev = "0" + str(x)
            else:
                file_nev = str(x)
            path = PATH_HO + file_nev
            # path = 'C:\\Users\\szatm\\PycharmProjects\\oszi\\M0_ho_201309' + str(x)
            eredmeny = napvizsgalobeki(path)
            string = ",".join(map(str, eredmeny)) + "\n"
            f.write(string)

if __name__ == '__main__':

    run()
