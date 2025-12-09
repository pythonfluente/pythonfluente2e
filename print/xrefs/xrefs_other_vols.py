#!/usr/bin/env python3

import subprocess
from pathlib import Path
from typing import NamedTuple

from bs4 import BeautifulSoup

def find_git_root():
    path = Path(__file__).resolve()
    while path != path.parent:
        if (path / '.git').is_dir():
            return path
        path = path.parent
    raise LookupError(f'no .git dir found in {path} or parents')

GIT_ROOT = find_git_root()

INVALID_MSG = 'asciidoctor: INFO: possible invalid reference: '

def list_invalid_xrefs(vol: int) -> list[str]:
    adoc = GIT_ROOT / f'vol{vol}/vol{vol}-cor.adoc'
    cmd = f'''asciidoctor -v {adoc} -o lixo'''
    result = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE, text=True)
    seen = set()
    xrefs = []
    for line in result.stderr.splitlines():
        assert line.startswith(INVALID_MSG), '? msg: ' + line
        xref = line[len(INVALID_MSG):].strip()
        if xref not in seen:
            xrefs.append(xref)
            seen.add(xref)

    return xrefs


def map_short_urls():
    htaccess_path = GIT_ROOT / 'links/FPY.LI.htaccess'
    with open(htaccess_path) as fp:
        lines = fp.readlines()
    long_short = {}
    for line in lines:
        # RedirectTemp /7s	https://pythonfluente.com/2/#anatomy_of_classes_sec
        if line.startswith('RedirectTemp'):
            _, short, long = line.split()
            if long in long_short:
                existing_short = long_short[long]
                if len(existing_short) < len(short):
                    short = existing_short
                elif existing_short <= short:
                    short = existing_short
            long_short[long] = short
    return long_short


def cap_vol(cap: int) -> int:
    return ((cap - 1) // 8) + 1


class XrefTarget(NamedTuple):
    ident: str
    vol: int
    ch: int
    lbl: str = '?'


def find_xref_target(ident) -> XrefTarget:
    for ch in range(1, 25):
        with open(GIT_ROOT / f'online/cap{ch:02d}.adoc') as fp:
            adoc = fp.read()
        if f'[[{ident}]]' in adoc:
            return XrefTarget(ident, cap_vol(ch), ch)
    raise LookupError(f'[[{ident}]] not found')


def load_html_root():
    html_path = find_git_root() / 'online/index.html'
    with open(html_path) as fp:
        html = fp.read()
    return BeautifulSoup(html, 'html.parser')


def get_section_label(root: BeautifulSoup, xref: XrefTarget) -> str:
    element = root.find(id=xref.ident)    
    if element:
        text = element.get_text(strip=True).split()[0].rstrip('.')
        assert text.startswith(f'{xref.ch}.'), text + '|' + repr(xref)
        return f'Seção {text}'
    raise LookupError(f'element {xref.ident!r} not found')


def get_example_label(root: BeautifulSoup, xref: XrefTarget) -> str:
    element = root.find(id=xref.ident)    
    if element:
        text = element.get_text(strip=True).split('.')[0]
        return  f'{text} do Capítulo {xref.ch}'
    raise LookupError(f'element {xref.ident!r} not found')


def label_targets(xrefs: list[XrefTarget]) -> list[XrefTarget]:
    html_path = find_git_root() / 'online/index.html'
    with open(html_path) as fp:
        html = fp.read()
    root = BeautifulSoup(html, 'html.parser')
    result = []
    for xref in xrefs:
        label = 'XXX'
        if xref.ident.endswith('_sec'):
            label = get_section_label(root, xref)
        if xref.ident.startswith('ex_'):
            label = get_example_label(root, xref)
        result.append(xref._replace(lbl=label))
    return result

if __name__ == '__main__':
    #print(find_git_root())
    long_short = map_short_urls()
    xrefs = [find_xref_target(ident) for ident in list_invalid_xrefs(2)]
    
    for xref in label_targets(xrefs):
        #print(xref)
        short = long_short['https://pythonfluente.com/2/#' + xref.ident]
        print(f'<<{xref.ident}>>\thttps://fpy.li{short}[«{xref.lbl}»] (vol.{xref.vol})')
