class mon_iterateur:

    def __init__(self, debut, fin):
        self.debut = debut
        self.fin = fin

    def __iter__(self):
        return self

    def __next__(self):
        courant = self.debut
        if self.debut > self.fin:
            raise StopIteration

        self.debut += 1
        return courant


print("Iterateur :", end="")
mi = mon_iterateur(3, 6)
for i in mi:
    print(i," ", end="")


def mon_generateur(debut, fin):
    valeur = debut
    while valeur <= fin:
        yield valeur
        valeur += 1

print()
print("Générateur :", end="")

for g in mon_generateur(4, 8):
    print(g, " ", end="")
print()
