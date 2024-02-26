from numbers import Number
from ._lisp_expression import LispExpression
from .lisp_list import LispList
from .lisp_nil import LispNil
from .lisp_bool import LispBool 
from .lisp_number import LispNumber
from .lisp_string import LispString

def resolve_type(value:object) -> LispExpression:
    from .python_object import PythonObject
    if isinstance(value, LispExpression):
        return value
    elif value is None:
        return LispNil()
    elif isinstance(value, bool):
        return LispBool(value)
    elif isinstance(value, Number):
        return LispNumber(value)
    elif isinstance(value, str):
        return LispString(value)
    elif isinstance(value, list):
        return LispList(*[resolve_type(x) for x in value])
    else:
        return PythonObject(value)