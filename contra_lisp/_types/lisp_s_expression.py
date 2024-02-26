from ._lisp_callable import LispCallable
from .lisp_list import LispList


class LispSExpression(LispList, LispCallable):
    '''Callable s-expression.'''

    __lisp_type__ = 's-expression'

    def _wrap_str(self, body:str) -> str:
        return f'({body})'

