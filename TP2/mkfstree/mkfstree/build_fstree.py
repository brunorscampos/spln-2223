import os

def build_fstree(structure, rest, parent_path=''):
    for item in structure:
        if isinstance(item, tuple):
            directory_name, sub_structure = item
            directory_path = os.path.join(parent_path, directory_name)
            os.makedirs(directory_path, exist_ok=True)
            build_fstree(sub_structure, rest, directory_path)
        else:
            file_name = item
            file_path = os.path.join(parent_path, file_name)
            f = open(file_path, 'w')
            content = [x for x in rest if x[0] == file_name]
            if len(content):
                f.write(content[0][1])
            f.close()