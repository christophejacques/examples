from typing import Dict, List, Callable
from functools import partial


class Regles:
    __liste: Dict[str, Callable] = dict()

    @classmethod
    def get_liste(self):
        return self.__liste

    @classmethod
    def get_fonction(self, fonction: str):
        return self.__liste[fonction]

    @classmethod
    def print(self):
        for regle in self.__liste():
            print(regle)

    @classmethod
    def add(self, fonction_name: str, fonction: Callable):
        self.__liste[fonction_name] = fonction


# Decorateur: Recuperation des regles
def regle(fonction):
    Regles.add(fonction.__name__, fonction)

    def parametres(*args, **kwargs):
        return fonction(*args, **kwargs)
    return parametres


class Personne:

    def __init__(self, nom: str, prenom: str, age: int, dept_naissance: str):
        self.nom = nom.upper()
        self.prenom = prenom
        self.age = age
        self.dept_naissance = dept_naissance

    def get_age(self):
        return self.age


@regle
def is_adult(personne: Personne):
    return personne.age >= 18


@regle
def live_in(personne: Personne, depts: list):
    return personne.dept_naissance in depts


@regle
def age_add(personne: Personne, annees: int):
    return personne.age + annees


def_regles: Dict = { 
    "operateur": "AND",
    "content": [
        {
            "fonction": "is_adult",
            "parametres": ""
        },
        {
            "operateur": "NOT",
            "content": [
                {
                    "fonction": "live_in",
                    "parametres": ["045", "054"]
                }
            ]
        }
    ]
}

p = Personne("Jacques", "Chris", 50, "045")


def eprint(*args, **kwargs):
    print(*args, **kwargs, end="")


def decodage(regles, operateur=None, first: bool = True) -> Callable:
    return_fonc: Callable

    if not isinstance(regles, Dict):
        raise Exception("Erreur de decodage", regles)

    fonction = regles.get("fonction", None)
    if fonction is not None:
        parametres = regles.get("parametres", None)
        if first and operateur == "NOT":
            eprint(f"{operateur} ")

        eprint(f"{fonction}(")
        if parametres is None:
            eprint(")")
            return_fonc = fonction

        else:
            eprint(f"{parametres})")
            return_fonc = partial(Regles.get_fonction(fonction), *parametres)

        return return_fonc

    # Operateur
    operateur = regles.get("operateur", None)

    if operateur is None:
        raise Exception("Erreur de decodage", regles)

    eprint("[")
    content: List = regles.get("content", [])
    if len(content) > 0:
        return_fonc = decodage(content[0], operateur)

    elif operateur == "NOT":
        raise Exception("L'operateur NOT n'accepte qu'un seul parametre")

    for regle in content[1:]:
        eprint(f" {operateur} ")
        return_fonc = decodage(regle, operateur, False)

    eprint("]")

    return return_fonc


def main():
    decodage(def_regles)
    print()


if __name__ == '__main__':
    main()
