#!/usr/bin/env python

"""
update map of xrefs to different volumes
"""

import subprocess
import sys

def main():

    print()

def capture_stderr(command):
    result = subprocess.run(command, shell=True, stderr=subprocess.PIPE, text=True)
    return result.stderr

if __name__ == '__main__':
    main()