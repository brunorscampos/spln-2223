#!/usr/bin/env python3 

from gensim.models import Word2Vec
from gensim.utils import tokenize
from glob import glob
import argparse

parser = argparse.ArgumentParser(
    prog='Cria Modelo',
    epilog='MAde for SPLN22/23'
)

parser.add_argument('dir')
parser.add_argument('--epochs','-e',default=10)
parser.add_argument('--vector_size','-v',default=300)
parser.add_argument('--out','-o',default='.')
args = parser.parse_args()
dir = args.dir
epochs = int(args.epochs)
vector_size = int(args.vector_size)
out = args.out

files = glob(f'{dir}/*.txt')

sentences = []
for file in files:
    f = open(file,"r")
    for line in f:
        sentences.append(list(tokenize(line,lowercase=True)))
    f.close()

model = Word2Vec(sentences,epochs=epochs,vector_size=vector_size)
model.save(out + '.vec')