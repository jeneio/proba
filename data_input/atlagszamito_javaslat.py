# -*- coding: utf-8 -*-
__author__ = 'jakabgabor'

ATLAGOLT_HOSSZ = 2

l = [1, 2, 3, 4, 5, 6]
_ret = (zip(*[iter(l)]*ATLAGOLT_HOSSZ))

# a kapott listabol:
atl = [sum(x) / ATLAGOLT_HOSSZ for x in _ret]
print(atl)
