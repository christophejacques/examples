import inspect
from typing import Callable


def debug(fonction):
    sig = inspect.signature(fonction)
    # print(dir(fonction))
    liste_types: list = list()
    index: int = 0
    for nom, param in sig.parameters.items():
        if param.annotation ==  inspect._empty:
            if index == 0:
                liste_types.append(object)
            else:
                liste_types.append(object)
        else:
            liste_types.append(param.annotation)

    def params(self, *args, **kwargs):
        if self.__DEBUG__:
            print("[debug]", end=" ")
            print(self.__class__.__name__, end=".")
            print(fonction.__name__, end="")
            print(args[0:], end=" ")
            print(kwargs)

        if not isinstance(self, liste_types[0]):
            msg: str = ""
            msg += f"{self.__class__.__name__}."
            msg += f"{fonction.__name__} "
            msg += "Param self incorrect."
            raise TypeError(msg)

        for index, type_param in enumerate(liste_types[1:]):
            if not isinstance(args[index], type_param):
                msg: str = ""
                msg += f"{self.__class__.__name__}."
                msg += f"{fonction.__name__} "
                msg += f"param n°{index+1} "
                msg += f"type: {args[index].__class__.__name__!r} obtenu"
                msg += f", alors que {type_param.__name__!r} attendu."
                raise TypeError(msg)

        type_result = fonction.__annotations__.get("return")
        result = fonction(self, *args, **kwargs)
        if type_result:
            if not isinstance(result, type_result):
                msg: str = ""
                msg += f"{self.__class__.__name__}."
                msg += f"{fonction.__name__} "
                msg += "Result type error."
                raise TypeError(msg)
        
        return result
    return params


class MaClasse: 

    def add(self, a: int, b: int=0) -> int:
        return a+b

    def diff(self, a: int, b: int=0) -> int:
        return a-b

    def mult(self, a: int, b: int=0) -> int:
        return a*b

    def divint(self, a: int, b: int=0) -> int:
        return a//b

    def fusion(self, a, b) -> str:
        return a+b


def ajout_decorateur(classe: type, decorateur: Callable):
    for methode in dir(classe):
        if methode[:2] == "__":
            continue

        if not callable(getattr(classe, methode)):
            continue

        # Ajoute le decorateur debug aux methode de la classe
        # print("Add decorateur to:", f"{classe.__name__}.{methode}")
        setattr(classe, "__DEBUG__", True)
        setattr(classe, methode, decorateur(getattr(classe, methode)))


ajout_decorateur(MaClasse, debug)

mc = MaClasse()
print(mc.fusion("1", "2"))
# print(mc.diff(5, 2))

