from ...env import Env
from ...exceptions import ReturnStatement
from ..._types import special_form, resolve_type, LispExpression

# TODO:
# return statement should return value from the current function scope, not just block scope
# (function could have many nested blocks). Need to look into a way to keep track of execution context
@special_form('return')
def Return(self, *args:LispExpression, env:Env) -> LispExpression:
    if len(args) > 1:
        raise SyntaxError(f'Only a single value may be passed to {self.name} statement.')
    return_value = resolve_type(args[0])
    raise ReturnStatement(value=return_value, expression=self)
