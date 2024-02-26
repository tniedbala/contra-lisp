from ...env import Env
from ...exceptions import ContinueStatement
from ..._types import special_form, resolve_type, LispExpression

@special_form('continue')
def Continue(self, *args:LispExpression, env:Env) -> LispExpression:
    if len(args) > 0:
        raise SyntaxError(f'{self.name} statement may not include arguments.')
    raise ContinueStatement(expression=self)