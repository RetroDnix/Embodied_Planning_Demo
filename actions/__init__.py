from actions import store, base, utils

def get_functions(module, prefix='actions.') -> list:
    functions = []
    for name in dir(module):
        try:
            f = getattr(module, name)
            if callable(f) and f.__module__.startswith(prefix):
                functions.append(f)
        except:
            pass
    return functions


ACTION_DICT = {
    "base": get_functions(base),
    "store": get_functions(store)
}

Fuction = {
    "utils" : utils
}

