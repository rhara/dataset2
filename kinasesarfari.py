#!/usr/bin/env python

from lmnet.ftp import gFTP

ftp = gFTP('ftp.ebi.ac.uk')
ftp.chdir('/pub/databases/chembl/KinaseSARfari/releases/5.01')
ftp.set_local('ChEMBL/KinaseSARfari/5.01')

for fname in ftp.dl():
    ftp.retr(fname)
