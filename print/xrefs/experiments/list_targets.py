#!/usr/bin/env python3

import sys
import os


def vol_of_chapter(ch: int) -> int:
    return (ch-1) // 8 + 1


def main(adoc_names):
    for adoc_name in sorted(adoc_names):
        ch = int(os.path.basename(adoc_name)[3:5])
        with open(adoc_name) as adoc:
            lines = adoc.readlines()
        for line in lines:
            if line.startswith('[['):
                ch_id = line.strip()[2:-2]
                print(f'    {ch} : {ch_id!r},')
                break

if __name__ == '__main__':
    main(sys.argv[1:])
