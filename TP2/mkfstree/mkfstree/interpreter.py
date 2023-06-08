#!/usr/bin/env python3 
from lark import Tree
from lark.visitors import Interpreter

class MyInterpreter(Interpreter):
    def __init__(self,name,author) -> None:
        super().__init__()
        self.dic = {}
        self.dic["vars"] = {}
        self.dic["structure"] = []
        if name: 
            self.dic["vars"]["name"] = name
        if author: 
            self.dic["vars"]["author"] = author
        
    def start(self,start):
        # start: meta tree
        for random in start.children:
            self.visit(random)
        return self.dic

    def meta(self,meta):
        # meta: "===" "meta" config
        return self.visit(meta.children[0])

    def config(self,config):
        # config: name author var*
        for var in config.children:
            nome, value = self.visit(var)
            if nome not in self.dic["vars"]: 
                self.dic["vars"][nome] = value
    
    def name(self,name):
        # name: "name:" ID?
        nome = "name"
        if len(name.children):
            value = name.children[0].value
        else: value = ""
        return nome, value
    
    def author(self,author):
        # author: "author:" ID?
        nome = "author"
        if len(author.children):
            value = author.children[0].value
        else: value = ""
        return nome, value
    
    def var(self,var):
        # var: ID ":" ID?
        nome = var.children[0].value
        if len(var.children):
            value = var.children[1].value
        else: value = ""
        return nome, value
    
    def tree(self,tree):
        # tree: "===" "tree" structure
        return self.visit(tree.children[0])
    
    def structure(self,structure):
        # structure: element*
        elements = []
        for element in structure.children:
            elements.append(self.visit(element))
        self.dic["structure"] = elements
    
    def element(self,element):
        # element: file | directory
        return self.visit(element.children[0])
    
    def file(self,file):
        # file: identificador ("." identificador)? ";"
        res = ""
        res += self.visit(file.children[0])
        if len(file.children)>1:
            res += "." + self.visit(file.children[1])
        return res
    
    def directory(self,directory):
        # directory: identificador "/" ("-" element)*
        name = self.visit(directory.children[0])
        elements = []
        for element in directory.children[1:]:
            if type(element) == Tree:
                elements.append(self.visit(element))
        return name, elements
        
    def identificador(self,identificador):
        # !identificador: "{{" ID "}}" | ID
        if len(identificador.children)>1:
            return self.dic["vars"][identificador.children[1].value]
        else: 
            return identificador.children[0].value