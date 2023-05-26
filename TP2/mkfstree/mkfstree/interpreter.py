#!/usr/bin/env python3 
from lark import Token,Tree,Discard
from lark.visitors import Interpreter

class MyInterpreter(Interpreter):
    def start(self,start):
        # start: meta tree
        self.dic = {}
        self.dic["vars"] = {}
        self.dic["structure"] = []
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
            self.dic["vars"][nome] = value
    
    def name(self,name):
        # name: "name:" ID
        nome = "name"
        value = name.children[0].value
        return nome, value
    
    def author(self,author):
        # author: "author:" ID
        nome = "author"
        value = author.children[0].value
        return nome, value
    
    def var(self,var):
        # var: ID ":" ID
        nome = var.children[0].value
        value = var.children[1].value
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
        # file: identificador "." identificador
        name = self.visit(file.children[0])
        extension = self.visit(file.children[1])
        return name + "." + extension
    
    def directory(self,directory):
        # directory: identificador "/" ( "-" element)*
        name = self.visit(directory.children[0])
        elements = []
        for element in directory.children[1:]:
            elements.append(self.visit(element))
        return name, elements
        
    def identificador(self,identificador):
        # !identificador: "{{" ID "}}" | ID
        if len(identificador.children)>1:
            return self.dic["vars"][identificador.children[1].value]
        else: 
            return identificador.children[0].value