#!/usr/bin/env python3 
import sys

def main_mktemplateskel(directory):
    print(directory,"WIP :)")
    pass
    
if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        print("Use: python3 mktemplateskel.py <directory>")
        sys.exit()
    main_mktemplateskel()