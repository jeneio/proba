
jkb = False

if jkb:
    PATH_HO = 'D:\\M0_nyers\\homerseklet\\M0_ho_201309'
else:
    PATH_HO = 'C:\\Users\\Oszi\\Desktop\\adatok\\eredeti\\ho\\M0_ho_201309'
    PATH_SARU = 'C:\\Users\\Oszi\\Desktop\\adatok\\eredeti\\saru\\M0_saru_201309'
    PATH_NYUL = 'C:\\Users\\Oszi\\Desktop\\adatok\\nyulas\\M0_nyul_201309'


# segédlista a nyúlások számításához: ezek fixek, tartalmazzák hogy a deltaT hőmérsékleti adatsorból melyik
    # keresztmetszetek lesznek érdekesek (a mozgó sarukhoz tartozók)
HO_KM = [True,False,True,False,True,False,True, # jobb ártéri
         True,False,True,False,True,False,True, # meder
         True,False,True,False,True,False,True] # bal ártéri
# a fix támasztól való távolsághoz a nyúlás képletében az L-hez
SARU_TAV = [73500, 0, 0, 0, 73500, 0, 147000, # jobb ártéri
            108500, 0, 0, 0, 108500, 0, 217000, # meder
            147000, 0, 73500, 0, 0, 0, 73500] # bal ártéri
ACEL = 0.000012 # lin. hőtág. együttható