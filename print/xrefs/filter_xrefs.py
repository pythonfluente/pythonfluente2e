#!/usr/bin/env python3

"""
This script takes the output of this:

```
./pdf_export.sh ../vol1/vol1.adoc 2> invalid-xrefs.txt
```

and lists the xrefs, once each, in the order they appear.

"""

import sys

PREFIX = 'asciidoctor: INFO: possible invalid reference: '


def good_id(xref):
    return any([
        xref.startswith('ch_'),
        xref.endswith('_ex'),
        xref.endswith('_sec'),
        xref.endswith('_part'),
        xref.endswith('_tbl'),
    ])

def main():
    # see this module's docstring for input file
    adoc_msgs = sys.argv[1]
    with open(adoc_msgs) as fp:
        msgs = fp.readlines()

    seen = set()
    xrefs = []
    for line in (m for m in msgs if m.startswith(PREFIX)):
        xref = line[len(PREFIX):].strip()
        if xref in seen:
            continue
        xrefs.append(xref)
        seen.add(xref)

    for xref in xrefs:
        if not good_id(xref):
            print('???', end='')
        print(xref)


if __name__ == '__main__':
    main()