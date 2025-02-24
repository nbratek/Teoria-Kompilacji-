class Symbol:
    pass


class VariableSymbol:
    def __init__(self, name, type, size=None):
        self.name = name
        self.type = type
        self.size = size



class SymbolTable(object):

    def __init__(self, parent, name):
        self.parent_scope = parent
        self.name = name
        self.symbols = {}

    def put(self, name, symbol):
        self.symbols[name] = symbol

    def get(self, name):
        if name in self.symbols:
            return self.symbols[name]
        else:
            return self.parent_scope.get(name)

    def pushScope(self, name):
        return SymbolTable(self, name)

    def popScope(self):
        return self.parent_scope


