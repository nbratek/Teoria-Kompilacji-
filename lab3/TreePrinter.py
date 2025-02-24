import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:
    @staticmethod
    def indent(length):
        return ''.join('|  ' * length)

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass

    @addToClass(AST.BinaryExpression)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}{self.operator}")
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Conditional)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}{self.operator}")
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.UnaryMinus)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}UMINUS")
        self.right.printTree(indent + 1)

    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}{self.operator}")
        self.variable.printTree(indent + 1)
        self.expression.printTree(indent + 1)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}{self.name}")

    @addToClass(AST.IfStatement)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}IF")
        self.condition.printTree(indent + 1)
        print(f"{TreePrinter.indent(indent)}THEN")
        self.instruction.printTree(indent + 1)

    @addToClass(AST.IfElseStatement)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}IF")
        self.condition.printTree(indent + 1)
        print(f"{TreePrinter.indent(indent)}THEN")
        self.instruction.printTree(indent + 1)
        print(f"{TreePrinter.indent(indent)}ELSE")
        self.else_instruction.printTree(indent + 1)

    @addToClass(AST.WhileLoop)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}WHILE")
        self.condition.printTree(indent + 1)
        self.instruction.printTree(indent + 1)

    @addToClass(AST.ForLoop)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}FOR")
        self.variable.printTree(indent + 1)
        self.range.printTree(indent + 1)
        self.instruction.printTree(indent + 1)

    @addToClass(AST.LoopRange)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}RANGE")
        self.start.printTree(indent + 1)
        self.end.printTree(indent + 1)

    @addToClass(AST.BreakStatement)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}BREAK")

    @addToClass(AST.ContinueStatement)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}CONTINUE")

    @addToClass(AST.PrintStatement)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}PRINT")
        self.items_to_print.printTree(indent + 1)

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        for instr in self.instructions:
            if instr:
                instr.printTree(indent)

    @addToClass(AST.MatrixTransposition)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}TRANSPOSE")
        self.matrix.printTree(indent + 1)

    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}MATRIX")
        for vector in self.matrix:
            if vector:
                vector.printTree(indent + 1)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}VECTOR")
        for elem in self.vector:
            if elem:
                elem.printTree(indent + 1)

    @addToClass(AST.Number)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}{self.value}")

    @addToClass(AST.MatrixInitialization)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}REF")
        print(f"{TreePrinter.indent(indent + 1)}{self.identifier}")
        print(f"{TreePrinter.indent(indent + 1)}{self.row_index}")
        print(f"{TreePrinter.indent(indent + 1)}{self.col_index}")

    @addToClass(AST.VectorInitialization)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}VECTOR INIT")
        self.identifier.printTree(indent + 1)
        print(f"{TreePrinter.indent(indent + 1)}{self.index}")

    @addToClass(AST.MatrixFunctionCall)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}{self.name}")
        print(f"{TreePrinter.indent(indent + 1)}{self.argument}")

    @addToClass(AST.PrintItems)
    def printTree(self, indent=0):
        for val in self.values:
            if val:
                val.printTree(indent)
