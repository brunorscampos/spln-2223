#!/usr/bin/env python3 
from .directory_structure import directory_structure, build_template

def main_mktemplateskel(args):
    directory = args.directory
    name = args.name
    author = args.author
    content = args.content
    output = args.output
    structure, rest = directory_structure(directory,content)
    build_template(name, author, structure, rest, output)