"""
URL shortener for .htaccess redirects

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
        key = fields[1]
        assert key[0] == '/'
        key = key[1:]
        assert len(key) > 0
        yield (key, fields[2])


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