#!/usr/bin/env python

from lmnet.ftp import gFTP

ftp = gFTP('ftp.ncbi.nlm.nih.gov')
ftp.chdir('/pubchem/Compound/CURRENT-Full/SDF')

ftp.set_local('pubchem/Compund/CURRENT-Full/SDF')

for fname in ftp.dl():
    ftp.retr(fname)
