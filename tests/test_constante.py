from typing import Final  # , final
from dataclasses import dataclass


if False:
    constante: Final[int] = 10
    print(f"Initialisation de constante à {constante}")

    print(f"constante = {constante}  # doit être 10")

    print("Mise à jour de constante à 5")
    constante = 5  # lighting Erreur doit être notifiée

    print(f"constante = {constante}  # doit être 5")


class Const[unType]:
    def __init__(self, arg: unType):
        self.valeur = arg
        self.type = type(arg)

    def __eq__(self, other: object):
        if other.__class__ is not self.type:
            msg: str = f"le paramètre {other!r} est de type {other.__class__.__name__}"
            msg += f", type {self.type.__name__} attendu"
            raise TypeError(msg)
        return self.valeur == other


if False:
    entier: Const[int] = Const(1)
    print(entier == 1)

    caractere: Const[str] = Const("1")
    try:
        print(caractere == 1)
    except Exception as erreur:
        print("erreur:", erreur)


@dataclass(frozen=True)
class Konstante:
    PI: float = 3.1415


k = Konstante()
try:
    k.PI = 3.14
except Exception as erreur:
    print(erreur)


class Constante:
    __data: dict = dict()

    @classmethod
    def __setattr__(cls, key, value):
        cls.__setitem__(key, value)

    @classmethod
    def __getattr__(cls, key):
        return cls.__data.get(key)

    @classmethod
    def __setitem__(cls, key, value):
        if key in cls.__data:
            # raise Exception(f"La clé {key!r} a déjà été initialisée et ne peut donc pas être modifiée !")
            print(f"La clé {key!r} a déjà été initialisée et ne peut donc pas être modifiée !")
            return

        cls.__data[key] = value

    @classmethod
    def __getitem__(cls, key):
        if key not in cls.__data:
            # raise Exception(f"La clé {key!r} a déjà été initialisée et ne peut donc pas être modifiée !")
            print(f"La clé {key!r} n'existe pas !")
            return

        return cls.__data.get(key)

    @classmethod
    def __str__(cls):
        return f"{cls.__data}"


def fonc0():
    const = Constante()
    const.cle0 = 0
    const.cle1 = 1
    const.cle2 = 2


def fonc1():
    const = Constante()
    const["cle3"] = 3
    const["cle4"] = 4
    const["cle5"] = 5


def fonc2():
    const = Constante()
    const.cle6 = 6
    const["cle7"] = 7
    const["cle8"] = 8
    const.cle2 = 20


def fonc3():
    const = Constante()
    print(const)
    # print(dir(const))


[eval(f"fonc{f}()") for f in range(4)]
