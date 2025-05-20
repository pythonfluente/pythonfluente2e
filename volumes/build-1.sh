#!/bin/bash
set -e  # exit when any command fails
asciidoctor -v vol-1.adoc -o vol-1.html
open vol-1.html
