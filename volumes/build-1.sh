#!/bin/bash
set -e  # exit when any command fails
asciidoctor -v vol1.adoc -o vol1.html
open vol1.html
