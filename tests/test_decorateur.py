from functools import wraps, partial
from datetime import datetime


TIMEFORMAT = "%Y-%m-%d %H:%M:%S.%f"


def log(level, *args, **kwargs):
    date_heure = str(datetime.now().strftime(TIMEFORMAT))[:23]
    print(f"{date_heure} | {level.upper():8} |", 
        *args, **kwargs, flush=True)


class Print:
    debug = False
        
    @classmethod
    def dprint(cls, *args, **kwargs):
        if Print.debug:
            log("debug", *args, **kwargs)

    @classmethod
    def print(cls, *args, **kwargs):
        for kwarg in kwargs.copy():
            if kwarg in ("success", "info", "warn", "error"):
                kwargs.pop(kwarg)
                log(kwarg, *args, **kwargs)
                return


fprint = Print.dprint
success = partial(Print.print, success=True)
info = partial(Print.print, info=True)
warn = partial(Print.print, warn=True)
error = partial(Print.print, error=True)


def debug(*argsp, **kwargsp):

    def fonction(fonction):
        @wraps(fonction)
        def params(*args, **kwargs):
            ddebug = Print.debug
            if argsp:
                Print.debug = argsp[0]
            elif "print" in kwargsp:
                Print.debug = kwargsp.get("print")
            else:
                Print.debug = True

            try:
                res = fonction(*args, **kwargs)
            finally:
                Print.debug = ddebug

            return res
        return params
    return fonction


def test(valeur=0):
    fprint(f"Hello test({valeur})", )


def test1():
    test(1)


@debug(print=True)
def test2():
    test(2)


@debug(False)
def test3():
    test(3)


@debug()
def test4():
    test(4)
    1 / 0


def main():
    info("Debut")
    for fonction in (test1, test2, test3, test4):
        info(f"BEGIN {fonction.__name__}()")
        try:
            fonction()

        except Exception as erreur:
            error(erreur)
            error(f"END {fonction.__name__}")
        else:
            success(f"END {fonction.__name__}")

    info("Fin")


if __name__ == '__main__':
    main()
