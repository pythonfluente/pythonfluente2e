#!/bin/bash
set -e  # exit when any command fails
bundle exec asciidoctor -v Livro.adoc -o index.html
open index.html
