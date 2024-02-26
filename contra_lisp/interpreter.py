from typing import ClassVar, List
from dataclasses import dataclass, field
from .token import Token
from .reader import Reader
from .env import Env
from ._types import *
from ._builtins import default_env
from .exceptions import LispException, BreakStatement, ContinueStatement, ReturnStatement



@dataclass(repr=False, init=False)
class Interpreter:

    reader: ClassVar[Reader] = Reader()

    env: Env = None
    '''Interpreter global environment.'''

    output: LispExpression = None

    def __init__(self):
        self.env = default_env()
        self.env['eval'].eval = self.eval

    @property
    def source(self) -> str:
        return self.reader.source
    
    @property
    def tokens(self) -> List[Token]:
        return self.reader.tokens

    @property
    def block(self) -> LispBlock:
        return self.reader.block

    def read(self, source:str) -> LispProgram:
        block = self.reader.read(source)
        block.__class__ = LispProgram
        return block
        
    def eval_dotref(self, dotref:LispDotRef, env:Env) -> LispExpression:
        keys = str(dotref).split('.')
        obj = env
        for key in keys:
            if type(obj) in [Env, LispObject]:
                obj = obj[key]
            else:
                obj = resolve_type(getattr(obj.__lisp_py_value__, key))
        return obj
    
    def eval_s_expression(self, expression:LispSExpression, env:Env):
        fn = self.eval(expression.first(), env)
        args = expression.rest()
        if isinstance(fn, LispFunctionType) or isinstance(fn, PythonObject):
            args = [self.eval(arg, env) for arg in args]
        return fn(*args, env=env)
    
    def eval_program(self, block:LispProgram, env:Env) -> LispExpression:
        env = block.__lisp_env__ or env
        _ = [self.eval(subexpression, env) for subexpression in block[:-1]]
        return self.eval(block.last(), env)
    
    def eval_block(self, block:LispBlock, env:Env) -> LispNil | LispObject | LispBlock:
        '''Return object if block contains object definition; otherwise eval each expression sequentially, 
        returning the final expression if '''
        env = block.__lisp_env__ or env
        if isinstance(block, LispProgram):
            return self.eval_program(block, env)
        if len(block) > 1 and block[1] == LispSymbol(':'):
            return LispObject(block, env)
        try:
            _ = [self.eval(subexpression, env) for subexpression in block[:-1]]
            result = self.eval(block.last(), env)
            if isinstance(result, LispBlock):
                return result
            return LispNil()
        except ReturnStatement as return_statement:
            return return_statement.value
        except BreakStatement:
            return LispNil()
        except ContinueStatement:
            return LispNil()

    def eval(self, expression:LispExpression, env:Env) -> LispExpression:
        while type(expression) in [LispProgram, LispBlock, LispSExpression]:
            if isinstance(expression, LispBlock):
                expression = self.eval_block(expression, env)
                continue
            elif isinstance(expression, LispSExpression):
                expression = self.eval_s_expression(expression, env)
                continue
        if type(expression) == LispKeyword:
            return expression
        elif type(expression) == LispDotRef:
            return self.eval_dotref(expression, env)
        elif type(expression) == LispSymbol:
            return env[expression]
        return expression

    def print(self, expression:LispExpression):
        print(expression.__lisp_repr__(), flush=True)

    def execute(self, source:str):
        block = self.read(source)
        self.output = self.eval(block, self.env)
        self.print(self.output)

    def repl(self):
        while True:
            try:
                source = input(' > ')
                if source.strip() == '.quit': return
                self.execute(source)
            except EOFError:
                print('\n', flush=True)
                return
            except LispException as error:
                print(f'\n{error}\n', flush=True)
            except Exception as error:
                raise