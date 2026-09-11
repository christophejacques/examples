import builtins


screen: list[str] = list()


def est_vide(func):
    # Fonction de référence vide
    def func_vide(): pass
    def func_vide_doc(): """Docstring"""; pass  # noqa: E702
    
    # Récupération du bytecode
    code = func.__code__.co_code
    
    # Compare avec le bytecode d'une fonction vide (avec ou sans docstring)
    return code == func_vide.__code__.co_code or code == func_vide_doc.__code__.co_code


def printf(*args, **kwargs):
    # print(*args, **kwargs, flush=True)
    ligne: str = "".join(map(str, args))
    if not kwargs.get("fonction", False):
        ligne = f"  {ligne}"
    screen.append(f"{ligne}")


def fabs():
    printf("abs(5) ==", abs(5))
    printf("abs(-5) ==", abs(-5))


def fall():
    if all([True, False]):
        printf("Tout est True")
    else:
        printf("au moins un est Faux")


def fany():
    if any([True, False]):
        printf("Au moins un est True")
    else:
        printf("Tout est Faux")


def fascii():
    printf("ascii('\\u0012') ==", ascii("\u0012"))


def faiter(): ...
def fanext(): ...
def fbreakpoint(): ...
def fbytearray(): ...

    
def fbin():
    printf("bin(12)=", bin(12))


def fbool():
    printf("bool(12)=", bool(12))


def fbytes():
    printf("bytes(4)=", bytes(4))


def fcallable():
    if callable(fcallable):
        printf("  fcallable est callable")


def fchr():
    printf("chr(65)=", chr(65))


def fclassmethod(): ...
def fcompile(): ...


def fcomplex():
    c1 = complex(1, 2)
    c2 = complex(3, 4)
    printf(f"{c1}+{c2}=", c1+c2)


def fcopyright(): ...
def fcredits(): ...
def fdelattr(): ...
def fdict(): ...
def fdir(): ...


def fdivmod(): 
    printf("divmod(15, 2)=", divmod(15, 2))


def fenumerate(): ...
def feval(): 
    printf("eval('2+3-1/2')=", eval('2+3-1/2'))


def fexec(): ...
def fexit(): ...
def ffilter(): 
    printf("filter(nombrepair, [1, 2, 3, 4])=", list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4])))


def ffloat(): 
    printf("float('5.25') = ", float("5.25"))


def fformat(): ...
def ffrozenset(): ...
def fgetattr(): ...
def fglobals(): ...
def fhasattr(): ...
def fhash(): 
    printf("hash('azerty')=", hash("azerty"))


def fhelp(): ...
def fhex(): ...
def fid(): ...
def finput(): ...
def fint():
    printf("int('5') = ", int("5"))


def fisinstance(): 
    printf("isinstance(5, int)=", isinstance(5, int))
    printf("isinstance(5.5, int)=", isinstance(5.5, int))


def fissubclass(): ...
def fiter(): ...
def flen(): ...
def flicense(): ...
def flist(): ...
def flocals(): ...
def fmap(): ...
def fmax(): ...
def fmemoryview(): ...
def fmin(): ...
def fnext(): ...
def fobject(): ...
def foct(): ...
def fopen(): ...
def ford(): ...
def fpow(): ...
def fprint(): ...
def fproperty(): ...
def fquit(): ...
def frange(): ...
def frepr(): ...
def freversed(): ...
def fround(): ...
def fset(): ...
def fsetattr(): ...
def fslice(): ...
def fsorted(): ...
def fstaticmethod(): ...
def fstr(): ...
def fsum(): 
    printf("sum(range(2, 5)) = ", sum(range(2, 5)))


def fsuper(): ...
def ftuple(): ...
def ftype(): ...
def fvars(): ...
def fzip(): ...


def main():
    for fonction in sorted(dir(builtins)):
        if all([fonction[0] in "azertyuiopmlkjhgfdsqwxcvbn"]):

            try:
                if est_vide(eval("f"+fonction)):
                    continue
            except Exception:
                continue

            printf(f"{fonction}:", fonction=True)
            try:
                eval("f"+fonction)()

            except Exception as e:
                printf(e)


main()

for ligne in screen:
    print(ligne)
