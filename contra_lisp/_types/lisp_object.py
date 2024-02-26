import re 
from typing import Any, Dict, Iterator, List, Tuple
from ..grammar import Grammar
from ._lisp_expression import LispExpression
from ._lisp_collection import LispCollection
from .lisp_block import LispBlock
from .lisp_symbol import LispSymbol
from .lisp_keyword import LispKeyword
from .lisp_bool import LispBool
from .python_object import PythonObject

grammar = Grammar()

class LispObject(LispCollection):

    __lisp_type__ = 'object'

    def __init__(self, block:LispBlock, env:'Env'):
        from lisp import Env
        super().__init__(self)
        self.members = {}
        self.__lisp_start_token__ = block.__lisp_start_token__
        self.__lisp_end_token__ = block.__lisp_end_token__
        self.__lisp_env__ = Env(parent=env)
        # TODO: need to ensure "this" is a constant
        self.__lisp_env__['this'] = self
        self.init_members(block)
    
    @property
    def __lisp_py_value__(self) -> Dict[str, Any]:
        return {str(key): value.__lisp_py_value__ for key, value in self.items()}
    
    @property
    def __lisp_readonly__(self) -> bool:
        return self[LispKeyword('@readonly')]
    
    def __contains__(self, key:str|LispSymbol) -> bool:
        key = self.get_key(key)
        return key in self.members
    
    def __len__(self) -> int:
        return len(self.members)
    
    def __iter__(self) -> Iterator:
        return self.members.__iter__()
    
    # TODO:
    # override __getattr__() & __setattr__() for convenience using from python

    def __getitem__(self, key:str|LispSymbol) -> Any:
        key = self.get_key(key)
        return self.members[key]

    def __setitem__(self, key:str|LispSymbol, value:Any):
        # if self.__lisp_readonly__:
        #     raise AttributeError(f'Cannot set key {key} of readonly object.')
        key = self.get_key(key)
        value = PythonObject(value) if not isinstance(value, LispExpression) else value
        value.__lisp_ast_parent__ = self
        self.members[key] = value
    
    def keys(self) -> List[LispSymbol]:
        return list(self.members.keys())
    
    def values(self) -> List[LispExpression]:
        return list(self.members.values())
    
    def items(self) -> List[Tuple[LispSymbol, LispExpression]]:
        return list(self.members.items())

    def get_key(self, key:str|LispSymbol):
        if type(key) == str:
            if grammar.is_symbol(key):
                key = LispSymbol(key)
            elif grammar.is_keyword(key):
                key = LispKeyword(key)
            else:
                self.raise_invalid_key(key)
        if not isinstance(key, LispSymbol):
            self.raise_invalid_key(key)
        return key

    def set_default_key(self, key:LispSymbol, value:LispExpression):
        key.__lisp_ast_parent__ = self
        value.__lisp_ast_parent__ = self
        dict.__setitem__(self, key, value)

    def init_members(self, block:LispBlock):
        self.validate_block(block)
        for i in range(0, len(block), 3):
            key = block[i]
            value = block[i+2]
            self.members[key] = self.__lisp_env__.eval(value)

    def _wrap_str(self, body) -> str:
        return f'{self.__lisp_type__}{{{body}}}'
    
    @classmethod
    def raise_invalid_key(cls, key:str|LispSymbol):
        raise SyntaxError(f'Invalid object key: {key}')
    
    @classmethod
    def is_object(cls, block:LispBlock) -> bool:
        try:
            cls.validate_block(block)
            return True
        except:
            return False
    
    @classmethod
    def validate_block(cls, block:LispBlock):
        '''Indicate whether an unevaluated block expression is a valid object definition.'''
        if len(block) % 3 != 0:
            raise SyntaxError(f'Mismatched number of keys/values passed to {cls.__lisp_type__}.')
        assign = LispSymbol(':')
        for i in range(0, len(block), 3):
            key = block[i]
            op = block[i+1]
            if op != assign:
                raise SyntaxError(f'key/value assignments for {cls.__lisp_type__} require assignment operator (:); got "{op}".')
            if not isinstance(key, LispSymbol):
                cls.raise_invalid_key(key)

