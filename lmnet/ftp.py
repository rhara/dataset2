from ftplib import FTP
import dateutil.parser as dtparser
import sys, os, time
import tqdm
from .util import prettysize, prettymtime

class gFTP:
    def __init__(self, host, user='anonymous', passwd='hara.ryuichiro@gmail.com', timeout=10):
        self.ftp = FTP(host, user, passwd, timeout=timeout)
        self.localdir = None
        self.ls = []
        self.D = {}

    def chdir(self, path):
        self.ftp.cwd(path)
        self.ls.clear()
        self.ftp.dir('.', self.ls.append)
        self.D.clear()
        for line in self.ls:
            it = line.split(maxsplit=8)
            mode, size, mtime1, mtime2, mtime3, fname = it[0], it[4], it[5], it[6], it[7], it[8]
            mtime = ' '.join([mtime1, mtime2, mtime3])
            mtime = time.mktime(dtparser.parse(mtime).timetuple())
            size = int(size)
            n = 0
            for x in mode:
                n *= 2
                if x != '-':
                    n += 1
            mode = oct(n)[2:]
            self.D[fname] = (mode, size, mtime)

    def set_local(self, dirname=None):
        if dirname:
            self.localdir = os.path.abspath(dirname)
            os.makedirs(self.localdir, exist_ok=True)
            os.chdir(self.localdir)
        else:
            self.localdir = os.path.abspath('.')

    def dl(self):
        for fname in self.D:
            already_exists = os.path.exists(fname)
            mode, size, mtime = self.D[fname]
            if already_exists:
                st = os.stat(fname)
                size_from_os = st.st_size
                mtime_from_os = st.st_mtime
                if size_from_os == size and mtime_from_os == mtime:
                    continue
            if len(mode) == 4 and mode[0:1] == '1':
                continue
            yield fname

    def retr(self, fname):
        mode, size, mtime = self.D[fname]
        out = open(fname, 'wb')
        print(f'Download {prettymtime(mtime)} {fname} ({prettysize(size)})')
        with tqdm.tqdm(total=size, unit_scale=True, desc=fname, miniters=1, file=sys.stdout, leave=False) as pbar:
            def cb(data):
                pbar.update(len(data))
                out.write(data)
            self.ftp.retrbinary(f'RETR {fname}', cb)
        out.close()
        os.utime(fname, (mtime, mtime))
