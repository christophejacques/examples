from threading import Thread
from time import sleep

MONOTACHE=1
MULTITACHE=2


def somme(a, b):
    print(f"- {a} + {b} = ", end="")
    sleep(1)
    c = a + b
    print(f"{c}", end=" - ")
    sleep(1)


def multiplication(a, b):
    print(f"- {a} x {b} = ", end="")
    sleep(1)
    c = a * b
    print(f"{c}", end=" - ")
    sleep(1)


def division(a, b):
    print(f"- {a} / {b} = ", end="")
    sleep(1)
    c = a // b
    print(f"{c}", end=" - ")
    sleep(1)
    c = a % b
    print(f"reste {c}", end=" - ")
    sleep(1)


def message(texte):
    for x in texte:
        sleep(0.1)
        print(x, end="")
    print()


class uneTache(Thread):

    def __init__(self, mode, fonction, *args):
        Thread.__init__(self)
        self.mode = mode
        self.fonction = fonction
        self.params = args

    def run(self):
        self.fonction(*self.params)
        self.end()

    def end(self):
        if self.mode == MULTITACHE:
            print(f"Fin du {self.getName()} : *{self.fonction.__name__}*")
        else:
            print("Fini !")


class mesTaches:

    def __init__(self, mode=MONOTACHE):
        self.liste = []
        self.mode = mode
        self.running = False

    def add(self, mode, fonction, *args):
        if self.is_running():
            print("Traitements en cours ...")
            return

        self.liste.append(uneTache(mode, fonction, *args))

    def clear(self):
        self.liste.clear()

    def is_running(self):
        res = False
        for t in self.liste:
            res = res or t.isAlive()

        return res

    def run(self):
        if self.is_running():
            print("Traitements en cours ...")
            return

        for t in self.liste:
            if t.mode == MONOTACHE:
                print(f"Début du {t.getName()} avec *{t.fonction.__name__}* en MONO-TACHE", end=" ")
                t.start()
                t.join()

        for t in self.liste:
            if t.mode == MULTITACHE:
                print(f"Début du {t.getName()} avec *{t.fonction.__name__}* en MULTI-TACHE")
                t.start()

        if self.mode == MONOTACHE:
            for t in self.liste:
                if t.mode == MULTITACHE:
                    t.join()

        self.clear()


lst = mesTaches()

lst.add(MONOTACHE, somme, 7, 12)
lst.add(MONOTACHE, multiplication, 3, 7)
lst.add(MULTITACHE, message, "Comment allez vous ?")
lst.add(MONOTACHE, message, "il était une fois l'èsoîse")

lst.run()
print("Suite/Fin du code ...")

lst1 = mesTaches()
lst1.add(MULTITACHE, message, "Salut les copains de la terre promise du lendemain")
lst1.add(MULTITACHE, division, 27, 5)
lst1.run()

print("Fin du code ...")
