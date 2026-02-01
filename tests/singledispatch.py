from datetime import datetime as dt
from functools import singledispatch


@singledispatch
def to_string(obj):
    # raise NotImplementedError(f"function to_string of type {obj.__class__.__name__} is not implemented.")
    return (f"=> function to_string of type {obj.__class__.__name__} is not implemented.")

@to_string.register
def _(i: int):
    return f"integer: {i}"

@to_string.register
def _(f: float):
    return f"float: {f:_.2f}"

@to_string.register
def _(l: list):
    if len(l) > 3:
        msg = f"list:({len(l)}) ["
        for x in l[:3]:
            msg += str(x) + ", "
        msg += "...]"
        return msg
    else:
        return f"list:({len(l)}) {l}"

@to_string.register
def _(d: dt):
    return f"datetime: {(d).isoformat()}"

@to_string.register
def _(s: set):
    return f"set:({len(s)}) {s}"

@to_string.register
def _(s: str):
    return f"string:({len(s)}) {s}"

class User: ...

print(to_string(12))
print(to_string(12.00))
print(to_string(dt.now() ))
print(to_string([1, 2, 3]))
print(to_string([1, 2, 3, 4, 5]))
print(to_string({1, 3, 3, 4, 5}))
print(to_string("chaine de caratères"))
print(to_string(User()))
