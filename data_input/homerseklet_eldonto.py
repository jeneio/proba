# listát létrehozni

elsokm = [22.5,22.4,22.1,22.9]

#megadni, hogy mekkora hőmérsékleteltérést tekintünk azonos hőmérsékletnek
y = input ('mekkora hőmérsékletkülönbséget tekintsek azonos hőmérsékletnek? ')
y=int(y)
x = max(elsokm)-min(elsokm)
#eldönteni, hogy azonos-e a hőmérséklet a vizsgált km 4 pontján
if x < y:
    print('a vizsgált km minden pontja egyenlő hőmérsékletűnek tekinthető')
    print('a max. hőm. kül. = ',x)
else: print('a vizsgált km pontjai nem egyenlő hőmérsékletűek','a max. hőm. kül. = ',x)

