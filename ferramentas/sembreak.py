#!/usr/bin/env python3

import fileinput
import re
import shutil
import sys
from time import strftime


RE_PERIOD = re.compile(r'(\w\w\w)\. +([A-Z])')


def sembreak(text):
    return RE_PERIOD.sub(r'\1.\n\2', text)


def main(adoc_name):
    bkp_name = adoc_name + strftime('-%H-%M-%S') + '.bkp'
    shutil.copy2(adoc_name, bkp_name)

    with open(adoc_name) as fp:
        lines = fp.readlines()

    with open(adoc_name, 'wt') as fp:
        for line in lines:
            if line[0].isalpha():
                line = sembreak(line)
            fp.write(line)


if __name__ == '__main__':
    main(sys.argv[1])