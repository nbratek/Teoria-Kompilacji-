
import AST
from SymbolTable import SymbolTable, VariableSymbol
from collections import defaultdict

class NodeVisitor:
    def __init__(self):
        self.global_scope = SymbolTable(None, "global")
        self.current_scope = self.global_scope
        self.loop_depth = 0

    def visit(self, node):
        method_name = f"visit_{node.__class__.__name__}"
        visitor_method = getattr(self, method_name, self.generic_visit)
        if visitor_method == self.generic_visit:
            print(f"Warning: No method to visit {node.__class__.__name__}")
        return visitor_method(node)

    def generic_visit(self, node):
        if isinstance(node, list):
            for item in node:
                self.visit(item)
        else:
            for child in getattr(node, "children", []):
                self.visit(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        super().__init__()
        self.allowed_ops = defaultdict(lambda: defaultdict(dict))
        self.define_operations()

    def define_operations(self):
        self.allowed_ops['+']['int']['int'] = 'int'
        self.allowed_ops['+']['int']['float'] = 'float'
        self.allowed_ops['+']['float']['int'] = 'float'
        self.allowed_ops['+']['float']['float'] = 'float'

        self.allowed_ops['-']['int']['int'] = 'int'
        self.allowed_ops['-']['int']['float'] = 'float'
        self.allowed_ops['-']['float']['int'] = 'float'
        self.allowed_ops['-']['float']['float'] = 'float'

        self.allowed_ops['*']['int']['int'] = 'int'
        self.allowed_ops['*']['int']['float'] = 'float'
        self.allowed_ops['*']['float']['int'] = 'float'
        self.allowed_ops['*']['float']['float'] = 'float'

        self.allowed_ops['/']['int']['int'] = 'int'
        self.allowed_ops['/']['int']['float'] = 'float'
        self.allowed_ops['/']['float']['int'] = 'float'
        self.allowed_ops['/']['float']['float'] = 'float'

        comparison_ops = ['>', '<', '>=', '<=', '==', '!=']
        for op in comparison_ops:
            self.allowed_ops[op]['int']['int'] = 'bool'
            self.allowed_ops[op]['int']['float'] = 'bool'
            self.allowed_ops[op]['float']['int'] = 'bool'
            self.allowed_ops[op]['float']['float'] = 'bool'


    def verify_operation(self, operator, type1, type2, lineno):
        result = self.allowed_ops.get(operator, {}).get(type1, {}).get(type2)
        if result is None:
            print(f"[{lineno}]: Error: Invalid operation {type1} {operator} {type2}")
        return result

    def visit_Instructions(self, node: AST.Instructions):
        for stmt in node.instructions:
            self.visit(stmt)

    def visit_Assignment(self, node: AST.Assignment):
        name = node.var.name
        evaluated_type = self.visit(node.expression)

        if evaluated_type in ["vector", "matrix"]:
            dimensions = getattr(node.expression, "dims", None)
            self.global_scope.put(name, VariableSymbol(name, evaluated_type, size=dimensions))
        else:
            self.global_scope.put(name, VariableSymbol(name, evaluated_type))

    def visit_BinaryExpression(self, node: AST.BinaryExpression):
        if not isinstance(node.left, AST.Node) or not isinstance(node.right, AST.Node):
            print(f"[{node.line}]: Error: Binary expression operands must be valid AST nodes")
            return None

        left = self.visit(node.left)
        right = self.visit(node.right)

        result = self.verify_operation(node.operator, left, right, node.line)
        if result is None:
            print(f"[{node.line}]: Error in binary operation {left} {node.operator} {right}")
        return result

    def visit_Number(self, node: AST.Number):
        if "." in str(node.value):
            node.type = "float"
        else:
            node.type = "int"
        return node.type

    def visit_Vector(self, node):
        if not isinstance(node.vector, list):
            print(f"[{node.line}]: Error: Vector should be a list")
            return

        for item in node.vector:
            if not isinstance(item, AST.Number) and not isinstance(item, AST.Var):
                print(f"[{node.line}]: Error: Vector elements must be numbers or variables")
                return
            self.visit(item)

        if not node.vector:
            print(f"[{node.line}]: Error: Empty vector")
            return

        if any(not hasattr(element, "type") or element.type != node.vector[0].type for element in node.vector):
            print(f"[{node.line}]: Error: Vector elements must be of the same type")
            return

        node.type = "vector"
        node.size = (1, len(node.vector))

    def visit_Matrix(self, node):
        if not isinstance(node.matrix, list):
            print(f"[{node.line}]: Error: Matrix should be a list of vectors")
            return

        for row in node.matrix:
            if not isinstance(row, AST.Vector):
                print(f"[{node.line}]: Error: Each row in a matrix must be a vector")
                return
            self.visit(row)

        initial_size = node.matrix[0].size if node.matrix else None
        if initial_size is None:
            print(f"[{node.line}]: Error: Matrix rows not properly defined")
            return

        if any(row.size != initial_size for row in node.matrix):
            print(f"[{node.line}]: Error: Inconsistent row sizes in matrix")
            return

        node.type = "matrix"
        node.size = (len(node.matrix), initial_size[1])

    def visit_MatrixRef(self, node):
        self.visit(node.row_index)
        self.visit(node.col_index)
        self.visit(node.id)

        if node.id.type != "matrix":
            print(f"[{node.line}]: Error: Variable is not a matrix")
            return

        self._validate_index(node.row_index, node.id.size[0], node.line, "row")
        self._validate_index(node.col_index, node.id.size[1], node.line, "column")

    def visit_VectorRef(self, node):
        if not isinstance(node.index, AST.Number) and not isinstance(node.index, AST.Range):
            print(f"[{node.line}]: Error: Vector index must be a number or a range")
            return

        self.visit(node.index)
        self.visit(node.id)

        if not isinstance(node.id, AST.Var) or node.id.type != "vector":
            print(f"[{node.line}]: Error: Variable is not a vector")
            return

        self._validate_index(node.index, node.id.size[1], node.line, "vector index")

    def visit_Var(self, node: AST.Var):
        if not isinstance(node.name, str):
            print(f"[{node.line}]: Error: Variable name must be a string")
            return None

        symbol = self.global_scope.get(node.name)
        if symbol is None:
            print(f"Undefined variable {node.name} (line {node.line})")
            return None
        return symbol.type

    def visit_Transposition(self, node: AST.Transposition):
        self.visit(node.matrix)
        if node.matrix.type not in ("matrix", "vector"):
            print(f"[{node.line}]: Transposition: only matrix or vector can be transposed")
            return

        node.type = node.matrix.type
        node.size = (node.matrix.size[1], node.matrix.size[0])

    def visit_While(self, node: AST.While):
        self.symbol_table = self.global_scope.pushScope("while")
        self.loop_depth += 1
        self.visit(node.cond)
        self.visit(node.instr)
        self.global_scope = self.symbol_table.popScope()
        self.loop_depth -= 1

    def visit_For(self, node: AST.For):
        self.current_scope = self.current_scope.pushScope('for')
        self.loop_depth += 1
        t1 = self.visit(node.cond_start)
        t2 = self.visit(node.cond_end)

        if t1 is None or t2 is None or t1 != "int" or t2 != "int":
            print(f"[{node.lineno}]: Error: Operand types in for loop range must be 'int'")
            self.current_scope.put(node.id, None)
        else:
            if isinstance(node.id, AST.Var):
                self.current_scope.put(node.id.name, VariableSymbol(node.id.name, t1))
            else:
                print(f"[{node.lineno}]: Error: Invalid loop variable")

        self.visit(node.body)

        self.current_scope = self.current_scope.popScope()
        self.loop_depth -= 1

    def visit_Continue(self, node: AST.Continue):
        if self.loop_depth == 0:
            print(f"Line {node.line}: 'Continue' statement used outside of a loop")

    def visit_Break(self, node: AST.Break):
        if self.loop_depth == 0:
            print(f"Line {node.line}: 'Break' statement used outside of a loop")

    def visit_Return(self, node: AST.Return):
        expr_type = self.visit(node.expression)
        if expr_type is None:
            print(f"[{node.line}]: Return error: cannot return None type")
        # else:
        #     print(f"[{node.line}]: Return statement with type '{expr_type}'")
    def visit_Print(self, node: AST.Print):
        for expr in node.to_print.values:
            expr_type = self.visit(expr)
            if expr_type is None:
                print(f"[{node.line}]: Print error: invalid expression")

    def visit_Ifelse(self, node: AST.Ifelse):
        self.visit(node.cond)

        self.current_scope = self.current_scope.pushScope("if")
        self.visit(node.instr)
        self.current_scope = self.current_scope.popScope()

        self.current_scope = self.current_scope.pushScope("else")
        self.visit(node.instr_else)
        self.current_scope = self.current_scope.popScope()

    def visit_If(self, node: AST.If):
        self.visit(node.cond)

        self.current_scope = self.current_scope.pushScope("if")
        self.visit(node.instr)
        self.current_scope = self.current_scope.popScope()

    def _validate_index(self, index, size_limit, line, index_type):
        if isinstance(index, AST.Range):
            if not isinstance(index.left, AST.Number) or not isinstance(index.right, AST.Number):
                print(f"[{line}]: Error: {index_type.capitalize()} range must consist of numbers")
                return
            if index.left.value < 0 or index.right.value > size_limit:
                print(f"[{line}]: Error: {index_type.capitalize()} out of bounds")
        elif isinstance(index, AST.Number):
            if index.type != "int":
                print(f"[{line}]: Error: {index_type.capitalize()} must be of type int")
            elif index.value < 0 or index.value >= size_limit:
                print(f"[{line}]: Error: {index_type.capitalize()} out of bounds")
        else:
            print(f"[{line}]: Error: Invalid {index_type.capitalize()} type")


