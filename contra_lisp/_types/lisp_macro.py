from abc import abstractmethod
from ._lisp_expression import LispExpression
from ._lisp_macro_type import LispMacroType
from .lisp_block import LispBlock


class LispMacro(LispMacroType):

    __lisp_type__ = 'macro'
    __lisp_name__ = 'macro'

    @abstractmethod
    def __call__(self, *args:LispExpression, env:'Env') -> LispBlock:
        pass
