#!/usr/bin/env python3

import re
import configparser


book_dir = '../capitulos/' 
FILES = [book_dir+"/cap%02d.adoc"%i for i in range(1,25)]

def find_anchors(file):
    """Encontra todas as âncoras em um capítulo"""
    brack_re = re.compile(r'\[(\[[\w-]+\])\]\n+(?:\[[\w=" -]+\]\n)?=* ?(.*)') 
    list_brack = re.findall(brack_re,file)
    return list_brack


def find_refs(file):
    """Encontra todas as referências em um capítulo"""
    refs_re = re.compile(r'<<([\w_]+)>>') 
    list_refs = re.findall(refs_re,file)
    return list_refs


def find_all_anchors():
    """Procura e grava todas as âncoras dos capítulos no arquivo anchors.ini"""
    anchors_ini = "# Aqruivo conténdo as ancoras de cada capítulo"
    anchors = []
    for file_name in FILES:
        with open(file_name,"r",encoding="utf-8") as fp:
            file = fp.read()
        anchors = find_anchors(file)  #Lista de Tuplas
        anchors_ini = anchors_ini+"\n"+anchors[0][0]+"\n"  # Insere o identificador do capítulo
        anchors = anchors[1:]  # Remove a tupla do capítulo
        for anchor in anchors:
            ident, text = anchor
            ident = ident[1:-1]
            anchors_ini += f'{ident} = {text}\n' 
    with open("anchors.ini","w",encoding="utf-8") as fp:
        fp.write(anchors_ini)

def find_all_xrefs(repeticao = "False"):
    """Procura as referências cruzadas e gera o arquivo xrefs_xparts.ini"""
    xrefs_ini = '''# Referências cruzadas para outras partes
# Aqui só aparecem xrefs <<xxxx>> para outras partes do livro'''
    anchors = configparser.ConfigParser()
    anchors.read('anchors.ini')

    chapters = anchors.sections()  # Lista dos capítulos
    chap_part =  [(i, 'parte 1') for i in chapters[0:6]]
    chap_part += [(i, 'parte 2') for i in chapters[6:10]]
    chap_part += [(i, 'parte 3') for i in chapters[10:16]]
    chap_part += [(i, 'parte 4') for i in chapters[16:21]]
    chap_part += [(i, 'parte 5') for i in chapters[21:]]
    parte = dict(chap_part)

    for file in FILES:
        with open(file,"r",encoding="utf-8") as fp:
            f = fp.read()
        actual_chap = re.search(r'\[\[[\w-]+\]\]', f).group(0)[2:-2]
        xrefs_ini += f'\n[{actual_chap}]\n'  # Escreve o nome do capítulo no arquivo
        xrefs_chap = dict() #  {xref, parte}
        refs = find_refs(f)
        for ref in refs:
            if ref in xrefs_chap and repeticao:  
                continue  # Pula caso a ref já esteja listada
            elif ref in anchors[actual_chap]:
                continue  # Pula caso a referência esteja no próprio capítulo
            elif ref in chapters and parte[ref] != parte[actual_chap]:
                #Analisa se a referência é um capítulo
                xrefs_chap[ref] = parte[ref]
            else:
                for chapter in chapters:  # Procura em cada cap pela âncora
                    if ref in anchors[chapter]:
                        if parte[chapter] != parte[actual_chap]:
                            xrefs_chap[ref] = f'{parte[chapter]} , {chapter}'
                    break
                else:
                    xrefs_ini += f'{ref} = NÃO ENCONTRADA\n'
        for xref, xpart in xrefs_chap.items():
                        xrefs_ini += f'{xref} = {xpart}\n'

    with open("xrefs_xparts.ini","w",encoding="utf-8") as fp:
        fp.write(xrefs_ini)



if __name__ == "__main__":
    find_all_anchors()
    find_all_xrefs()
    print("Done!")    
 