class C1:
    def __new__(self, *args):
        if self.__name__ != "C1":
            print("- New C1:", self.__name__, args)
        return super().__new__(self, *args)

    def __init__(self):
        self.c1 = "C1"


class C2:
    def __new__(self, *args):
        if self.__name__ != "C2":
            print("- New C2:", self.__name__, args)
        return super().__new__(self, *args)

    def __init__(self):
        self.c2 = "C2"


class C3(C1, C2):
    def __new__(self, *args):
        print("New:", self.__name__, args)
        return super().__new__(self, *args)

    def __init__(self):
        for classe in C3.__bases__:
            classe.__init__(self)

        for attrib in dir(self):
            if attrib[0] != "_":
                print(f'self.{attrib} = {getattr(self, attrib)}')


c1 = C1()
c2 = C2()

c3 = C3()
