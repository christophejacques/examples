# import inspect
import json

from typing import Dict, List, Callable
from functools import wraps


class Regles:
    __liste: Dict[str, Callable] = dict()

    @classmethod
    def clear(self):
        self.__liste.clear()

    @classmethod
    def loadFromJson(self, filename: str):
        with open(filename) as fhandle:
            liste_regles = json.load(fhandle)
            print(len(liste_regles), "règles ont été chargées")
            return liste_regles

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
        # print("add", fonction_name, inspect.signature(fonction))
        self.__liste[fonction_name] = fonction


# Decorateur: Recuperation des regles
def regle(fonction):
    Regles.add(fonction.__name__, fonction)

    @wraps(fonction)
    def parametres(*args, **kwargs):
        return fonction(*args, **kwargs)
    return parametres


class Adresse:
    libelle_rue: str
    code_postal: str
    libelle_ville: str

    def __init__(self, libelle_rue: str, code_postal: str, libelle_ville: str):
        self.libelle_rue = libelle_rue
        self.code_postal = code_postal
        self.libelle_ville = libelle_ville.upper()


class Personne:
    sexe: str

    def __init__(self, nom: str, prenom: str, age: int, dept_naissance: str,
            libelle_rue: str, code_postal: str, libelle_ville: str):
        self.nom = nom.upper()
        self.prenom = prenom.title()
        self.age = age
        self.dept_naissance = dept_naissance
        self.adresse = Adresse(libelle_rue, code_postal, libelle_ville)

    def __str__(self) -> str:
        nom = self.nom
        prenom = self.prenom
        age = self.age
        dept_naissance = self.dept_naissance
        code_postal = self.adresse.code_postal
        libelle_ville = self.adresse.libelle_ville
        return (f"{self.__class__.__name__}({nom=}, {prenom=}, {age=}, {dept_naissance=}, " +
                f"{code_postal=}, {libelle_ville=})")


class Homme(Personne):
    sexe: str = "H"


class Femme(Personne):
    sexe: str = "F"


@regle
def exists(personne: Personne) -> bool:
    return True


@regle
def is_adult(personne: Personne) -> bool:
    return personne.age >= 18


@regle
def has_sexe(personne: Personne, sexe: str) -> bool:
    return personne.sexe == sexe


@regle
def has_code_postal(personne: Personne, code_postal: str) -> bool:
    return personne.adresse.code_postal == code_postal


@regle
def live_in(personne: Personne, depts: list) -> bool:
    return personne.dept_naissance in depts


@regle
def age_add(personne: Personne, annees: int):
    return personne.age + annees


@regle
def is_instance(objet: object, nom_classe: str) -> bool:
    try:
        classe = eval(nom_classe)
    except Exception:
        return False

    return isinstance(objet, classe)


def eprint(*args, **kwargs):
    print(*args, **kwargs, end="")


class Fonctions:
    definition: str 
    fonction: Callable

    def __init__(self):
        self.clear()

    def clear(self):
        self.definition = ""
        self.fonction = None

    def decoder(self, regle: Dict):
        self.fonction = self.decoder_regle(regle)
        eprint(self.definition)

    def __call__(self, classe):
        return self.fonction(classe)

    def run(self, classe):
        return self.fonction(classe)

    def fusion_fonction(self, f1, f2, operateur) -> Callable:
        match operateur:
            case "AND":
                return lambda x: f1(x) and f2(x)
            case "OR":
                return lambda x: f1(x) or f2(x)
            case _:
                raise Exception(f"Operateur {operateur!r} non géré.")

    def fonction_classe(self, operateur: str, fonction, parametres=None) -> Callable:
        if operateur == "NOT":
            if parametres is None or parametres == "":
                return lambda classe: not Regles.get_fonction(fonction)(classe)
            else:
                return lambda classe: not Regles.get_fonction(fonction)(classe, parametres)
        else:
            if parametres is None or parametres == "":
                return lambda classe: Regles.get_fonction(fonction)(classe)
            else:
                return lambda classe: Regles.get_fonction(fonction)(classe, parametres)

    def decoder_regle(self, regles: Dict, operateur=None, first: bool = True) -> Callable:
        return_fonc: Callable

        if not isinstance(regles, Dict):
            raise Exception("Erreur de decodage", regles)

        fonction = regles.get("fonction", None)
        if fonction is not None:
            parametres = regles.get("parametres", None)
            if first and operateur == "NOT":
                self.definition += f"{operateur} "

            self.definition += f"{fonction}({parametres})"

            return_fonc = self.fonction_classe(operateur, fonction, parametres)

            return return_fonc

        # Operateur
        operateur = regles.get("operateur", None)

        if operateur is None:
            raise Exception("Erreur de decodage", regles)

        self.definition += "["

        content: List = regles.get("content", [])
        if len(content) > 0:
            return_fonc = self.decoder_regle(content[0], operateur)
        else:
            raise Exception(f"L'operateur {operateur} doit avoir au moins un parametre")

        if len(content) > 1 and operateur == "NOT":
            raise Exception("L'operateur NOT n'accepte qu'un seul parametre")

        for regle in content[1:]:
            self.definition += f" {operateur} "

            return_fonc = self.fusion_fonction(
                return_fonc, 
                self.decoder_regle(regle, operateur, False), 
                operateur)

        self.definition += "]"

        return return_fonc


def main():
    liste_personnes: list = list()
    liste_personnes.append(Homme("Jack", "Chris", 50, "040", "rue Dupanloup", "45000", "Orleans"))
    liste_personnes.append(Homme("Jack", "chris", 15, "087", "rue Dupanloup", "87000", "Limoges"))
    liste_personnes.append(Homme("Jack", "Chris", 50, "045", "rue Dupanloup", "45000", "Orleans"))
    liste_personnes.append(Femme("Jack", "sylva", 50, "087", "rue Dupanloup", "87000", "Limoges"))
    liste_personnes.append(Femme("Jack", "Sylva", 15, "040", "rue Dupanloup", "45000", "Orleans"))

    liste_regles: list = Regles.loadFromJson("liste_fonctions.json")
    fonction = Fonctions()

    for une_regle in liste_regles:

        fonction.clear()
        eprint("Regle: ")
        try:
            fonction.decoder(une_regle)

        except Exception as erreur:
            print("ERREUR:", erreur)
            print()
            continue

        print()
        for personne in liste_personnes:
            try:
                if not fonction(personne):
                    continue
            except Exception as erreur:
                print("ERREUR:", erreur)
                break
                
            print("-", personne)

        print()


if __name__ == '__main__':
    main()
