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

    def print(self):
        print(self.a)


u1 = Unique(1, key=True)
u2 = Unique(2, key=False)

u1.print()
print(id(u1))

u2.print()
print(id(u2))
