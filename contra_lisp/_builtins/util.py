import functools
from typing import Callable
from .._types import LispExpression, resolve_type

def reduce(op:Callable, *args:LispExpression) -> LispExpression:
    return functools.reduce(lambda a, b: resolve_type(op(a, b)), args)