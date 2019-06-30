__author__ = "JACQUES Christophe"

import time
from utils.operation import *
from utils.personnes import Homme, Femme
# from utils.robot import *

debut = time.perf_counter()
print()

if __name__ != '__main__':
    exit()

# -------------------------------------------------------------------------------------------------------------------
def exemple1():
    vtuple = (1, 2, 3, 4, 5)
    vliste = [1, 2, 3, 4, 5]
    vset = {1, 2, 3, 4, 5}

    print(vtuple)
    print(vliste)
    print(vset)

    print(tuple(vset))
    print(list(vset))
    print(set(vliste))


def exemple2():
    dico = {
        "tuple": (1, 2, 3, 4, 5),
        "liste": [2, 4, 6, 8],
        "set": {3, 6, 9}
    }
    for j, k in enumerate(dico):
        print("%-1s : %-5s = %s" % (j, k, dico[k]))

    for a, b, c in zip(dico["tuple"], dico["liste"], dico["set"]):
        print(a, b, c)

    for x in sorted(dico["set"]):
        print(x)


def find(maListe, chaine):
    for i, e in enumerate(maListe):
        print("Testing element n°%d : %s" % (i, e))
        if e == chaine:
            break
    else:
        return -1
    return i


def exemple3():
    couleurs = ["red", "green", "blue", "yellow"]
    print(couleurs)
    print(sorted(couleurs))
    print(sorted(couleurs, key=len))
    print(find(couleurs, "white"))
    print(find(couleurs, "red"))


def exemple4():
    dico = {"mattieu": "rouge", "isa": "blue", "vero": "black"}

    for a, b in dico.items():
        print(a, b)


def exemple5():
    print("Exemple 5")
    print("---------")
    couleurs = ["red", "green", "blue", "red", "yellow"]

    d = {}

    print("Initialisation")
    print("nb red = %d" % d.get("red", 0))

    print(couleurs)
    couleurs.pop()
    print("Method pop()  => ", couleurs)

    couleurs.pop(0)
    print("Method pop(0) => ", couleurs)

    for c in couleurs:
        d[c] = d.get(c, 0) + 1

    print("nb red = %d" % d.get("red", 0))
    print(d)


def toDict(l):
    # if type(l) == type({"":""}):
    if isinstance(l, dict):
        print("c'est un dico")
        print(dir(l))
        print(l.__dir__)

    a = 1


def exemple6():
    print(dir())
    print("---------")

    f = lambda x: print("Fonction f(" + str(x) + ")")
    d = {"k": "cle"}

    # toDict(d)
    print(factoriel(3))


import sys


def exemple7():
    print(time.time())

    for x in dir(sys):
        print("[" + x + "]</BR>")

        texte = " "
        for y in dir(x):
            if not y.startswith("__"):
                texte = texte + " " + y

        print(texte)

    print(time.process_time())


def exemple8():
    print(substring("azertyqsdfgh", 2, 8))


# parametre optionel p
def substring(s, d, f, p=0):
    if p:
        return s[d:f:p]
    else:
        return "pas de p".upper()


def exemple9():
    pere = Homme("BERNARD", "Victor")
    mere = Femme("BERNARD", "Irène", "LARDE")

    fils = Homme("LHUILLIER", "Laurent").faitBebeAvec(Femme("LHUILLIER", "Manon"), Femme("CUNEY", "Nathalie"))
#    fils.faitBebeAvec(Femme("LHUILLIER", "Manon"), Femme("CUNEY", "Nathalie"))

    fille = Femme("BERNARD","Pascale")
    fille.faitBebeAvec(fils, Homme("LHUILLIER", "Michel"))
    pere.faitBebeAvec(fille, mere)

    fille = Femme("BERNARD","Claudine")
    fille.faitBebeAvec(Homme("FOURTOU", "Fabrice"), Homme("FOURTOU", "Claumi"))
    pere.faitBebeAvec(fille, mere)

    fille = Femme("BERNARD","Brigitte")
    fille.faitBebeAvec(Homme("JACQUES", "Christophe"), Homme("JACQUES", "Jean-Claude"))
    pere.faitBebeAvec(fille, mere)

#    pere.printIdentite()
    mere.printIdentite()


def exemple10():
    for x in range(1, 100):

        listeNombresPremiers = decomposePremiers(x)
        if len(listeNombresPremiers) == 1:
            print("%d est un nombre premier" % x)
        else:
            print(x, "=>", listeNombresPremiers)


def exemple11():
    name = input("Enter your name : ")
    print("Your name is = " + name)


def exemple12():
    a = 1
    b = 2
    a, b = b, a
    print(a, b)


def exemple13():
    """
    Recherche des nombres parfait
    :return: None
    """
    for x in range(1, 10000):
        somme = 0
        lsDiviseursPropres = decomposeDiviseurs(x)

        for y in lsDiviseursPropres:
            somme += y

        if x == somme:
            print("%d est un nombre parfait" % x)


def exemple14():
    """
    Tests des Fonctions sur liste
    :return:
    """
    couleurs = ["red", "green", "blue", "yellow", "green"]
    print("Liste : ", couleurs)
    print("Taille de la liste : {0}".format(couleurs.__len__()))

    s = "blue"
    print("Position de '%s' : %d" % (s, couleurs.index(s)))

    s = "orange"
    couleurs.append("orange")
    print("Ajout de la valeur '%s' dans la liste : " % s, couleurs)

    couleurs.pop(0)
    print("Suppression du premier élément de la liste : ", couleurs)

    couleurs.pop()
    print("Suppression du dernier élément de la liste : ", couleurs)

    s = "green"
    print("Compte le nombre de '%s' dans la liste : %d" % (s, couleurs.count(s)))

    l = ["pink", "red", "marron"]
    couleurs.extend(l)
    print("Ajout de la liste %s : " % l, couleurs)

    print("Extraction d'une partir de la liste [1:4:2] : ", couleurs[1:4:2])

    if True:
        lf = []

        lf.append(lambda x : 0)
        lf.append(lambda x : x)
        lf.append(lambda x : 2 * x)
        lf.append(lambda x : 3 * x)
        lf.append(lambda x : 4 * x)
    else:
        lf = [(lambda y: y * x) for x in range(5)]

    print("Fabrication liste par fonction x*y :")
    taille = len(lf)
    for i, f in enumerate(lf):
        print("Table des %d =" % i, [f(x) for x in range(10)])

    couleurs.clear()
    print("Suppression du contenu de la liste : ", couleurs)


exemple13()


# -------------------------------------------------------------------------------------------------------------------
print()
fin = time.perf_counter()
print("Duree = %f micro sec" % ((fin - debut) * 1000000))
