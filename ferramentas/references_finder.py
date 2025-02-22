#!/usr/bin/env python3

import re


book_dir = '../capitulos/'


list_of_files = [book_dir+"/cap%02d.adoc"%i for i in range(1,25)]


def find_anchors(f):
    brack_re = re.compile(r'\[(\[[\w-]+\])\]\n+(?:\[[\w=" -]+\]\n)?=* ?(.*)') 
    list_brack = re.findall(brack_re,f)
    return list_brack


def find_xrefs(f):
    ltrt_re = re.compile(r'<<([\w_]+)>>') 
    list_ltrt = re.findall(ltrt_re,f)
    return list_ltrt


def find_all_anchors():
    dot_ini = ""
    anchors = []
    files = list_of_files
    
    for file_name in files:
        with open(file_name,"r",encoding="utf-8") as fp:
            f = fp.read()
        anchors = find_anchors(f)  #Lista das Tuplas
        dot_ini = dot_ini+"\n"+anchors[0][0]+"\n"  # insere o ident to capitulo
        anchors = anchors[1:]  # Tuplas do cap
        for anchor in anchors:
            ident, text = anchor
            ident = ident[1:-1]
            dot_ini += f'{ident} = {text}\n'
        
    with open("anchors.ini","w",encoding="utf-8") as fp:
        fp.write(dot_ini)


if __name__ == "__main__":
    find_all_anchors()
    print("Done!")    
 