
class C:
    N: int = 0

    def __init__(self):
        C.N += 1
        print("Auto exec")

    def print(self):
        print(f"C.print({self.N})")

    def var(self, a, b):
        pass


print("debut")
c = C()
c.print()
d = C()
d.print()
d.var(0, 1)
print("fin")
