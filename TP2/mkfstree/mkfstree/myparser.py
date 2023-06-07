#!/usr/bin/env python3 
from lark import Lark

grammar = r'''
start: meta tree

meta: "===" "meta" config
config: name author var*
name: "name" ":" ID?
author: "author" ":" ID?
var: ID ":" ID?

tree: "===" "tree" structure
structure: element*
element: file
       | directory
file: identificador ("." identificador)? ";"
directory: identificador "/" ("-" element)*

!identificador: "{{" ID "}}"
              | ID

COMMENT: "//" /.*/
ID: /[a-zA-Z0-9_-]+/

%import common.WS
%ignore WS
%ignore COMMENT
'''

myparser = Lark(grammar)
