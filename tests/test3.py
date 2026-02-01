print("debut")

d: dict[str, int] = dict()

class maClasse:
    def __init__(self):
        print("__init__")

    def __and__(self, other):
        print("__and__")
        return True

    def __add__(self, other):
        print("__add__")
        return 0


def test_maClasse():
    m = maClasse()
    m + m, m & m


def boucle_for1():
    l = [chr(x) for x in range(65, 75)]
    print(l)
    taille = len(l)
    for i, val in enumerate(l):
        print(i, val, end= " - ")
        if val == "F":
            l.pop(i)
    print()
    print(l)
    print()


def boucle_for2():
    l = [chr(x) for x in range(65, 75)]
    print(l)
    taille = len(l)
    i = 0
    while i < taille:
        val = l[i]
        print(i, val, end= " - ")
        if val == "F":
            l.pop(i)
            taille -= 1
        else:
            i += 1
    print()
    print(l)


class maListe:
    def __init__(self, elements: list = []):
        self.elements = elements
        self.index = -1
        self.taille = len(elements)

    def pop(self, index=None):
        if index is None:
            index = 0 if self.index < 0 else self.index

        self.elements.pop(index)
        self.taille = self.taille - 1
        if index <= self.index and self.index > 0:
            self.index -= 1

    def __iter__(self):
        self.index = -1
        return self

    def __next__(self):
        if self.index + 1 < self.taille:
            self.index += 1
            return self.elements[self.index]

        self.index = -1
        raise StopIteration

    def __str__(self):
        return f"{self.elements}"


def boucle_for3():
    ml = maListe([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    print(ml)
    for i, v in enumerate(ml):
        print(i, v, end=" - ")
        if v == 5:
            ml.pop()

    print()
    print(ml)
    ml.pop()
    print(ml)

    for v in ml:
        print( v, end=" - ")
        if v == 2:
            ml.pop()

    print()
    print(ml)

    for _ in range(len(ml.elements)):
        ml.pop()
        print(ml)


boucle_for1()
boucle_for2()
boucle_for3()

print("Démineur")

print("fin")
