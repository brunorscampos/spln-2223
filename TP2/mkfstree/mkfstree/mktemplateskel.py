#!/usr/bin/env python3 
from .directory_structure import directory_structure, build_template
import sys

def main_mktemplateskel(args):
    directory = args.directory
    name = args.name
    author = args.author
    content = args.content
    output = args.output
    structure, rest = directory_structure(directory,content)
    build_template(name, author, structure, rest, output)
    
if __name__ == "__main__":
    if len(sys.argv) == 2:
        directory = sys.argv[1]
    else:
        print("Use: python3 mktemplateskel.py <directory>")
        sys.exit()
    main_mktemplateskel(directory)