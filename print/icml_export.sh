#!/bin/bash
asciidoctor -b docbook $1.adoc
pandoc -s -f docbook -t icml -o $1.icml $1.xml
