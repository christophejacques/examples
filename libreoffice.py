import msvcrt
import random

print("loading LibreOfficeFile")

class LibreOfficeFile:

    def __init__(self, fdcr):
        self.fdcr = fdcr
        self.current_feuille = None
        self.feuilles = {}

    def save_colonne(self, num_col):
        if self.current_feuille:
            self.feuilles[self.current_feuille].append(num_col)

        else:
            print("Aucune feuille n'est active !")

    def ajouter_feuille(self, nom_feuille):
        if not nom_feuille in self.feuilles:
            self.current_feuille = nom_feuille
            self.feuilles[nom_feuille] = []
            fin = 0
            for i in range(random.randint(1, 5)):
                debut = random.randint(fin+1, fin+10)
                fin = debut + random.randint(1, 5)
                for col in range(debut, fin):
                    self.save_colonne(col)

            print(f"Feuille : *{nom_feuille}* ajoutée avec colonnes : {self.feuilles[nom_feuille]}")

        else:
            print(f"*{nom_feuille}* déjà présente avec {self.feuilles[nom_feuille]}")

    def restore_colonnes(self):
        print(f"restauration : {len(self.feuilles)} feuilles")
        for feuille in self.feuilles:
            print(" ", feuille, end=" : ")
            for num_col in self.feuilles[feuille]:
                print(f"{num_col}, ", end="")

            print()

        self.feuilles.clear()
        print("colonnes restaurées !")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        for i, arg in enumerate(args):
            if arg: print(i, arg)

        self.restore_colonnes()

    def __repr__(self):
        return f"print : {self.feuilles}\n"



try:
    with LibreOfficeFile("objFdCR") as fichier:

        for num in range(10):
            fichier.ajouter_feuille(f"Feuille {random.randint(2, 10)}")

        # print(fichier)

        a =1/10


except Exception as e:
    print(e)

print(fichier)

#msvcrt.getch()
