# -*- coding: utf-8 -*-
#!/usr/bin/env python3 

# 0. Quebras de pagina                        OK
# 1. Separar pontuação das palavras           OK
# 2. Marcar capitulos                         OK
# 3. Separar paragrafos de linhas pequenas.   ??
# 4. Juntar linhas da mesma frase.            OK
# 5. Uma frase por linha                      OK?

import fileinput
import re

text = ""
for line in fileinput.input():
    text += line

regex_cap = r".*(CAP[ÍI]TULO \w+).*\r?\n([\wàáéèíìòóúùãõêâîôû0-9\-,\ ]+)\r?\n"
text = re.sub(regex_cap,"### \g<1> ###\n# \g<2> #",text)

regex_nl = r"([a-zàáéèíìòóúùãõêâîôû0-9,;\-\–])\r\n\r\n([\-\–a-z0-9])"
regex_nl2 = r"\r\n\r\n"

regex_pont = r"([a-zàáéèíìòóúùãõêâîôû0-9)])([!?,;.:][^.])"

regex_sr = r"Sr\."
regex_sra = r"Sra\."
regex_prof = r"Prof\."
regex_profa = r"Profa\."

regex_nl3 = r"([A-Za-zÁÀÉÈàáéèíìòóúùãõêâîôû0-9,;\-\–])\r?\n([\-\–\"\“A-Za-zàáéèíìòóúùãõêâîôû(0-9])"

regex_line = r" (\.”?) ([“A-Z])"

text = re.sub(regex_nl,"\g<1>\n\g<2>",text)
text = re.sub(regex_nl2,"\n",text)

text = re.sub(regex_sr,"SR",text)
text = re.sub(regex_sra,"SRA",text)
text = re.sub(regex_prof,"PROF",text)
text = re.sub(regex_profa,"PROFA",text)

text = re.sub(regex_pont,"\g<1> \g<2>",text)
text = re.sub(regex_nl3,"\g<1> \g<2>",text)

text = re.sub(regex_line," \g<1>\n\g<2>",text)

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
