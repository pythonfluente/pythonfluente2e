#!/usr/bin/env python3

import fileinput
from collections import Counter
import unicodedata

def main():
    non_ascii = Counter()
    for line in fileinput.input():
        if line.isascii():
            continue
        for char in line:
            if not char.isascii():
                non_ascii[char] += 1


    for char, count in non_ascii.most_common():
        name = unicodedata.name(char)
        print(f'{count:5d}  {char}  {name}')


if __name__ == '__main__':
    main()
