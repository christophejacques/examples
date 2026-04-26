import json
import csv

from typing import Dict, Callable, List, Generator
from functools import wraps
from inspect import signature


class Regles:
    __liste: Dict[str, Callable] = dict()

    @classmethod
    def clear(cls):
        cls.__liste.clear()

    @classmethod
    def get_liste(cls):
        return cls.__liste

    @classmethod
    def get_fonction(cls, fonction: str):
        return cls.__liste[fonction]

    @classmethod
    def print(cls):
        for regle in cls.__liste():
            print(regle)

    @classmethod
    def add(cls, fonction_name: str, fonction: Callable):
        cls.__liste[fonction_name] = fonction


# Decorateur: Recuperation des regles
def regle(fonction):
    Regles.add(fonction.__name__, fonction)

    @wraps(fonction)
    def parametres(*args, **kwargs):
        return fonction(*args, **kwargs)
    return parametres


class Fonction:
    definition: str 
    fonction: Callable

    def __init__(self):
        self.clear()

    def __call__(self, classe):
        return self.fonction(classe)

    def clear(self):
        self.definition = ""
        self.fonction = None

    def decoder(self, regle: Dict):
        self.fonction = self.decoder_regle(regle)
        print(self.definition, end="")

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
            raise Exception(f"L'operateur {operateur!r} doit avoir au moins un parametre")

        if len(content) > 1 and operateur == "NOT":
            raise Exception("L'operateur NOT n'accepte qu'un seul parametre")

        for une_regle in content[1:]:
            self.definition += f" {operateur} "

            return_fonc = self.fusion_fonction(
                return_fonc, 
                self.decoder_regle(une_regle, operateur, False), 
                operateur)

        self.definition += "]"

        return return_fonc


class Outils:

    @classmethod
    def loadFromJson(cls, nom_fichier: str) -> List[Dict]:
        with open(nom_fichier) as fhandle:
            liste_regles = json.load(fhandle)
            print(len(liste_regles), "règles ont été chargées")
            return liste_regles

    @classmethod
    def loadFromString(cls, chaine: str, dictionnary: Dict = dict()) -> Generator:
        for donnees in map(lambda x: x.strip(), chaine.split("\n")):
            if donnees == "":
                continue

            nom_classe, *args = donnees.split(";")            
            try:
                classe = eval(nom_classe)
            except Exception:
                if nom_classe.upper() in dictionnary:
                    classe = dictionnary.get(nom_classe.upper())
                    if classe is None:
                        continue
                else:
                    raise TypeError(f"Classe ou fonction {nom_classe!r} inconnue.")

            # print(classe, signature(classe))
            result = classe(*args)
            if result is None:
                continue

            yield result

    @classmethod
    def loadFromCsv(cls, nom_fichier: str, dictionnary: Dict) -> List:
        content: List = list()

        with open(nom_fichier, encoding="utf-8") as fhandle:

            donnees = csv.reader(fhandle, delimiter=";")

            for ligne in donnees:
                sexe, nom, prenom, age, dept, rue, cp, ville = ligne
                if sexe.upper() in dictionnary:
                    personne = dictionnary.get(sexe.upper(), "")(
                        nom, prenom, int(age), dept, rue, cp, ville)
                else:
                    raise TypeError(f"Type de personne {sexe!r} inconnu.")

                content.append(personne)

        print(len(content), "personnes ont été chargées")
        return content


class MaClasse:
    def __init__(self, a: int, *args):
        self.args = args

    def __str__(self):
        return f"{self.__class__.__name__}{self.args}"


class Somme:
    def __init__(self, *args):
        self.args = args
        self.total = sum(map(lambda x: int(x), args))

    def __str__(self):
        return f"{self.__class__.__name__}{self.args} = {self.total}"


def somme(*args) -> int:
    return sum(map(lambda x: int(x), args))


if __name__ == "__main__":

    classes: Dict = {
        "HOMME": MaClasse,
        "FEMME": MaClasse
    }

    if False:
        liste_personnes: list = Outils.loadFromCsv("liste_personnes.csv", classes)
        for personne in liste_personnes:
            print("-", personne)

        print()
        liste_regles: list[Dict] = Outils.loadFromJson("liste_fonctions.json")
        fonction = Fonction()
        for une_regle in liste_regles:
            fonction.clear()
            print("- ", end="")
            try:
                fonction.decoder(une_regle)

            except Exception as erreur:
                print("ERREUR:", erreur)
                continue

            print()

    liste_classes: Generator = Outils.loadFromString("""
        print;Debut [
        MaClasse;0;1;2;3;4
        Somme;1;2;3
        somme;1;2;3
        print;] Fin
        """)

    for instance in liste_classes:
        print(instance)
