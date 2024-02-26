from ...env import Env
from ..._types import special_form, LispExpression, LispSymbol, LispFunction

# def __init__(self, params:LispList, body:LispExpression, name:LispSymbol=None):

@special_form('fn')
def Fn(self, *args:LispExpression, env:Env) -> LispFunction:
    name = None
    match len(args):
        case 2:
            params = args[0]
            body = args[1]
        case 3:
            name = args[0]
            params = args[1]
            body = args[2]
        case _:
            raise SyntaxError('Invalid number of arguments provided to function definition.')
    fn = LispFunction(params, body, env, name)
    if name is not None:
        env[name] = fn
    return fn