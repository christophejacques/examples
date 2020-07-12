#from msvcrt import getch
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


def fib(n):
    return 1 if n<= 2 else fib(n-1) + fib(n-2)


print("Fibonacci : ", end="")
for n in range(1, 5):
    print(fib(n), end=" ")

print()

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