from typing import Type

class ClasseMere:
    def __init__(self, screen):
        print("ClasseMere: initialisation instance")
        self.screen = screen

    def __str__(self):
        return f"{self.screen=}"


class UneClasse(ClasseMere):
    def __init__(self, val):
        print("UneClasse: initialisation instance", val)
        self.val = val

    def __str__(self):
        return super().__str__() + f" - {self.val=}"


def initialise_classe(une_classe: Type, *args, **kwargs) -> Type:
    init_temp = une_classe.__init__
    del une_classe.__init__

    instance = une_classe("MERE")

    une_classe.__init__= init_temp
    une_classe.__init__(instance, *args, **kwargs)

    return instance

uc = initialise_classe(UneClasse, 5)
print(uc)
