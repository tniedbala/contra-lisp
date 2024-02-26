from typing import Any, List
from ._lisp_expression import LispExpression
from ._lisp_collection import LispCollection
from .lisp_nil import LispNil


class LispList(list, LispCollection):
    '''List type.'''

    __lisp_type__ = 'list'

    def __init__(self, *args):
        list.__init__(self)
        LispCollection.__init__(self)
        for arg in args:
            self += arg
    
    @property
    def __lisp_py_value__(self) -> List[Any]:
        return [expr.__lisp_py_value__ for expr in self]
    
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
        return f'[{body}]'
    
    def __iadd__(self, expression:LispExpression) -> 'LispList':
        '''Append expression to list (referencing list as ast parent).'''
        expression.__lisp_ast_parent__ = self
        self.append(expression)
        return self
    
    def first(self) -> LispExpression:
        if len(self) == 0:
            return LispNil()
        return self[0]
    
    def rest(self) -> 'LispList':
        if len(self) <= 1:
            return LispList()
        return LispList(*self[1:])
    
    def last(self) -> LispExpression:
        if len(self) == 0:
            return LispNil()
        return self[-1]
    
