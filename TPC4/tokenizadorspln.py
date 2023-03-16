# -*- coding: utf-8 -*-
#!/usr/bin/env python3 

# 0. Quebras de pagina
# 1. Separar pontuação das palavras
# 2. Marcar capitulos                         OK
# 3. Separar paragrafos de linhas pequenas.
# 4. Juntar linhas da mesma frase.
# 5. Uma frase por linha

import sys
import fileinput
import re

text = ""
for line in fileinput.input():
    text += line

regex_cap = r".*(CAP[ÍI]TULO \w+).*"
text = re.sub(regex_cap,"\n# \g<1>",text)

regex_nl = r"([a-z0-9,;\-\–\.\?])\r\n\r\n([\-\–a-z0-9])?"

text = re.sub(regex_nl,"\g<1>\n\g<2>",text)

arr_poemas = []
arr_cartas = []

def guarda_poema(poema):
    arr_poemas.append(poema[1])
    return f">>{len(arr_poemas)}<<"

def guarda_carta(carta):
    arr_cartas.append(carta[1])
    return f"<<{len(arr_cartas)}>>"

regex_poema = r"<poema>(.*?)</poema>"
text = re.sub(regex_poema,guarda_poema,text,flags=re.S)

regex_carta = r"<carta>(.*?)</carta>"
text = re.sub(regex_carta,guarda_carta,text,flags=re.S)

print(text)
