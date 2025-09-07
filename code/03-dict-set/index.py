# adapted from Alex Martelli's example in "Re-learning Python"
# http://www.aleax.it/Python/accu04_Relearn_Python_alex.pdf
# (slide 41) Ex: lines-by-word file index

# tag::INDEX[]
"""Constrói um índice que mapeie cada palavra → lista de ocorrências"""

import re
import sys

WORD_RE = re.compile(r'\w+')

index = {}
with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            word = match.group()
            column_no = match.start() + 1
            location = (line_no, column_no)
            index.setdefault(word, []).append(location)  # <1>

# exibe em ordem alfabética
for word in sorted(index, key=str.upper):
    print(word, index[word])
# end::INDEX[]
