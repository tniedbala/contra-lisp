from typing import Callable
from ._lisp_callable import lisp_callable
from ._lisp_function_type import LispFunctionType


class LispBuiltinFunction(LispFunctionType):

    __lisp_type__ = 'builtin-function'


def builtin_function(name:str) -> Callable[[Callable], type]:
    return lisp_callable(name, type=LispBuiltinFunction)
