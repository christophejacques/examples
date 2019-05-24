# coding: utf-8
from math import sqrt

def ajoute_deux(v):
    return v + 2


def factoriel(n):
    """def factoriel recursif"""
    if n < 2:
        return 1
    else:
        return n * factoriel(n-1)


def factoriel2(n):
    """def factoriel incremental"""
    resultat = 1
    for i in range(2, n+1):
        resultat *= i

    return resultat

def decomposePremiers(n):
    """Décomposition en nombres premiers"""
    if n < 2:
        return [n]

    nb = n
    res = []
    x = 2
    while nb % x == 0:
        res.append(x)
        nb //= x

    x = 3
    while x <= sqrt(nb):
        while nb % x == 0:
            res.append(x)
            nb //= x
        else:
            x += 2

    if nb > 1:
        res.append(nb)

    if len(res) == 1:
        return [n]
        # print("%d est un nombre premier" % (n))
    else:
        return res
        # print("%d => %s" % (n, "{0}".format(res)))


def decomposeDiviseurs(n):
    """Décomposition en nombres divisant"""

    res = []
    for x in range(1, n):
        if n % x == 0:
            res.append(x)

    return res



def suppressionDoublons(liste):
    index = 0

    while len(liste) > index+1:
        if liste[index] == liste[index+1]:
            liste.pop(index)
        else:
            index += 1

    return liste

# print(suppressionDoublons([1, 2, 2, 3]) )
# print( decomposeDiviseurs(2) )