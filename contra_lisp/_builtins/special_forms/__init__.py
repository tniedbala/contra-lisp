from ._break import Break
from ._continue import Continue
from ._eval import Eval
from .fn import Fn
from ._import import Import
from ._return import Return
from ._set import Set

SPECIAL_FORMS = [
    Break, Continue, Fn, Import, Return, Set, Eval,
]