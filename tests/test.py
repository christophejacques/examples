import typing
import sys

from typing import Type


# 1. Ajouter le dossier contenant le module au sys.path
# import os
# path_to_lib = os.path.abspath("../p5/lib")
path_to_lib = "../p5/lib"
if path_to_lib not in sys.path:
    sys.path.insert(0, path_to_lib)
    print(f"{path_to_lib!r} added to PATH.")

# p5 = __import__('p5')
# print(dir(p5))

# help(typing.Type)
# exit()

# for m in dir(typing):
#     if m[0] not in "AZERTYUIOPMLKJHGFDSQWXCVBN":
#         continue
#     print(m)

# exit()

class Unique:
    __instance = None

    def __new__(cls, *args, **kwargs):
        print("__new__", args, kwargs)
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, a: int, key: bool):
        # print("__init__", a)
        self.a = a
        self.key = key

    def print(self):
        print(self.a, self.key)


u1 = Unique(1, key=True)
u2 = Unique(2, key=False)

u1.print()
print(id(u1))

u2.print()
print(id(u2))
