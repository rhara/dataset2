#!/bin/sh

BASEDIR='/share/public_data/PDB'

mkdir -p ${BASEDIR}
rsync -rlptvzihP --delete --port=33444 \
      rsync.wwpdb.org::ftp/data/structures/divided/pdb/ ${BASEDIR}/ 2>/dev/null | \
    tee ${BASEDIR}/logs
