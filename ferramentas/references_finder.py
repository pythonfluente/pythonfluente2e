# Isso é um rascunho
import re

book_dir = __file__[:-35]
chapter_dir = "capitulos/"
chapter1 = "cap01.adoc"


F = open(book_dir+chapter_dir+chapter1,"r",encoding="utf-8")
f = F.read()
F.close()


#com regex


list_of_files = [book_dir+"capitulos/cap%02d.adoc"%i for i in range(1,25)]


def find_brackets(f):
    brack_re = re.compile('\[\[[\w &]*\]\]')
    list_brack = re.findall(brack_re,f)
    return list_brack

def find_brackets2(f):
    brack_re = re.compile('(\[\[.*\]\])\n+=* ?(.*)')
    list_brack = re.findall(brack_re,f)
    return list_brack

def find_markdown():
    pass



def find_all_brackets():
    dot_ini = ""
    brackets = []
    files = list_of_files
    
    for i in range(23):
        F = open(files[i],"r",encoding="utf-8")
        f = F.read()
        F.close()
        L = find_brackets2(f)  #Lista das Tuplas
        dot_ini = dot_ini+"\n"+L[0][0][1:-1]+"\n"  # Remove a tupla do cap
        L = L[1:]  # Tuplas do cap
        for i in L:
            j = list(i)
            j[0]=j[0][2:-2]  # Remove os [[  ]]
            dot_ini = dot_ini+" = ".join(j)+"\n"
        
    out = open("chapter.ini","w",encoding="utf-8")
    out.write(dot_ini)
        
        #brackets.extend()
    return dot_ini
        
        
 
