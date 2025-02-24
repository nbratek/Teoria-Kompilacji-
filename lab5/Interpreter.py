import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys
import numpy as np

sys.setrecursionlimit(10000)
operations = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '<': lambda x, y: x < y,
            '>': lambda x, y: x > y,
            '<=': lambda x, y: x <= y,
            '>=': lambda x, y: x >= y,
            '==': lambda x, y: x == y,
            '!=': lambda x, y: x != y,
            '.+': lambda x, y: mat_add(x, y),
            '.-': lambda x, y: mat_sub(x, y),
            '.*': lambda x, y: mat_mul(x, y),
            './': lambda x, y: mat_div(x, y)
        }

def mat_add( a, b):
    if isinstance(a[0], list):
        return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]
    return [a[i] + b[i] for i in range(len(a))]


def mat_sub(a, b):
    if isinstance(a[0], list):
        return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]
    return [a[i] - b[i] for i in range(len(a))]


def mat_mul( a, b):
    if isinstance(a[0], list):
        return [[a[i][j] * b[i][j] for j in range(len(a[0]))] for i in range(len(a))]
    return [a[i] * b[i] for i in range(len(a))]


def mat_div(a, b):
    if isinstance(a[0], list):
        return [[a[i][j] / b[i][j] for j in range(len(a[0]))] for i in range(len(a))]
    return [a[i] / b[i] for i in range(len(a))]


class Interpreter(object):
    def __init__(self, operations):
        self.operations = operations
    @on('node')
    def visit(self, node):
        pass

    @when(AST.InstructionsOrEmpty)
    def visit(self, node: AST.Instructions):
        self.memory = MemoryStack()
        self.memory.push('global')
        node.instructions.accept(self)

    @when(AST.Instructions)
    def visit(self, node: AST.Instructions):
        for instruction in node.instructions:
            instruction.accept(self)

    @when(AST.BinaryExpression)
    def visit(self, node: AST.BinaryExpression):
        l = node.left.accept(self)
        r = node.right.accept(self)
        return self.operations[node.operator](l, r)

    @when(AST.Condition)
    def visit(self, node: AST.Condition):
        left_result = node.left.accept(self)
        right_result = node.right.accept(self)
        operator = node.operator
        return self.operations[operator](left_result, right_result)

    @when(AST.Uminus)
    def visit(self, node: AST.Uminus):
        result = node.right.accept(self)
        if isinstance(result, list):
            if result and isinstance(result[0], list):
                return [[-x for x in row] for row in result]
            else:
                return [-x for x in result]
        else:
            return -result

    @when(AST.Id)
    def visit(self, node: AST.Id):

        return self.memory.get(node.name)

    @when(AST.IntNum)
    def visit(self, node: AST.IntNum):
        return int(node.intnum)

    @when(AST.Float)
    def visit(self, node: AST.Float):
        return float(node.floatnum)

    @when(AST.String)
    def visit(self, node: AST.String):
        return str(node.string)

    @when(AST.Ifelse)
    def visit(self, node: AST.Ifelse):
        if node.cond.accept(self):
            self.execute_block(node.instr, 'if')
        elif node.instr_else is not None:
            self.execute_block(node.instr_else, 'else')

    def execute_block(self, instructions, context_type):
        self.memory.push(context_type)
        try:
            if isinstance(instructions, AST.Instructions):
                instructions.accept(self)
            else:
                for instruction in instructions:
                    instruction.accept(self)
        except BreakException as e:
            raise e
        finally:
            self.memory.pop()

    @when(AST.While)
    def visit(self, node: AST.While):
        self.memory.push("while")
        try:
            while node.cond.accept(self):
                try:
                    if isinstance(node.instr, list):
                        for instruction in node.instr:
                            try:
                                instruction.accept(self)
                            except ContinueException:
                                break
                            except BreakException:
                                raise
                    else:
                        try:
                            node.instr.accept(self)
                        except ContinueException:
                            continue
                        except BreakException:
                            raise
                except BreakException:
                    break
        finally:
            self.memory.pop()

    @when(AST.For)
    def visit(self, node: AST.For, n: AST.Range):
        iterator = node.var
        start = n.left.accept(self)
        end = n.right.accept(self)
        self.memory.push("for")
        self.memory.set(iterator.id, start)
        try:
            while self.memory.get(iterator.id) <= end:
                try:
                    if isinstance(node.instr, list):
                        for instruction in node.instr:
                            try:
                                instruction.accept(self)
                            except ContinueException:
                                break
                            except BreakException:
                                raise
                    else:
                        try:
                            node.instr.accept(self)
                        except ContinueException:
                            continue
                        except BreakException:
                            raise
                    self.memory.set(iterator.id, self.memory.get(iterator.id) + 1)
                except BreakException:
                    break
        finally:
            self.memory.pop()


    @when(AST.Return)
    def visit(self, node: AST.Return):
        raise ReturnValueException(node.expression.accept(self))

    @when(AST.Break)
    def visit(self, node: AST.Break):
        raise BreakException()

    @when(AST.Continue)
    def visit(self, node: AST.Continue):
        raise ContinueException()

    @when(AST.Print)
    def visit(self, node: AST.Print):
        to_print = [element.accept(self) for element in node.to_print]
        print(*to_print, sep=' ')

    @when(AST.Assignment)
    def visit(self, node: AST.Assignment):
        if not isinstance(node.var, AST.Variable):
            if node.operator == '=':
                self.memory.set(node.var.id, node.expression.accept(self))
            else:
                self.memory.set(node.var.id,
                                operations[node.operator[0]](self.memory.get(node.var.id), node.expression.accept(self)))
        else:
            matrix = self.memory.get(node.var.id.id)
            if isinstance(node.var.index[0], tuple):
                x = [i for i in range(node.var.index[0][0].accept(self), node.var.index[0][1].accept(self))]
            else:
                x = [node.var.index[0].accept(self)]
            if isinstance(node.var.index[1], tuple):
                y = [i for i in range(node.var.index[1][0].accept(self), node.var.index[1][1].accept(self))]
            else:
                y = [node.var.index[1].accept(self)]
            if node.operator == '=':
                for i in x:
                    for j in y:
                        matrix[j][i] = node.expression.accept(self)
            else:
                for i in x:
                    for j in y:
                        matrix[j][i] = operations[node.operator[0]](matrix[j][i], node.expression.accept(self))

            self.memory.set(node.var.id.id, matrix)

    @when(AST.Vector)
    def visit(self, node: AST.Vector):
        return [element.accept(self) for element in node.vector]

    @when(AST.MatrixRef)
    def visit(self, node: AST.Variable):
        matrix = self.memory.get(node.id.id)
        x = node.index[0].accept(self)
        y = node.index[1].accept(self)
        return matrix[x][y]

    @when(AST.MatrixFunction)
    def visit(self, node: AST.MatrixFunction):
        func = node.name
        args = [arg.accept(self) for arg in node.args]

        def create_matrix(rows, cols, fill_value):
            return [[fill_value for _ in range(cols)] for _ in range(rows)]

        def create_identity_matrix(size):
            return [[1 if i == j else 0 for i in range(size)] for j in range(size)]

        matrix_creators = {
            'zeros': lambda args: create_matrix(args[0], args[1] if len(args) > 1 else args[0], 0),
            'ones': lambda args: create_matrix(args[0], args[1] if len(args) > 1 else args[0], 1),
            'eye': lambda args: create_identity_matrix(args[0])
        }
        return matrix_creators[func](args)