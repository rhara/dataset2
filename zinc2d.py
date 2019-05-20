import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse as dtparse
import time

url = 'http://files.docking.org/2D/AA'
page = requests.get(url).text
soup = BeautifulSoup(page, 'html.parser')
for node in soup.find_all('a'):
    href = node.get('href')
    if href.endswith('.smi') or href.endswith('.txt'):
        res = requests.head(url + '/' + href)
        mtime = time.mktime(dtparse(res.headers['Last-Modified']).timetuple())
        size = res.headers['Content-Length']
        print(href, size, mtime)
