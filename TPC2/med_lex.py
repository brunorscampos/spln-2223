"""
DIC : ES

ES -> ES LINHA_B E
    | E

E : ITEMS

ITEMS -> ITEMS '\n' ITEM
       | ITEM

ITEM -> AT_CONC
      | LING

AT_CONC : ID ':' VAL

LING : ID_LING ':' '\n' TS

TS -> TS '\n' T
    | T

T : '-' VAL AT_TS

AT_TS -> AT_TS AT_T
       |

AT_T : '\n' '+' ID ':' VAL
"""
import ply.lex as lex

literals = "+\n:-"
tokens = ['ID','ID_LING','VAL','LINHA_B','WS']

def t_ID(t): 
    r'\w+(?=\ *:)'
    if t.value in ['en','es','pt','la']:
        t.type = 'ID_LING'
    print()
    return t

def t_VAL(t): 
    r'\w[^\n+:-]+'
    return t

def t_LINHA_B(t): 
    r'\n{2}'
    return t

def t_WS(t):
    r'\ '
    pass

def t_error(t):
    print(f"Illegal character {t.value[0]} at line {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()
with open('teste.txt','r') as f:
    conteudo = f.read()
    lexer.input(conteudo)

for tok in lexer:
    print(tok)