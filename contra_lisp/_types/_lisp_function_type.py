from ._lisp_callable import LispCallable


class LispFunctionType(LispCallable):
    '''Base class for lisp function types, which have args evaluated prior to binding to parameters.'''

    __lisp_name__ = 'function-type'

