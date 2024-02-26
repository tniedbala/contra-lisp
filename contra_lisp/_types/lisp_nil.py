from typing import Any
from ._lisp_scalar import LispScalar


class LispNil(LispScalar):
    '''Lisp `nil` type.'''

    __lisp_type__ = 'nil'
    
    @property
    def __lisp_py_value__(self) -> None:
        return None

    def __str__(self) -> str:
        return 'nil'
    
    def __bool__(self) -> bool:
        return False
    
    def __eq__(self, value:Any) -> bool:
        if value is None: return True
        return type(value) == type(self)
    
    def __lisp_repr__(self) -> str:
        return 'nil'
    
