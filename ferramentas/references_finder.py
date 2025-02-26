#!/usr/bin/env python3

import re
import configparser


book_dir = '../capitulos/'
list_of_files = [book_dir+"/cap%02d.adoc"%i for i in range(1,25)]

def find_anchors(f):
    brack_re = re.compile(r'\[(\[[\w-]+\])\]\n+(?:\[[\w=" -]+\]\n)?=* ?(.*)') 
    list_brack = re.findall(brack_re,f)
    return list_brack


def find_refs(f):
    refs_re = re.compile(r'<<([\w_]+)>>') 
    list_refs = re.findall(refs_re,f)
    return list_refs


def find_all_anchors():
    anchors_ini = "# Aqruivo conténdo as ancoras de cada capítulo"
    anchors = []
    files = list_of_files
    
    for file_name in files:
        with open(file_name,"r",encoding="utf-8") as fp:
            f = fp.read()
        anchors = find_anchors(f)  #Lista das Tuplas
        anchors_ini = anchors_ini+"\n"+anchors[0][0]+"\n"  # insere o ident to capitulo
        anchors = anchors[1:]  # Tuplas do cap
        for anchor in anchors:
            ident, text = anchor
            ident = ident[1:-1]
            anchors_ini += f'{ident} = {text}\n'
        
    with open("anchors.ini","w",encoding="utf-8") as fp:
        fp.write(anchors_ini)

def find_all_xrefs():
    xrefs_ini = '''# Referências cruzadas para outras partes
# Aqui só aparcem xrefs <<xxxx>> para outras partes do livro'''
    anchors = configparser.ConfigParser()
    anchors.read('anchors.ini')

    chaps = anchors.sections()  # Lista dos capítulos
    chap_part =  [(i, 'parte 1') for i in set(chaps[0:6])]
    chap_part += [(i, 'parte 2') for i in set(chaps[6:10])]
    chap_part += [(i, 'parte 3') for i in set(chaps[10:17])]
    chap_part += [(i, 'parte 4') for i in set(chaps[17:22])]
    chap_part += [(i, 'parte 5') for i in set(chaps[22:])] #TODO falta um cap nesse último?
    parte = dict(chap_part)

    for file in list_of_files:
        with open(file,"r",encoding="utf-8") as fp:
            f = fp.read()
        actual_chap = re.search(r'\[\[[\w-]+\]\]', f).group(0)[2:-2]
        xrefs_ini += f'\n[{actual_chap}]\n'  # Escreve o nome do capítulo no arquivo
        xrefs_chap = dict() #  {xref, part}
        refs = find_refs(f)
        for ref in refs:
            if ref in xrefs_chap:  
                continue  # Pula caso a ref já esteja listada
            elif ref in anchors[actual_chap]:
                continue  # Pula caso a referência esteja no próprio capítulo
            elif ref in chaps and parte[ref] != parte[actual_chap]:
                #Analisa se a referência é um capítulo
                xrefs_chap[ref] = parte[ref]
            else:
                for chap in chaps:
                    if ref in anchors[chap]:
                        if parte[chap] != parte[actual_chap]:
                            xrefs_chap[ref] = parte[chap]
                    break
                else:
                    xrefs_ini += f'{ref} = NÃO ENCONTRADA\n'
        for xref, xpart in xrefs_chap.items():
                        xrefs_ini += f'{xref} = {xpart}\n'

    with open("xrefs_xparts.ini","w",encoding="utf-8") as fp:
        fp.write(xrefs_ini)






if __name__ == "__main__":
    find_all_xrefs()
    print("Done!")    
 