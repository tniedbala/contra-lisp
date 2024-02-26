from ._lisp_callable import LispCallable


class LispMacroType(LispCallable):
    '''Base class for lisp special forms & macros, whose args are not evaluated prior to binding to parameters.'''

    __lisp_name__ = 'macro-type'
