"""
# URL shortener for .htaccess redirects

This script reads a `.htaccess` file and a plain text file with
URLs (the target URLs).

It outputs a list of target URLs and their corresponding short URLs,
made from paths in the FPI.LI domain like `/2d`, `/2e`, etc.
This list is used to replace the target URLs with short URLs
in the `.adoc` files where the target URLs are used.

If a target URL is not in the `.htaccess` file,
the script generates a new short URL
and appends a new `RedirectTemp` directive to the `.htaccess` file.


## `.httaccess` file

A file named `.htaccess` in this format is deployed to the web server
at FPY.LI to redirect short URLs to target URLs (the longer ones).

```
# added: 2025-05-26 16:01:24
RedirectTemp /2d https://mitpress.mit.edu/9780262111584/the-art-of-the-metaobject-protocol/
RedirectTemp /2e https://dabeaz.com/per.html
RedirectTemp /2f https://pythonfluente.com/2/#iter_closer_look

```

When a user agent requests a URL like `https://fpy.li/2d`,
the web server responds with a 302 redirect to the longer URL
`https://mitpress.mit.edu/9780262111584/the-art-of-the-metaobject-protocol/`.

A temporary redirect (code 302)
tells user agents to come back to the same URL at FPY.LI later,
and not update their bookmark.
This allows me update the target URL, if needed.

## Redirects in memory

The `redirects` dict maps short paths to target URLs.
It's loaded from data in the `.htaccess` file.

## Targets in memory

The `targets` dict maps target URLs to short paths.
It's also loaded from data in the `.htaccess` file,
but the algorithm is more complicated.

The same target URL can be mapped to multiple short paths
due to past mistakes when updating the `.htaccess` file.

When loading the `.htaccess` file,
if a target URL is already in the `targets` dict,
we compare the existing short path with the new one
and save the shorter one in the `targets` dict.

That way, we ensure that the shortest path is used for each target URL
in the list of replacements we output to apply to the `.adoc` files.


## Shortening URLs

The `targets` dict maps target URLs to short paths.

To shorten a target URL, find it in the `targets` dict.
If the target URL is found:
    use the existing path.
If the target URL is not found:
    generate a new short path;
    store target and path in both `targets` and `redirects` dicts;
    collect new short path and target URL in a `new_redirects` list
    to be appended to the `.htaccess` file later.
Targets in memory

To avoid generating a new short URL for a target URL,



the `shortener` module provides a way to generate new short URLs


Procedure:

0. create empty dicts named targets and redirects
1. given a target_url, find it in targets;
    1.1. if found, use the short_url stored there
    1.2. if not, generate new short_url and store it in targets and redirects

"""


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