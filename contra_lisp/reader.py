from typing import ClassVar, List
from dataclasses import dataclass, field
from .grammar import Grammar
from .token import Token, Comment
from .lexer import Lexer
from ._types import *


@dataclass(init=False, repr=False)
class Reader:

    lexer: ClassVar[Lexer] = Lexer()
    '''Language lexer.'''

    block: LispBlock = None
    '''Root lisp block parsed from source code'''

    index: int = -1
    '''Current token index.'''

    @property
    def grammar(self) -> Grammar:
        return self.lexer.grammar

    @property
    def source(self) -> str:
        return self.lexer.source
    
    @property
    def tokens(self) -> List[Token]:
        return self.lexer.tokens

    @property
    def current_token(self) -> Token:
        return self.tokens[self.index]

    @property
    def EOF(self) -> bool:
        return self.index >= len(self.tokens) - 1
    
    def next_token(self) -> Token:
        if self.EOF: raise EOFError()
        self.index += 1
        return self.current_token

    def tokenize(self, source:str) -> List[Token]:
        return self.lexer.tokenize(source)
    
    def read(self, source:str) -> LispBlock:
        self.lexer.tokenize(source)
        self.index = -1
        self.block = LispBlock()
        while not self.EOF:
            token = self.next_token()
            self.block += self.read_form(token)
        return self.block

    def read_form(self, token:Token) -> LispExpression:
        match token.source:
            case '[':
                return self.read_collection(LispList, end=']')
            case '(':
                return self.read_collection(LispSExpression, end=')')
            case '{':
                return self.read_collection(LispBlock, end='}')
            case _:
                return self.read_scalar()

    def read_scalar(self):
        token = self.current_token
        source = token.source
        grammar = self.grammar
        expression: LispExpression = None
        if isinstance(token, Comment):
            expression = LispComment(str(token))
        elif token.source == 'nil':
            expression = LispNil()
        elif source in ['true','false']:
            expression = LispBool(str(token)=='true')
        elif grammar.is_number(source):
            expression = LispNumber(token.source)
        elif grammar.is_single_quote_str(source):
            expression = LispString(str(token).strip("'"))
        elif grammar.is_double_quote_str(source):
            expression = LispString(str(token).strip('"'))
        elif grammar.is_keyword(source):
            expression = LispKeyword(str(token))
        elif grammar.is_dotref(source):
            expression = LispDotRef(str(token))
        elif grammar.is_reserved_char(source) | grammar.is_symbol(source):
            expression = LispSymbol(str(token))
        else:
            raise SyntaxError(f'Unrecognized input at line {token.line}, column {token.start}: "{token}"')
        expression.__lisp_token__ = token
        return expression
        
    def read_collection(self, collection_type:type, end:str) -> LispCollection:
        collection = collection_type()
        start_token = self.current_token
        while (token := self.next_token()) and (not self.EOF) and (token.source != end):
            collection += self.read_form(token)
            if self.EOF:
                raise EOFError(f'Expected matching "{end}".')
        collection.__lisp_start_token__ = start_token
        collection.__lisp_end_token__ = token
        return collection
