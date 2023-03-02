import re
import json
        
vocab_med = {}

with open("medicina.xml","r") as f:
    med = str(f.read())
    
med = re.sub(r"<page number=\"\d+\" position=\"absolute\" top=\"\d+\" left=\"\d+\" height=\"\d+\" width=\"\d+\">","",med)
med = re.sub(r"</page>","",med)
med = re.sub(r"<fontspec id=\"\d+\" size=\"\d+\" family=\".+\" color=\".+\"/>","",med)
med = re.sub(r"<text top=\"\d+\" left=\"\d+\" width=\"\d+\" height=\"\d+\" font=\"\d+\">V</text>\n<text top=\"\d+\" left=\"\d+\" width=\"\d+\" height=\"\d+\" font=\"\d+\">ocabulario</text>\n<text top=\"\d+\" left=\"\d+\" width=\"\d+\" height=\"\d+\" font=\"\d+\">\d+</text>","",med)
med = re.sub(r"<text top=\"\d+\" left=\"\d+\" width=\"\d+\" height=\"\d+\" font=\"\d+\">(<b>)?\ *(</b>)?</text>\n","",med)
med = re.sub(r"\n(?=<text top=\"\d+\" left=\"\d+\" width=\"\d+\" height=\"\d+\" font=\"1?[32]\"><?b?>?\ *\d+\ +)","###",med)
med = re.sub(r"<.+?>","",med)
med = re.sub(r"(^\s*\n)+","",med)
med = re.sub(r"(?<=\ es\ |\ en\ |\ pt\ |\ la\ )\n","",med)
med = re.sub(r"\n\ +(?=es\ +|en\ +|pt\ +|la\ +)","\n@@@",med)

entries = re.split(r"###",med)
entries = entries[1:]

for entry in entries:
    elems = re.split(r"@@@",entry)
    e = {}
    #i, nome, genero, area = re.findall(r"(\d+)(?:\ |\n)+((?:(?:\w|-)+(?:\ |\n)*?)+)\ +(\w)\n(?:\ |\n)*(\w+\ *?)",elems[0])[0]
    #print(i)
    e['nome'] = elems[0]
    for elem in elems[1:]:
        if elem[0:2] == "es":
            e['es'] = elem
        elif elem[0:2] == "en":
            e['en'] = elem
        elif elem[0:2] == "pt":
            e['pt'] = elem
        elif elem[0:2] == "la":
            e['la'] = elem
    vocab_med[e['nome']] = e
    
print(len(vocab_med))

with open("medicina.json", "w") as f:
    json.dump(vocab_med,f,indent=4)
