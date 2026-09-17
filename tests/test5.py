from __future__ import annotations
import inspect

from typing import Optional, Callable, Dict, List, Self, Generator, Any
from inspect import signature, _ParameterKind


def fprint(*args, **kwargs):
    print(*args, **kwargs, flush=True)


def definition_types(fonction):

    print(fonction.__annotations__)

    params = [eval(v) for k, v in fonction.__annotations__.items() if k != "return"]
    retour = fonction.__annotations__.get("return")

    def ctrl_params(*args, **kwargs):
        print("test", args, kwargs)
        for index, arg in enumerate(args):
            if params[index] is Self:
                if index == 0:
                    continue
                msg = "Fonction "
                msg += fonction.__name__ 
                msg += f"(param n°{index}) -> '"
                msg += arg.__class__.__name__ 
                msg += "' au lieu de 'Self'"
                raise TypeError(msg)

            elif not isinstance(arg, params[index]):
                msg = "Fonction "
                msg += fonction.__name__ 
                msg += f"(param n°{index}) -> '"
                msg += arg.__class__.__name__ 
                msg += "' au lieu de '" 
                msg += params[index].__name__ + "'"
                raise TypeError(msg)

        res = fonction(*args, **kwargs)
        if retour is not None:
            if not isinstance(res, eval(retour)):
                msg = "Resultat de la Fonction "
                msg += fonction.__name__ 
                msg += "() -> de type '"
                msg += res.__class__.__name__ 
                msg += "' au lieu de '" 
                msg += retour + "'"
                raise TypeError(msg)

        return res

    return ctrl_params 


def deco(fonction):
    # print("check:", fonction.__name__)
    # print("Fonction:", fonction.__qualname__)
    # isSubFonc: bool = "." in fonction.__qualname__
    # isFonction: bool = inspect.isfunction(fonction) and not isSubFonc
    sig = signature(fonction)

    return_type = eval(fonction.__annotations__.get("return", "Any"))

    params = list(sig.parameters.keys())
    isMethode: bool = params and params[0] in ('self', 'cls')

    def wrapper(*args, **kwargs):

        nbargs = len(args) - 1

        for idx, parametre in enumerate(sig.parameters.items()):
            nom, param = parametre
            if False:
                print("param", param)
                print("- name:", param.name)
                print("- annotation:", param.annotation)
                print("- default:", param.default)
                print("- kind:", param.kind)

            if idx > nbargs and param.kind != _ParameterKind.VAR_POSITIONAL:
                msg = f"il manque le paramètre n°{1+idx} {param.name!r} "
                msg += f"de type {param.annotation!r}"
                raise TypeError(msg)

            type_param = param.annotation
            # valeur_defaut = param.default

            if idx == 0 and isMethode:
                classe_name = fonction.__qualname__.split(".")[0]
                arg_class = args[idx].__class__.__name__
                if arg_class != classe_name and arg_class != "type":
                    msg = f"Le premier parametre n'est pas de type {classe_name!r}, "
                    msg += f"mais de type {arg_class!r}"
                    raise TypeError(msg)
                    
            if type_param is inspect.Parameter.empty:
                continue

            else:
                type_var = eval(type_param)

            # print(args[idx].__class__, type_var)
            if not args[idx].__class__ is type_var:
                msg = f"La variable {nom} ({args[idx]}) "
                msg += f"est de type {args[idx].__class__.__name__!r} "
                msg += f"au lieu de {type_var.__name__!r}"
                raise TypeError(msg)

            result = fonction(*args, **kwargs)
            if (return_type not in (None, Any)
                    and not isinstance(result, return_type.__class__)):
                msg = f"Le résultat est de type {result.__class__.__name__!r} "
                msg += f"au lieu de {return_type.__name__!r}"
                raise TypeError(msg)

        return result
    return wrapper


def res():
    return "0"


@deco
def sommemulti(a: int, *args) -> int:
    print("somme()", sum(args)+a)
    return res()


try:
    sommemulti(1, 2, 3, 4, 5)
except Exception as erreur:
    print("sommemulti(1, 2,...), erreur:", erreur)

# exit()
try:
    sommemulti()
except Exception as erreur:
    print("sommemulti(), erreur:", erreur)


# @definition_types
def somme(c, b: int) -> int:
    return c + b


class Test:
    def __init__(self, valeur):
        self.valeur = valeur

    def add(self, a, b: int, c: int = 0, *args, **kwargs) -> int:
        self.valeur += b
        return self.valeur 

    def __str__(self):
        return f"valeur = {self.valeur}"


class MaClasse:
    @deco
    def methode_instance(self, x: int):
        fprint("MaClasse.methode_instance", x)

    @classmethod
    @deco
    def methode_classe(cls, s: str):
        fprint("MaClasse.methode_classe", s)

    @staticmethod
    @deco
    def methode_statique(b: bool):
        fprint("MaClasse.methode_statique", b)


@deco
def fonction_classique(x: int):
    fprint("fonction_classique", x)


mc = MaClasse()

mc.methode_instance(2)
try:
    mc.methode_instance("2")
except Exception as erreur:
    print("mc.methode_instance(), erreur:", erreur)

mc.methode_classe("2")
try:
    mc.methode_classe(2)
except Exception as erreur:
    print("mc.methode_classe(), erreur:", erreur)

mc.methode_statique(True)
try:
    mc.methode_statique(2)
except Exception as erreur:
    print("mc.methode_statique(), erreur:", erreur)

fonction_classique(5)
try:
    fonction_classique("5")
except Exception as erreur:
    print("fonction_classique(), erreur:", erreur)


print("fin")
