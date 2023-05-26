#!/usr/bin/env python3 
import os
import re

path = os.getcwd()

def read_code(filename):
    with open(filename, "r") as f:
        return f.read()
    
def process_rest(contents, vars):
    rest = []
    for var in vars:
        contents = [x.replace("{{" + var + "}}",vars[var]) for x in contents]
    for content in contents:
        pattern = r'===\s*([\w\{\}\-]+\.\w+)\n*((.|\n)+)'
        match = re.match(pattern, content)
        if match:
            rest.append((match.group(1), match.group(2).strip()))
        else:
            print("ERROR 42:",content)
    return rest