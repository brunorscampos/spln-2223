import ply.yacc as yacc
from med_lex import tokens

start = 'dic'

def p_1(p): 
    r'dic : es'
    p[0] = p[1]
    print(p[0])

def p_2(p): 
    r'es : es LINHA_B e'
    p[0] = p[1] + "\n\n" + p[3]

def p_3(p):
    r'es : e'
    p[0] = p[1]
    
def p_4(p): 
    r'e : INDICE "\n" items'
    p[0] = p[1] + "\n" + p[3]

def p_5(p):
    r'items : items "\n" item'
    p[0] = p[1] + "\n" + p[3]

def p_6(p): 
    r'items : item'
    p[0] = p[1]

def p_7(p): 
    r'item : at_conc'
    p[0] = p[1]

def p_8(p): 
    r'item : ling'
    p[0] = p[1]

def p_9(p): 
    r'at_conc : ID ":" VAL ";"'
    p[0] = p[1] + ":" + p[3] + ";"

def p_10(p):
    r'ling : ID_LING ":" VAL at_ts ";"'
    p[0] = p[1] + ":" + p[3] + p[4] + ";"

def p_11(p): 
    r'at_ts : at_ts at_t'
    p[0] = p[1] + p[2]

def p_12(p): 
    r'at_ts :'
    p[0] = f""

def p_13(p): 
    r'at_t : "\n" "+" ID ":" VAL'
    p[0] = f"\n+ {p[3]} : {p[5]}"

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}', [{p.lexpos}]")

parser=yacc.yacc(debug=True)
with open("teste.txt","r") as f:
    conteudo = f.read()
    parser.parse(conteudo)
