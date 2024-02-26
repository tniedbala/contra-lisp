from .lisp_string import LispString
from ..token import Comment


class LispComment(LispString):

    __lisp_type__ = 'comment'


        