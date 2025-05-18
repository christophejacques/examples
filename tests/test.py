import json


class Registres:
    __filename: str = "registres.json"
    __data: dict

    def __init__(self, application: str):
        self.clear()
        self.__application = application
        self.load_file()

    def load_file(self) -> None:
        try:
            with open(self.__filename) as reg:
                self.__data = json.load(reg).get(self.__application, {})

        except FileNotFoundError as fnfe:
            print("Initialisation de la base de registres")
            with open(self.__filename, "w") as reg:
                json.dump({}, reg)
                self.__data = dict()

    def save_file(self) -> None:
        with open(self.__filename) as reg:
            self.__reg = json.load(reg)

        self.__reg[self.__application] = self.__data
        with open(self.__filename, "w") as reg:
            json.dump(self.__reg, reg)

    def clear(self) -> None:
        self.__data = dict()

    def load(self, chemin_registre) -> object:
        res : dict = self.__data
        for registre in chemin_registre.split("."):
            res = res.get(registre, None)
            if res is None:
                return

        return res

    def save(self, chemin_registre, valeur) -> None:
        res : dict = self.__data

        # Creation / Recuperation des informations du chemin_registre
        for registre in chemin_registre.split(".")[:-1]:
            temp = res.get(registre, None)
            if temp is None:
                res[registre] = dict()
                res = res.get(registre, {})
            else:
                res = temp

        # Creation / Mise a jour de la cle de registre finale
        registre = chemin_registre.split(".")[-1]
        res[registre] = valeur


if __name__ == "__main__":
    print("Initialisation de la base de registres pour l'application: UnitTest")
    reg = Registres("UnitTest")

    print("Chargement des données de la base de registres")
    reg.load_file()

    print("Ajout d'une clé de registre simple")
    titre = "test de fonctionnalite"
    reg.save("titre", titre)

    print("Ajout d'une clé de registre multiple")
    propriete_titre = "Ballet de lignes"
    reg.save("proprietes.titre", propriete_titre)

    print("controle de la récupération des valeurs")
    assert titre == reg.load("titre")
    assert propriete_titre == reg.load("proprietes.titre")

    print("Suppression des données de la base de registre")
    reg.clear()
    # reg.save_file()

    print("Fonctionnement : OK")
