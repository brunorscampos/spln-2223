### SPLN - TP2 - Template multi-file
##### Bruno Campos, PG50275

Package criado como projeto prático. 
Permite a criação de diretorias estruturadas a partir de um template, automatizando a criação de diretorias e ficheiros (bem como o conteúdo de ficheiros se desejado).
Adicionalmente, é fornecida uma ferramenta complementar que cria um template a partir da diretoria desejada.  

## Usage: 

######  mkfstree [-h] [-n NAME] [-a AUTHOR] [--version] template_file

    positional arguments:
        template_file

    optional arguments:
        -h, --help            show this help message and exit
        -n NAME, --name NAME  Project name
        -a AUTHOR, --author AUTHOR
                                Project author
        --version, -V         show program's version number and exit


######  mktemplateskel [-h] [-n NAME] [-a AUTHOR] [-c] [-V] [-o OUTPUT] directory

    positional arguments:
        directory             Root directory

    optional arguments:
        -h, --help            show this help message and exit
        -n NAME, --name NAME  Project name
        -a AUTHOR, --author AUTHOR
                                Project author
        -c, --content         Specify if file contents should be included
        -V, --version         show program's version number and exit
        -o OUTPUT, --output OUTPUT

## Template Example:

    === meta                        // declaration of name and author are mandatory (but can be left empty)
    name: teste
    author: JJoao
    // ... declare desired variables here

    === tree                        // desired structure of the directory tree

    pyproject.toml;
    {{name}}/                       // replaced with variable value 
    - __init__.py;
    - {{name}}.md;
    - {{name}};                   // '-' to declare files or directories inside a directory
    exemplo/
    - aninhado/
        - adeus.txt;
    README.md;
    tests/                          // directories end with '/'
    - test-1.py;                  // files end in ';'

    === pyproject.toml              // declare file contents (not mandatory)
    [build-system]
    requires = ["flit_core >=3.2,<4"]
    build-backend = "flit_core.buildapi"

    [project]
    name = "{{name}}"
    authors = [ {name = "{{author}}", email = "FIXME"}]
    license = {file = "LICENSE"}
    dynamic = ["version", "description"]
    dependencies = [ ]
    readme = "{{name}}.md"

    [project.scripts]
    ## script1 = "{{name}}:main"

    === {{name}}.md

    # NAME

    {{name}} - FIXME the fantastic module for...

    === __init__.py
    """ FIXME: docstring """
    __version__ = "0.1.0"

    === test-1.py
    import pytest
    import {{name}} 

    def test_1():
        assert "FIXME" == "FIXME"