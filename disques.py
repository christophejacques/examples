import os
import sys
import shutil


def getScreenSize():
    global nb_colonnes
    try:
        nb_colonnes = shutil.get_terminal_size().columns
        # print(nb_colonnes)
    except OSError:
        nb_colonnes = 200


class Disk:
    __Dirs: list = []
    __Files: list = []

    level = ["Po", "To", "Go", "Mo", "Ko", "o "]
    size = [1024**i for i in range(len(level) - 1, -1, -1)]

    @staticmethod
    def int2human(entier: int) -> str:
        for i, maxi in enumerate(Disk.size):
            if entier >= maxi:
                return "{:.2f} {}".format(entier / maxi, Disk.level[i])
        return "0 o"

    @classmethod
    def __init__(self):
        self.__Dirs = []
        self.__Files = []
        self.directory = None

    @classmethod
    def read_directory(self):
        self.__init__()

        for element in os.scandir(self.repertoire):
            if element.is_dir():
                self.__Dirs.append(element)
            elif element.is_file():
                self.__Files.append(element)
            else:
                print("fichier non typé:", element.name)

    @classmethod
    def nb_dirs(self):
        return len(self.__Dirs)

    @classmethod
    def get_dirs(self):
        return [directory for directory in self.__Dirs]

    @classmethod
    def nb_files(self):
        return len(self.__Files)

    @classmethod
    def get_files(self):
        return [file for file in self.__Files]

    @classmethod
    def get_size(self):
        return sum([file.stat().st_size for file in self.__Files])

    @classmethod
    def dir(self, directory: str = "."):
        getScreenSize()
        self.repertoire = directory
        self.read_directory()
        if self.nb_dirs() > 0:
            print("Répertoires :", directory)

            taille = 1
            for rep in self.get_dirs():
                if len(rep.name) > taille:
                    taille = len(rep.name)
            taille += 2

            taille_ligne = 0
            for i, rep in enumerate(self.get_dirs()):
                nom_rep = ("{:" + str(taille) + "s} ").format(
                    "[{}]".format(rep.name))
                taille_ligne += len(nom_rep)
                if taille_ligne > nb_colonnes:
                    print()
                    taille_ligne = len(nom_rep)

                print(nom_rep, end="")

            if self.nb_files() > 0:
                print("\n")

        if self.nb_files() > 0:
            print("Fichiers :")

            taille = 1
            for fichier in self.get_files():
                if len(fichier.name) > taille:
                    taille = len(fichier.name)

            taille_ligne = 0
            for i, fichier in enumerate(self.get_files()):
                nom_fichier = ("{:" + str(taille) + "s}").format(fichier.name)
                nom_fichier += "{:>12s}    ".format(
                    Disk.int2human(fichier.stat().st_size))
                taille_ligne += len(nom_fichier)
                if taille_ligne >= nb_colonnes:
                    print()
                    taille_ligne = len(nom_fichier)

                print(nom_fichier, end="")

        print()

        res = f"\nTotal Reps: {self.nb_dirs()}, "
        res += f"Fichiers: {self.nb_files()}, "
        res += f"Taille Fichiers:"
        print(res, Disk.int2human(self.get_size()))


def main():
    d = Disk()
    d.dir(sys.argv[1] if len(sys.argv) == 2 else ".")


if __name__ == "__main__":
    main()
