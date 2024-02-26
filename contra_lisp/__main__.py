from argparse import ArgumentParser
from .interpreter import Interpreter

parser = ArgumentParser(
    prog = 'Lisp Interpreter',
)

if __name__ == '__main__':
    interpreter = Interpreter()
    interpreter.repl()