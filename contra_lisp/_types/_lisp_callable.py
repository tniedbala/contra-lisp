from abc import abstractmethod
from typing import Callable, Protocol
from ._lisp_expression import LispExpression
from .lisp_symbol import LispSymbol
from .util import resolve_type


class LispCallable(LispExpression):
    '''Base callable type.'''

    __lisp_type__ = 'callable'

    def __init__(self, *args, **kwargs):
        self.name = self.__lisp_type__

    @property
    def symbol(self) -> LispSymbol:
        symbol = LispSymbol(self.name)
        return symbol

    @abstractmethod
    def __call__(self, *args:LispExpression, env:'Env') -> LispExpression:
        pass
    
    def __lisp_repr__(self) -> str:
        name = f'::{self.name}' if self.name != self.__lisp_type__ else ''
        return f'<{self.__lisp_type__}{name}>'



class DecoratorCallbackFunction(Protocol):

    def __call__(self:LispCallable, *args:LispExpression, env:'Env') -> LispExpression:
        pass



def lisp_callable(name:str, type:type, constant=True) -> Callable[[Callable], type]:

    def decorator(fn:DecoratorCallbackFunction) -> type:

        class CallableSubclass(type):

            def __init__(self, *args, **kwargs):
                super().__init__(self, *args, **kwargs)
                self.name = name
                self.__lisp_constant__ = constant

            def __call__(self, *args:LispExpression, env:'Env') -> LispExpression:
                return resolve_type(fn(self, *args, env=env))
            
        CallableSubclass.__name__ = fn.__name__
        CallableSubclass.__qualname__ = fn.__qualname__
        CallableSubclass.__doc__ = fn.__doc__
        
        return CallableSubclass
    
    return decorator