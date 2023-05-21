#!/usr/bin/env python3 
import os

path = os.getcwd()

def read_code(filename):
    with open(filename, "r") as f:
        return f.read()