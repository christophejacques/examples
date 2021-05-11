# coding: utf-8

if __name__ != "__main__":
    print("loading personnes.py", end=" ... ")

def IIf(boolean, siVrai, siFaux):
    return siVrai if boolean else siFaux


def siPluriel(nombre, strOui, strNon=""):
    if nombre > 1:
        return strOui
    else:
        return strNon


class Personne():
    """Documentation de la classe Personne()
    def __init__(self, nom, prenom):
    def nom(self):
    def nom(self, nom):
    def pere(self):
    def pere(self, nom):
    def mere(self):
    def mere(self, nom):
    def sexe(self):
    def printIdentite(self):
"""

    @property
    def sexe(self):
        """propriete sexe de la classe Personne()
        Ne doit jamais être utilisé directement
        :return:
        """
        return None

    def __init__(self, nom, prenom):
        """Constructeur Personne()
    :param nom:
    :param prenom:
        """
        self.pere = None
        self.mere = None
        self.nom = nom
        self.prenom = prenom
        self.__enfants = []

    @property
    def nom(self):
        """getter Nom()"""
        return self.__nom

    @nom.setter
    def nom(self, nom):
        """setter Nom()"""
        self.__nom = nom

    @property
    def pere(self):
        """getter pere()"""
        return self.__pere

    @pere.setter
    def pere(self, pere):
        """setter pere()"""
        self.__pere = pere

    @pere.deleter
    def pere(self):
        self.__pere = None

    @property
    def mere(self):
        """getter mere()"""
        return self.__mere

    @mere.setter
    def mere(self, mere):
        """setter mere()"""
        self.__mere = mere

    @mere.deleter
    def mere(self):
        self.__mere = None

    def printIdentite(self, indentation=0, enligne=False):
        """Impression identite"""

        if self.pere is None:
            strPere = "Père inconnu"
        else:
            strPere = "%s %s" % (self.pere.nom, self.pere.prenom)

        if self.mere is None:
            strMere = "Mère inconnue"
        else:
            strMere = "%s %s" % (self.mere.nom, self.mere.prenom)

        strParents = "(%s et %s)" % (strPere, strMere)

        espace = "".zfill(2*indentation).replace("0", " ")
        if enligne:
            strNom = "%s- %s" % (espace, self.nom)
            if self.sexe == "Femme":
                if self.nom != self.nomNaissance:
                    strNom = "%s (née %s)" % (strNom, self.nomNaissance)
            print("%s %s %s" % (strNom, self.prenom, strParents))

        else:
            print("%sPrénom : %s" % (espace, self.prenom))
            strNom = "%sNom    : %s" % (espace, self.nom)
            if self.sexe == "Femme":
                if self.nom != self.nomNaissance:
                    strNom = "%s (née %s)" % (strNom, self.nomNaissance)

            print("%s %s" % (strNom, strParents))

        nbenfants = len(self.__enfants)
        if nbenfants > 0:
            strPluriel = siPluriel(nbenfants, "s")
            print("%sListe de%s %d enfant%s" % (espace, strPluriel, nbenfants, strPluriel))

            for e in self.__enfants:
                e.printIdentite(indentation+1, True)
            # print()

    def faitBebeAvec(self, enfant, conjoint = None):
        """faitBebeAvec(enfant, conjoint = None):
    :param enfant:
    :param conjoint:
    :return:
"""
        if conjoint is None:
            if self.sexe == "Femme":
                enfant.mere = self
            else:
                enfant.pere = self

        else:
            enfant.mere = IIf(conjoint.sexe == "Femme", conjoint, self)
            enfant.pere = IIf(conjoint.sexe == "Homme", conjoint, self)

            """
            if conjoint.sexe == "Femme":
                enfant.mere = conjoint
                enfant.pere = self

            elif conjoint.sexe == "Homme":
                enfant.pere = conjoint
                enfant.mere = self
            """

            conjoint.__enfants.append(enfant)

        self.__enfants.append(enfant)
        return self


class Homme(Personne):
    """class Homme()
    dérive de la classe Personne()
"""
    @property
    def sexe(self):
        """getter sexe()"""
        return "Homme"


class Femme(Personne):
    """class Femme()
    dérive de la classe Personne()
"""
    def __init__(self, nom, prenom, nomNaissance = None):
        """Constructeur Femme()
    :param nom:
    :param prenom:
        """
        # Appel du Super Constructeur
        Personne.__init__(self, nom, prenom)

        if nomNaissance is None:
            self.nomNaissance = nom
        else:
            self.nomNaissance = nomNaissance

    @property
    def sexe(self):
        """getter sexe()"""
        return "Femme"

if __name__ != "__main__":
    print("ok")

