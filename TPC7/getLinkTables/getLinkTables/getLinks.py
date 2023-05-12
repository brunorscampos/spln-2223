#!/usr/bin/env python3 
from bs4 import BeautifulSoup as bs
import requests

# 1) buscar tabelas
# 2) fazer script getLinks para buscar links (a com href) escreva para fora o link e o texto associado
# para todos os links com 'category=???' | grep 'category='
# for a in $(getLinks <url> | grep 'category='): do getTables $a; done

def getLinks(url):
    conteudo = requests.get(url).text
    doc_tree = bs(conteudo,'lxml')
    links = [x for x in doc_tree.find_all('a') if "href" in x.attrs]
    for a in links:
        print(a['href'])