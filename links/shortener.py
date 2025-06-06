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
    def key(k):
        parts = k.split('-')
        if len(parts) > 1:
            parts = ['z' + p.rjust(8, '0') if p.isnumeric() else p for p in parts]
        return (len(k), '-' in k, parts)
    return min(a, b, key=key)


def load_redirects(pairs: Iterable[tuple[str, str]]) -> tuple[dict, dict]:
    redirects = {}
    for key, url in pairs:
        existing_url = redirects.get(key)
        if existing_url:
            if len(existing_url) < len(url):
                continue
            elif len(existing_url) == len(url):
                url = choose(existing_url, url)
            