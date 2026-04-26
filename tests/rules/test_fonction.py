from typing import Dict
from regles import regle, Fonction, Outils


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
def age_add(personne: Personne, annees: int) -> int:
    return personne.age + annees


@regle
def is_instance(objet: object, nom_classe: str) -> bool:
    try:
        classe = eval(nom_classe)
    except Exception:
        return False

    return isinstance(objet, classe)


def main():
    index: int
    une_regle: Dict

    classes: Dict = {
        "HOMME": Homme,
        "FEMME": Femme
    }

    fonction: Fonction = Fonction()
    liste_personnes: list[Personne] = Outils.loadFromCsv("liste_personnes.csv", classes)
    liste_regles: list[Dict] = Outils.loadFromJson("liste_fonctions.json")

    for index, une_regle in enumerate(liste_regles):

        fonction.clear()
        print(f"Regle {1+index}: ", end="")
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
