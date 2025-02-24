import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:
    @classmethod
    def indent(cls, level):
        return '|  ' * level

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

    @addToClass(AST.Condition)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}{self.operator}")
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Uminus)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}UMINUS")
        self.right.printTree(indent + 1)

    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}{self.operator}")
        self.var.printTree(indent + 1)
        self.expression.printTree(indent + 1)

    @addToClass(AST.Var)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}{self.name}")

    @addToClass(AST.String)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}{self.string}")

    @addToClass(AST.If)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}IF")
        self.cond.printTree(indent + 1)
        print(f"{TreePrinter.indent(indent)}THEN")
        self.instr.printTree(indent + 1)

    @addToClass(AST.Ifelse)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}IF")
        self.cond.printTree(indent + 1)
        print(f"{TreePrinter.indent(indent)}THEN")
        self.instr.printTree(indent + 1)
        print(f"{TreePrinter.indent(indent)}ELSE")
        self.instr_else.printTree(indent + 1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}WHILE")
        self.cond.printTree(indent + 1)
        self.instr.printTree(indent + 1)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}FOR")
        self.var.printTree(indent + 1)
        self.range.printTree(indent + 1)
        self.instr.printTree(indent + 1)


    @addToClass(AST.Range)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}RANGE")
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}BREAK")

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}CONTINUE")

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}PRINT")
        self.to_print.printTree(indent + 1)

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        for instr in self.instructions:
            instr.printTree(indent)

    @addToClass(AST.Transposition)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}TRANSPOSE")
        self.matrix.printTree(indent + 1)

    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}MATRIX")
        for vector in self.matrix:
            vector.printTree(indent + 1)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}VECTOR")
        for elem in self.vector:
            elem.printTree(indent + 1)

    @addToClass(AST.Number)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}{self.value}")

    @addToClass(AST.MatrixRef)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}REF")
        print(f"{TreePrinter.indent(indent + 1)}{self.id}")
        print(f"{TreePrinter.indent(indent + 1)}{self.row_index}")
        print(f"{TreePrinter.indent(indent + 1)}{self.col_index}")

    @addToClass(AST.VectorRef)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}VECTOR INIT")
        self.id.printTree(indent + 1)
        print(f"{TreePrinter.indent(indent + 1)}{self.index}")

    @addToClass(AST.MatrixFunction)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}{self.name}")
        for arg in self.args:
            print(f"{TreePrinter.indent(indent + 1)}{arg}")

    @addToClass(AST.ToPrint)
    def printTree(self, indent=0):
        for val in self.values:
            val.printTree(indent)

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        print(f"{TreePrinter.indent(indent)}RETURN")
        self.expression.printTree(indent + 1)
