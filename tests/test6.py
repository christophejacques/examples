from collections import namedtuple


Ville = namedtuple("Ville", ["codePostal", "codeInsee", "Libelle"])
ville = Ville(45000, 45125, "orléans")

print(ville)
