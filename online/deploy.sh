
#!/bin/bash
set -e  # exit when any command fails
asciidoctor Livro.adoc -o index.html

#scp index.html dh_kqh7yy@pdx1-shared-a1-19.dreamhost.com:/home/dh_kqh7yy/pythonfluente.com/index.html
rsync -avz --delete index.html dh_kqh7yy@pythonfluente.com:~/pythonfluente.com/2/

open https://pythonfluente.com/2/
