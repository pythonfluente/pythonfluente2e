
#!/bin/bash
set -e  # exit when any command fails
./build.sh
rsync -avz --delete index.html dh_kqh7yy@pythonfluente.com:~/pythonfluente.com/

#scp index.html dh_kqh7yy@pendleton.dreamhost.com:/home/dh_kqh7yy/pythonfluente.com/index.html
