# -*- coding: utf-8 -*-

import csv

path = 'C:\\Users\\X250-User\\Downloads\\ho\\M0_ho_20130901.ret'
with open(path) as f:
    reader = csv.reader(f, delimiter="\t")
    d = list(reader)
