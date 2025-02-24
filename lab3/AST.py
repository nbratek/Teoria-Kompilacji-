class Node(object):
    pass


class BinaryExpression(Node):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right


class Conditional(Node):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right


class UnaryMinus(Node):
    def __init__(self, right):
        self.right = right


class Assignment(Node):
    def __init__(self, operator, variable, expression):
        self.operator = operator
        self.variable = variable
        self.expression = expression


class Variable(Node):
    def __init__(self, name):
        self.name = name


class IfStatement(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction


class IfElseStatement(Node):
    def __init__(self, condition, instruction, else_instruction):
        self.condition = condition
        self.instruction = instruction
        self.else_instruction = else_instruction


class WhileLoop(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction


class ForLoop(Node):
    def __init__(self, variable, range_, instruction):
        self.variable = variable
        self.range = range_
        self.instruction = instruction


class LoopRange(Node):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class BreakStatement(Node):
    def __init__(self):
        pass


class ContinueStatement(Node):
    def __init__(self):
        pass


class ReturnStatement(Node):
    def __init__(self, expression):
        self.expression = expression


class PrintStatement(Node):
    def __init__(self, items_to_print):
        self.items_to_print = items_to_print


class Instructions(Node):
    def __init__(self, instructions):
        self.instructions = instructions


class MatrixTransposition(Node):
    def __init__(self, matrix):
        self.matrix = matrix


class Matrix(Node):
    def __init__(self, matrix):
        self.matrix = matrix


class Vector(Node):
    def __init__(self, vector):
        self.vector = vector


class Number(Node):
    def __init__(self, value):
        self.value = value


class MatrixInitialization(Node):
    def __init__(self, identifier, row_index, col_index):
        self.identifier = identifier
        self.row_index = row_index
        self.col_index = col_index


class VectorInitialization(Node):
    def __init__(self, identifier, index):
        self.identifier = identifier
        self.index = index


class MatrixFunctionCall(Node):
    def __init__(self, name, argument):
        self.name = name
        self.argument = argument


class PrintItems(Node):
    def __init__(self, values):
        self.values = values


class Error(Node):
    def __init__(self):
        pass
