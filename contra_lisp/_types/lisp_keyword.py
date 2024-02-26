from ..token import Token
from .lisp_symbol import LispSymbol


class LispKeyword(LispSymbol):

    __lisp_type__ = 'keyword'
