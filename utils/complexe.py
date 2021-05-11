if __name__ != "__main__":
    print("loading complexe.py", end=" ... ")


from math import sqrt, atan2, degrees


class Complexe():
    """class Complexe()

    Methodes :
        def __init__(self, reel=0, imaginaire=0):

    Opérations :
        def __add__(self, other):
        def __sub__(self, other):
        def __len__(self):

    Comparaisons :
        def __lt__(self, other):
        def __le__(self, other):
        def __eq__(self, other):
        def __gt__(self, other):

    Restitutions :
        def __format__(self, format_spec):
        def __repr__(self):

    Attributs :
        reel
        imaginaire
        taille

    """

    def __init__(self, reel=0, imaginaire=0):
        """def __init__(self, reel=0, imaginaire=0):
    Constructeur de la class Complexe()
:param
    reel        : partie reel de type float
    imaginaire  : partie imaginaire de type float
    taille      : longueur de l'objet de type float
        """
        self.reel = reel
        self.imaginaire = imaginaire
        self.taille = sqrt(reel*reel + imaginaire*imaginaire)

    def __class_getitem__(cls, item):
        print("__class_getitem__(cls, item)")

    def __add__(self, other):
        """def __add__(self, other):
    utilisé lors de l'addition de 2 objets de type Complexe (self + other) avec l'operateur "+"
:param
    other : objet de type Complexe()
:return:
    objet de type Complexe()
"""
        return Complexe(self.reel + other.reel, self.imaginaire + other.imaginaire)

    def __sub__(self, other):
        """def __sub__(self, other):
    utilisé lors de la soustraction de 2 objets de type Complexe (self - other) avec l'operateur "-"
:param
    other : objet de type Complexe()
:return:
    objet de type Complexe()
"""
        return Complexe(self.reel - other.reel, self.imaginaire - other.imaginaire)

    def copy(self):
        return Complexe(self.reel, self.imaginaire)


    def __len__(self):
        """def __len__(self):
    retourne la longeur du Complexe
:return:
    int(sqrt(reel² + imaginaire²))
        """
        return int(sqrt(self.reel * self.reel + self.imaginaire * self.imaginaire))

    def __lt__(self, other):
        return self.taille < other.taille

    def __le__(self, other):
        return self.taille <= other.taille

    def __eq__(self, other):
        return self.taille == other.taille

    def __ge__(self, other):
        return self.taille >= other.taille

    def __gt__(self, other):
        return self.taille > other.taille

    def __format__(self, format_spec):
        """fonction appellee lors de l'utilisation de la fonction "".format()

        :param format_spec: parametre complementaire (reel, imaginaire)
        :return:
        """
        if format_spec.lower() == "reel":
            return f"{self.reel}"
        elif format_spec.lower() == "imaginaire":
            return f"{self.imaginaire}i"
        else:
            return f"{self.reel}+{self.imaginaire}i"

    def __repr__(self):
        """Method appelee lors d'un print()
        pour la représentation de la classe sous forme de chaine de caracteres
        """
        if self.imaginaire == 0:
            return f"{self.reel}"
        elif self.imaginaire < 0:
            return f"{self.reel}{self.imaginaire}i"
        else:
            return f"{self.reel}+{self.imaginaire}i"

    def angle(self, radian=False):
        """def angle(self):
:return:
    retourne l'angle défini par les coordonnées de l'objet
        """
        if radian:
            return atan2(self.imaginaire, self.reel)
        else:
            return degrees(atan2(self.imaginaire, self.reel))

if __name__ != "__main__":
    print("ok")

