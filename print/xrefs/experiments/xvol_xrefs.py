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
    adoc = find_git_root() / 'vol2/vol2-cor.adoc'
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

SHORTENER_OUTPUT = '''
+ /4q	https://pythonfluente.com/2/#ch_ifaces_prot_abc
+ /4r	https://pythonfluente.com/2/#ch_op_overload
+ /4s	https://pythonfluente.com/2/#ch_generators
+ /4t	https://pythonfluente.com/2/#ch_seq_methods
= /22	https://pythonfluente.com/2/#pattern_matching_case_study_sec
+ /4v	https://pythonfluente.com/2/#classes_protocols_part
+ /4w	https://pythonfluente.com/2/#how_slicing_works_sec
+ /4x	https://pythonfluente.com/2/#sliceable_sequence_sec
= /25	https://pythonfluente.com/2/#virtual_subclass_sec
+ /4y	https://pythonfluente.com/2/#lispy_environ_sec
+ /4z	https://pythonfluente.com/2/#subclass_builtin_woes_sec
+ /52	https://pythonfluente.com/2/#slots_sec
= /29	https://pythonfluente.com/2/#typeddict_sec
+ /53	https://pythonfluente.com/2/#ch_class_metaprog
= /2a	https://pythonfluente.com/2/#problems_annot_runtime_sec
+ /54	https://pythonfluente.com/2/#ch_more_types
+ /55	https://pythonfluente.com/2/#ch_descriptors
+ /56	https://pythonfluente.com/2/#ch_inheritance
= /2c	https://pythonfluente.com/2/#positional_pattern_implement_sec
+ /57	https://pythonfluente.com/2/#ch_async
+ /58	https://pythonfluente.com/2/#runtime_annot_sec
+ /59	https://pythonfluente.com/2/#multi_hashing_sec
+ /5a	https://pythonfluente.com/2/#iterable_reducing_sec
+ /5b	https://pythonfluente.com/2/#flexible_new_sec
+ /5c	https://pythonfluente.com/2/#ch_closure_decorator
+ /5d	https://pythonfluente.com/2/#ch_design_patterns
+ /5e	https://pythonfluente.com/2/#lispy_parser_sec
+ /5f	https://pythonfluente.com/2/#overload_sec
+ /5g	https://pythonfluente.com/2/#numbers_abc_proto_sec
+ /5h	https://pythonfluente.com/2/#runtime_checkable_proto_sec
+ /5j	https://pythonfluente.com/2/#variance_sec
+ /5k	https://pythonfluente.com/2/#generic_iterable_types_sec
+ /5m	https://pythonfluente.com/2/#typed_double_sec
+ /5n	https://pythonfluente.com/2/#enhancing_with_init_subclass_sec
+ /5p	https://pythonfluente.com/2/#more_type_hints_further_sec
+ /5q	https://pythonfluente.com/2/#max_overload_sec
'''

SHORT_URLS = {line.split()[2]:line.split()[1] for line
              in SHORTENER_OUTPUT.strip().split('\n')}


def replace_xrefs_to_vols():
    html_path = find_git_root() / 'online/index.html'
    with open(html_path) as fp:
        html = fp.read()
    root = BeautifulSoup(html, 'html.parser')
    replacements = []
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
            
        #else:
        #    raise ValueError(f'unexpected xref: {xref!r}')
        link = BASE_URL + '#' + xref
        #print(f'<<{xref}>>', f'{text} &#91;vol.{volume}, fpy.li{SHORT_URLS[link]}&#93;')
        # https://fpy.li/24[«Capítulo 24»] (vol.3)
        repl = f'<<{xref}>>\t {link}[«{text}»] (vol.{volume})'
        print(repl)
        replacements.append(repl)
    return replacements


if __name__ == '__main__':
    replace_xrefs_to_vols()
