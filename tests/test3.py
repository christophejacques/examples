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


m = maClasse()
m + m, m & m

print("fin")
