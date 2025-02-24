from typing import Optional, Dict, Any

class Symbol:
    pass

class VariableSymbol(Symbol):
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type

class SymbolTable:
    def __init__(self, parent: Optional['SymbolTable'], name: str):
        self.parent_scope: Optional[SymbolTable] = parent
        self.name: str = name
        self.symbols: Dict[str, Symbol] = {}
        self.type: Dict[str, str] = {}
        self.dims: Dict[str, Any] = {}

    def put(self, name: str, symbol: Symbol) -> None:
        self.symbols[name] = symbol

    def get(self, name: str) -> Optional[Symbol]:
        symbol = self.symbols.get(name)
        if symbol:
            return symbol
        if self.parent_scope:
            return self.parent_scope.get(name)
        raise KeyError(f"Symbol \"{name}\" not found in Scope: \"{self.name}\"")

    def get_dims(self, name: str) -> Any:
        if name in self.dims:
            return self.dims[name]
        if self.parent_scope:
            return self.parent_scope.get_dims(name)
        raise KeyError(f"Dimensions for \"{name}\" not found in Scope: \"{self.name}\"")

    def get_type(self, name: str) -> str:
        type = self.type.get(name)
        if type:
            return type
        if self.parent_scope:
            return self.parent_scope.get_type(name)
        raise KeyError(f"Type for \"{name}\" not found in Scope: \"{self.name}\"")

    def pushScope(self, name: str) -> 'SymbolTable':
        return SymbolTable(self, name)

    def popScope(self) -> Optional['SymbolTable']:
        return self.parent_scope
