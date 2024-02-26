from typing import Any
from decimal import Decimal
from ..token import Token
from ._lisp_scalar import LispScalar


class LispNumber(Decimal, LispScalar):

    __lisp_type__ = 'number'

    def __new__(cls, value):
        obj = super(LispNumber, cls).__new__(cls, value)
        obj.__lisp_ast_parent__ = None
        obj.__lisp_token__ = None
        return obj
        
    @property
    def __lisp_py_value__(self) -> Decimal:
        return Decimal(self)
    
    def __repr__(self) -> str:
        return f'{type(self).__name__}({self})'
    
    def __lisp_repr__(self) -> str:
        return str(self)

