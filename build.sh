#!/bin/bash
set -e  # exit when any command fails
asciidoctor Livro.adoc -o index.html
open index.html
