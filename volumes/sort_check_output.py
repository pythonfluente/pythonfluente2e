#!/usr/bin/env python3

import fileinput
import re

def extract_key(line):
    match = re.search(r'\[\s*(\d+)\s*\]', line)
    return int(match.group(1)) if match else 0

lines = []
for line in fileinput.input():
    lines.append(line)

sorted_lines = sorted(lines, key=extract_key)

for line in sorted_lines:
    print(line, end='')