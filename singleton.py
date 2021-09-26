def singleton(classe):
    instances = {}
    
    def get_instance(*args, **kwargs):
        if classe not in instances:
            print(f"initialise singleton : {classe.__name__}{args}")
            instances[classe] = classe(*args, **kwargs)
        
        return instances[classe]
    
    return get_instance


class Operator:
    
    def __init__(self, operateur):
        if operateur == "+":
            self.operateur = self.somme
        elif operateur == "*":
            self.operateur = self.multiplication
        elif operateur == "/":
            self.operateur = self.division
        elif operateur == "@A":
            self.operateur = self.moyenneA
        elif operateur == "@G":
            self.operateur = self.moyenneG

    @staticmethod
    def somme(liste_valeurs):
        return sum(liste_valeurs)

    @staticmethod
    def moyenneA(liste_valeurs):
        if liste_valeurs:
            return sum(liste_valeurs)/len(liste_valeurs)
        else:
            return 0

    # @staticmethod
    def moyenneG(self, liste_valeurs):
        return pow(self.multiplication(liste_valeurs), 1/len(liste_valeurs))

    # @staticmethod
    def multiplication(self, liste_valeurs):
        res = 1
        for val in liste_valeurs:
            res *= val
        return res

    @staticmethod
    def division(liste_valeurs):
        res = liste_valeurs[0]
        for val in liste_valeurs[1:]:
            res /= val
        return res


@singleton
class Nombres(Operator):
    """Class Nombre()"""
    
    def __init__(self, *args):
        self.liste_val = args
    
    def __repr__(self):
        return f"Valeur = {self.liste_val}"
    
    def calcul(self, operateur):
        Operator.__init__(self, operateur)
        try:
            res = self.operateur(self.liste_val)
        except Exception as e:
            res = "{}".format(e)
        return res


ns = Nombres(7, 2, 1)
n = Nombres(3, 4, 5)

try:
    from utils.definition import printdef

    print(f"addition = {n.calcul('+')}")
    o = Nombres()
    print(f"multiplication = {o.calcul('*')}")
    print(f"Division = {o.calcul('/')}")
    print(f"moyenne arithmétique = {o.calcul('@A')}")
    print(f"moyenne géométrique = {o.calcul('@G')}")

    #printdef(m)

except Exception as e:
    print("Error")
    print(f"{e}")

from msvcrt import getch

# print("Press any key.", end="")
#getch()
