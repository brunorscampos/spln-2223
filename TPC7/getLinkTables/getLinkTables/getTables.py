#!/usr/bin/env python3 
from bs4 import BeautifulSoup as bs
import requests
import sys

# 1) buscar tabelas
# 2) fazer script getLinks para buscar links (a com href) escreva para fora o link e o texto associado
# para todos os links com 'category=???' | grep 'category='
# for a in $(getLinks <url> | grep 'category='): do getTables $a; done

def getTables(url,goal):
    conteudo = requests.get(url).text
    doc_tree = bs(conteudo,'lxml')
    tabelas = doc_tree.find_all('table')
    i=0
    for tabela in tabelas:
        i+=1
        if goal and i!=goal: continue
        print('-----------------','TABELA',i,'-----------------')
        linhas = tabela.find_all('tr')
        for linha in linhas:
            linha_txt = ""
            celulas = [x.text for x in linha.find_all('td')]
            linha_txt = "::".join(celulas)
            print(linha_txt)
            
if __name__ == "__main__":
    if len(sys.argv)>1:
        url = sys.argv[1]
        if len(sys.argv)>2: goal = int(sys.argv[2])
        else: goal = 0
        getTables(url,goal)
    else:
        print("Usage: python3 a.py <url>")
        sys.exit()