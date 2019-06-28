#!/usr/bin/env python

from lmnet.http import gHTTP
from itertools import product

#1 1_p0.(0...41).sdf 1_p1.(0...7).sdf 1_p2.(0...5).sdf 1_p3.(0...4).sdf
#2 2_p0.(0...4).sdf 2_p1.0.sdf 2_p2.0.sdf 2_p3.0.sdf
#6 6_p0.(0...130).sdf 6_p1.(0...18).sdf 6_p2.(0...11).sdf
#7 7_p0.(0...2).sdf 7_p1.0.sdf 7_p2.0.sdf 7_p3.0.sdf
#10 10_p0.(0...192).sdf 10_p1.(0...52).sdf 10_p2.(0...47).sdf 10_p3.(0...32).sdf



for cat in [6]:
    http = gHTTP(f'http://zinc.docking.org/db/bysubset/{cat}', pattern='^.*\.(sdf\.gz)$')
    http.set_local(f'/share/public_data/ZINC12/6/{cat}')
    for fname in http.dl():
        http.retr(fname)
    http.reset()
