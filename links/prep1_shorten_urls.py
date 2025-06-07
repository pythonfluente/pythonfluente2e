#!/usr/bin/env python3

import fileinput
import re

URL_RE = re.compile(r"""https?://[^\s[<>"']+""")


def find_urls(fpy=True, long=True):
    found = 0
    for line in (l.rstrip() for l in fileinput.input()):
        if match := URL_RE.search(line):
            url = match.group()
            is_fpy = '://fpy.li/' in url
            if (is_fpy and not fpy) or (not is_fpy and not long):
                continue
            print(url)
            found += 1
    # print('FOUND', found, 'URLs')


if __name__ == '__main__':
    find_urls(fpy=False)
