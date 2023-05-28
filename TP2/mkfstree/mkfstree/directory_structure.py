#!/usr/bin/env python3 
import os
import sys

def get_entry(result, level):
    if level < 0: return result
    else: return get_entry(result[-1][1], level - 1)

def directory_structure(root_dir,content):
    result = []
    rest = []
    first = True
    for dir_name, _, file_names in os.walk(root_dir):
        level = dir_name.replace(root_dir, '').count(os.sep)
        current_dir = os.path.basename(dir_name)
        if level == 0: entry = result
        else: entry = get_entry(result, level - 1)
        if first: 
            result += file_names
            first = False
        else: entry.append((current_dir, file_names))
        if content:
            for file_name in file_names:
                file_path = os.path.join(dir_name, file_name)
                with open(file_path, 'r') as file:
                    file_content = file.read()
                    rest.append((file_name, file_content))
    return result, rest
    
def build_tree(structure, indent=0):
    for item in structure:
        if isinstance(item, str):
            print('\t' * indent + ("- " if indent else "") + item)
        else:
            directory, files = item
            print('\t' * indent + ("- " if indent else "") + directory + '/')
            build_tree(files, indent+1)

def build_template(name, author, structure, rest, output):
    if output:
        sys.stdout = open(output, 'w')
    print("=== meta")
    print("name:",name if name else "")    
    print("author:", author if author else "")
    print()
    print("=== tree")
    print()
    
    build_tree(structure,0)
    print()
    
    for file, content in rest:
        if content:
            print("===",file)
            print(content)
            print()
    sys.stdout = sys.__stdout__