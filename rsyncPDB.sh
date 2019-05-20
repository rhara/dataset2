#!/bin/sh

mkdir -p PDB
rsync -rlptvzihP --delete --port=33444 \
      rsync.wwpdb.org::ftp/data/structures/divided/pdb/ PDB/ 2>/dev/null | \
    tee PDB/logs
