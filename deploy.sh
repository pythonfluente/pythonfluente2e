
#!/bin/bash
set -e  # exit when any command fails
asciidoctor Livro.adoc -o index.html

#scp index.html dh_kqh7yy@pendleton.dreamhost.com:/home/dh_kqh7yy/pythonfluente.com/index.html
rsync -avz --delete index.html dh_kqh7yy@pythonfluente.com:~/pythonfluente.com/

open https://pythonfluente.com
