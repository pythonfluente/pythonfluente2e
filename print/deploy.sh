
#!/bin/bash
set -e  # exit when any command fails
# asciidoctor Livro.adoc -o index.html

scp $1 dh_kqh7yy@pdx1-shared-a1-19.dreamhost.com:/home/dh_kqh7yy/pythonfluente.com/
# rsync -avz --delete ../vol1/pyfl-vol1-pre1.pdf dh_kqh7yy@pythonfluente.com:~/pythonfluente.com/2/

# open https://pythonfluente.com/2/
