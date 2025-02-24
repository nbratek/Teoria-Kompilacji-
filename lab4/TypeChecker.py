from collections import defaultdict
import AST
from SymbolTable import SymbolTable


class NodeVisitor(object):
    def __init__(self):
        self.symbol_table = SymbolTable(None, "global")
        self.current_scope = self.symbol_table
        self.loop_indent = 0

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

class TypeChecker(NodeVisitor):

    def __init__(self):
        super().__init__()
        self.allowed_ops = defaultdict(lambda: defaultdict(dict))
        self.define_operations()

    def define_operations(self):
        for op in ['+', '-', '*', '/']:
            self.allowed_ops[op]['int']['int'] = 'int'
            self.allowed_ops[op]['int']['float'] = 'float'
            self.allowed_ops[op]['float']['int'] = 'float'
            self.allowed_ops[op]['float']['float'] = 'float'
            self.allowed_ops[op]['vector']['vector'] = 'vector'

        comparison_ops = ['>', '<', '>=', '<=', '==', '!=']
        for op in comparison_ops:
            self.allowed_ops[op]['int']['int'] = 'bool'
            self.allowed_ops[op]['int']['float'] = 'bool'
            self.allowed_ops[op]['float']['int'] = 'bool'
            self.allowed_ops[op]['float']['float'] = 'bool'
            self.allowed_ops[op]['vector']['vector'] = 'bool'

    def verify_operation(self, operator, type1, type2, lineno):
        result = self.allowed_ops.get(operator, {}).get(type1, {}).get(type2)
        if result is None:
            print(f"{lineno}: Error: Invalid operation {type1} {operator} {type2}")
        return result

    def visit_InstrOrEmpty(self, node: AST.InstrOrEmpty):
        self.visit(node.instructions)

    def visit_Instructions(self, node: AST.Instructions):
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_Id(self, node: AST.Id):
        return self.symbol_table.get(node.id)
        pass

    def visit_BinExpr(self, node: AST.BinExpr):
        node.v_type = 'float'
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op
        if op not in self.allowed_ops or type1 not in self.allowed_ops[op] or type2 not in self.allowed_ops[op][type1]:
            print(f"{node.lineno} {type1} {op} {type2} is not correct")
            return None
        if 'vector' in (type1, type2):
            left_dims = self.resolve_dimensions(node.left, 'TRANSPOSE' in (getattr(node.left, 'operation', ''),))
            right_dims = self.resolve_dimensions(node.right, 'TRANSPOSE' in (getattr(node.right, 'operation', ''),))
            if len(left_dims) != len(right_dims) or any(leftd != rightd for leftd, rightd in zip(left_dims, right_dims)):
                print(f"{node.lineno} Vector sizes do not match")
                return None
            node.dims = left_dims
        node.v_type = self.allowed_ops[op][type1][type2]
        return node.v_type

    def resolve_dimensions(self, operand, transposed):
        if isinstance(operand, AST.Id):
            dims = self.symbol_table.get_dims(operand.id)
        elif hasattr(operand, 'dims'):
            dims = operand.dims
        else:
            dims = []

        return dims[::-1] if transposed else dims

    def visit_Variable(self, node: AST.Variable):
        dims = self.symbol_table.dims[node.id.id]
        if len(dims) != len(node.index):
            print(f"{node.lineno} Inconsistent vector dimensions.")
            return None
        for i in range(len(node.index)):
            if self.visit(node.index[i]) != 'int':
                print(f"{node.lineno} Vector index must be int")
                return None

            if node.index[i].intnum >= dims[i].intnum:
                print(f"{node.lineno} Index not valid for the dimension size.")
                return None
        return self.symbol_table.type[node.id.id]

    def visit_Vector(self, node: AST.Vector):
        expected_dims = [len(node.vector[0])] if isinstance(node.vector[0], list) else [1]
        if isinstance(node.vector[0], AST.Vector):
            expected_dims = node.vector[0].dims
        for element in node.vector:
            if isinstance(element, AST.Vector):
                self.visit(element)
                element_dims = element.dims
            elif isinstance(element, list):
                element_dims = [len(element)]
            else:
                element_dims = [1]
            if element_dims != expected_dims:
                print(f"{node.lineno} Dimension mismatch in vectors")
                return None
        return 'vector'

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

    def visit_Transposition(self, node: AST.Transpose):
        self.visit(node.val)
        if node.val.type not in ("matrix", "vector"):
            print(f"[{node.lineno}]: Transposition: only matrix or vector can be transposed")
            return

        node.type = node.matrix.type
        node.size = (node.matrix.size[1], node.matrix.size[0])

    def visit_If(self, node: AST.If):
        self.visit(node.cond)

        self.current_scope = self.current_scope.pushScope("if")
        self.visit(node.if_body)
        self.current_scope = self.current_scope.popScope()

        self.current_scope = self.current_scope.pushScope("else")
        self.visit(node.else_body)
        self.current_scope = self.current_scope.popScope()

    def visit_Return(self, node: AST.Return):
        return self.visit(node.expr)

    def visit_Break(self, node: AST.Break):
        if self.loop_indent == 0:
            print(f"Line {node.lineno}: 'Break' statement used outside of a loop")

    def visit_Continue(self, node: AST.Continue):
        if self.loop_indent == 0:
            print(f"Line {node.lineno}: 'Continue' statement used outside of a loop")

    def visit_For(self, node:AST.For):
        self.symbol_table = self.symbol_table.pushScope('for')
        self.loop_indent += 1
        t1 = self.visit(node.cond_start)
        t2 = self.visit(node.cond_end)

        if t1 is None or t2 is None or t1 != t2:
            print(f"{node.lineno} something wrong with operand types")
            self.symbol_table.put(node.id, None)

        else:
            if isinstance(node.id, AST.Id):
                self.symbol_table.put(node.id.id, t1)
            else:
                self.symbol_table.put(node.id, t1)

        self.visit(node.body)
        self.symbol_table = self.symbol_table.popScope()
        self.loop_indent -= 1

    def visit_While(self, node: AST.While):
        self.symbol_table = self.symbol_table.pushScope("while")
        self.loop_indent += 1
        self.visit(node.cond)
        self.visit(node.body)
        self.symbol_table = self.symbol_table.popScope()
        self.loop_indent -= 1



    def visit_Print(self, node: AST.Print):
        for i in node.printargs:
            self.visit(i)




    def visit_Unary(self, node: AST.Uneg):
        return self.visit(node.expr)

    def visit_MatrixFunc(self, node: AST.MatrixFunc):
        for el in node.dims:
            if self.visit(el) != 'int':
                print(f"{node.lineno} matrix function takes int")
                return None
        return 'vector'

    def visit_AssignOp(self, node: AST.AssignOp):
        rhs_type = self.visit(node.right)
        if rhs_type is None:
            return None
        target_id = node.left.id if isinstance(node.left.id, str) else node.left.id.id
        if node.op == '=':
            self.symbol_table.put(target_id, rhs_type)
            if rhs_type == 'vector':
                if isinstance(node.right, AST.Unary) and node.right.operation == "TRANSPOSE":
                    self.symbol_table.dims[target_id] = node.right.expr.dims[::-1]
                    self.symbol_table.type[target_id] = node.right.expr.type
                elif hasattr(node.right, 'dims'):
                    direct_dims = node.right.dims.intnum if isinstance(node.right.dims, AST.IntNum) else node.right.dims
                    self.symbol_table.dims[target_id] = direct_dims
                    self.symbol_table.type[target_id] = rhs_type
        else:
            existing_type = self.symbol_table.get(target_id)
            if existing_type == 'vector' and rhs_type == 'vector':
                existing_dims = self.symbol_table.dims[target_id]
                rhs_dims = node.right.dims
                if not all(e == r for e, r in zip(existing_dims, rhs_dims)):
                    print(f"{node.lineno} Dimension mismatch")
                    return None
            operation_result_type = self.allowed_ops.get(node.op, {}).get(existing_type, {}).get(rhs_type)
            if operation_result_type:
                return operation_result_type
            else:
                print(f"{node.lineno} Unsupported operation '{node.op}' on types {existing_type} and {rhs_type}")
                return None


    def visit_String(self, node: AST.String):
        return 'str'

    def visit_IntNum(self, node: AST.IntNum):
        return 'int'

    def visit_FloatNum(self, node: AST.FloatNum):
        return 'float'

