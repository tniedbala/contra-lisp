from ...env import Env
from ..._types import special_form, LispExpression, LispSymbol

# TODO: allow assignment to dotrefs
@special_form('set')
def Set(self, *args:LispExpression, env:Env) -> LispExpression:
    if len(args) < 3 or len(args) % 3 != 0:
        raise SyntaxError(f'Invalid number of arguments passed to {self.name_}')
    assign = LispSymbol('=')
    for i in range(0, len(args), 3):
        op = args[i+1]
        if op != assign:
            raise SyntaxError(f'(set ...) expected assignment operator ({assign}); got "{op.__lisp_repr__()}')
        symbol = args[i]
        value = env.eval(args[i+2])
        env[symbol] = value
    return value