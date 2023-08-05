# definition d'un decorateur
def decorateur(fonction):

    def methode(*args, **kvargs):
        print(f"Exec {fonction.__name__}{args}", end='')
        res = fonction(*args, **kvargs)
        print(f" = {res}")

        return res

    return methode


class mon_iterateur:

    @decorateur
    def __init__(self, debut, fin=None):
        if type(debut) != int:
            raise TypeError("Le 1er paramêtre n'est pas de type Entier")

        if fin is not None and type(fin) != int:
            raise TypeError("Le 2ème paramêtre n'est pas de type Entier")

        if fin is None:
            self.debut = 1
            self.fin = debut
        else:
            self.debut = debut
            self.fin = fin

    def __iter__(self):
        return self

    def __next__(self):
        courant = self.debut
        if self.debut > self.fin:
            raise StopIteration

        self.debut += 1
        return courant


@decorateur
def mon_generateur(debut, fin=None):
    if type(debut) != int:
        raise TypeError("Le 1er paramêtre n'est pas de type Entier")

    if fin is not None and type(fin) != int:
        raise TypeError("Le 2ème paramêtre n'est pas de type Entier")

    if fin is None:
        fin = debut
        debut = 1

    valeur = debut
    while valeur <= fin:
        yield valeur
        valeur += 1


print("Iterateur : ", end="")
for i in mon_iterateur(4):
    print(i, end=" ")

print("\nGénérateur : ", end="")
for g in mon_generateur(4):
    print(g, end=" ")

print()
try:
    pass
except Exception as e:
    print("Erreur:", e)
