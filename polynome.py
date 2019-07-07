# content:UTF-8
import math


class Polynome:
    def __init__(self, *coef):
        self.coef = coef

    def __repr__(self):
        return "Polynome{!r}".format(self.coef)

    def __add__(self, other):
        return Polynome(*(x+y for x, y in zip(self.coef, other.coef)))

    def __call__(self, *args, **kwargs):
        somme = 0
        for p, d in enumerate(reversed(self.coef)):
            somme += d * math.pow(args[0], p)

        return somme


a = Polynome(1, 2, 3)
b = Polynome(4, -1, 2)
c = a + b

print(a)
print(b)
print(c)

print("a(2)=", a(2))