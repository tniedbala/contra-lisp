from typing import Any
from .token import Token


class LispException(Exception):

    def __init__(self, expression=None):
        self.expression = expression

    def __str__(self) -> str:
        source_location = f'\nSource: {self.source_location}' if self.token is not None else ''
        return self.message + source_location
    
    @property
    def message(self) -> str:
        return self.args[1] if len(self.args) > 1 else type(self.__name__)
    
    @property
    def token(self) -> Token:
        from ._types import LispCollection, LispScalar
        if isinstance(self.expression, Token):
            return self.expression
        elif isinstance(self.expression, LispScalar):
            return self.expression.__lisp_token__
        elif isinstance(self.expression, LispCollection):
            return self.expression.__lisp_start_token__

    @property
    def source_location(self) -> str:
        token = self.token
        if self.token is not None:
            return f'line {token.line}, column {token.start}: "{token.source}"'
        

class BreakStatement(LispException):
    
    @property
    def message(self) -> str:
        return 'Error: Break statement may only be called from within a block expression.'


class ContinueStatement(LispException):
    
    @property
    def message(self) -> str:
        return 'Error: Continue statement may only be called from within a block expression.'


class ReturnStatement(LispException):

    def __init__(self, value:Any, expression=None):
        super().__init__(expression)
        self.value = value
    
    @property
    def message(self) -> str:
        return 'Error: Return statement may only be called from within a block expression.'