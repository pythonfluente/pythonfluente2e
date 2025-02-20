# Isso é um rascunho
import re

book_dir = __file__[:-32]

list_of_files = [book_dir+"capitulos/cap%02d.adoc"%i for i in range(1,25)]

def find_brackets(f):
    brack_re = re.compile('\[(\[[\w-]+\])\]\n+(?:\[[\w=" -]+\]\n)?=* ?(.*)') 
    list_brack = re.findall(brack_re,f)
    return list_brack


def find_LTRT(f):
    ltrt_re = re.compile('<<([\w_]+)>>') 
    list_ltrt = re.findall(ltrt_re,f)
    return list_ltrt

def find_all_brackets():
    dot_ini = ""
    brackets = []
    files = list_of_files
    
    for i in range(23):
        F = open(files[i],"r",encoding="utf-8")
        f = F.read()
        F.close()
        L = find_brackets(f)  #Lista das Tuplas
        dot_ini = dot_ini+"\n"+L[0][0]+"\n"  # Remove a tupla do título do cap
        L = L[1:]  # Tuplas do cap
        for i in L:
            j = list(i)
            j[0]=j[0][1:-1]  # Remove os [[  ]] antes de escrever no arquivo
            dot_ini = dot_ini+" = ".join(j)+"\n"
        
    out = open("chapter.ini","w",encoding="utf-8")
    out.write(dot_ini)
        
        #brackets.extend()
    return dot_ini
        
        
 
