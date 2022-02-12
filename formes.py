import math
from abc import ABCMeta, abstractmethod


class CoordonneesError(Exception):
    pass


class Forme(metaclass=ABCMeta):
    """Définition d'une Forme à x points"""
    nb_points = 0

    def __init__(self, coords: set):
        nb = len(coords)
        if nb != self.nb_points * 2:
            raise CoordonneesError("Le nombre de coordonnées ne correspond pas à la forme: "
                f"{nb} coordonnées au lieu de {2*self.nb_points} ({self.__class__.__name__})")
        if sum([0 if type(x) in (int, float) else 1 for x in coords]) > 0:
            raise TypeError("Les coordonnées doivent être de type numérique")
        self.coords = coords

    def __str__(self):
        res = self.__class__.__name__ + "(coords=("
        for idx in range(self.nb_points-1):
            x, y = self.coords[2*idx:2*idx+2]
            res += f"({x}, {y}), "
        idx += 1
        x, y = self.coords[2*idx:2*idx+2]
        res += f"({x}, {y})))"
        return res

    @abstractmethod
    def perimetre(self):
        pass

    @abstractmethod
    def aire(self):
        pass


class Cercle(Forme):
    """Définition d'un cercle de rayon r
    coords : Liste des coordonnées des points du rayon (x, y)

    def aire() -> float
    def perimetre() -> float
    """
    nb_points = 2

    @property
    def rayon(self):
        return Ligne(self.coords).perimetre()

    def perimetre(self):
        """Calcul du périmètre d'un cercle : 2.PI.r"""
        return self.rayon * math.pi * 2

    def aire(self):
        """Calcul de l'aire d'un cercle : PI.r²"""
        return self.rayon * self.rayon * math.pi


class Ligne(Forme):
    """Definition d'une Forme à 1 points"""
    nb_points = 2

    def perimetre(self):
        x1, y1, x2, y2 = self.coords
        dx = abs(x2-x1)
        dy = abs(y2-y1)
        return math.sqrt(dx*dx + dy*dy)

    def aire(self):
        return None


class Triangle(Forme):
    """Definition d'une Forme à 3 points

    coords : Liste des coordonnées des points de la forme (x, y)

    def aire() -> float
    def perimetre() -> float
    """
    nb_points = 3

    def perimetre(self):
        """Calcul du périmètre d'un rectangle (a + b + c)"""
        a = Ligne(self.coords[:4]).perimetre()
        b = Ligne(self.coords[2:]).perimetre()
        c = Ligne(self.coords[:2]+self.coords[-2:]).perimetre()
        return a + b + c

    def aire(self):
        """Calcul de l'aire d'un rectangle
        s = (a + b + c) / 2
        A = sqrt(s.(s-a).(s-b).(s-c))
        """
        a = Ligne(self.coords[:4]).perimetre()
        b = Ligne(self.coords[2:]).perimetre()
        c = Ligne(self.coords[:2]+self.coords[-2:]).perimetre()
        ds = (a + b + c) / 2

        return math.sqrt(ds*abs(ds-a)*abs(ds-b)*abs(ds-c))


class Quadrilataire(Forme):
    """Definition d'une Forme à 4 points"""
    nb_points = 4


class Rectangle(Quadrilataire):
    """Sous-classe de Quadrilataire :
    Definition d'une Forme à 4 points
    dont les 2 cotés ayant le même sommet ont leur 2 cotés opposés de parrallele
    et dont tous les angles sont de 90°

    coords : Liste des coordonnées des points de la forme (x, y)

    def aire() -> float
    def perimetre() -> float
    """

    def perimetre(self) -> float:
        """Calcul du périmètre d'un rectangle (2x(l + L)"""
        x1, y1, x2, y2, x3, y3 = self.coords[:6]
        return 2*(Ligne((x1, y1, x2, y2)).perimetre() + Ligne((x3, y3, x2, y2)).perimetre())

    def aire(self) -> float:
        """Calcul de l'aire d'un rectangle (l x L)"""
        x1, y1, x2, y2, x3, y3 = self.coords[:6]
        return Ligne((x1, y1, x2, y2)).perimetre() * Ligne((x3, y3, x2, y2)).perimetre()


class Carre(Rectangle):
    """Sous-classe de Rectangle :
    Definition d'une Forme à 4 points dont tous les cotés ont la même taille
    et dont tous les angles sont de 90°

    coords : Liste des coordonnées des points du carré 4x(x, y)

    def aire() -> float
    def perimetre() -> float
    """

    def aire(self) -> float:
        """Calcul de l'aire d'un carré (l²)"""
        x1, y1, x2, y2 = self.coords[:4]
        longeur = Ligne((x1, y1, x2, y2)).perimetre()
        return longeur*longeur

    def perimetre(self) -> float:
        """Calcul du périmètre d'un carré (2xl)"""
        x1, y1, x2, y2 = self.coords[:4]
        return 2 * Ligne((x1, y1, x2, y2)).perimetre()


def main1():
    t = Triangle((0, 0, 0, 5, 2, 3,))
    print(t)
    print("- Périmètre:", t.perimetre())
    print("- Aire:", t.aire(), "\n")

    r = Rectangle((0, 0, 2, 0, 2, 1, 0, 1))
    print(r)
    print("- Périmètre:", r.perimetre())
    print("- Aire:", r.aire(), "\n")

    r = Carre((0, 0, 2, 0, 2, 2, 0, 2))
    print(r)
    print("- Périmètre:", r.perimetre())
    print("- Aire:", r.aire(), "\n")

    c = Cercle((0, 0, 0, 5))
    print(c)
    print("- Périmètre:", c.perimetre())
    print("- Aire:", c.aire(), "\n")


if __name__ == '__main__':
    main1()
