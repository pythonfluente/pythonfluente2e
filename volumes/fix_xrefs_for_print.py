#!/usr/bin/env python3

import configparser
import os
import re
import shutil
import subprocess
import sys
from glob import glob
from pathlib import Path

ANCHORS_PATH = Path('../ferramentas/anchors.ini')
ANCHOR_RE = re.compile(r'\[(\[[\w-]+\])\]\n+(?:\[[\w=" -]+\]\n)?=* ?(.*)') 

VOLUME_MAP = {
    1 : {
        1 : 'ch_data_model',
        2 : 'ch_sequences',
        3 : 'ch_dicts_sets',
        4 : 'ch_str_bytes',
        5 : 'ch_dataclass',
        6 : 'ch_refs_mut_mem',
    },
    2 : {
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
    },
    3 : {
        17 : 'ch_generators',
        18 : 'ch_with_match',
        19 : 'ch_concurrency_models',
        20 : 'ch_executors',
        21 : 'ch_async',
        22 : 'ch_dynamic_attrs',
        23 : 'ch_descriptors',
        24 : 'ch_class_metaprog',
    }
}

CHAPTERS_BY_LABEL = {VOLUME_MAP[vo][ch] : (vo, ch) for vo in VOLUME_MAP for ch in VOLUME_MAP[vo]}
CHAPTERS_BY_NUMBER = {CHAPTERS_BY_LABEL[label][1] : (CHAPTERS_BY_LABEL[label][0], label) for label in CHAPTERS_BY_LABEL}

def list_invalid_refs():
    command = 'asciidoctor -v vol-1.adoc'
    output = subprocess.run(command, shell=True, stderr=subprocess.PIPE, text=True)
    assert output.returncode == 0
    res = set()
    for line in output.stderr.splitlines():
        if 'invalid reference' in line:
            res.add(line.split()[-1])
        else:
            print('*** Unexpected output:', line, file=sys.stderr)
            sys.exit(1)
    return sorted(res)


def find_anchors(path):
    """Encontra todas as âncoras nos AsciiDoc de um path"""
    with open(path) as fp:
        text = fp.read()
    return ANCHOR_RE.findall(text)


def load_anchors():
    config = configparser.ConfigParser()
    config.read(ANCHORS_PATH, encoding='utf-8')
    ch_count = len(config.sections())
    assert ch_count == 24, f'Expected 24 sections (chapters), found {ch_count}'
    result = {}
    for n, ch_id in enumerate(config.sections(), 1):
        section = config[ch_id]
        for key, value in section.items():
            #print(f"  {key} = {value}")
            assert key not in result, f"Duplicate key {key!r}: {value!r}"
            result[key] = (n, value)    
    return result


def backup(filename: str) -> None:
    msg = ''
    copy_name = filename + '.bkp'
    try:
        shutil.copy2(filename, copy_name)
    except FileNotFoundError:
        msg = f'File {filename!r} not found.'
    if not msg and not os.path.exists(copy_name):
        msg = f'Unable to create {copy_name!r}.'
    if msg:
        print(msg, file=sys.stderr)
        sys.exit(1)


def replace(subs, filename: str) -> None:
    with open(filename) as fp:
        adoc = fp.read()

    for ref, new_text in subs.items():
        adoc = adoc.replace(ref, new_text)

    with open(filename, 'w') as fp:
        fp.write(adoc)


def expand_anchor(ref, anchors):
    assert ref in anchors, f'Anchor {ref!r} not found in anchors dict'
    ch_num, text = anchors[ref]
    vol, _ = CHAPTERS_BY_NUMBER[ch_num]
    return f'fpy.li/2p?{ref}[{text}] (vol. {vol}, cap. {ch_num})'


def build_substitutions(refs, anchors):
    subs = {}
    for ref in refs:
        key = f'<<{ref}>>'
        if ref.startswith('ch_') or ref.startswith('vo_'):
            value = '_{' + ref + '}_'
        else:
            value = expand_anchor(ref, anchors)
        subs[key] = value
    
    return subs


def main():
    irefs = list_invalid_refs()
    anchors = load_anchors()
    subs = build_substitutions(irefs, anchors)
    for filename in glob('1/*.adoc'):
        print('processing', filename)
        backup(filename)
        replace(subs, filename)


if __name__ == "__main__":
    main()
