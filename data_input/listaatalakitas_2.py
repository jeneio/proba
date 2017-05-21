# -*- coding: utf-8 -*-

import csv
import itertools
from __init__ import PATH_HO, PATH_SARU, PATH_NYUL, PATH_ELM, ACEL, SARU_TAV, HO_KM
import pickle
from collections import Counter
from operator import sub


# ezzel csinálom meg az adatok rendezését
def darabolo(be, nagydb, kisdb, kezdet):
    lista = []
    z = kezdet
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

        if '_saru_' in path:
            d = [sor[0:24] for sor in d]
            _ret = []
            for sor in d:
                _ret.append([float(x)-float(y) for x, y in zip(sor, d[0])])
            d = _ret

        d_km = list(itertools.chain.from_iterable(d))

        # a bolvasott fájl rendezése km, időpont és szenzor szerint
        keresztmetszetlista = []
        for keresztmetszet in range(0, 21):
            # meghívom a darabolót az egy sorban levő adataimra.
            # 84 érték tartozik egy időponthoz (+egy üres).
            # 4 szenzorunk van.
            # az utolsó paraméter a darabolás kezdetének pozícióját határozza meg
            km = darabolo(d_km, 85, 4, 4*keresztmetszet)
            # list_1 = [km[0], km[1], km[2]]
            keresztmetszetlista.append(km)
        # keresztmetszetlista [keresztmetszet] [időpont(4érték)] [szenzorérték]

        egypercesatlagT = dbcsokkento(6, keresztmetszetlista)
        egypercesatlag = transzponalonagy(egypercesatlagT)

        with open('egypercesatlag_%s.adat' % path[-8:], 'wb') as f:
            pickle.dump(egypercesatlag, f)

    return egypercesatlag

# ezzel csinálom meg az adatok rendezését és bővítését, hogy minden szenzorhoz legyen
def sarudarabolo(be, nagydb, kisdb, kezdet):
    lista = []
    z = kezdet
    while z < len(be):
        l2 = []
        for x in range(0, kisdb):
            l2.append(float(be[z + x]))
        z = z + nagydb
        lista.append(l2)
    return lista


def saru_beolvaso(path):

    # mérési adatok beolvasása
    with open('.'.join([path, 'ret'])) as f:
        reader = csv.reader(f, delimiter="\t")
        d = list(reader)
    # elmozdulások előállítása minden nap 0. időponthoz viszonyítva
    if '_saru_' in path:
        d = [sor[0:24] for sor in d]
        _ret = []
        for sor in d:
            _ret.append([float(x)-float(y) for x, y in zip(sor, d[0])])
        d = _ret

    d_saru = list(itertools.chain.from_iterable(d))
    saru = []
    # meghívom a darabolót az egy sorban levő adataimra.
    # 24 érték tartozik egy időponthoz (+egy üres).
    # 2 sarunk van.
    # az utolsó paraméter a darabolás kezdetének pozícióját határozza meg
    for pilon in range(0,12):
        saru.append(darabolo(d_saru, 24, 2, 2*pilon))

    return saru
# az elkészült elmozdulás adatsorokat használom, hogy ne számoljon olyan sokáig, ezek a fájlok úgyis elő vannak már állítva
def elm_beolvaso(path):

    # elmozdulasi adatok beolvasása
    d = []
    with open('.'.join([path, 'ret'])) as f:
        reader = csv.reader(f, delimiter=" ")
        for row in reader:
            new = []
            for item in row:
                new.extend(item.split("\n"))
            d.append(new)
            #d = list(reader)
    # elmozdulások előállítása minden nap 0. időponthoz viszonyítva
    d = [sor[0:24] for sor in d]
    _ret = []
    for sor in d:
        _ret.append([float(x)-float(y) for x, y in zip(sor, d[0])])
    d = _ret

    d_saru = list(itertools.chain.from_iterable(d))
    saru = []
    # meghívom a darabolót az egy sorban levő adataimra.
    # 24 érték tartozik egy időponthoz (+egy üres).
    # 2 sarunk van.
    # az utolsó paraméter a darabolás kezdetének pozícióját határozza meg
    for pilon in range(0,12):
        saru.append(darabolo(d_saru, 24, 2, 2*pilon))

    return saru

