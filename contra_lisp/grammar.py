import re
from typing import List
from dataclasses import dataclass

# skip whitespace & commas
SKIPCHARS = r'[\s,]+'

# comments
SINGLELINE_COMMENT = r'#'
MULTILINE_COMMENT = r'^###\B'

# parens, square & curly braces
BRACE = r'\{{1,2}|\}{1,2}|[)(]|\[|\]'

# symbols containing special characters, reserved for builtin objects
RESERVED_CHAR = r'\.\.\.|[@:+=*/%^<>!&|~`?\-]+'
SYMBOL = r'[a-zA-Z_]+[a-zA-Z0-9_-]*\??'

# keywords
KEYWORD = f'@{SYMBOL}'

# dotref - dot operator for referencing object members
OBJECT_KEY = r'[a-zA-Z_-]+[a-zA-Z0-9_-]*\??'
DOTREF = f'(?:{OBJECT_KEY}|@)\\.{OBJECT_KEY}(?:\\.{OBJECT_KEY})*'

# strings
DOUBLE_QUOTE_STR = r'"(?:\\.|[^\\"])*"'
SINGLE_QUOTE_STR = r"'(?:\\.|[^\\'])*'"

# numeric
NUMBER = r'-?(?:\d*\.?\d+|\d+\.\d*)'

# composite tokenizing pattern
# TODO: add multiline comments
TOKEN = \
    f'({SKIPCHARS}|{MULTILINE_COMMENT}|{SINGLELINE_COMMENT}' \
    f'|{BRACE}|{NUMBER}|{DOTREF}|{SYMBOL}|{KEYWORD}|{RESERVED_CHAR}' \
    f'|{DOUBLE_QUOTE_STR}|{SINGLE_QUOTE_STR})'


@dataclass(repr=False, init=False)
class Grammar:
    SKIPCHARS           = re.compile(SKIPCHARS)
    SINGLELINE_COMMENT  = re.compile(SINGLELINE_COMMENT)
    MULTILINE_COMMENT   = re.compile(MULTILINE_COMMENT)
    BRACE               = re.compile(BRACE)
    RESERVED_CHAR       = re.compile(RESERVED_CHAR)
    OBJECT_KEY          = re.compile(OBJECT_KEY)
    SYMBOL              = re.compile(SYMBOL)
    KEYWORD             = re.compile(KEYWORD)
    DOTREF              = re.compile(DOTREF)
    DOUBLE_QUOTE_STR    = re.compile(DOUBLE_QUOTE_STR)
    SINGLE_QUOTE_STR    = re.compile(SINGLE_QUOTE_STR)
    NUMBER              = re.compile(NUMBER)
    TOKEN               = re.compile(TOKEN)

    def skip(self, source:str) -> bool:
        return bool(self.SKIPCHARS.match(source))
    
    def is_comment(self, source:str) -> bool:
        return self.is_singleline_comment(source) | self.is_multiline_comment(source)

    def is_singleline_comment(self, source:str) -> bool:
        return bool(self.SINGLELINE_COMMENT.match(source))

    def is_multiline_comment(self, source:str) -> bool:
        return bool(self.MULTILINE_COMMENT.match(source))

    def is_brace(self, source:str) -> bool:
        return bool(self.BRACE.match(source))
    
    def is_symbolic(self, source:str) -> bool:
        return self.is_reserved_char(source) | self.is_symbol(source) | self.is_keyword(source) | self.is_dotref(source)

    def is_reserved_char(self, source:str) -> bool:
        return bool(self.RESERVED_CHAR.match(source))

    def is_symbol(self, source:str) -> bool:
        return bool(self.SYMBOL.match(source))

    def is_keyword(self, source:str) -> bool:
        return bool(self.KEYWORD.match(source))

    def is_dotref(self, source:str) -> bool:
        return bool(self.DOTREF.match(source))
    
    def is_object_key(self, source:str) -> bool:
        return bool(self.OBJECT_KEY.match(source))

    def is_number(self, source:str) -> bool:
        return bool(self.NUMBER.match(source))
    
    def is_string(self, source:str) -> bool:
        return self.is_single_quote_str(source) | self.is_double_quote_str(source)

    def is_single_quote_str(self, source:str) -> bool:
        return bool(self.SINGLE_QUOTE_STR.match(source))

    def is_double_quote_str(self, source:str) -> bool:
        return bool(self.DOUBLE_QUOTE_STR.match(source))

    def is_token(self, source:str) -> bool:
        return bool(self.TOKEN.match(source))
    
    def split(self, source:str) -> List[re.Match]:
        return list(self.TOKEN.finditer(source))


WS = r'[\s,]'
SPECIAL_CHARS = r'[@:+=*/%^<>!&|~`?\-]+'
SYMBOL = r'[a-zA-Z_-]+[a-zA-Z0-9_-]*\??'