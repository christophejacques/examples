import re
import typing

from io import TextIOWrapper, BufferedWriter
from typing import Collection, Container, ContextManager
from typing import Type, NewType
from typing import Final, final
from typing import Match, Optional


def list_typing_objects():
    for o in dir(typing):
        if o.startswith("_"):
            continue
        print(o)
    exit()

# list_typing_objects()


def test_match(text: str) -> None:
    # On cherche un pattern : "Nom: [Lettres], Age: [Chiffres]"
    pattern = r"Nom: (?P<name>\w+), Age: (?P<age>\d+)"
    
    # re.search renvoie un objet Match ou None
    match: Optional[Match[str]] = re.search(pattern, text)

    if match:
        # On peut maintenant accéder aux groupes capturés en toute sécurité
        name = match.group("name")
        age = match.group("age")
        print(f"👤 Utilisateur trouvé : {name} ({age} ans)")
        
        # On peut aussi obtenir les positions (index) dans la chaîne
        start, end = match.span()
        print(f"📍 Trouvé entre les positions {start} et {end}")

    else:
        print("❌ Aucune correspondance trouvée.")


class Database:
    def __init__(self):
        # Un attribut qui ne doit jamais changer après l'initialisation
        self.TIMEOUT: Final[int] = 30

    @final
    def connect(self):
        print("Connexion sécurisée en cours...")


class MyDatabase(Database):
    # ❌ Erreur : Impossible d'écraser une méthode décorée avec @final
    def connect(self):
        print("Tentative de modification du comportement")


# Tentative de réassignation
def test_final():
    # Une constante globale
    MAX_CONNECTIONS: Final = 10
    MAX_CONNECTIONS = 20  # ❌ Erreur signalée par l'analyseur de type "mypy"


def ouvrir_fichier(nom: str) -> BufferedWriter:
  print("Creating file:", nom)
  bf = open(nom, "wb")
  return bf


def fermer_fichier(file_handle: BufferedWriter):
    file_handle.close()
    print("file closed")


def test_fichier():
    fh = ouvrir_fichier("fichier.bin")
    if isinstance(fh, BufferedWriter):
        print("filehandle is BufferedWriter")

        fh.write(b"Tableau :\n")
        fh.write(b"\x09a b c")
        fh.write(b"\x09def")
        fh.write(b"\x09ghi\n")
        fh.write(b"\x09123")
        fh.write(b"\x09\x09456")
        fh.write(b"\x09789")

    fermer_fichier(fh)


def test_newtype():
    UserId = NewType("UserId", int)

    class User:
        
        def __init__(self, nom):
            self.nom = nom
            self.user_id = UserId(0)

        def get_id(self):
            return self.user_id


    u = User("cja")
    print(u.user_id)
    print(u.get_id())


def verifier_presence_et_taille(elements: Collection[str], cible: str) -> None:
    # On peut utiliser len() grâce à Collection
    print(f"Nombre d'éléments : {len(elements)}")
    
    # On peut utiliser 'in' grâce à Collection
    if cible in elements:
        print(f"'{cible}' est présent.")
    else:
        print(f"'{cible}' est absent.")


def test_collection():
    ma_liste: list = ["Alice", "Bob", "Charlie"]
    mon_set: set = {"Alice", "Bob", "Charlie"}
    mon_tuple: tuple = ("Alice", "Bob", "Charlie")

    # Tout cela fonctionne parfaitement :
    verifier_presence_et_taille(ma_liste, "Alice")
    verifier_presence_et_taille(mon_set, "Eve")
    verifier_presence_et_taille(mon_tuple, "Bob")


def verifier_acces(autorises: Container[int], utilisateur_id: int) -> bool:
    # La seule opération garantie par Container est 'in'
    if utilisateur_id in autorises:
        return True
    return False

def test_container():
    # Fonctionne avec une liste
    print(verifier_acces([1, 2, 3], 2))  # True

    # Fonctionne avec un set (très performant pour Container)
    print(verifier_acces({10, 20, 30}, 10))  # True

    # Fonctionne avec un range
    print(verifier_acces(range(0, 100), 50))  # True


def division_par_0():
    return 1 / 0

def test_raise():
    try:
        division_par_0()
    except Exception as erreur:
        print("Erreur raise()", erreur)
        raise
    finally:
        print("Fin raise()")

def open_file(nom: str) -> ContextManager:
  return open(nom, "rb")

def test_contextmanager():
    with open_file("fichier.bin") as fh:
        res = "1"
        while res:
            res = fh.readline().decode()
            print(res, end="")
    print()


if __name__ == "__main__":

    # test_final()
    # test_fichier()
    # test_newtype()
    # test_collection()
    # test_container()
    # test_raise()
    # test_contextmanager()
    test_match("Bonjour, Nom: Alice, Age: 30")