# előállítom minden pillanathoz minden szenzorra a delta T hőmérséklet különbséget a 0. időponthoz viszonyítva.
def homersekletkulonbseg(lista):
        lista = [sor[0:84] for sor in lista] # egy időponthoz 84 adat tartozik (3*7 km *4 szenzor=84)
        _ret = []
        for sor in lista:
            _ret.append([float(x)-float(y) for x, y in zip(sor, lista[0])])
        return _ret

# nyúlások kiszámítása 0. időponthoz és fáljba írása és listába rakása a későbbi forgalom és hőmérséklet elmozdulások
# szétválasztásához
# ez később kiderült hogy nem valós eredményre vezet, mert szenzoronként határozza meg a nyúlást elméleti alapon,
# nem veszi figyelembe a valós km-et
def homelmozdulas (homlista,anyagallando,sarutav,path):
    nyullista = [] #teljes nyúlásokat tartalmazó lista, ezt fogom feltölteni adatokkal
    with open(path + '.ret', 'w') as f:
        for x in range (0,len(homlista)):
                string1 = "" # szóközzel fogom elválasztani az adatokat az exceles könnyebb beolvasáshoz
                kisnyullista = [] #segédlista
                for y in range (0, len(homlista[0])):
                    a = int(y / 4) # 4esével lépjen (ugyanazon szenzorokhoz tartozó érték kijelölése)
                    if HO_KM[a]:
                        # nyúlások előállítása, listába rakása és kiíratás előkészítése
                        nyul = anyagallando*sarutav[a]*homlista[x][y]
                        string = str(nyul) + " "
                        string1 = string1 + string
                        kisnyullista.append(nyul) #feltöltöm az időpontokhoz tartozó adatokkal
                f.write(string1 + "\n") # új sorba a következő időpont értékei
                nyullista.append(kisnyullista)  # teljes lista összeállítása
    return nyullista

# a forgalom és a hőmérséklet elmozdulásainak szétválasztására 1 perces módusz értékeket állítok elő mozgó átlaggal.
# a kapott módusz értékek várhatóan csak a hőmérsékleti hatásokat tartalmazzák majd
def modusz (bemenolista):
    moduszlista=Counter(bemenolista)
    return moduszlista.most_common(1)[0][0]

# a módusz előállításához vennem kell egy időtartamot, hogy mekkora adatmennyiséget tekintek egy "ablaknak".
#  ez majd 120 adat lesz a run3-ban, azaz 1 percnyi adat
def homerseklettenylegeselmozdulas (bemenolista,idotartam):
    eredmeny=[]
    #print(len(bemenolista)) #pillerek szama
    #print(len(bemenolista[0])) #be- es kifolyasi oldal
    #print(len(bemenolista[0][0])) #idopontok egy piller egy ertekere (be ES kifolyasi oldal)
    helyidotartam = idotartam
    for x in range (0,len(bemenolista)): #0-12 pillér
        napipiller=[]
        for y in range (0,len(bemenolista[x])): #0-158240 időpont
            l0=[]
            l1=[]
            if y > len(bemenolista[x])-idotartam: # az utolsó ablak elemei
                helyidotartam = helyidotartam -1
            for idoindex in range(0,helyidotartam):
                l0.append(bemenolista[x][y + idoindex][0])
                l1.append(bemenolista[x][y + idoindex][1])
            if l0 != [] and l1 != []:
                egypercesmoduszbe = modusz(l0)
                egypercesmoduszki = modusz(l1)
            napipiller.append([egypercesmoduszbe,egypercesmoduszki])
        helyidotartam = idotartam
        eredmeny.append(napipiller)
        napipiller=[]
        print("Elkeszult piller: "+str(x+1))
    # print(len(eredmeny[2]))
    return eredmeny

