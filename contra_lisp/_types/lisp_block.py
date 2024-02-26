from ._lisp_callable import LispCallable
from .lisp_list import LispList


class LispBlock(LispList, LispCallable):
    '''Callable block of expressions to be executed sequentially. Returns `nil` unless explicit
    call to `(return)` is provided.'''

    __lisp_type__ = 'block'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__lisp_env__ = None
        '''Env containing bound variables; intended for blocks returned from functions/macros.'''

    def _wrap_str(self, body:str) -> str:
        return f'{{ {body} }}'
    
