from utils.complexe import *
from datetime import datetime

td = datetime.now()


def fdebugger(fonction):

    def methode(*args, **kvargs):
        print(f"Exec fonction : {fonction.__name__}{args}", end='')
        res = fonction(*args, **kvargs)
        print(f"= {res}")

        return res

    return methode


def addition(a, b):
    return a+b


def soustraction(a, b):
    return a-b


# print(addition(soustraction(10,4), 8))


c1 = Complexe(0,3)
c2 = Complexe(3,0)

print(f"{c1} + {c2} = {c1-c2}")

print(c1 < c2, end=', ')
print(c1 <= c2, end=', ')
print(c1 == c2, end=', ')
print(c1 >= c2, end=', ')
print(c1 > c2 )

# print("part Réelle = {0:reel}".format(c1))
# print("Part Imaginaire = {0:imaginaire}".format(c1))
print("{0}".format(c1))


tf = datetime.now()
print()
print("durée =", tf-td)