#szétválasztom a hőmérsékleti és a forgalmi hatást ezzel majd, tehát két lista különbségére van szükségem elemenként
def elmozdulaskulonbseg(eredetilista,kivonandolista):
    eredmeny=[]
    for x in range (0,len(eredetilista)): #0-12, x=egy piller
        napipiller=[]
        for y in range(0,len(eredetilista[x])): #0-158240 y=egy idopont
            napipiller.append([er-ki for er,ki in zip(eredetilista[x][y],kivonandolista[x][y])]) # be- es kifolyasi
                                                                             # oldali ertekek parba rendezese es kivonasa
        eredmeny.append(napipiller)
        print("Elkeszult piller kulonbseg: "+str(x+1))
    return eredmeny
# a futások előállítása (bármilyen hatásra)
def futas (bemenolista):
    napifutas=[]
    for x in range (0, len(bemenolista)): # pillérek 1-12
        napipillerfutas=[]
        for y in range (0, len(bemenolista[x])): # időpont 0-158000körül
            if y==0: # a 0. érték bevitele (amúgy ez mindig 0)
                napipillerfutas.append(bemenolista[x][y])
            else: # az i-edik elem (a=bemenolista[x][y]) és az (i-1)-dik elem (e=bemenolista[x][y-1]) különbségének az
                #  abszolútértéke, ezt hozzáadva az összegzett lista előző eleméhez (ef=napipillerfutas[y-1])
                # abs(a - e) + ef
                k=[abs(a - e) + ef for a, e, ef in zip(bemenolista[x][y], bemenolista[x][y-1],napipillerfutas[y-1])]
                napipillerfutas.append(k)
        napifutas.append(napipillerfutas)
        print("Elkeszult piller futas: " + str(x + 1))
    return napifutas


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

def run2():
    for x in range (31,32):
        if x < 10:
            file_nev = "0" + str(x)
        else:
            file_nev = str(x)
        path = PATH_SARU + file_nev
        eredmeny = saru_beolvaso(path)


        # kiíROM FÁJLBA AZ ELMOZDUÁS ÉRTÉKEKET
        with open('201308'+file_nev+'_elm.ret', 'w') as f:
            for z in range(0,len(eredmeny[0])):
                string1 = ""
                for y in range(0, len(eredmeny)):
                    string = " ".join(map(str, eredmeny[y][z])) + " "
                    string1 = string1 + string
                f.write(string1 +"\n")

