from ..env import Env
from .functions import BUILTIN_FUNCTIONS
from .special_forms import SPECIAL_FORMS


def default_env():
    functions = [fn() for fn in BUILTIN_FUNCTIONS]
    special_forms = [form() for form in SPECIAL_FORMS]
    return Env({
        **{fn.symbol: fn for fn in functions},
        **{form.symbol: form for form in special_forms},
    })