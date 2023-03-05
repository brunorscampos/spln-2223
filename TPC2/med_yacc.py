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
import ply.yacc as yacc
from med_lex import tokens

def p_1(p): "DIC : ES"; p[0] = p[1]; print("GAMER\n",p[0])

def p_2(p): "ES : ES LINHA_B E"; p[0] = p[1] + "\n\n" + p[3]; print(p[0])

def p_3(p): "ES : E"; p[0] = p[1]; print(p[0])

def p_4(p): "E : ITEMS"; p[0] = p[1]; print(p[0])

def p_5(p): "ITEMS : ITEMS '\n' ITEM"; p[0] = p[1] + "\n" + p[3]; print(p[0])

def p_6(p): "ITEMS: ITEM"; p[0] = p[1]; print(p[0])

def p_7(p): "ITEM : AT_CONC"; p[0] = p[1]; print(p[0])

def p_8(p): "ITEM : LING"; p[0] = p[1]; print(p[0])

def p_9(p): "AT_CONC : ID ':' VAL"; p[0] = p[1] + ":" + p[3]; print(p[0])

def p_10(p): "LING : ID_LING ':' '\n' TS"; p[0] = p[1] + ":\n" + p[4]; print(p[0])

def p_11(p): "TS : TS '\n' T"; p[0] = p[1] + "\n" + p[3]; print(p[0])

def p_12(p): "TS : T"; p[0] = p[1]; print(p[0])

def p_13(p): "T : '-' VAL AT_TS"; p[0] = "-" + p[2] + p[3]; print(p[0])

def p_14(p): "AT_TS : AT_TS AT_T"; p[0] = p[1] + p[2]; print(p[0])

def p_15(p): "AT_TS : "; p[0] = f""; print(p[0])

def p_16(p): "AT_T : '\n' '+' ID ':' VAL"; p[0] = f"\n+ {p[3]} : {p[5]}"; print(p[0])

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}', [{p.lexer.lineno}]")

parser=yacc.yacc()
with open('teste.txt','r') as f:
    conteudo = f.read()
    parser.parse(conteudo)
