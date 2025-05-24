from glob import glob
from pathlib import Path
import re

EXCLUDE = [re.compile(regex) for regex in (
    r'http://fluentpython.com',
    r'http://fluentpython.com/data/flags',
    r'http://localhost:8000/flags',
    r'http://localhost:8001/flags',
    r'http://localhost:8002/flags',
    r'http://oreilly.com'
)]

def wanted(url):
    for regex in EXCLUDE:
        if regex.match(url):
            return False
    if 'fpy.li/' in url:
        return False
    if '$$' in url:
        return False
    return True


______ = re.compile(r'(https?://[^[]{1,80}?)\${0,2}\[(.*?)\]')
URL_RE = re.compile(r'(https?://[^\["`$\n]+)([\["])')

start = 27

seen = set()

for path in sorted(glob('1/*.adoc')): # [start:start+3]:
    text = Path(path).read_text()
    matches = URL_RE.findall(text)
    if not matches: continue
    # print('_' * 60 + path)
    for url, delim in matches:
        assert '\n' not in url
        # if wanted(url):
        #     print(f'{url}\t{delim}')
        if (url not in seen) and wanted(url):
            print(url)
            seen.add(url)
