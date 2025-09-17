#!/bin/bash
set -e  # exit when any command fails
bundle exec asciidoctor-pdf -v --theme pyfl-fontmix-theme.yml -a pdf-fontsdir=./fonts/ $1
open "${1%.*}.pdf"
