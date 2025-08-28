#!/bin/bash
set -e  # exit when any command fails
bundle exec asciidoctor-pdf -v --theme pyfl-theme.yml $1
open "${1%.*}.pdf"