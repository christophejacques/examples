import functools
import inspect
from typing import Callable, Optional, TypeVar


class ctrlVars:
    """
    Permet de controler la validite des variables utilisees
    pour toutes les methodes d'une classe
    """
    __DEBUG__: bool = True
    classe: Optional[type]
    nom_classe: Optional[str]

    def __init__(self, fonction: Callable):
        # On garde une trace de la fonction d'origine
        functools.update_wrapper(self, fonction)

        self.liste_types: list = list()
        self.fonction = fonction
        self.nom_classe = None
        self.classe = None

        # recuperation et sauvegarde de tous les types
        # des variables dans la definition de la methode
        sig = inspect.signature(fonction)
        index: int = -1
        for nom, param in sig.parameters.items():
            index += 1
            if param.annotation == inspect._empty:
                self.liste_types.append(object)
            elif isinstance(param.annotation, TypeVar):
                self.liste_types.append(TypeVar)
            else:
                self.liste_types.append(param.annotation)

            # print(f"annot={param.annotation!r}", type(param.annotation))

    def __set_name__(self, classe: type, name: str):
        """
        Appelé automatiquement par Python quand la classe 'classe' 
        est finalisée. C'est ici qu'on récupère le nom !
        """
        # print("Appel __set_name__()", self, classe, name)
        if self.liste_types[0] is object:
            # mise a jour de la classe dans l'element "0"
            self.liste_types[0] = classe

        self.classe = classe
        self.nom_classe = classe.__name__

    def print_debug(self, result, type_result, *args, **kwargs):
        if self.__DEBUG__:
            print("[debug]", end=" ")
            if self.classe:
                print(self.nom_classe, end=".")
            print(self.fonction.__name__, end="")
            print(args[(1 if self.classe else 0):], end=" ")
            print(kwargs, end=" <-> ")
            print(self.liste_types, end=" -> ")
            if type_result is None:
                print("NoneType", end="\n  > ")
            else:
                print(type_result.__name__, end="\n  > ")
            print(result)

    def raise_error(self, type_result, *args, **kwargs):
        if self.__DEBUG__:
            print("[debug]", end=" ")
            if self.classe:
                print(self.nom_classe, end=".")
            print(self.fonction.__name__, end="")
            print(args[(1 if self.classe else 0):], end=" ")
            print(kwargs, end=" <-> ")
            print(self.liste_types, end=" -> ")
            if type_result is None:
                print("NoneType", end="\n  > ")
            else:
                print(type_result.__name__, end="\n  > ")

        raise self.error

    def __call__(self, *args, **kwargs):
        """
        Logique du wrapper exécutée lors de l'appel de la méthode.
        """
        nb_args = len(args)
        type_var = {}
        type_param = object
        self.error = None
        for index, type_param in enumerate(self.liste_types):
            if index >= nb_args:
                # il y a moins de parametres utilisés que definis
                continue

            if type_param == TypeVar:
                if type_var:
                    type_param = type_var["classe"]
                else:
                    type_param = args[index].__class__
                    type_var["classe"] = type_param

            if not isinstance(args[index], type_param):
                # le parametre controle n'est pas du bon type
                msg: str = ""
                msg += f"Param n°{index + (0 if self.classe else 1)} "
                if self.classe:
                    msg += f"de {self.nom_classe}."
                else:
                    msg += f"de "
                msg += f"{self.fonction.__name__}(), "
                msg += f"type {args[index].__class__.__name__!r} reçu"
                msg += f", alors que {type_param.__name__!r} attendu."

                self.error = TypeError(msg)


        type_result = self.fonction.__annotations__.get("return")
        real_type_result = type_result
        if isinstance(type_result, TypeVar):
            # si le type du retour est [T] on recupere le type des parametres
            real_type_result = type_var.get("classe", object)
            type_result = TypeVar

        if self.error:
            self.raise_error(type_result, *args, **kwargs) 

        result = self.fonction(*args, **kwargs)
        if real_type_result:
            if not isinstance(result, real_type_result):
                # le resultat de la methode n'est pas du bon type
                msg: str = ""
                msg += "Resultat de "
                if self.classe:
                    msg += f"{self.nom_classe}."
                msg += f"{self.fonction.__name__}() "
                msg += "de type "
                msg += f"{result.__class__.__name__!r},"
                msg += " mais "
                msg += f"{real_type_result.__name__!r}"
                msg += " attendu."

                self.error = TypeError(msg)
                self.raise_error(type_result, *args, **kwargs) 

        self.print_debug(result, type_result, *args, **kwargs)

        return result

    def __get__(self, instance, classe):
        """
        Nécessaire pour que 'self' soit correctement passé à la méthode décorée.
        """
        if instance is None:
            return self
        return functools.partial(self.__call__, instance)


class User:
    """
    class permettant de tester 
    la classe de controle de validite des variables : ctrlVars
    """
    def set_nom(self, nom: str) -> None:
        pass

    def add(self, a: int, b: int = 0, *args) -> int:
        res = a + b + sum(args)
        return res

    def join(self, a: str, b: str = "", *args) -> str:
        res = a + b
        for arg in args:
            res += arg
        return res

    def keyword(self, **kwargs) -> dict:
        return kwargs


def somme[T: (int, str)](a: T, b: T) -> T:
    return (a+b)


@ctrlVars
def ajout_decorateur(classe: type, decorateur: type):
    """
    Ajout le decorateur 'ctrlVars' a chaque methode d'une classe
    """
    if not isinstance(classe, type):
        raise TypeError(f"L'objet {classe.__name__!r} n'est pas une classe.")

    for methode in dir(classe):
        if methode[:2] == "__":
            # on ne controle pas les magics methods
            continue

        if not callable(getattr(classe, methode)):
            # on ne controle pas les variables simples
            # uniquement les methodes
            continue

        # Ajoute le decorateur debug aux methode de la classe
        # print("Add decorateur to:", f"{classe.__name__}.{methode}")
        setattr(classe, methode, decorateur(getattr(classe, methode)))

        # methode __set_name__ appelee automatiquement si decorateur
        # ajoute manuellement (ne fonctionne pas lors de l'ajout ici)
        getattr(classe, methode).__set_name__(classe, methode)

    print(f"Classe {classe.__name__!r} mise à jour !")



@ctrlVars
def main():
    global somme
    somme = ctrlVars(somme)
    
    somme(1, 2)
    assert somme("<1>", "<2>") == "<1><2>"
    try:
        somme(1, "<2>")
    except Exception as erreur:
        print("Erreur:", erreur)

    # exit()
    ajout_decorateur(User, ctrlVars)

    u = User()
    u.set_nom("Alice")

    u.add(2)
    u.add(2, 3)
    u.add(1, 2, 3, 4)

    u.join("1", "5")
    u.join("65")
    u.join("1", "2", "3", "4")

    u.keyword()
    u.keyword(a=1, b=2, ctrl=True)


if __name__ == "__main__":
    main()
