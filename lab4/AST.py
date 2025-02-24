from typing import Any, Optional

class Node(object):
    def print_indent(self, indent: int):
        print(indent * "|\t", end="")

class InstrOrEmpty(Node):
    def __init__(self, instructions: Optional[Any] = None, lineno: Optional[Any] = 0):
        self.instructions = instructions
        self.lineno = lineno

class Instructions(Node):
    def __init__(self, instructions: Optional[Any] = None, lineno: Optional[Any] = 0):
        self.instructions = instructions
        self.lineno = lineno

class If(Node):
    def __init__(self, cond: Any, if_body: Any, else_body: Optional[Any] = None):
        self.cond = cond
        self.if_body = if_body
        self.else_body = else_body

class Return(Node):
    def __init__(self, expr: Optional[Any] = None, lineno: Optional[Any] = 0):
        self.expr = expr
        self.lineno = lineno

class Break(Node):
    def __init__(self, lineno: Optional[Any] = 0):
        self.lineno = lineno

class Continue(Node):
    def __init__(self, lineno: Optional[Any] = 0):
        self.lineno = lineno

class For(Node):
    def __init__(self, id: Any, cond_start: Any, cond_end: Any, body: Any, lineno: Optional[Any] = 0):
        self.id = id
        self.cond_start = cond_start
        self.cond_end = cond_end
        self.body = body
        self.lineno = lineno

class While(Node):
    def __init__(self, cond: Any, body: Any, lineno: Optional[Any] = 0):
        self.cond = cond
        self.body = body
        self.lineno = lineno

class AssignOp(Node):
    def __init__(self, left: Any, op: Any, right: Any, lineno: Optional[Any] = 0):
        self.left = left
        self.op = op
        self.right = right
        self.lineno = lineno

class Print(Node):
    def __init__(self, printargs: Any, lineno: Optional[Any] = 0):
        self.printargs = printargs
        self.lineno = lineno

class String(Node):
    def __init__(self, string: str, lineno: Optional[Any] = 0):
        self.string = string
        self.lineno = lineno

class IntNum(Node):
    def __init__(self, intnum: int, lineno: Optional[Any] = 0):
        self.intnum = intnum
        self.lineno = lineno

class FloatNum(Node):
    def __init__(self, floatnum: float, lineno: Optional[Any] = 0):
        self.floatnum = floatnum
        self.lineno = lineno

class Variable(Node):
    def __init__(self, id: Any, index: Optional[Any] = None, lineno: Optional[Any] = 0):
        self.id = id
        self.index = index
        self.lineno = lineno

class Id(Node):
    def __init__(self, id: Any, lineno: Optional[Any] = 0):
        self.id = id
        self.lineno = lineno

class BinExpr(Node):
    def __init__(self, left: Any, op: Any, right: Any, lineno: Optional[Any] = 0, dims: Optional[Any] = None, type: Optional[Any] = None):
        self.left = left
        self.op = op
        self.right = right
        self.lineno = lineno
        self.dims = dims
        self.type = type

class Uminus(Node):
    def __init__(self, val: Any, lineno: Optional[Any] = 0):
        self.val = val
        self.lineno = lineno

class Uneg(Node):
    def __init__(self, val: Any, lineno: Optional[Any] = 0):
        self.val = val
        self.lineno = lineno

class Transpose(Node):
    def __init__(self, val: Any, lineno: Optional[Any] = 0):
        self.val = val
        self.lineno = lineno

class Matrix(Node):
    def __init__(self, matrix: Any, lineno: Optional[Any] = 0):
        self.matrix = matrix
        self.lineno = lineno

class MatrixFunc(Node):
    def __init__(self, func: Any, dims: Any, lineno: Optional[Any] = 0, type: str = 'int'):
        self.func = func
        self.dims = dims
        self.lineno = lineno
        self.type = type

class Vector(Node):
    def __init__(self, vector, lineno):
        self.vector = vector
        self.lineno = lineno
        self.dims = [len(vector)]
        self.type = None

        if isinstance(vector[0], Vector):
            self.dims += vector[0].dims
        elif isinstance(vector[0], list):
            self.dims += [len(vector[0])]

        cd = vector
        while isinstance(cd, list) or isinstance(cd, Vector):
            if isinstance(cd, list):
                cd = cd[0]
            else:
                cd = cd.vector[0]

        if isinstance(cd, IntNum):
            self.type = 'int'
        if isinstance(cd, FloatNum):
            self.type = 'float'
        if isinstance(cd, String):
            self.type = 'str'

    def __repr__(self):
        return f"[{self.vector}], {self.dims}, {self.type}, {self.lineno}"

class Unary(Node):
    def __init__(self, operation: str, expr: Any, lineno: Optional[Any] = 0, dims: Optional[Any] = None):
        self.operation = operation
        self.expr = expr
        self.lineno = lineno
        self.dims = dims

class Error(Node):
    def __init__(self):
        pass
