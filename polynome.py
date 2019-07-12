# content:UTF-8


class Polynome:
    def __init__(self, *coef):
        self.coef = coef

    def __repr__(self):
        s = ""
        signe = ""
        for i, coef in enumerate(reversed(self.coef)):
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
        return Polynome(*(x+y for x, y in zip(self.coef, other.coef)))

    def __call__(self, *args, **kwargs):
        somme = 0
        for p, d in enumerate(reversed(self.coef)):
            somme += d * pow(args[0], p)

        return somme


a = Polynome(0, 2, 3)
b = Polynome(-1, 0, -2)
c = a + b

print(a)
print(b)
print(c)

print("a(2)=", a(2))
print(type(a))