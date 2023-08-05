# coding: utf-8


class Matrice:

    def __init__(self, lignes, colonnes):
        self.lignes = lignes
        self.colonnes = colonnes

        self.cellule = []
        une_colonne = []

        for j in range(colonnes):
            une_colonne.append(0)

        for i in range(lignes):
            self.cellule.append(une_colonne.copy())

    def __add__(self, other):
        if self.lignes == other.lignes and self.colonnes == other.colonnes:
            res = Matrice(self.lignes, self.colonnes)
            for i in range(self.lignes):
                for j in range(self.colonnes):
                    res.cellule[i][j] = self.cellule[i][j] + other.cellule[i][j]
            return res

        else:
            raise Exception("Les 2 matrices ne sont pas de la même taille")

    def __sub__(self, other):
        if self.lignes == other.lignes and self.colonnes == other.colonnes:
            res = Matrice(self.lignes, self.colonnes)
            for i in range(self.lignes):
                for j in range(self.colonnes):
                    res.cellule[i][j] = self.cellule[i][j] - other.cellule[i][j]
            return res

        else:
            raise Exception("Les 2 matrices ne sont pas de la même taille")

    def __repr__(self):
        strformat = "{0:2}"
        res = "["
        for i in range(self.lignes-1):
            res += "("
            for j in range(self.colonnes-1):
                res += (strformat + ", ").format(self.cellule[i][j])

            res += (strformat + "), ").format(self.cellule[i][self.colonnes-1])

        res += "("
        for j in range(self.colonnes-1):
            res += (strformat + ", ").format(self.cellule[self.lignes-1][j])

        res += (strformat + ")]").format(self.cellule[self.lignes-1][self.colonnes-1])

        return res

    def set_val(self, ligne, colonne, valeur):
        self.cellule[ligne][colonne] = valeur

    def get_val(self, ligne, colonne):
        return self.cellule[ligne][colonne]


m = Matrice(4, 5)
n = Matrice(4, 5)

print("init")
print(m)
print(n)

print("eval")
for i in range(m.lignes):
    for j in range(m.colonnes):
        m.set_val(i, j, (i+1)*(j+1))
        n.set_val(i, j, (i+1)+(j+1))

print(m)
print(n)

print("add")
print(m+n)
