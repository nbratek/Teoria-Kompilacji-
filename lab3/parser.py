from sly import Parser
from scanner import Scanner
import AST

class Mparser(Parser):
    tokens = Scanner.tokens

    debugfile = 'parser.out'

    precedence = (
        ('nonassoc', 'IFX'),
        # to fill ...
        # ('nonassoc', 'IF'),
        ('nonassoc', 'ELSE'),
        # ('right', 'MULASSIGN', 'DIVASSIGN', 'SUBASSIGN', 'ADDASSIGN'),
        ('nonassoc', 'LT', 'GT', 'GEQ', 'LEQ', 'EQ', 'NEQ'),
        ('left', '+', '-'),
        ('left', 'MATADD', 'MATSUB'),
        ('left', '*', '/'),
        ('left', 'MATMUL', 'MATDIV'),
        ('right', 'UMINUS'),
        ('left', "'")
        # to fill ...
    )

    def error(self, p):
        if p:
            print(f"Syntax error at line {p.lineno}")

    @_('optional_instructions')
    def program(self, p):
        return p[0]

    @_('instructions',
       '')
    def optional_instructions(self, p):
        return p[0] if p else None


    @_('instructions instruction',
       'instruction')
    def instructions(self, p):
        if len(p) == 1:
            return AST.Instructions([p[0]])
        return AST.Instructions(p[0].instructions + [p[1]])

    @_('expression "+" expression',
       'expression "-" expression',
       'expression "*" expression',
       'expression "/" expression',
       'expression MATADD expression',
       'expression MATSUB expression',
       'expression MATMUL expression',
       'expression MATDIV expression', )
    def expression(self, p):
        return AST.BinaryExpression(p[1], p[0], p[2])

    @_('expression LT expression',
       'expression LEQ expression',
       'expression GT expression',
       'expression GEQ expression',
       'expression EQ expression',
       'expression NEQ expression', )
    def condition(self, p):
        return AST.Conditional(p[1], p[0], p[2])

    @_('"-" expression %prec UMINUS')
    def unary_minus(self, p):
        return AST.UnaryMinus(p[1])

    @_('expression "\'"')
    def transpose(self, p):
        return AST.MatrixTransposition(p[0])

    @_('"[" vectors "]"')
    def matrix(self, p):
        return p[1]

    @_('vectors "," vector',
       'vector')
    def vectors(self, p):
        if len(p) == 1:
            return AST.Matrix([p[0]])
        return AST.Matrix(p[0].matrix + [p[2]])

    @_('"[" elements "]"')
    def vector(self, p):
        return p[1]

    @_('elements "," element',
       'element')
    def elements(self, p):
        if len(p) == 1:
            return AST.Vector([p[0]])
        return AST.Vector(p[0].vector + [p[2]])

    @_('ID',
       'number', )
    def element(self, p):
        return p[0]

    @_('INTNUM',
       'FLOATNUM')
    def number(self, p):
        return AST.Number(p[0])

    @_('ID "[" INTNUM "," INTNUM "]"')
    def matrix_init(self, p):
        return AST.MatrixInitialization(p[0], p[2], p[4])

    @_('ID "[" INTNUM "]"')
    def vector_init(self, p):
        return AST.VectorInitialization(p[0], p[2])

    @_('EYE "(" INTNUM ")"',
       'ONES "(" INTNUM ")"',
       'ZEROS "(" INTNUM ")"')
    def matrix_function(self, p):
        return AST.MatrixFunctionCall(p[0], p[2])

    @_('variable assignment_operator expression',
       'matrix_init assignment_operator expression',
       'vector_init assignment_operator expression')
    def assignment(self, p):
        return AST.Assignment(p[1], p[0], p[2])

    @_('ID')
    def variable(self, p):
        return AST.Variable(p[0])

    @_('IF "(" condition ")" instruction %prec IFX')
    def instruction(self, p):
        return AST.IfStatement(p[2], p[4])

    @_('IF "(" condition ")" instruction ELSE instruction')
    def instruction(self, p):
        return AST.IfElseStatement(p[2], p[4], p[6])

    @_('WHILE "(" condition ")" instruction')
    def instruction(self, p):
        return AST.WhileLoop(p[2], p[4])

    @_('FOR variable "=" range instruction')
    def instruction(self, p):
        return AST.ForLoop(p[1], p[3], p[4])

    @_('expression ":" expression')
    def range(self, p):
        return AST.LoopRange(p[0], p[2])

    @_('"{" instructions "}"',
       'instruction_end ";"')
    def instruction(self, p):
        if len(p) == 2:
            return p[0]
        return p[1]

    @_('BREAK')
    def instruction_end(self, p):
        return AST.BreakStatement()

    @_('CONTINUE')
    def instruction_end(self, p):
        return AST.ContinueStatement()

    @_('RETURN expression')
    def instruction_end(self, p):
        return AST.ReturnStatement(p[1])

    @_('PRINT items_to_print')
    def instruction_end(self, p):
        return AST.PrintStatement(p[1])

    @_('assignment')
    def instruction_end(self, p):
        return p[0]

    @_('=',
       'ADDASSIGN',
       'SUBASSIGN',
       'MULASSIGN',
       'DIVASSIGN')
    def assignment_operator(self, p):
        return p[0]

    @_('STRING',
       'expression',
       'expression "," items_to_print',
       'STRING "," items_to_print')
    def items_to_print(self, p):
        if len(p) == 1:
            return AST.PrintItems([p[0]])
        return AST.PrintItems([p[0], p[2]])

    @_('variable',
       'unary_minus',
       'matrix',
       'transpose',
       'matrix_function',
       'number')
    def expression(self, p):
        return p[0]
