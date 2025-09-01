#!/usr/bin/env python

import subprocess
from bs4 import BeautifulSoup
from pathlib import Path

CHAPTER_ID = {
    1 : 'ch_data_model',
    2 : 'ch_sequences',
    3 : 'ch_dicts_sets',
    4 : 'ch_str_bytes',
    5 : 'ch_dataclass',
    6 : 'ch_refs_mut_mem',
    7 : 'ch_func_objects',
    8 : 'ch_type_hints_def',
    9 : 'ch_closure_decorator',
    10 : 'ch_design_patterns',
    11 : 'ch_pythonic_obj',
    12 : 'ch_seq_methods',
    13 : 'ch_ifaces_prot_abc',
    14 : 'ch_inheritance',
    15 : 'ch_more_types',
    16 : 'ch_op_overload',
    17 : 'ch_generators',
    18 : 'ch_with_match',
    19 : 'ch_concurrency_models',
    20 : 'ch_executors',
    21 : 'ch_async',
    22 : 'ch_dynamic_attrs',
    23 : 'ch_descriptors',
    24 : 'ch_class_metaprog',
}

CHAPTER_NUMBER = {i:n for (n, i) in CHAPTER_ID.items()}


def find_git_root():
    path = Path(__file__).resolve()
    while path != path.parent:
        if (path / '.git').is_dir():
            return path
        path = path.parent
    raise LookupError(f'no .git dir found in {path} or parents')


INVALID_MSG = 'asciidoctor: INFO: possible invalid reference: '


def list_invalid_xrefs() -> list[str]:
    adoc = find_git_root() / 'vol1/vol1.adoc'
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


def get_section_title(ident: str, root: BeautifulSoup) -> str:
    element = root.find(id=ident)    
    if element:
        return element.get_text(strip=True)
    raise LookupError(f'element {ident!r} not found')


def section_numbers(sec_title: str):
    parts = sec_title.split('.')
    numbers = []
    for part in parts:
        try:
            numbers.append(int(part))
        except ValueError:
            break
    assert len(numbers) > 0, 'no number prefix: ' + repr(sec_title)
    return numbers

BASE_URL = 'https://pythonfluente.com/2/'

PART_VOL = {
    'data_structures_part': 1,
    # 'function_objects_part': 2,  # may be vol 2 or 3
    'classes_protocols_part': 2,
    'control_flow_part': 3,
    'metaprog_part': 3,
}

PART_TITLE = {
    'data_structures_part': 'I—Estruturas de dados',
    'function_objects_part': 'II—Funções como objetos',
    'classes_protocols_part': 'III—Classes e protocolos',
    'control_flow_part': 'IV—Controle de fluxo',
    'metaprog_part': 'V—Metaprogramação',
}

def replace_xrefs_to_vols():
    html_path = find_git_root() / 'online/index.html'
    with open(html_path) as fp:
        html = fp.read()
    root = BeautifulSoup(html, 'html.parser')
    for xref in list_invalid_xrefs():
        if xref.startswith('ch_'):
            chapter = CHAPTER_NUMBER[xref]
            text = f'Capítulo {chapter}'
            volume = (chapter - 1) // 8 + 1
        elif xref.endswith('_part'):
            volume = PART_VOL[xref]
            text = PART_TITLE[xref]
        elif xref.endswith('_sec'):
            title = get_section_title(xref, root)
            numbers = section_numbers(title)
            number_str = '.'.join(str(n) for n in numbers)
            chapter = numbers[0]
            volume = (chapter - 1) // 8 + 1
            text = f'Seção {number_str}'
        else:
            raise ValueError(f'unexpected xref: {xref!r}')
        link = BASE_URL + '#' + xref
        print(f'<<{xref}>>', f'{text} [vol.{volume}, {link}]')

if __name__ == '__main__':
    replace_xrefs_to_vols()
