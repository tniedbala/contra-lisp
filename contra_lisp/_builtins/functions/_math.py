import operator
from ..._types import builtin_function, LispExpression
from ...env import Env
from ..util import reduce


@builtin_function('+')
def Add(self, *args:LispExpression, env:Env) -> LispExpression:
    return reduce(operator.add, *args)


@builtin_function('-')
def Subtract(self, *args:LispExpression, env:Env) -> LispExpression:
    return reduce(operator.sub, *args)


@builtin_function('*')
def Multiply(self, *args:LispExpression, env:Env) -> LispExpression:
    return reduce(operator.mul, *args)


@builtin_function('/')
def Divide(self, *args:LispExpression, env:Env) -> LispExpression:
    return reduce(operator.truediv, *args)


@builtin_function('//')
def FloorDiv(self, *args:LispExpression, env:Env) -> LispExpression:
    return reduce(operator.floordiv, *args)


@builtin_function('^')
def Exponent(self, *args:LispExpression, env:Env) -> LispExpression:
    return reduce(operator.pow, *args)