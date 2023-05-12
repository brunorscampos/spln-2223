# -*- coding: utf-8 -*-
#!/usr/bin/env python3 
"""Module to get links and tables from URLs."""

# 1) buscar tabelas
# 2) fazer script getLinks para buscar links (a com href) escreva para fora o link e o texto associado
# para todos os links com 'category=???' | grep 'category='
# for a in $(getLinks <url> | grep 'category='): do getTables $a; done

__version__ = "0.1"

import argparse
from get_links import get_links
from get_tables import get_tables

def get_arguments_links(__version__):
    parser = argparse.ArgumentParser(
        prog='getLinks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=f'''
    --------------------------------------------------------------------
                      GetLinks v{__version__}
    --------------------------------------------------------------------'''
    )
    parser.add_argument('url')
    parser.add_argument('--version','-V', action='version', version='%(prog)s '+__version__)
    return parser.parse_args()

def get_arguments_tables(__version__):
    parser = argparse.ArgumentParser(
        prog='getTables',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=f'''
    --------------------------------------------------------------------
                      GetTables v{__version__}
    --------------------------------------------------------------------'''
    )
    parser.add_argument('url')
    parser.add_argument('--goal','-g')
    parser.add_argument('--version','-V', action='version', version='%(prog)s '+__version__)
    return parser.parse_args()

def getLinks():
    args = get_arguments_links(__version__)
    url = args.url
    get_links(url)

def getTables():
    args = get_arguments_tables(__version__)
    url = args.url
    goal = 0
    if args.goal:
        goal = int(args.goal)
    get_tables(url,goal)