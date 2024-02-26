from typing import Callable
from ...env import Env
from ..._types import LispSpecialForm, LispExpression, LispSymbol


class Eval(LispSpecialForm):

    def __init__(self, eval:Callable[[LispExpression, Env], LispExpression]=None):
        self.__lisp_constant__ = True
        self.eval = eval
        self.name = 'eval'

    def __call__(self, expression:LispExpression, env:Env) -> LispExpression:
        return self.eval(expression, env)