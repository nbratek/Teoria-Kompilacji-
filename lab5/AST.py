from typing import Any, List, Optional


class Node(object):
    type: Optional[Any] = None
    size: Optional[Any] = None

    def accept(self, visitor):
        return visitor.visit(self)

    def generic_visit(self, visitor):
        raise Exception('No visit_{} method'.format(self.__class__.__name__))


class BinaryExpression(Node):
    def __init__(self, operator, left, right, line=0):
        self.operator = operator
        self.left = left
        self.right = right
        self.line = line


class Condition(Node):
    def __init__(self, operator, left, right, line=0):
        self.operator = operator
        self.left = left
        self.right = right
        self.line = line


class Uminus(Node):
    def __init__(self, right, line=0):
        self.right = right
        self.line = line


class Assignment(Node):
    def __init__(self, operator, var, expression, line=0):
        self.operator = operator
        self.var = var
        self.expression = expression
        self.line = line


class Variable(Node):
    def __init__(self, id, index=0, line=0):
        self.id = id
        self.index = index
        self.line = line


class Var(Node):
    def __init__(self, name, line=0):
        self.name = name
        self.line = line

class IntNum(Node):
    def __init__(self, intnum, line=0):
        self.intnum = intnum
        self.line = line


class Float(Node):
    def __init__(self, floatnum, line=0):
        self.floatnum = floatnum
        self.line = line


class String(Node):
    def __init__(self, string, line=0):
        self.string = string
        self.line = line


class If(Node):
    def __init__(self, cond, instr, line=0):
        self.cond = cond
        self.instr = instr
        self.line = line


class Ifelse(Node):
    def __init__(self, cond, instr, instr_else, line=0):
        self.cond = cond
        self.instr = instr
        self.instr_else = instr_else
        self.line = line


class While(Node):
    def __init__(self, cond, instr, line=0):
        self.cond = cond
        self.instr = instr
        self.line = line


class For(Node):
    def __init__(self, var, range, instr, line=0):
        self.var = var
        self.range = range
        self.instr = instr
        self.line = line


class Range(Node):
    def __init__(self, left, right, line=0):
        self.left = left
        self.right = right
        self.line = line


class Break(Node):
    def __init__(self, line=0):
        self.line = line


class Continue(Node):
    def __init__(self, line=0):
        self.line = line


class Return(Node):
    def __init__(self, expression, line=0):
        self.expression = expression
        self.line = line


class Print(Node):
    def __init__(self, to_print, line=0):
        self.to_print = to_print
        self.line = line

class InstructionsOrEmpty(Node):
    def __init__(self, instructions=None, lineno=None):
        super().__init__(instructions=instructions, lineno=lineno)

class Id(Node):
    def __init__(self, name, line=0):
        self.name = name
        self.line = line


class Instructions(Node):
    def __init__(self, instructions: List[Any], line=0):
        self.instructions = instructions
        self.line = line


class Transposition(Node):
    def __init__(self, matrix, line=0):
        self.matrix = matrix
        self.line = line


class Matrix(Node):
    def __init__(self, matrix: List[Any], line=0):
        self.matrix = matrix
        self.line = line


class Vector(Node):
    def __init__(self, vector: List[Any], line=0):
        self.vector = vector
        self.line = line


class Number(Node):
    def __init__(self, value, line=0):
        self.value = value
        self.line = line


class VectorRef(Node):
    def __init__(self, id, index, line=0):
        self.id = id
        self.index = index
        self.line = line


class MatrixRef(Node):
    def __init__(self, id, row_index, col_index, line=0):
        self.id = id
        self.row_index = row_index
        self.col_index = col_index
        self.line = line


class MatrixFunction(Node):
    def __init__(self, name, args: List[Any], line=0):
        self.name = name
        self.args = args
        self.line = line


class ToPrint(Node):
    def __init__(self, values: List[Any], line=0):
        self.values = values
        self.line = line


class Error(Node):
    def __init__(self, line=0):
        self.line = line
