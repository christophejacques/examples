import functools
import inspect
from typing import Callable


class ctrlVars:
    """
    Permet de controler la validite des variables utilisees
    pour toutes les methodes d'une classe
    """
    __DEBUG__ = True

    def __init__(self, fonction):
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
            if param.annotation ==  inspect._empty:
                self.liste_types.append(object)
            else:
                self.liste_types.append(param.annotation)


    def __set_name__(self, classe, name):
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

    def __call__(self, *args, **kwargs):
        """
        Logique du wrapper exécutée lors de l'appel de la méthode.
        """
        nb_args = len(args)

        if self.__DEBUG__:
            print("[debug]", end=" ")
            if self.classe:
                print(self.nom_classe, end=".")
            print(self.fonction.__name__, end="")
            print(args[(1 if self.classe else 0):], end=" ")
            print(kwargs, end=" <-> ")
            print(self.liste_types, end="\n  > ")

        for index, type_param in enumerate(self.liste_types):
            if index >= nb_args:
                # il y a moins de parametres utilisés que definis
                continue

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
                raise TypeError(msg)

        type_result = self.fonction.__annotations__.get("return")
        result = self.fonction(*args, **kwargs)
        if type_result:
            if not isinstance(result, type_result):
                # le resultat de la methode n'est pas du bon type
                msg: str = ""
                msg += "Resultat de "
                if self.classe:
                    msg += f"{self.nom_classe}."
                msg += f"{self.fonction.__name__}() "
                msg += "de type "
                msg += f"{result.__class__.__name__!r},"
                msg += " mais "
                msg += f"{type_result.__name__!r}"
                msg += " attendu."
                raise TypeError(msg)

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
        print(f"User.set_nom = {nom}")

    def add(self, a: int, b: int=0, *args) -> int:
        res = a + b + sum(args)
        print(res)
        return res

    def join(self, a: str, b: str="", *args) -> str:
        res = a + b
        for arg in args:
            res += arg
        print(f"{a!r}+{b!r}+{args} = {res!r}" )
        return res

    def keyword(self, **kwargs) -> dict:
        print(kwargs)
        return kwargs


def somme(a: int, b: int) -> int:
    print(a+b)
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


if True:
    somme = ctrlVars(somme)
    # ajout_decorateur(somme, ctrlVars)
    somme(2, 7)
    exit()


def test():
    ajout_decorateur(User, ctrlVars)

    # Test
    somme(1, 2)

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
    test()
