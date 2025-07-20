#!/usr/bin/env python3

import fileinput
import re


RE_PERIOD = re.compile(r'(\w\w\w)\. +([A-Z])')


def sembreak(text):
    return RE_PERIOD.sub(r'\1.\n\2', text)


def main():
    for line in fileinput.input(encoding="utf-8"):
        if line[0] not in '.| ':
            line = sembreak(line)
        print(line, end='')


if __name__ == '__main__':
    main()