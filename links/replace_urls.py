#!/usr/bin/env python3

import sys

def main(pairs_file, adoc_path):
    pairs = []
    for line in pairs_file.readlines():
        pair = line.split()[-2:]
        assert len(pair) == 2, f'pair not found: {line}'
        assert pair[0].startswith('/'), f'no path: {line}'
        pairs.append(pair)

    assert len(pairs) > 0, f'no pairs found in {pairs_path}'

    with open(adoc_path) as fp:
        adoc = fp.read()

    initial_adoc = adoc

    replaced = set()

    for path, url in pairs:
        if url in replaced:
            continue
        assert url in adoc, f'{url} not found in {adoc_path}'
        print(path, url)
        # append [ to match URLs in Asciidoc links `url[text]`, not URLs in code etc.
        short_url = f'https://fpy.li{path}['
        adoc = adoc.replace(url + '[', short_url)
        replaced.add(url)

    assert len(initial_adoc) > len(adoc), f'{adoc_path}: {len(initial_adoc)=} {len(adoc)=}'

    with open(adoc_path, 'w') as fp:
        fp.write(adoc)


if __name__ == '__main__':
    pairs_path = sys.argv[1]
    adoc_path = sys.argv[2]
    pairs_file = open(pairs_path)
    main(pairs_file, adoc_path)