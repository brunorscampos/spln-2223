import ply.yacc as yacc

def p_1(p): "DIC : ES"; pass

def p_2(p): "ES : ES LINHA_B E"; pass

def p_3(p): "ES : E"; pass

def p_4(p): "E : ITEMS"; pass

def p_5(p): "ITEMS : ITEMS '\n' ITEM"; pass

def p_6(p): "ITEMS: ITEM"; pass

def p_7(p): "ITEM : AT_CONC"; pass

def p_8(p): "ITEM : LING"; pass

def p_9(p): "AT_CONC : ID ':' VAL"; pass

def p_10(p): "LING : ID_LING ':' '\n' TS"; pass

def p_11(p): "TS : TS '\n' T"; pass

def p_12(p): "TS : T"; pass

def p_13(p): "T : '-' VAL AT_TS"; pass

def p_14(p): "AT_TS : AT_TS AT_T"; pass

def p_15(p): "AT_TS : "; pass

def p_16(p): "AT_T : '\n' '+' ID ':' VAL"; pass