#ez a program szolgál a nyers (pozíció) adatokból az elmozdulások létrehozására ( "A" rész )
# a két hatás szétválasztására: "B" rész: hőmérsékleti elmozdulás
#                               "C" rész: forgalomból keletkező elmozdulás
# beviteli adatok (kézzel beírni): vizsgált év, hónap = vizsgaltevhonap
#                                  vizsgált időablak a módusz előállításához, másodpercben = vizsgaltidoablak
#                                  __init__ fájlban a PATH_SARU elérési útvonala a vizsgált év, hónap dátumára végződjön!
def run3():
    # a vizsgált év és hónap megadása, módusz bevitele
    vizsgaltevhonap = "201308"
    vizsgaltidoablak = 60
    # a mintavétel gyakorisága fél másodperces, ezért beszorzom kettővel.
    vizsgaltidoablak=vizsgaltidoablak*2
    # figyelmeztet, hogy jó fájlból dolgozik-e
    if PATH_SARU =='C:\\Users\\Oszi\\Desktop\\adatok\\eredeti\\saru\\M0_saru_'+str(vizsgaltevhonap):
        print("A forrásfájl elérési útja helyesen van megadva.")
    else:
        print("A forrásfájl elérési útja helytelen, a dátum nem egyezik! Ellenőrizd a dátumot!")
    # a napok külön azért kell, hogyha csak pár nap érdekel, azt külön meg lehessen adni (teljes hónap vizsgálata esetén
    # figyelni kell arra, hogy a vizsgált hónap hány napos), akkor a 'for x in napok' kell aktívvá tenni 4 sorral lejjebb
    napok = [10,11,12,13]

    #for x in range(1,32):
    for x in (napok):
        try:
            if x < 10:
                file_nev = "0" + str(x)
            else:
                file_nev = str(x)
            path = PATH_SARU + file_nev
            elmozdulasertekek = saru_beolvaso(path) # elmozdulást állít elő pozíciókból
            elmozdulasertekekmodusz = homerseklettenylegeselmozdulas(elmozdulasertekek, vizsgaltidoablak) # móduszt állít elő vizsgaltidoablek/60 perces
                                                                     # adatmennyiségre, azaz a hőmérsékleti elmozdulást kapom
            elmozdulasertekekkulonbseg=elmozdulaskulonbseg(elmozdulasertekek,elmozdulasertekekmodusz)
                                                                    # teljes elmozdulás-hőm.elmozdulás=forgalmi hatások

            # "A" rész: elso idopontra normalizalt ertekek kiíratása = elmozdulások (ezek már készek nálam)
            """with open( vizsgaltevhonap + file_nev + '_elm.ret', 'w') as f:
                for z in range(0, len(elmozdulasertekek[0])):
                    string1 = ""
                    for y in range(0, len(elmozdulasertekek)):
                        string = " ".join(map(str, elmozdulasertekek[y][z])) + " "
                        string1 = string1 + string
                    f.write(string1 + "\n")"""
            # "B" rész: normalizalt ertekek modusza a hőmérsékletváltozásból adódó elmozdulások kiíratása
            with open(vizsgaltevhonap + file_nev + '_homelm.ret', 'w') as f:
                for z in range(0, len(elmozdulasertekekmodusz[0])):
                    string1 = ""
                    for y in range(0, len(elmozdulasertekekmodusz)):
                        string = " ".join(map(str, elmozdulasertekekmodusz[y][z])) + " "
                        string1 = string1 + string
                    f.write(string1 + "\n")
            # "C" rész: normalizalt ertekek es a modusz kulonbsege = a forgalombólból adódó elmozdulások kiíratása
            with open(vizsgaltevhonap + file_nev + '_forgelm.ret', 'w') as f:
                for z in range(0, len(elmozdulasertekekkulonbseg[0])):
                    string1 = ""
                    for y in range(0, len(elmozdulasertekekkulonbseg)):
                        string = " ".join(map(str, elmozdulasertekekkulonbseg[y][z])) + " "
                        string1 = string1 + string
                    f.write(string1 + "\n")
        except FileNotFoundError:
            print("Az adott napra nincsenek adatok: " + str(x))
        except IndexError:
            print("Az adott napra nincs teljes adatsor: " + str(x))

# hőmérsékletkülönbségek
def run_deltaT():
    for x in range (1,31):
        if x < 10:
            file_nev = "0" + str(x)
        else:
            file_nev = str(x)
        path = PATH_HO + file_nev
        # mérési adatok beolvasása
        with open('.'.join([path, 'ret'])) as f:
            reader = csv.reader(f, delimiter="\t")
            d = list(reader)
        eredmeny = homersekletkulonbseg(d)
        nyul_path = PATH_NYUL + file_nev

        a=homelmozdulas(eredmeny,ACEL,SARU_TAV,nyul_path)


# ez itt egy próbálkozás, félbehagyva egyelőre
def saruatlag():
    x = 1
    if x < 10:
        file_nev = "0" + str(x)
    else:
        file_nev = str(x)
    path = PATH_SARU + file_nev
    eredmeny = saru_beolvaso(path)
    s_atlagt = dbcsokkento(20,eredmeny)
    s_atlag=transzponalonagy(s_atlagt)
    print(len(s_atlag[0]))
    with open('saru_atlag.ret', 'w') as f:
        for x in range (0,len(s_atlag[4])):
        #for y in range (0,len(s_atlag[4][0])):
        #string = " ".join(map(str, s_atlag[4][x]))+" "
            for y in range(0,20):
                string = " ".join(map(str, s_atlag[4][x])) + "\n"
                f.write(string)

