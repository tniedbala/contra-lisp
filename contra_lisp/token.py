from dataclasses import dataclass


@dataclass
class Token:
    '''Container for tokenized input text.'''

    source: str
    '''String input.'''

    line: int
    '''Line number (1-indexed).'''

    start: int
    '''Start column (0-indexed)'''

    end: int
    '''End column (0-indexed)'''

    def __str__(self) -> str:
        return self.source
    


class Comment(Token):
    '''Container for tokenized comments.'''
    pass



@dataclass
class MultilineComment(Comment):
    '''Container for tokenized multiline comments.'''

    source: str
    '''String input.'''

    line: int
    '''Starting line number of multiline comment.'''

    start: int
    '''Start column (0-indexed) of first line of multiline comment.'''

    end: int
    '''End column (0-indexed) of first line of multiline comment.'''

    start_token: Token = None
    '''Starting token of multiline  comment.'''

    end_token: Token = None
    '''Ending token of multiline comment.'''
