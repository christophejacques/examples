# coding: utf-8

if __name__ != "__main__":
    print("loading operation.py", end=" ... ")


def ajoute_deux(v: int) -> int:
    return v + 2


def factoriel(n: int) -> int:
    """def factoriel recursif"""
    if n < 2:
        return 1
    else:
        return n * factoriel(n-1)


def factoriel2(n: int) -> int:
    """def factoriel incremental"""
    resultat = 1
    for i in range(2, n+1):
        resultat *= i

    return resultat


def decomposePremiers(n: int) -> list[int]:
    """Décomposition en nombres premiers"""
    if n < 2:
        return [n]

    nb = n
    res = []
    x = 2
    while nb & 1 == 0:
        res.append(x)
        nb //= 2

    x = 3
    while x*x <= nb:
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


def decomposeDiviseurs(n: int) -> list[int]:
    """Décomposition en nombres divisant"""

    res = []
    for x in range(1, n):
        if n % x == 0:
            res.append(x)

    return res


def suppressionDoublons(liste: list) -> list:
    index = 0

    while len(liste) > index+1:
        if liste[index] == liste[index+1]:
            liste.pop(index)
        else:
            index += 1

    return liste


if __name__ == "__main__":
    import time
    debut = time.perf_counter()

    try:
        liste = [1, 2, 2, 3]
        print(suppressionDoublons(liste))
        print(list(set(liste)))
        print(decomposeDiviseurs(200))

        print(decomposePremiers(200))
        
        print(decomposePremiers(321_180_009_873_217))
        
        print("\nDurée: {0:.2f}s".format(time.perf_counter()-debut))

    except Exception as e:
        print(f"Erreur: {e}")
        