#ez a program szolgál a már elkészített elmozdulás fájlokból a futások létrehozására
# a két hatásra külön végzi:  "A" rész: forgalmi futások
#                             "B" rész: hőmérsékleti futások
def run4():
    # a vizsgált év és hónap megadása
    vizsgaltevhonap = "201308"
    # a napok külön azért kell, hogyha csak pár nap érdekel, azt külön meg lehessen adni,
    # ekkor a 'for x in napok' kell aktívvá tenni 6 sorral lejjebb
    napok=[10,11,12,13]

    kiirolistaforg=[] #futások kiírásához
    kiirolistahom=[]
    # "A" rész: forgalmi futás összegzés és fájlkiíratás
    #for x in napok:
    for x in range (1,32):
        try:
            if x < 10:
                file_nev = "0" + str(x)
            else:
                file_nev = str(x)
            path = PATH_ELM + vizsgaltevhonap + file_nev + '_forgelm'
            elmozdulasertekek = elm_beolvaso(path) # elmozdulást állít elő pozíciókból
            forgalmifutas=futas(elmozdulasertekek)
            #a futasok kiíratása (nálam már elkészítve)
            with open(vizsgaltevhonap + file_nev + '_forgfutas.ret', 'w') as f:
                for z in range(0, len(forgalmifutas[0])):
                    string1 = ""
                    for y in range(0, len(forgalmifutas)):
                        string = " ".join(map(str, forgalmifutas[y][z])) + " "
                        string1 = string1 + string
                    f.write(string1 + "\n")
            kiirolista1=[] # a kiíratáshoz előkészítő lista
            for piller in range (0, len(forgalmifutas)):
                kiirolista1.append(forgalmifutas[piller][len(forgalmifutas[piller])-1])
            kiirolistaforg.append(kiirolista1)
        except FileNotFoundError:
            print("Az adott napra nincsenek adatok: " + str(x))
        except IndexError:
            print("Az adott napra nincs teljes adatsor: " + str(x))
    # ez mindig az utolsó időponthoz tartozó futást írja ki, ezáltal a napi összfutást a forgalomból, sarunként.
    try:
        with open(vizsgaltevhonap + file_nev + '_forgfutasnapi.ret', 'w') as f:
            for z in range(0, len(kiirolistaforg[0])):
                string1 = ""
                for y in range(0, len(kiirolistaforg)):
                    string = " ".join(map(str, kiirolistaforg[y][z])) + " "
                    string1 = string1 + string
                f.write(string1 + "\n")
    except IndexError:
        print("Az adott napra nincs teljes adatsor: " + str(x))
    # "B" rész: homérsékleti futás összegzés és fájlkiíratás (ugyanúgy mint az előbb futásra)
    for x in napok:
    #for x in range (1,32):
        try:
            if x < 10:
                file_nev = "0" + str(x)
            else:
                file_nev = str(x)
            path = PATH_ELM + 'vizsgaltevhonap'+ file_nev + '_homelm'
            # path = 'C:\\Users\\szatm\\PycharmProjects\\oszi\\M0_ho_201309' + str(x)
            elmozdulasertekek = elm_beolvaso(path) # elmozdulást állít elő pozíciókból
            homfutas=futas(elmozdulasertekek)
            #a futasok kiíratása
            with open('vizsgaltevhonap' + file_nev + '_homfutas.ret', 'w') as f:
                for z in range(0, len(homfutas[0])):
                    string1 = ""
                    for y in range(0, len(homfutas)):
                        string = " ".join(map(str, homfutas[y][z])) + " "
                        string1 = string1 + string
                    f.write(string1 + "\n")
            kiirolista2 = []
            for piller in range(0, len(homfutas)):
                kiirolista2.append(homfutas[piller][len(homfutas[piller])-1])
            kiirolistahom.append(kiirolista2)
        except FileNotFoundError:
            print("Az adott napra nincsenek adatok: " + str(x))
        except IndexError:
            print("Az adott napra nincs teljes adatsor: " + str(x))
    # ez mindig az utolsó időponthoz tartozó futást írja ki, ezáltal a napi összfutást a hőmérsékletből, sarunként.
    try:
        with open('vizsgaltevhonap' + file_nev + '_homfutasnapi.ret', 'w') as f:
            for z in range(0, len(kiirolistahom[0])):
                string1 = ""
                for y in range(0, len(kiirolistahom)):
                    string = " ".join(map(str, kiirolistahom[y][z])) + " "
                    string1 = string1 + string
                f.write(string1 + "\n")
    except IndexError:
        print("Az adott napra nincs teljes adatsor: " + str(x))



if __name__ == '__main__':

    run4()