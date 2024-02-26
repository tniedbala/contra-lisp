from typing import Any
from ._lisp_expression import LispExpression
from ._lisp_callable import LispCallable
from .util import resolve_type


class PythonObject(LispCallable):

    __lisp_type__ = 'python-object'

    def __init__(self, value:Any):
        super().__init__(self)
        if isinstance(value, LispExpression):
            self._value = value.__lisp_py_value__
        else:
            self._value = value
        self.resolve_name()

    def __call__(self, *args:LispExpression, env:'Env') -> LispExpression:
        python_object = self.__lisp_py_value__
        args = [arg.__lisp_py_value__ for arg in args]
        return resolve_type(python_object(*args))

    @property
    def __lisp_py_value__(self) -> Any:
        return self._value
    
    def resolve_name(self) -> str:
        obj = self.__lisp_py_value__
        name = obj.__name__ if hasattr(obj, '__name__') else type(obj).__name__
        module_name = obj.__module__ if hasattr(obj, '__module__') else type(obj).__module__
        self.name = f'{module_name}.{name}' if module_name != '' else name