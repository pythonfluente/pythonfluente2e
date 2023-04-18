#!/bin/bash
set -e  # exit when any command fails
asciidoctor livro.adoc -o index.html
open index.html
