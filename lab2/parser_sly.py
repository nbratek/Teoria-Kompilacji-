from sly import Parser
from scanner_sly import Scanner

class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = 'parser.out'

    precedence = (
        ('nonassoc', 'IFX'),
    # to fill ...
        #('nonassoc', 'IF'),
        ('nonassoc', 'ELSE'),
        #('right', 'MULASSIGN', 'DIVASSIGN', 'SUBASSIGN', 'ADDASSIGN'),
        ('nonassoc', 'LT', 'GT', 'GEQ', 'LEQ', 'EQ', 'NEQ'),
        ('left', '+', '-'),
        ('left', 'MATADD', 'MATSUB'),
        ('left', '*', '/'),
        ('left', 'MATMUL', 'MATDIV'),
        ('right', 'UMINUS'),
        ('left', "'")
    # to fill ...
    )

    @_('optional_instructions')
    def program(self, p):
        pass

    @_('instructions',
       '')
    def optional_instructions(self, p):
        pass

    @_('instructions instruction',
       'instruction')
    def instructions(self, p):
        pass

    @_('expression "+" expression',
       'expression "-" expression',
       'expression "*" expression',
       'expression "/" expression',
       'expression MATADD expression',
       'expression MATSUB expression',
       'expression MATMUL expression',
       'expression MATDIV expression')
    def expression(self, p):
        pass

    @_('expression LT expression',
       'expression LEQ expression',
       'expression GT expression',
       'expression GEQ expression',
       'expression EQ expression',
       'expression NEQ expression')
    def condition(self, p):
        pass


    @_('"-" expression %prec UMINUS')
    def unary_minus(self, p):
        pass

    @_('expression "\'"')
    def transpose(self, p):
        pass

    @_('"[" vectors "]"')
    def matrix(self, p):
        pass

    @_('vectors "," vector', 'vector')
    def vectors(self, p):
        pass

    @_('"[" elements "]"')
    def vector(self, p):
        pass

    @_('elements "," element', 'element')
    def elements(self, p):
        pass

    @_('ID', 'number')
    def element(self, p):
        pass

    @_('INTNUMBER', 'FLOATNUMBER')
    def number(self, p):
        pass

    @_('ID "[" INTNUMBER "]"')
    def vector_init(self, p):
        pass

    @_('ID "[" INTNUMBER "," INTNUMBER "]"')
    def matrix_init(self, p):
        pass

    @_('EYE "(" INTNUMBER ")"',
       'ONES "(" INTNUMBER ")"',
       'ZEROS "(" INTNUMBER ")"')
    def matrix_function(self, p):
        pass

    @_('IF "(" condition ")" instruction %prec IFX',
       'IF "(" condition ")" instruction ELSE instruction',
       'WHILE "(" condition ")" instruction',
       'FOR ID "=" expression ":" expression instruction',
       '"{" instructions "}"',
       'instruction_end ";"')
    def instruction(self, p):
        pass

    @_('ID assignment_operator expression',
       'matrix_init assignment_operator expression',
       'vector_init assignment_operator expression')
    def assignment(self, p):
        pass

    @_('ID',
       'unary_minus',
       'matrix',
       'transpose',
       'matrix_function',
       'number')
    def expression(self, p):
        pass


    @_('=',
       'ADDASSIGN',
       'SUBASSIGN',
       'MULASSIGN',
       'DIVASSIGN')
    def assignment_operator(self, p):
        pass

    @_('assignment',
       'RETURN expression',
       'BREAK',
       'CONTINUE',
       'PRINT items_to_print')
    def instruction_end(self, p):
        pass



    @_('STRING',
       'expression',
       'expression "," items_to_print',
       'STRING "," items_to_print')
    def items_to_print(self, p):
        pass

    def print_error(p, message):
        p = p.error
        print("Syntax error in {0}, at line {1}: LexToken({2}, '{3}')".format(message, p.lineno, p.type, p.value))
