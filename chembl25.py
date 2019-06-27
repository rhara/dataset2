#!/usr/bin/env python

from lmnet.ftp import gFTP

ftp = gFTP('ftp.ebi.ac.uk')
ftp.chdir('/pub/databases/chembl/ChEMBLdb/releases/chembl_25')
ftp.set_local('/share/public_data/ChEMBL/ChEMBLdb/25')

for fname in ftp.dl():
    ftp.retr(fname)
