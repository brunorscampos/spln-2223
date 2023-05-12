### SPLN - TPC7
##### Bruno Campos, PG50275

Este trabalho consiste projeto flit para recolher links e tabelas de URLs.

Instalation: 
    flit build
    flit install -s
Usage:
    getLinks <url>
    getTables <url> --goal
    'for a in $(getLinks <url> | grep 'category='): do getTables $a; done'