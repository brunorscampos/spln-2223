#!/usr/bin/env python3 
from .interpreter import MyInterpreter
from .myparser import myparser
from .build_fstree import build_fstree
from .utils import read_code, process_rest
import sys

def main_mkfstree(filename):
    input_code = read_code(filename)
    split_text = input_code.split('===')
    tree = ''.join(['===' + x for x in split_text[1:3]])
    parse_tree = myparser.parse(tree)
    data = MyInterpreter().visit(parse_tree)
    
    contents = ['===' + x for x in split_text[3:]]
    rest = process_rest(contents,data["vars"])
    
    print("======================================   TREE   ==============================================")
    for k in data:
        print(k,data[k])
    
    build_fstree(data["structure"], rest)
    
if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        print("Use: python3 mkfstree.py <filename>")
        sys.exit()
    main_mkfstree(filename)