import re
from typing import ClassVar, List
from dataclasses import dataclass, field
from .token import Token, Comment, MultilineComment
from .grammar import Grammar


@dataclass(init=False, repr=False)
class Lexer:

    grammar: ClassVar[Grammar] = Grammar()
    '''Reader Grammar object.'''

    source: str = None
    '''String input.'''

    lines: List[str] = field(default_factory=list)
    '''String input, split into a list of lines.'''

    index: int = -1
    '''Index of current line.'''

    tokens: List[Token] = None
    '''List of tokens extracted from source code.'''
    
    @property
    def line_number(self) -> int:
        return self.index + 1

    @property
    def EOF(self) -> bool:
        return self.line_number >= len(self.lines)
    
    @property
    def current_line(self) -> str:
        return self.lines[self.index]
    
    def next_line(self) -> str:
        '''Increment line index and return the new current line.'''
        if self.EOF: raise EOFError()
        self.index += 1
        line = self.current_line
        return line
    
    def tokenize(self, source:str) -> List[Token]:
        self.source = source
        self.lines = source.splitlines()
        self.tokens = []
        self.index = -1
        while not self.EOF:
            self.tokens += self.read_tokens()
        return self.tokens

    def read_tokens(self) -> List[Token]:
        tokens = []
        line = self.next_line()
        prev_match = None
        for match in self.grammar.split(line):
            source = match.group(0)
            if self.grammar.skip(source):
                prev_match = match
                continue
            elif self.grammar.is_comment(source):
                tokens.append(self.read_comment(match))
                break
            elif prev_match and prev_match.end() != match.start():
                col = prev_match.end()
                pointer = (col * " ") + '^'
                raise SyntaxError(f'Invalid character at line {self.line_number}, column {col}:\n{line}\n{pointer}')
            else:
                tokens.append(Token(
                    source = source,
                    line = self.line_number,
                    start = match.start(),
                    end = match.end(),
                ))
                prev_match = match
        return tokens
    
    def read_comment(self, match:re.Match) -> Comment:
        source = match.group(0)
        if self.grammar.is_singleline_comment(source):
            return self.read_singleline_comment(match)
        return self.read_multiline_comment(match)

    def read_singleline_comment(self, match:re.Match) -> Comment:
        line = self.current_line
        start = match.start()
        return Comment(
            source = line[start:],
            line = self.line_number,
            start = start,
            end = len(line) - 1,
        )
    
    # TODO: implement multiline comments
    def read_multiline_comment(self, match:re.Match) -> MultilineComment:
        raise NotImplemented()

