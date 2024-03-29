from abc import ABCMeta, abstractmethod


class Operator(metaclass=ABCMeta):
    
    def __init__(self, p1):
        print("Operator __init__({})".format(p1))

    @abstractmethod
    def getName(self, p1):
        pass

    def setName(self, p1):
        print("Operator setName({})".format(p1))


class Nombres(Operator):
    
    def __init__(self, p2):
        # Operator.__init__(self, p2)
        super().__init__(p2)
        print("Nombres __init__({})".format(p2))
    
    def getName(self, p1):
        """Doit etre redéclarée dans la classe Nombre sinon Erreur d'instanciation"""
        print("Nombres getName({})".format(p1))


try:
    n = Nombres(5)
    n.setName(1)
    n.getName(1)

except Exception as e:
    print("Error")
    print(f"{e}")
