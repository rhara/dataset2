#!/usr/bin/env python

from lmnet.http import gHTTP
from itertools import product

chars = 'ABCDEFGHIJK'

for sig in product(chars, chars):
    sig = sig[0] + sig[1]

    http = gHTTP(f'http://files.docking.org/2D/{sig}', pattern='^.*\.(smi|txt)$')
    http.set_local(f'/share/public_data/ZINC15/2D/{sig}')
    for fname in http.dl():
        http.retr(fname)
    http.reset()
