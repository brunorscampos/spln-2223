#!/usr/bin/env python3 
from lark import Lark

grammar = r'''
start: meta tree rest*

meta: "===" "meta" config
config: name author var*
name: "name:" ID
author: "author:" ID
var: ID ":" ID

tree: "===" "tree" structure
structure: element*
element: file
       | directory
file: identificador "." identificador
directory: identificador "/" ( "-" element)*

rest: "===" file content
content: line+
line: TEXT NEWLINE 
TEXT: /[^=\r\n][^\r\n]+/
NEWLINE: /[\r]?[\n]/

!identificador: "{{" ID "}}"
              | ID

COMMENT: "//" /.*/
ID: /[a-zA-Z0-9_-]+/

%import common.WS
%ignore WS
%ignore COMMENT
'''

myparser = Lark(grammar)
