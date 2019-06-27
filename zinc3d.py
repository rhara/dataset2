#!/usr/bin/env python

from lmnet.http import gHTTP
from itertools import product

chars = ['ABCDEFGHIJK', 'HLMR', 'LMNOP']

for sig in product(chars[0], chars[0], chars[1], chars[2]):
    sig1 = sig[0] + sig[1]
    sig2 = sig[0] + sig[1] + sig[2] + sig[3]

    http = gHTTP(f'http://files.docking.org/3D/{sig1}/{sig2}', pattern='^(.*\.(smi|txt|gz)|num_.*)$')
    http.set_local(f'/share/public_data/ZINC15/3D/{sig1}/{sig2}')
    for fname in http.dl():
        http.retr(fname)
    http.reset()
