from ..token import Token
from ._lisp_expression import LispExpression


class LispScalar(LispExpression):
    '''Base scalar type.'''

    __lisp_type__ = 'scalar'
    
    def __init__(self, token=None):
        super().__init__(self)
        self.__lisp_token__: Token = token
        '''Token referencing object underlying source code.'''

