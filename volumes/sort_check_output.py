#!/usr/bin/env python3

import fileinput
import re

TASK_RE = re.compile(r'\[\s*(\d+)\]')

def task_id(line):
    found = TASK_RE.match(line)
    return int(match.group(1)) if found else 0

for line in sorted(fileinput.input(), key=task_id):
    print(line, end='')
