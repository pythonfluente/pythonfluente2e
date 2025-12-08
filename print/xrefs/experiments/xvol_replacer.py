#!/usr/bin/env python

import sys
import os
import tempfile
import shutil

def load_replacements(mapping_file):
    replacements = []
    with open(mapping_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            old, new = line.split(maxsplit=1)
            replacements.append((old, new))
    return replacements

def replace_in_file(file_path, replacements):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_filename = temp_file.name
        with open(file_path, 'r') as original_file:
            content = original_file.read()
            for old_text, new_text in replacements:
                content = content.replace(old_text, new_text)
            temp_file.write(content)
    shutil.move(temp_filename, file_path)

def main():
    if len(sys.argv) < 3:
        print("xvol_replacer.py mapping_file.tsv file1.txt file2.txt ...")
        sys.exit(1)
    
    mapping_file = sys.argv[1]
    target_files = sys.argv[2:]
    
    replacements = load_replacements(mapping_file)
    
    for file_path in target_files:
        if os.path.exists(file_path) and not os.path.isdir(file_path):
            replace_in_file(file_path, replacements)

if __name__ == "__main__":
    main()