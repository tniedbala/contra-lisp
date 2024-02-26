from ..token import Token
from ._lisp_scalar import LispScalar

class LispString(str, LispScalar):

    __lisp_type__ = 'string'

    def __new__(cls, value):
        obj = super(LispString, cls).__new__(cls, value)
        obj.__lisp_ast_parent__ = None
        obj.__lisp_token__ = None
        return obj

    @property
    def __lisp_py_value__(self) -> str:
        return str(self)
    
    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self}')"
    
    def __str__(self) -> str:
        return str.__str__(self)
    
    def __lisp_repr__(self) -> str:
        return f"'{self}'"
    
    def __lisp_str__(self) -> str:
        return str(self)
