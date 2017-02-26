# -*- coding: utf-8 -*-

import csv
import pprint as pp

path = 'C:\\Users\\X250-User\\Downloads\\ho\\M0_ho_20130901'

with open('.'.join([path, 'ret'])) as f:
    reader = csv.reader(f, delimiter="\t")
    d = list(reader)
ds = [list(x) for x in zip(*d)]

# _ds = []
# for d in ds:
#     _ = []
#     for x in d:
#         _.append(float(x))
#     _ds.append(_)
#
_ds = []
for d in ds:
    _ds.append([float(x) for x in d])



with open('.'.join([path, 'tim'])) as f:
    reader = csv.reader(f, delimiter="\t")
    t = list(reader)

import time
import datetime
s = '2013-09-01 00:00:01'
print(time.mktime(datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S").timetuple()))
s = '2013-09-01 00:00:11'
print(time.mktime(datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S").timetuple()))

# pp.pprint(t)