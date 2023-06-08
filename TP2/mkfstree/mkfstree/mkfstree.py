#!/usr/bin/env python3 
from .interpreter import MyInterpreter
from .myparser import myparser
from .build_fstree import build_fstree
from .utils import read_code, process_rest

def main_mkfstree(args):
    template_file = args.template_file
    name = args.name
    author = args.author
    input_code = read_code(template_file)
    split_text = input_code.split('===')
    tree = ''.join(['===' + x for x in split_text[1:3]])
    parse_tree = myparser.parse(tree)
    data = MyInterpreter(name,author).visit(parse_tree)
    
    contents = ['===' + x for x in split_text[3:]]
    rest = process_rest(contents,data["vars"])
    
    build_fstree(data["structure"], rest)