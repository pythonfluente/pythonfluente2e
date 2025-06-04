#!/usr/bin/env python3

import fileinput
import re

URL_RE = re.compile(r'https?://([^\s<>"\']+)')

def find_urls(fpy=True, long=True):
    for line in (l.rstrip() for l in fileinput.input()):
        if found := URL_RE.search(line):
            is_short = found.group(1).startswith('fpy.li')
            if ((is_short and not fpy) or 
                (not is_short and not long)):
                continue
            print(fileinput.filelineno(),line)        


if __name__ == '__main__':
    find_urls()
