#!/usr/bin/env python3

import fileinput
from collections import Counter, namedtuple
import unicodedata
from operator import attrgetter

UniChar = namedtuple('UniChar', 'char name categ count')

def main():
    non_ascii = Counter()
    for line in fileinput.input():
        if line.isascii():
            continue
        for char in line:
            if not char.isascii():
                non_ascii[char] += 1

    chars = []
    for char, count in non_ascii.items():
        name = unicodedata.name(char)
        categ = unicodedata.category(char)
        chars.append(UniChar(char, name, categ, count))
       
    chars.sort(key=attrgetter('categ', 'char'))
        
    for char, name, categ, count in chars:
        print(f'U+{ord(char):04x}\t{char}\t{categ}\t{count}\t{name} ')


if __name__ == '__main__':
    main()
