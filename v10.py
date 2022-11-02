from abc import abstractmethod, ABCMeta

print("Debut")


class Program(metaclass=ABCMeta):
    
    @abstractmethod
    def run(self):
        pass


class System(Program):

    def run(self):
        pass
        

s = System()


def dans(liste: list, *valeurs) -> bool:
    for valeur in valeurs:
        if valeur in liste:
            print("Param trouvé:", valeur)
            return True
    return False


def main(*params) -> None:
    if dans(("-f", "--force"), *params):
        print("dedans")
    else:
        print("Aucun parametre existant:", *params)
        

if __name__ == "__main__":
    try:
        main("--help", "-h")
        main("--force", "-f")

    except Exception as e:
        print("Error:", e)

print("Fin")
