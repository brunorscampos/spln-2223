# -*- coding: utf-8 -*-
#!/usr/bin/env python3 
"""Module template multi-file."""

__version__ = "0.1"

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
    parser.add_argument('directory')
    parser.add_argument('--version','-V', action='version', version='%(prog)s '+__version__)
    return parser.parse_args()

def mkfstree():
    args = get_arguments_mkfstree(__version__)
    filename = args.filename
    main_mkfstree(filename)

def mktemplateskel():
    args = get_arguments_mktemplateskel(__version__)
    directory = args.directory
    main_mktemplateskel(directory)