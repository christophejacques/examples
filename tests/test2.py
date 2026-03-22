from typing import Type, Any

class ClasseMere:
    def __init__(self, *args):
        print("ClasseMere: init  =>", args)
        self.args = args

    def __initinstance__(self, screen, window):
        print("ClasseMere: initialisation instance =>", screen, window)
        self.screen = screen
        self.window = window

    def __str__(self):
        return f"{self.screen=} {self.window=}"


class UneClasse(ClasseMere):
    def __init__(self, *args):
        print("UneClasse: init instance", args)
        self.args = args

    def __str__(self):
        return super().__str__() + f" - {self.args=}"


def initialise_classe(
        nom_classe: Type[Any], 
        screen, 
        window, 
        *args, **kwargs) -> Type:

    init_method = nom_classe.__init__
    nom_classe.__init__ = nom_classe.__initinstance__
    instance = nom_classe(screen, window)

    nom_classe.__init__= init_method
    nom_classe.__init__(instance, *args, **kwargs)

    return instance


uc = initialise_classe(UneClasse, "screen", "window", 5)
print(uc)
