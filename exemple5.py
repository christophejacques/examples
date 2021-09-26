from msvcrt import getch
import inspect

# Decorateur
def checkParams(fonction):

    def getParams(*p, **k):
        res = fonction(*p)
        print("Call {}{} = {}".format(fonction.__name__, p, res))
        return res

    return getParams

def addition(a, b):
    return a + b


class ClassePrincipale:
    variable = 0
    
    def __init__(self, attr):
        self.attribut = attr
        
    @checkParams
    def methode(self, p=0):
        ClassePrincipale.variable += 1
        print("methode(self) = {}".format(ClassePrincipale.variable))
        return p
        
    def printHeritageAttribut(self):
        print(self.sousAttribut)
    

class SousClasse(ClassePrincipale):
    @checkParams
    def __init__(self, attr, sousAttribut):
        ClassePrincipale.__init__(self, attr)
        self.sousAttribut = sousAttribut
        
    def sousMethode(self):
        print("sousMethode(self)")


def format_int(entier : int) -> str:
    lst_entier = str(entier)[::-1]
    res = ""
    for i, c in enumerate(lst_entier):
        if i>0 and i % 3 == 0: res = "_" + res
        res = c + res
    return res


class Fibonnacci:
    __data = {}

    @staticmethod
    def add(number, value):
        Fibonnacci.__data[number] = value

    @staticmethod
    def get(number):
        return Fibonnacci.__data.get(number)


def fib(n):
    if n <= 2:
        fib_n = Fibonnacci.get(n)
        if not fib_n: Fibonnacci.add(n, 1)
        return 1
    else:
        fib_n_1 = Fibonnacci.get(n-1)
        if not fib_n_1: 
            fib_n_1 = fib(n-1)
            Fibonnacci.add(n-1, fib_n_1)

        fib_n_2 = Fibonnacci.get(n-2)
        if not fib_n_2: 
            fib_n_2 = fib(n-2)
            Fibonnacci.add(n-2, fib_n_2)

    return fib_n_1 + fib_n_2


print("Fibonacci : ")
print(format_int(fib(40)))
for n in range(1, 34):
    print(format_int(fib(n)))

print()
exit()

def printdef(cls):
    
    for propriete in filter(lambda x:x.startswith("isf"), dir(inspect)):
        liste = inspect.getmembers(cls, getattr(inspect, propriete))
        
        if len(liste) > 0:
            print(f"\nEléments *{propriete}* de : ", cls.__name__)
            for m in liste:
                print("-", f"{m[0]:25}:", type(m[1]))



try:
    printdef(ClassePrincipale)
    print()
    C = ClassePrincipale("attr")
    C.methode(5)

    print()
    ssC = SousClasse("attr", "ssAttr")
    ssC.methode()
    # ssC.printHeritageAttribut()
    

except Exception as e:
    print(e)

#getch()