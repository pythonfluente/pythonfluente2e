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


def arrange_sample(sample, row_len, filler=None):
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
        row = source[start:start+row_len]
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
    octets = bytes(i for i in range(129, 160))
    cp1252 = octets.decode('cp1252', errors='replace')
    used = (char for char in cp1252 if char in non_ascii)
    print('|====')
    compact_display(used, num_cols)
    print('|====')


    print('\n## Other')

    uchars: list[UniChar] = []

    for char, count in ((c, n) for c, n in non_ascii.items()
                        if ord(c) >= 256):
        name = unicodedata.name(char)
        categ = unicodedata.category(char)
        uchars.append(UniChar(char, name, categ, count))

    uchars.sort(key=attrgetter('categ', 'count'))

    print('[cols=">3,^1,11,1,>1"]')
    print('|====')
    for char, name, categ, count in uchars:
        print(f'|`U+{ord(char):04x}`|{char}|{name}|{categ}|{count}')
    print('|====')


if __name__ == '__main__':
    main()
