#!/usr/bin/env python3

import fileinput
import re

URL_RE = re.compile(r"""(https?://[^\s[<>"']+)\[""")


def find_urls(lines, fpy=True, long=True):
    urls = []
    for line in lines:
        if match := URL_RE.search(line.rstrip()):
            url = match.groups()[0]
            is_fpy = '://fpy.li/' in url
            if (is_fpy and not fpy) or (not is_fpy and not long):
                continue
            if url.endswith('fluentpython.com'):
                # keep uses in examples in chapter 20
                continue
            urls.append(url)
    return urls


def multi_find_urls(fpy=True, long=True):
    urls = find_urls(fileinput.input(), fpy, long)
    for url in urls:
        print(url)

if __name__ == '__main__':
    multi_find_urls(fpy=False)
