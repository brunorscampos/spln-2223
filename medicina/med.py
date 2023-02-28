import re

class Entrada:
    def __init__(self, e):
        elems = re.split(r"@@@",e)
        self.name = elems[0]
        for elem in elems[1:]:
            if elem[0:2] == "es":
                self.es = elem
            elif elem[0:2] == "en":
                self.en = elem
            elif elem[0:2] == "pt":
                self.pt = elem
            elif elem[0:2] == "la":
                self.la = elem
                
    def pretty_print(self):
        print(self.name)
        if hasattr(self,'es'):
            print(self.es,end="")
        if hasattr(self,'en'):
            print(self.en,end="")
        if hasattr(self,'pt'):
            print(self.pt,end="")
        if hasattr(self,'la'):
            print(self.la,end="")
    
    def to_string(self):
        r = self.name
        if hasattr(self,'es'):
            r+=self.es
        if hasattr(self,'en'):
            r+=self.en
        if hasattr(self,'pt'):
            r+=self.pt
        if hasattr(self,'la'):
            r+=self.la
        return r
        
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
    e = Entrada(entry)
    vocab_med[e.name] = e
    
print(len(vocab_med))

with open("medicinaTeste.txt", "w") as f:
    for entry in vocab_med.values():
        f.write(entry.to_string())
        f.write("\n\n")
