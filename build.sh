#!/bin/bash
set -e  # exit when any command fails
asciidoctor $1 Livro.adoc -o index.html
open index.html
