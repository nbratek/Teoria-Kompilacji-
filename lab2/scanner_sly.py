import sys
from sly import Lexer


class Scanner(Lexer):
    tokens = {"MATADD", "MATSUB", "MATDIV", "MATMUL", "ADDASSIGN", "SUBASSIGN",
              "MULASSIGN", "DIVASSIGN", "ID", "LEQ", "GEQ", "EQ", "NEQ", "LT", "GT",
              "STRING", "INTNUMBER", "FLOATNUMBER",
              'IF', "ELSE", "FOR", "WHILE", "BREAK", "CONTINUE", "RETURN", "PRINT", "EYE", "ZEROS", "ONES"
              }

    literals = {'+', '-', '*', '/', '=', '(', ')', '[', ']', '{', '}', ':', "'", ',', ';'}

    ignore = '  \t'
    ignore_comment = r'\#.*'
    #ignore_newline = r'\n+'

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    MATADD = r'\.\+'
    MATSUB = r'\.-'
    MATDIV = r'\.\*'
    MATMUL = r'\./'
    ADDASSIGN = r'\+='
    SUBASSIGN = r'-='
    MULASSIGN = r'\*='
    DIVASSIGN = r'/='
    #ASSIGN = r'='
    LT = r'<'
    GT = r'>'
    LEQ = r'<='
    GEQ = r'>='
    EQ = r'=='
    NEQ = r'!='
    STRING = r'\".*?\"'
    FLOATNUMBER = r'(\d+\.\d*|\.\d+)([eE][-]?\d+)?'
    INTNUMBER = r'\d+'


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

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f"({t.lineno}): Illegal character '{t.value[0]}'")
        self.index += 1


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()

    for tok in lexer.tokenize(text):
        print(tok)