# -*- coding: utf-8 -*-
#!/usr/bin/env python3 
"""Module to tokenize books."""

# 0. Quebras de pagina                        OK
# 1. Separar pontuação das palavras           OK
# 2. Marcar capitulos                         OK
    # titulo do capitulo na linha seguinte
    # KEYWORDS multilingua (CAPITULO/CHAPTER/...)
# 3. Separar paragrafos de linhas pequenas.   ??
# 4. Juntar linhas da mesma frase.            OK
# 5. Uma frase por linha                      OK?

__version__ = "0.3"

import fileinput
import re
import os
import sys
import argparse

arr_poemas = []
arr_cartas = []
regex_cap = r".*(CAP[ÍI]TULO \w+).*\r?\n([\wàáéèíìòóúùãõêâîôû0-9\-,\ ]+)\r?\n"
regex_nl = r"([a-zàáéèíìòóúùãõêâîôû0-9,;\-\–])\r\n\r\n([\-\–a-z0-9])"
regex_nl2 = r"\r\n\r\n"
regex_pont = r"([a-zàáéèíìòóúùãõêâîôû0-9)])([!?,;.:][^.])"
regex_sr = r"Sr\."
regex_sra = r"Sra\."
regex_prof = r"Prof\."
regex_profa = r"Profa\."
regex_nl3 = r"([A-Za-zÁÀÉÈàáéèíìòóúùãõêâîôû0-9,;\-\–])\r?\n([\-\–\"\“A-Za-zàáéèíìòóúùãõêâîôû(0-9])"
regex_line = r" (\.”?) ([“A-Z])"
regex_par = r" (\.”?)\r?\n([“A-Z])"
regex_poema = r"<poema>(.*?)</poema>"
regex_carta = r"<carta>(.*?)</carta>"
path = os.path.dirname(os.path.realpath(__file__))

def guarda_poema(poema):
    arr_poemas.append(poema[1])
    return f">>{len(arr_poemas)}<<"

def guarda_carta(carta):
    arr_cartas.append(carta[1])
    return f"<<{len(arr_cartas)}>>"

def process_text(text):
    text = re.sub(regex_cap,"### \g<1> ###\n# \g<2> #",text)
    text = re.sub(regex_nl,"\g<1>\n\g<2>",text)
    text = re.sub(regex_nl2,"\n",text)
    text = re.sub(regex_sr,"SR",text)
    text = re.sub(regex_sra,"SRA",text)
    text = re.sub(regex_prof,"PROF",text)
    text = re.sub(regex_profa,"PROFA",text)
    text = re.sub(regex_par,"\g<1>\n\n\g<2>",text)
    text = re.sub(regex_pont,"\g<1> \g<2>",text)
    text = re.sub(regex_nl3,"\g<1> \g<2>",text)
    text = re.sub(regex_line," \g<1>\n\g<2>",text)    
    text = re.sub(regex_poema,guarda_poema,text,flags=re.S)
    text = re.sub(regex_carta,guarda_carta,text,flags=re.S)
    return text

def remove_empty(l):
    return [x.strip() for x in l if x]

def get_conf(args,file_path):
    f = open(f'{path}{file_path}','r')
    txt = f.read()
    f.close()
    ln = txt.split('#')
    ln = remove_empty(ln)
    abrev_dic = {}
    for lan in ln:
        lingua,*abrevs = remove_empty(lan.split('\n'))
        if args.language[0] in lingua:
            abrev_dic[lingua] = abrevs
            break
    return abrev_dic

def process_arguments(__version__):
    parser = argparse.ArgumentParser(
        prog='tok',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=f'''
    --------------------------------------------------------------------
                      Tokenizer v{__version__}
    --------------------------------------------------------------------'''
    )
    parser.add_argument('input_file',metavar='filename',type=argparse.FileType('r'),nargs='?',help='input file of the text to tokenize',default=None)
    parser.add_argument('-o','--output',help='defines an output file',type=argparse.FileType('w'), nargs=1,default=None)
    parser.add_argument('-l','--language',help='language of input',type=str, nargs=1,default='en')
    parser.add_argument('--version','-V', action='version', version='%(prog)s '+__version__)

    return parser.parse_args()

def tokenizer():
    args = process_arguments(__version__)
    text = ""
    if not args.input_file:
        for line in sys.stdin:
            text+=line
    else:
        input = args.input_file
        text = input.read()
    
    chapter_delims = get_conf(args,'/conf/cap.txt')
    abrevs = get_conf(args,'/conf/abrev.txt')
    
    text = process_text(text)
    
    if not args.output:
        sys.stdout.write(text)
    else:
        file = args.output[0]
        file.write(text)
