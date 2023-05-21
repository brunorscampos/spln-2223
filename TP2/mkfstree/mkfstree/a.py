#!/usr/bin/env python3 
import os

def print_directory_structure(root_dir):
    for dir_name, sub_dirs, file_names in os.walk(root_dir):
        level = dir_name.replace(root_dir, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f"{indent}{os.path.basename(dir_name)}/")
        sub_indent = ' ' * 4 * (level + 1)
        for file_name in file_names:
            print(f"{sub_indent}{file_name}")

# Example usage
directory_path = '../TPC7'
print_directory_structure(directory_path)