list_1 = []



for x in range(0,20):
    a = 4
    b = x % a
    l1 = [x,b]

    list_1.append(l1)

for y in list_1:
    print(y)

list_2=[]
z=0
while z < 84:
    a=4
    l2=[]
    for x in range (0,4):
        b=(z+x)%a
        l2.append(z+x)
    z=z+4
    list_2.append(l2)
for y in list_2:
    print(y)
print(len(list_2))

