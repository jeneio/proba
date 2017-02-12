#sziasztok, Osszián vagyok, üdv, hali
#hello
#de
#proba
#na most elvileg sikerült
print('hi')
print('Hi '+'my name is Osszian')
print(5+8)
print(int('8')+5)
print(float('8.5')+5)
condition = 1
while condition < 10:
    print (condition)
    condition += 1
x = 4
y = 5
z = 10
if x > y:
    print ('x>y')
elif x > z:
    print ('x>z')
else:
    print ('x a legkisebb')

import statistics

proba_lista = [1,8,6,9,5,4,15,2,17,22,41,11,32,17]

x = statistics.mean(proba_lista)
print('átlag=',x)

y = statistics.median(proba_lista)
print('középérték=',y)

z = statistics.mode(proba_lista)
print('módusz=',z)

a = statistics.stdev(proba_lista)
print('szórás=',a)

b = statistics.variance(proba_lista)
print('szórásnégyzet=',b)