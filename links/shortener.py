"""
# URL shortener for .htaccess redirects

This script reads a `.htaccess` file and a plain text file with
URLs (the target URLs).

It outputs a list of target URLs and corresponding paths
for short URLs in the FPI.LI domain like `/2d`, `/2e`, etc.
This list is used to replace the target URLs with short URLs
in the `.adoc` files where the target URLs are used.

If a target URL is not in the `.htaccess` file,
the script generates a new short URL
and adds a new `RedirectTemp` directive to the `.htaccess` file,
appending it in place with a timestamp.

## Redirects in memory

The `redirects` dict maps short paths to target URLs.
It's loaded from data in the `.htaccess` file.

## Targets in memory

The `targets` dict maps target URLs to short paths.
It's also loaded from data in the `.htaccess` file,
but the algorithm is more complicated.

The same target URL can be mapped to multiple short paths
in `.htaccess` when the same target URL was added more
than once with different short paths by mistake.
We cannot fix these mistakes because the redundant
short paths are printed in Fluent Python Second Edition.

When loading the `.htaccess` file,
if a target URL is already in the `targets` dict,
we compare the existing short path with the new one
and save the shorter one in the `targets` dict.

That way, we ensure that the shortest path is used for each target URL
in the list of replacements to apply to the `.adoc` files.


## Shortening URLs

The `targets` dict maps target URLs to short paths.

To shorten a target URL, find it in the `targets` dict.
If the target URL is found:
    use the existing short path.
If the target URL is not found:
    generate a new short path;
    store target and path in both `targets` and `redirects` dicts;
    collect new short path and target URL in a `new_redirects` list
    to be appended to the `.htaccess` file at the end of the process.

"""

import itertools
from collections.abc import Iterable, Iterator


def parse_htaccess(text: str) -> Iterator[tuple[str, str]]:
    for line in text.splitlines():
        fields = line.split()
        if len(fields) < 3 or fields[0] != 'RedirectTemp':
            continue
        path = fields[1]
        assert path[0] == '/', f'Missing /: {path!r}'
        path = path[1:]  # Remove leading slash
        assert len(path) > 0, f'Root path in line {line!r}'
        yield (path, fields[2])


def choose(a: str, b: str) -> str:
    def key(k: str) -> tuple[int, bool, list[str]]:
        parts = k.split('-')
        if len(parts) > 1:
            parts = [(f'z{p:>08}' if p.isnumeric() else p) for p in parts]
        return len(k), '-' in k, parts

    return min(a, b, key=key)


def load_redirects(pairs: Iterable[tuple[str, str]]) -> tuple[dict, dict]:
    redirects = {}
    targets = {}
    for short_url, url in pairs:
        url = redirects.setdefault(short_url, url)
        existing_short_url = targets.get(url)
        if existing_short_url is None:
            targets[url] = short_url
        else:
            targets[url] = choose(short_url, existing_short_url)

    return redirects, targets


SDIGITS = '23456789abcdefghjkmnpqrstvwxyz'


def gen_short(start_len=1) -> Iterator[str]:
    """Generate every possible sequence of SDIGITS, starting with start_len"""
    length = start_len
    while True:
        for digits in itertools.product(SDIGITS, repeat=length):
            yield ''.join(digits)
        length += 1


def gen_unused_short(redirects: dict) -> Iterator[str]:
    """Generate next available short URL of len >= 2."""
    for short in gen_short(2):
        if short not in redirects:
            yield short
