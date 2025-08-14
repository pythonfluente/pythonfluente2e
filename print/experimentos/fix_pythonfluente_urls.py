#!/usr/bin/env python3

"""
In the volume 1 *.adoc files, find links in this form:

```
fpy.li/2p?{ref}[{text}] (vol. {vol}, cap. {ch_num})
```

Replace them with:

```
_{text} (vol.{vol}, cap.{ch_num}, fpy.li/{su})_
```

(vol.2, cap.13, fpy.li/q7)

Where {su} is the short URL for a URL to `pythonfluente.com`, such as:

```
https://pythonfluente.com/2/#{ref}
```

# Steps

1. Edited chapters with those links to isolate the few relevant links into
their own lines.

2. Used `grep fpy.li/2p 1/*.adoc > linkspyfl-web.txt` to follect those links.

3. Wrote list_pyfl_links(), use it to write `pyfl_refs.txt` 

```
./fix_pythonfluente_urls.py > pyfl_refs.txt
```

4. Sent `pyfl_refs.txt` to `short.py` from the
[Fluent Python example code repo](https://github.com/fluentpython/example-code-2e/tree/cf996500070e0d712a3b088d29428f74ddc9fa1f/links) 

"""

import re


ADOC_LINK_RE = re.compile(r'(.*?)\[(.*)]')

PYFL_BASE = 'https://pythonfluente.com/2/'

def list_pyfl_links():
    """Make list of links to PythonFluente.com"""
    with open('links-pyfl-web.txt') as fp:
        lines = fp.readlines()
    
    for line in lines:
        chapter_path, link = line.split(':', maxsplit=1)
        res = ADOC_LINK_RE.match(link)
        if res is None:
            print('NO MATCH:', line)
            continue
        else:
            url, text = res.groups()
            _, ref = url.split('?')
            #print(ref, text, sep='\t')
            print(PYFL_BASE + '#' + ref)

if __name__ == '__main__':
    list_pyfl_links()
