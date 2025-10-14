#!/bin/bash
set -e  # exit when any command fails
name="${1%.*}-miolo.pdf"
echo $name
bundle exec asciidoctor-pdf -v --theme pyfl-fontmix-theme.yml -a pdf-fontsdir=./fonts/ $1
pdfunite "${1%.*}.pdf" colofao.pdf $name
open $name
