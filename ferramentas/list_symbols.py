#!/usr/bin/env python3

"""
This CLI script reads stdin or a list of filenames and
prints to stdout an asciidoc document to
visually find missing glyphs after rendering to
HTML or PDF.

Example::

  $ ./list_symbols ../online/index.html > symbols.adoc
"""

import fileinput
from collections import Counter, namedtuple
import unicodedata
from operator import attrgetter
from time import strftime

UniChar = namedtuple('UniChar', 'char name categ count')

def count_non_ascii(lines, counter=None) -> Counter[str]:
    if counter is None:
        non_ascii = Counter()
    else:
        non_ascii = counter
    for line in lines:
        if line.isascii():
            continue
        for char in line:
            if not char.isascii():
                non_ascii[char] += 1
    return non_ascii


def arrange_sample(sample, row_len, filler='x'):
    '''
    Break `sample` iterable into rows of `row_len` items,
    filling the empty places in the last row if needed.
    >>> arrange_sample(range(6), 3)
    [[0, 1, 2], [3, 4, 5]]
    >>> arrange_sample(range(5), 3)
    [[0, 1, 2], [3, 4, None]]
    '''
    source = list(sample)
    rows = []
    for start in range(0, len(source), row_len):
        chars = source[start:start+row_len]
        chars = [(c if c != '\N{REPLACEMENT CHARACTER}' else '?') for c in chars]
        row = [f'&#x{ord(c):x};' for c in chars]
        if len(row) < row_len:
            row.extend([filler]*(row_len-len(row)))
        rows.append(row)
    return rows


def compact_display(characters, row_width):
    sample = arrange_sample(characters, row_width, ' ')
    for row in sample:
        for cell in row:
            print('|'+cell, end='')
        print()

def detail_display(counter, key=None):
    uchars: list[UniChar] = []

    for char, count in ((c, n) for c, n in counter.items()
                        if ord(c) >= 256):
        name = unicodedata.name(char)
        categ = unicodedata.category(char)
        uchars.append(UniChar(char, name, categ, count))

    if key is not None:
        uchars.sort(key=key)

    print('[cols=">2,^1,11,1,>1"]')
    print('|====')
    for char, name, categ, count in uchars:
        print(f'|`U+{ord(char):04x}`|{char}|{name}|{categ}|{count}')
    print('|====')

def main():
    print('Generated', strftime('%H:%M:%S'))
    non_ascii = count_non_ascii(fileinput.input())
    num_cols = 32

    print('\n## Latin 1\n')
    latin1 = [c for c in non_ascii if ord(c) < 256]
    print('|====')
    compact_display(latin1, num_cols)
    print('|====')

    print('\n## CP1252\n')
    octets = bytes(i for i in range(128, 160))
    cp1252 = octets.decode('cp1252', errors='replace')
    used = {char:count for char, count in non_ascii.items() if char in cp1252}
    # print('|====')
    # compact_display(used.keys(), num_cols)
    # print('|====')

    detail_display(used, key=lambda uc: -uc.count)

    print('\n## Other')

    detail_display({c : n for c, n in non_ascii.items() 
                          if (ord(c) >= 256) and c not in cp1252},
                   key=attrgetter('categ', 'count'))


if __name__ == '__main__':
    main()
