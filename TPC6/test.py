#!/usr/bin/env python3 

from gensim.models import Word2Vec
from gensim.utils import tokenize
from glob import glob
import argparse

parser = argparse.ArgumentParser(
    prog='Cria Modelo',
    epilog='MAde for SPLN22/23'
)

parser.add_argument('model')
parser.add_argument('--analogias','-a')
parser.add_argument('--similar','-s')
args = parser.parse_args()
model = args.model
analogias = args.analogias if args.analogias else "./val.txt"
similar = args.similar if args.analogias else "./similar.txt"

model = Word2Vec.load(model)

if args.analogias:
    f = open(analogias,'r')
else:
    f = open(similar,'r')

for line in f:
    words = line.split()
    if len(words) == 3:
        w1,w2,w3 = words
        if args.analogias:
            res = model.wv.most_similar(positive=[w1,w3],negative=[w2])
            print(res)
        elif args.similar:
            s1 = model.wv.similarity(w1,w2)
            s2 = model.wv.similarity(w1,w3)
            print("Sim",w1, ":",w2, "=",s1,"<" if s1<s2 else ">" if s1>s2 else "=","Sim",w1, ":",w3, "=",s2)