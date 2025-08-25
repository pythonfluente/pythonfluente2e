#!/usr/bin/env python3

import fileinput
import re

from collections.abc import Iterable, Iterator

ADOC_LINK_RE = re.compile(r'https?:[^\[]+[^\]]+')
ADOC_PASS_RE = re.compile(r'pass:\[([^\]]+)')


def block_parser(iter_lines: Iterable[str]) -> Iterator[tuple[bool, str]]:
    in_block = False
    delim = ''
    for line in iter_lines:
        line = line.rstrip()
        if line.startswith('[source'):
            assert not in_block, f'[source... in_block block {line!r}'
            in_block = True
        elif in_block and delim == '':
            assert len(line) == 4 and line.startswith(line[0] * 4), f'expected block delimiter, found {line!r}'
            delim = line
        elif in_block and line == delim:
            in_block = False
            delim = ''
        yield in_block, line

def prepare():
    for in_block, line in block_parser(fileinput.input()):
        if not in_block and len(line) > 80:
            if found := ADOC_PASS_RE.search(line):
                print(found.group(1))
                print()



if __name__ == '__main__':
    prepare()
