import builtins

screen: list[str] = list()

def printf(*args, **kwargs):
    # print(*args, **kwargs, flush=True)
    ligne: str = "".join(map(str, args))
    screen.append(f"{ligne}")

def fabs():
    printf("  abs(5) ==", abs(5))
    printf("  abs(-5) ==", abs(-5))

def fall():
    if all([True, False]):
        printf("  Tout est True")
    else:
        printf("  au moins un est Faux")

def fany():
    if any([True, False]):
        printf("  Au moins un est True")
    else:
        printf("  Tout est Faux")

def fascii():
    printf("  ascii('\\u0012') ==", ascii("\u0012"))

def faiter(): ...
def fanext(): ...
def fbreakpoint(): ...
def fbytearray(): ...
    
def fbin():
    printf("  bin(12)=", bin(12))

def fbool():
    printf("  bool(12)=", bool(12))

def fbytes():
    printf("  bytes(4)=", bytes(4))

def fcallable():
    if callable(fcallable):
        printf("  fcallable est callable")

def fchr():
    printf("  chr(65)=", chr(65))

def fclassmethod(): ...
def fcompile(): ...

def fcomplex():
    c1 = complex(1, 2)
    c2 = complex(3, 4)
    printf(f"  {c1}+{c2}=", c1+c2)

def fcopyright(): ...
def fcredits(): ...
def fdelattr(): ...
def fdict(): ...
def fdir(): ...
def fdivmod(): 
    printf("  divmod(15, 2)=", divmod(15, 2))
def fenumerate(): ...
def feval(): 
    printf("  eval('2+3-1/2')=", eval('2+3-1/2'))
def fexec(): ...
def fexit(): ...
def ffilter(): 
    printf("  filter(nombrepair, [1, 2, 3, 4])=", list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4])))
def ffloat(): 
    printf("  float('5.25') = ", float("5.25"))
def fformat(): ...
def ffrozenset(): ...
def fgetattr(): ...
def fglobals(): ...
def fhasattr(): ...
def fhash(): 
    printf("  hash('azerty')=", hash("azerty"))
def fhelp(): ...
def fhex(): ...
def fid(): ...
def finput(): ...
def fint():
    printf("  int('5') = ", int("5"))
def fisinstance(): 
    printf("  isinstance(5, int)=", isinstance(5, int))
    printf("  isinstance(5.5, int)=", isinstance(5.5, int))
def fissubclass(): ...
def fiter(): ...

# help(copyright)

def main():
    for fonction in sorted(dir(builtins)):
        if all([fonction[0] in "azertyuiopmlkjhgfdsqwxcvbn"]):
            printf(f"{fonction}:")
            try:
                eval("f"+fonction)()
            except Exception:
                pass

main()

for ligne in screen:
    print(ligne)
