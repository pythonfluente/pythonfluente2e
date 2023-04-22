#!/bin/bash
set -e  # exit when any command fails
asciidoctor -r ./ferramentas/addLazyLoadingImages.rb livro.adoc -o index.html
open index.html
