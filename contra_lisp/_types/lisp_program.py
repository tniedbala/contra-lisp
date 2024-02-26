from .lisp_block import LispBlock


class LispProgram(LispBlock):
    '''Root block object to be executed by the interpreter. Unlike standard blocks
    which return `nil` by default, this will return the result of the final expression
    within the block.'''

    __lisp_type__ = 'lisp-program'

    