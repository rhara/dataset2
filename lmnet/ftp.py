from ftplib import FTP, error_perm
import dateutil.parser as dtparser
import sys, os, time
import tqdm
from .util import prettysize, prettymtime

class gFTP:
    def __init__(self, host, user='anonymous', passwd='hara.ryuichiro@gmail.com', timeout=10):
        self.curdir = os.getcwd()
        self.ftp = FTP(host, user, passwd, timeout=timeout)
        self.localdir = None
        self.D = {}

    def chdir(self, path):
        self.ftp.cwd(path)
        self.D.clear()
        try:
            """
            If MLSD command on ftp server is supported
            """
            for fname, opt in self.ftp.mlsd('.'):
                if opt['type'] in ['cdir', 'pdir']:
                    continue
                mtime = opt['modify']
                mtime = time.mktime(time.strptime(mtime, '%Y%m%d%H%M%S'))
                self.D[fname] = (int(opt['size']), mtime)
        except error_perm:
            """
            If MLSD command on ftp server is not supported
            """
            ls = []
            print('No support for MLSD command', file=sys.stderr)
            self.ftp.dir('.', ls.append)
            for line in ls:
                it = line.split(maxsplit=8)
                mode, size, mtime1, mtime2, mtime3, fname = it[0], it[4], it[5], it[6], it[7], it[8]
                if mode[0] == 'd':
                    continue
                mtime = ' '.join([mtime1, mtime2, mtime3])
                mtime = time.mktime(dtparser.parse(mtime).timetuple())
                size = int(size)
                self.D[fname] = (size, mtime)

    def set_local(self, dirname=None):
        if dirname:
            self.localdir = os.path.abspath(dirname)
            os.makedirs(self.localdir, exist_ok=True)
            os.chdir(self.localdir)
        else:
            self.localdir = os.path.abspath('.')

    def reset(self):
        os.chdir(self.curdir)

    def dl(self):
        for fname in self.D:
            already_exists = os.path.exists(fname)
            size, mtime = self.D[fname]
            if already_exists:
                st = os.stat(fname)
                size_from_os = st.st_size
                mtime_from_os = st.st_mtime
                if size_from_os == size and mtime_from_os == mtime:
                    continue
            yield fname

    def retr(self, fname):
        size, mtime = self.D[fname]
        out = open(fname, 'wb')
        print(f'Download {prettymtime(mtime)} {fname} ({prettysize(size)})')
        with tqdm.tqdm(total=size, ncols=0, desc=fname) as pbar:
            def cb(data):
                pbar.update(len(data))
                out.write(data)
            self.ftp.retrbinary(f'RETR {fname}', cb)
        out.close()
        os.utime(fname, (mtime, mtime))
