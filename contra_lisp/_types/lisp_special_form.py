from abc import abstractmethod
from typing import Callable
from ._lisp_expression import LispExpression
from ._lisp_callable import lisp_callable
from ._lisp_macro_type import LispMacroType


class LispSpecialForm(LispMacroType):

    __lisp_type__ = 'special-form'
    __lisp_name__ = 'special-form'

    @abstractmethod
    def __call__(self, *args:LispExpression, env:'Env') -> LispExpression:
        pass


def special_form(name:str) -> Callable[[Callable], type]:
    return lisp_callable(name, type=LispSpecialForm)