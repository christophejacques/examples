import os
from importlib import import_module


def get_classes(fichier):
    mon_app = import_module(fichier)
    for classe_name in dir(mon_app):
        if not hasattr(mon_app, "Application"): continue
        classe = getattr(mon_app, classe_name)
        if not callable(classe): continue
        if not classe.__class__.__name__ == "ABCMeta": continue
        if not issubclass(classe, mon_app.Application): continue
        if classe == mon_app.Application: continue
        yield classe


def get_all_classes():
    liste_classes = []
    for file in os.scandir("."):
        fichier = file.name.lower()
        if file.is_file() and fichier.endswith(".py") and fichier != __file__[1+__file__.rindex("\\"):]:
            fichier = fichier.removesuffix(".py")
            print("\n[", fichier, "]")
            for classe in get_classes(fichier):
                print(" ", classe, end=", ")
                if classe.__name__ not in liste_classes:
                    print("CONFIG=", classe.DEFAULT_CONFIG)
                    liste_classes.append(classe.__name__)
    return liste_classes


if __name__ == "__main__":
    print("<Test>")
    print(get_all_classes())
