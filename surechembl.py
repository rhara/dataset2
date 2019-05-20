#!/usr/bin/env python

from lmnet.ftp import gFTP

ftp = gFTP('ftp.ebi.ac.uk')
ftp.chdir('/pub/databases/chembl/SureChEMBL/data')
ftp.set_local('ChEMBL/SureChEMBL')

for fname in ftp.dl():
    ftp.retr(fname)
