import sys
from pathlib import Path

# 1. Ajouter le dossier contenant le module au sys.path
path_to_lib = Path("..", "p5", "lib")

if path_to_lib not in sys.path:
    sys.path.insert(0, f"{path_to_lib}")
    print(f"{path_to_lib} added to PATH.")


class Unique:
    __instance = None

    def __new__(cls, *args, **kwargs):
        print("__new__", cls, args, kwargs)
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, a: int, key: bool):
        self.a, self.key = a, key        

    def print(self):
        print(self.a, self.key)


u1 = Unique(1, key=True)
u2 = Unique(2, key=False)

u1.print()
u2.print()
