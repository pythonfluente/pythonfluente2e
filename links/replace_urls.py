#!/usr/bin/env python3

import sys

def main():
    adoc_name = sys.argv[2]
    pairs_name = sys.argv[1]
    pairs = []
    with open(pairs_name) as fp:
        for line in fp.readlines():
            pair = line.split()[-2:]
            assert len(pair) == 2, f'pair not found: {line}'
            assert pair[0].startswith('/'), f'no path: {line}'
            pairs.append(pair)

    assert len(pairs) > 0, f'no pairs found in {pairs_name}'

    with open(adoc_name) as fp:
        adoc = fp.read()

    initial_adoc = adoc

    for path, url in pairs:
        assert url in adoc, f'{url} not found in {adoc_name}'
        print(path, url)
        short_url = 'https://fpy.li' + path
        adoc = adoc.replace(url, short_url)

    assert len(initial_adoc) < len(adoc), f'{adoc_name} not shortened'

    with open(adoc_name, 'w') as fp:
        fp.write(adoc)


if __name__ == '__main__':
    main()