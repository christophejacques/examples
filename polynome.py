# content:UTF-8
import itertools


def nz(val, sinone):
    return sinone if val == None else val


class Polynome:
    def __init__(self, *coef):
        self.coef = coef

    def __repr__(self):
        s = ""
        signe = ""
        for i, coef in enumerate(self.coef):
            if coef == 0:
                continue

            if coef == 1:
                scoef = "1" if i == 0 else ""
            elif coef == -1:
                scoef = "-1" if i == 0 else "-"
            else:
                scoef = str(coef)

            if i == 0:
                s = scoef
            elif i == 1:
                s = scoef + "x" + signe + s
            else:
                s = scoef + "x^" + str(i) + signe + s

            signe = " " if coef < 0 else " + "

        return "f(x) = " + s

    def __add__(self, other):
        return Polynome(*(nz(x, 0)+nz(y, 0) for x, y in itertools.zip_longest(self.coef, other.coef)))

    def __sub__(self, other):
        return Polynome(*(nz(x, 0)-nz(y, 0) for x, y in itertools.zip_longest(self.coef, other.coef)))

    def __call__(self, *args, **kwargs):
        somme = 0
        for p, d in enumerate(self.coef):
            somme += d * pow(args[0], p)

        return somme


a = Polynome(2, -2, 3)
b = Polynome(-3, -1)
c = a + b
d = a - b

print(a)
print(b)
print(c)
print(d)

print("a(2)=", a(2))
