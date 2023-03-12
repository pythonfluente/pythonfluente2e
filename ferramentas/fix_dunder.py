#!/usr/bin/env python3

import argparse
import os
import re
import shutil
import sys

SCRIPT = sys.argv[0]
RE_DUNDER_CODE = re.compile(r'`__.+?__`')
RE_DUNDER_IDENT = re.compile(r'`(__.+?__)`')

def backup(filename: str) -> None:
    msg = ''
    copy_name = filename + '.bkp'
    try:
        shutil.copy2(filename, copy_name)
    except FileNotFoundError:
        msg = f'File {filename!r} not found.'
    if not msg and not os.path.exists(copy_name):
        msg = f'Unable to create {copy_name!r}.'
    if msg:
        print(msg, file=sys.stderr)
        sys.exit(1)

def replace(filename: str) -> str:
    with open(filename) as fp:
        adoc = fp.read()

    for dunder_code in sorted(set(RE_DUNDER_CODE.findall(adoc))):
        ident = RE_DUNDER_IDENT.match(dunder_code)[1]
        adoc = re.sub(dunder_code, f'`+{ident}+`', adoc)
        print(ident)

    with open(filename, 'w') as fp:
        fp.write(adoc)

def main() -> None:
    parser = argparse.ArgumentParser(
        prog=SCRIPT,
        description='Subsitui `__dunder__` por `+__dunder__+`.',
        epilog=f'EXEMPLO:\n\t{SCRIPT} cap01.adoc')
    
    parser.add_argument('asciidoc_filename')
    args = parser.parse_args()
    backup(args.asciidoc_filename)
    replace(args.asciidoc_filename)


if __name__ == '__main__':
    main()
