import sys
from sly import Lexer


class Scanner(Lexer):
    tokens = {"MATADD", "MATSUB", "MATDIV", "MATMUL", "ADDASSIGN", "SUBASSIGN",
              "MULASSIGN", "DIVASSIGN", "ID", "LEQ", "GEQ", "EQ", "NEQ", "LT", "GT",
              "STRING", "INTNUM", "FLOATNUM",
              'IF', "ELSE", "FOR", "WHILE", "BREAK", "CONTINUE", "RETURN", "PRINT", "EYE", "ZEROS", "ONES"
              }

    literals = {'+', '-', '*', '/', '=', '(', ')', '[', ']', '{', '}', ':', "'", ',', ';'}

    ignore = ' \t'

    ignore_comment = r'\#.*'

    ADDASSIGN = r'\+='
    SUBASSIGN = r'-='
    MULASSIGN = r'\*='
    DIVASSIGN = r'/='
    MATADD = r'\.\+'
    MATSUB = r'\.-'
    MATMUL = r'\.\*'
    MATDIV = r'\./'
    LEQ = r'<='
    LT = r'<'
    GEQ = r'>='
    GT = r'>'
    NEQ = r'!='
    EQ = r'=='
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['for'] = FOR
    ID['while'] = WHILE
    ID['break'] = BREAK
    ID['continue'] = CONTINUE
    ID['return'] = RETURN
    ID['print'] = PRINT
    ID['eye'] = EYE
    ID['zeros'] = ZEROS
    ID['ones'] = ONES
    FLOATNUM = r'(\d+\.\d*|\.\d+)([eE][-]?\d+)?'
    INTNUM = r'\d+'
    STRING = r'\".*?\"'


    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print(f"({t.lineno}): Illegal character '{t.value[0]}'")
        self.index += 1