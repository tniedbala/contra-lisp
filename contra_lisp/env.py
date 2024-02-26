from typing import Any, Dict
from ._types import LispExpression, LispSymbol, resolve_type


class Env(dict):

    def __init__(self, env:Dict[LispSymbol, LispExpression]={}, parent:'Env'=None):
        super().__init__(env)
        object.__setattr__(self, 'parent', parent)

    def __getattr__(self, key:str|LispSymbol) -> LispExpression:
        return self[key]
    
    def __setattr__(self, key:str|LispSymbol, value:Any):
        self[key] = value

    def __getitem__(self, key:LispSymbol) -> LispExpression:
        key = self.get_key(key)
        if key in self:
            return dict.__getitem__(self, key)
        elif self.parent is not None:
            return self.parent[key]
        else:
            raise NameError(f'Name "{key}" is not defined.')

    def __setitem__(self, key:LispSymbol, value:LispExpression):
        key = self.get_key(key)
        if type(key) != LispSymbol:
            raise SyntaxError(f'Cannot assign to value to {key}.')
        # TODO: raise errors when attempting to set a constant or a bulitin
        dict.__setitem__(self, key, resolve_type(value))

    def get(self, key:LispSymbol, default=None):
        try:
            return self[key]
        except:
            return default
        
    def get_key(self, key:str|LispSymbol) -> LispSymbol:
        if isinstance(key, LispSymbol):
            return key
        elif isinstance(key, str):
            return LispSymbol(key)
        else:
            raise SyntaxError(f'Invalid value referenced as name; expected symbol, got "{key}".')

    def eval(self, expression:LispExpression):
        _eval = self.get('eval')
        if _eval is None:
            raise Exception('eval is undefined in the current environment.')
        return _eval(expression, self)
    