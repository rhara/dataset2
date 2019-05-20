import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse as dtparse
import sys, time, os, re
import tqdm


class gHTTP:
    def __init__(self, urlbase, pattern='(.*)'):
        self.curdir = os.getcwd()

        self.urlbase = urlbase
        self.localdir = None
        self.D = {}

        print(f'In {self.urlbase} ...', file=sys.stderr)
        listpage = requests.get(self.urlbase).text
        pat = re.compile(pattern)

        soup = BeautifulSoup(listpage, 'html.parser')

        for node in soup.find_all('a'):
            href = node.get('href')
            if pat.match(href):
                res = requests.head(self.urlbase + '/' + href)
                mtime = time.mktime(dtparse(res.headers['Last-Modified']).timetuple())
                size = int(res.headers['Content-Length'])
                self.D[href] = (size, mtime)

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

        res = requests.get(self.urlbase + '/' + fname, stream=True)

        pbar = tqdm.tqdm(total=size, ncols=0, desc=fname)

        with open(fname, 'wb') as out:
            for chunk in res.iter_content(chunk_size=1024):
                out.write(chunk)
                pbar.update(len(chunk))
        pbar.close()
        os.utime(fname, (mtime, mtime))
