from typing import Any
from ._lisp_expression import LispExpression
from .lisp_string import LispString
from ..token import Token


class LispSymbol(LispString):

    __lisp_type__ = 'symbol'
    
    def __repr__(self) -> str:
        return f"{type(self).__name__}({self})"
    
    def __eq__(self, value:LispExpression) -> bool:
        if type(value) == type(self):
            return self.__lisp_py_value__ == value.__lisp_py_value__
        return False
    
    def __hash__(self) -> int:
        return hash(f'{self.__lisp_type__}::{self}')
    
    def __lisp_repr__(self) -> str:
        return str.__str__(self)
        
