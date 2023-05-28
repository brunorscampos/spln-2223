# -*- coding: utf-8 -*-
#!/usr/bin/env python3 
"""Module template multi-file."""

__version__ = "0.5"

import argparse
from .mkfstree import main_mkfstree
from .mktemplateskel import main_mktemplateskel

def get_arguments_mkfstree(__version__):
    parser = argparse.ArgumentParser(
        prog='mkfstree',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=f'''
    --------------------------------------------------------------------
                      mkfstree v{__version__}
    --------------------------------------------------------------------'''
    )
    parser.add_argument('filename')
    parser.add_argument('--version','-V', action='version', version='%(prog)s '+__version__)
    return parser.parse_args()

def get_arguments_mktemplateskel(__version__):
    parser = argparse.ArgumentParser(
        prog='mktemplateskel',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=f'''
    --------------------------------------------------------------------
                      mktemplateskel v{__version__}
    --------------------------------------------------------------------'''
    )
    parser.add_argument('directory', help="Root directory")
    parser.add_argument("-n", "--name", help="Project name")
    parser.add_argument("-a", "--author", help="Project author")
    parser.add_argument('-c', '--content', action='store_true', help='Specify if file contents should be included')
    parser.add_argument('-V', '--version', action='version', version='%(prog)s '+__version__)
    parser.add_argument('-o', '--output')
    return parser.parse_args()

def mkfstree():
    args = get_arguments_mkfstree(__version__)
    filename = args.filename
    main_mkfstree(filename)

def mktemplateskel():
    args = get_arguments_mktemplateskel(__version__)
    print(args)
    main_mktemplateskel(args)