from ...env import Env
from ..._types import builtin_function, LispExpression, LispNil


@builtin_function('echo')
def Echo(self, *args:LispExpression, env:Env) -> LispNil:
    print(*args, flush=True)
    return LispNil()