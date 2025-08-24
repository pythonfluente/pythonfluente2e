#!/bin/bash
set -e  # exit when any command fails
asciidoctor-pdf -a media=preprint --theme pyfl-theme.yml $1
open "${1%.*}.pdf"