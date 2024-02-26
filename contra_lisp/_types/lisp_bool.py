from typing import Any
from ..token import Token
from ._lisp_scalar import LispScalar


class LispBool(LispScalar):

    __lisp_type__ = 'bool'

    def __init__(self, value:Token|bool=None):
        super().__init__()
        self._value = None
        if isinstance(value, Token):
            self.__lisp_token__ = value
            self._value = str(value) == 'true'
        elif isinstance(value, bool):
            self._value = value
        else:
            raise TypeError(f'Either Token or bool must be provided to {type(self).__name__}(); got {type(value).__name__}: {value}')
        if self.__lisp_token__ and str(self.__lisp_token__) not in ['true','false']:
            raise ValueError(f'Token passed to {type(self).__name__}() must contain either "true" or "false"; got "{self.__lisp_token__}"')

    @property
    def __lisp_py_value__(self) -> Any:
        return self._value

    def __lisp_repr__(self) -> str:
        return str(self._value).lower()
    
    def __str__(self) -> str:
        return self.__lisp_repr__()

    def __bool__(self) -> bool:
        return self._value
    
    def __eq__(self, value:Any) -> bool:
        return self.__lisp_py_value__ == value
    
