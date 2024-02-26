from ..token import Token
from ._lisp_expression import LispExpression


class LispCollection(LispExpression):
    '''Base collection type.'''

    __lisp_type__ = 'collection'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.__lisp_start_token__: Token = None
        '''Token of collection starting character.'''

        self.__lisp_end_token__: Token = None
        '''Token of collection ending character'''

    def __repr__(self) -> str:
        body = ', '.join([expr.__repr__() for expr in self])
        return f'{type(self).__name__}({body})'

    def __str__(self) -> str:
        body = ', '.join([str(expr) for expr in self])
        return f'{type(self).__name__}({body})'

    def __lisp_repr__(self) -> str:
        body = ' '.join([expr.__lisp_repr__() for expr in self])
        return self._wrap_str(body)

    def __lisp_str__(self) -> str:
        body = ' '.join([expr.__lisp_str__() for expr in self])
        return self._wrap_str(body)

    def _wrap_str(self, body:str) -> str:
        return f'{self.__lisp_type__}({body})'


