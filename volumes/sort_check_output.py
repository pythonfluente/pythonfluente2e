#!/usr/bin/env python3

import fileinput
import re

TASK_RE = re.compile(r'\[\s*(\d+)\]')

def extract_key(line):
    match = TASK_RE.search(line)
    return int(match.group(1)) if match else 0

for line in sorted(fileinput.input(), key=extract_key):
    print(line, end='')
