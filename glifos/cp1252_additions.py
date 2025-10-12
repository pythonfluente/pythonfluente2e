#!/usr/bin/env python3

from unicodedata import name

RC = '\N{REPLACEMENT CHARACTER}'

def cp1252():
    start = 128
    span = 32
    print('## Characters in CP1252 but not in Latin-1')
    for i in range(start, start+span):
        try:
            char = bytes([i]).decode('cp1252')
        except UnicodeDecodeError:
            char = ' '
            code = ' ' * 6 
            char_name = '_unused_'
        else:
            code = f'U+{ord(char):04X}'
            char_name = name(char)
        print(f'{i:X}  {code}  {char}  {char_name}')

cp1252()
