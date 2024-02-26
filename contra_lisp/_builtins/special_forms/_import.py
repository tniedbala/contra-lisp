import pkgutil
import builtins
from ...env import Env
from ..._types import special_form, LispExpression, LispBlock, LispSymbol, LispObject, LispDotRef, LispNil, PythonObject


def resolve_name(name:str) -> object:
    if hasattr(builtins, name):
        return getattr(builtins, name)
    return pkgutil.resolve_name(name)

# TODO:
# review how nested imports should be assigned to names
@special_form('import')
def Import(self, *args:LispExpression, env:Env) -> LispNil:
    for arg in args:
        if type(arg) is LispSymbol:
            env[arg] = PythonObject(resolve_name(str(arg)))
        elif type(arg) is LispDotRef:
            keys = str(arg).split('.')
            env[keys[-1]] = resolve_name(str(arg))
        elif type(arg) is LispBlock:
            LispObject.validate_block(arg)
            for i in range(0, len(arg), 3):
                key = arg[i]
                name = arg[i+2]
                if (type(key) != LispSymbol) or (type(name) not in [LispSymbol, LispDotRef]):
                    raise SyntaxError('Python import must map <symbol> to <symbol>.')
                env[key] = resolve_name(str(name))
                
