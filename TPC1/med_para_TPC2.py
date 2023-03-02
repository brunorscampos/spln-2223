import re
import json

vocab_med = {
    'completas' : {},
    'remissivas' : {},
}

with open("medicina.xml","r") as f:
    med = str(f.read())
    
med = re.sub(r'<text.* font="1">ocabulario.*</text>', r'###', med)
med = re.sub(r'.*\n###\n.*\n', r'___', med)
med = re.sub(r'<page.*\n|</page>\n', r'', med)
med = re.sub(r'<text.* font="3"><b>\s*(\d+.*)</b></text>', r'###C\1', med)
med = re.sub(r'<text.* font="3"><b>\s*(\S.*)</b></text>', r'###R\1', med)
med = re.sub(r'<text.* font="0">\s*(\w\w)\s*</text>', r'@\1', med)
med = re.sub(r'<text.*font="7">\s*<i>\s*(.*)</i>\.*</text>', r'@T\1', med)
med = re.sub(r'\n@T\s*\n(@T)?', r' ', med)
med = re.sub(r'<text.*font="5">\s*</text>\n', r'', med)
med = re.sub(r'(###[CR].*\n)<text.*font="6">\s*<i>\s*(.*)</i>\.*</text>', r'\1!\2', med)
med = re.sub(r'<text.*font="[05]">\s*</text>', r'', med)
med = re.sub(r'<text.*font="[05]">\s*(SIN\.-(.*?))?(VAR\.-(.*))?</text>', r'$S\2\n$V\4', med)
med = re.sub(r'<text.*font="[05]">\s*Vid\.-(.*)</text>', r'$I\1', med)
med = re.sub(r'\$I(.*)\n<text.*font="5">(.*)</text>',r'\1\2',med)
med = re.sub(r'<text.*font="9">(.*)</text>', r'#N\1', med)
med = re.sub(r'#N\s*Nota\.-', r'#N', med)
med = re.sub(r'<.*>\n?', r'', med)
med = re.sub(r'\n\s*\n', r'\n', med)

entries = med.split('###')

for entrada in entries:
    if entrada[0] == 'C':
        elems = entrada.split('\n')
        header = re.match(r'C(\d+)\s+((\w*\s*)+)\s+(\w)',elems[0])
        if header and header.groups:
            index = int(header.group(1))
            termo = header.group(2)
            genero = header.group(4)
            areas = []
            sinonimos = []
            variacoes = []
            traducoes = {
                'pt' : [],
                'en' : [],
                'es' : [],
                'la' : [],
            }
            nota = ''
            flag = ''
            for linha in elems:
                if len(linha) > 0:
                    if linha[0] == '!':
                        areas = linha[1:]
                        areas = re.sub(r'\s\s+',' ',areas)
                        areas = areas.split(' ')
                    elif '$S' in linha:
                        sinonimos = linha[2:]
                        sinonimos = sinonimos.split(';')
                    elif '$V' in linha:
                        variacoes = linha[2:]
                        variacoes = variacoes.split(';')
                    elif linha[0] == '@':
                        if '@es' in linha:
                            flag = 'es'
                        elif '@en' in linha:
                            flag = 'en'
                        elif '@pt' in linha:
                            flag = 'pt'
                        elif '@la' in linha:
                            flag = 'la'
                        elif flag:
                            traducoes[flag].append(linha[2:])
                    elif '#N' in linha:
                        nota += linha[2:]
            vocab_med['completas'][index] = {
                'index' : index,
                'termo' : termo,
                'genero' : genero,
                'areas' : areas,
                'sinonimos' : sinonimos,
                'variacoes' : variacoes,
                'traducoes' : traducoes,
                'nota' : nota,
            }
    elif entrada[0] == 'R':
        elems = entrada.split('\n')
        header = elems[0]
        termo = header[1:]
        vids = []
        for linha in elems:
            if '$I' in linha:
                vids.append(linha[2:])
        vocab_med['remissivas'][termo] = {
            'termo' : termo,
            'vids' : vids,
        }

with open("medicina_para_TPC2.json", "w") as f:
    json.dump(vocab_med,f,indent=4)
