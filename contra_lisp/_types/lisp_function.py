import itertools
from ._lisp_expression import LispExpression
from ._lisp_function_type import LispFunctionType
from .lisp_list import LispList
from .lisp_symbol import LispSymbol
from .lisp_nil import LispNil


# TODO: allow for specifying variadic and/or keyword args
class LispFunction(LispFunctionType):

    __lisp_type__ = 'function'
    
    def __init__(self, params:LispList, body:LispExpression, env:'Env', name:LispSymbol=None):
        self.__lisp_env__ = env
        self.validate(params, body, name)
        self.name = str(name) if name else self.__lisp_type__
        self.params = params
        self.body = body

    def __call__(self, *args:LispExpression, env:'Env') -> LispExpression:
        call_env = self.bind_env(*args)
        return call_env.eval(self.body)

    def bind_env(self, *args:LispExpression) -> 'Env':
        from ..env import Env
        if len(args) > len(self.params):
            raise ValueError(f'Incorrect number of positional arguments passed to {self.name}')
        call_env = Env(parent=self.__lisp_env__)
        for param, value in itertools.zip_longest(self.params, args):
            value = value or LispNil()
            call_env[param] = value
        return call_env

    def validate(self, params:LispList, body:LispExpression, name:LispSymbol=None):
        if name and type(name) != LispSymbol:
            raise SyntaxError(f'Function name must be a symbol; got <{name.__lisp_type__}>: "{name}"')
        if not type(params) == LispList:
            raise SyntaxError(f'Function parameters must be passed as list; got <{params.__lisp_type__}>.')
        for param in params:
            if not isinstance(param, LispSymbol):
                raise SyntaxError(f'Function parameters expected symbol; got <{param.__lisp_type__}>: "{param}".')
