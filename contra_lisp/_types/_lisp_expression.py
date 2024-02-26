from abc import abstractmethod
from typing import Any


class LispExpression:
    '''Language base object type.'''
    
    __lisp_type__ = 'expression'

    def __init__(self, *args, **kwargs):

        self.__lisp_ast_parent__: LispExpression = None
        '''Parent lisp expression in abstract syntax tree.'''

        self.__lisp_constant__: bool = False
        '''Used to indicate whether object should be treated as a constant.'''

    @property
    @abstractmethod
    def __lisp_py_value__(self) -> Any:
        '''Returns native python object represented by lisp type.'''
        pass

    @property
    def __lisp_ast_root__(self) -> 'LispExpression':
        '''Root lisp expression in abstract syntax tree.'''
        if self.__lisp_ast_parent__ is not None:
            return self.__lisp_ast_parent__.__lisp_ast_root__
        return self
    
    def __repr__(self) -> str:
        return f'{type(self).__name__}()'
    
    def __str__(self) -> str:
        return str(self.__lisp_py_value__)
    
    def __lisp_repr__(self) -> str:
        return f'<{self.__lisp_type__}>'
    
    def __lisp_str__(self) -> str:
        return str(self)