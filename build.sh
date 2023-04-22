#!/bin/bash
set -e  # exit when any command fails
asciidoctor livro.adoc -o index.html
sed -i -e 's/<img/& loading="lazy" /g' index.html # add lazy loading to images
open index.html
