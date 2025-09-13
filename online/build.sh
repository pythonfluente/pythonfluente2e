#!/bin/bash
# $1 is the root .adoc file
set -e  # exit when any command fails
bundle exec asciidoctor -v $1 -o index.html
open index.html
