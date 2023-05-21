#!/usr/bin/env python3 
from .interpreter import MyInterpreter
from .myparser import myparser
from .utils import read_code
import sys

def main_mkfstree(filename):
    
    input_code = read_code(filename)
    parse_tree = myparser.parse(input_code)
    data = MyInterpreter().visit(parse_tree)
    
    print("====================================================================================")
    for k in data:
        print(k,data[k])
    print("====================================================================================")
    
if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        print("Use: python3 main.py <filename>")
        sys.exit()
    main_mkfstree(filename)