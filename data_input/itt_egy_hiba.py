# -*- coding: utf-8 -*-
__author__ = 'jakabgabor'

x1 = 3
y1 = 2
deltatazonos = 4
z1 = 6
deltatkulonbseg = 5
igazhamis2 = []

if x1 and y1 <= deltatazonos and z1 > deltatkulonbseg:
    igazhamis2.append(True)
else:
    igazhamis2.append(False)

# itt igazat varunk, meg is kapjuk
print(igazhamis2)
print(igazhamis2[-1])

x1 = 20
if x1 and y1 <= deltatazonos and z1 > deltatkulonbseg:
    igazhamis2.append(True)
else:
    igazhamis2.append(False)

print(igazhamis2)  # itt egy hamist varunk, de igazat kapunk
print(igazhamis2[-1])  # na itt van a hiba mert az eredmeny True

# igy helyes
if x1 <= deltatazonos and y1 <= deltatazonos and z1 > deltatkulonbseg:
    igazhamis2.append(True)
else:
    igazhamis2.append(False)

print(igazhamis2)
