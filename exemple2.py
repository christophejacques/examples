from math import sqrt
from datetime import datetime

td = datetime.now()


def fdebugger(fonction):

    def methode(*args, **kvargs):
        print(f"Exec fonction : {fonction.__name__}{args}", end='')
        res = fonction(*args, **kvargs)
        print(f"= {res}")

        return res

    return methode


class Complexe():

    def __init__(self, reel, imaginaire):
        self.reel = reel
        self.imaginaire = imaginaire
        self.taille = sqrt(reel*reel + imaginaire*imaginaire)

    def __add__(self, other):
        return Complexe(self.reel + other.reel, self.imaginaire + other.imaginaire)

    def __sub__(self, other):
        return Complexe(self.reel - other.reel, self.imaginaire - other.imaginaire)

    def __len__(self):
        return int(sqrt(self.reel * self.reel + self.imaginaire * self.imaginaire))

    def __lt__(self, other):
        return self.taille < other.taille

    def __le__(self, other):
        return self.taille <= other.taille

    def __eq__(self, other):
        return self.taille == other.taille

    def __ge__(self, other):
        return self.taille >= other.taille

    def __gt__(self, other):
        return self.taille > other.taille

    def __repr__(self):
        """Method appelee lors d'un print()
        :return:
        """
        if self.imaginaire == 0:
            return f"{self.reel}"
        elif self.imaginaire < 0:
            return f"{self.reel}{self.imaginaire}i"
        else:
            return f"{self.reel}+{self.imaginaire}i"


def addition(a, b):
    return a+b


def soustraction(a, b):
    return a-b

# print(addition(soustraction(10,4), 8))


c1 = Complexe(2,3)
c2 = Complexe(3,-2)

print(f"{c1} + {c2} = {c1-c2}")

print(c1 < c2, end=', ')
print(c1 <= c2, end=', ')
print(c1 == c2, end=', ')
print(c1 >= c2, end=', ')
print(c1 > c2 )


tf = datetime.now()
print()
print("durée =", tf-td)
