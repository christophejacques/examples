if __name__ != "__main__":
  print("loading taches.py ... ", end="")

from threading import Thread
from time import sleep
from msvcrt import getch
import traceback

# ---------------------------------------------------------
#
# codage UTF-8 des instruction affichée via commande print()
# 
import sys, codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
# ---------------------------------------------------------

DEBUG=True
MONOTACHE=1
MULTITACHE=2

def fprint(*args, **kwargs):
  print(*args, flush=True, **kwargs)


def type_tache(mode):
  return "Mono" if mode == MONOTACHE else "Multi"


def somme(a, b):
    fprint(f"- {a} + {b} = ", end="")
    sleep(0.1)
    c = a + b
    fprint(f"{c}")
    sleep(0.1)


def soustraction(a, b):
    fprint(f"- {a} - {b} = ", end="")
    sleep(0.1)
    c = a - b
    fprint(f"{c}")
    sleep(0.1)


def multiplication(a, b):
    fprint(f"- {a} x {b} = ", end="")
    sleep(0.1)
    c = a * b
    fprint(f"{c}")
    sleep(0.1)


def division(a, b):
    fprint(f"- {a} / {b} = ", end="")
    sleep(0.1)
    c = a // b
    fprint(f"{c}", end=" - ")
    sleep(0.1)
    c = a % b
    fprint(f"reste {c}")
    sleep(0.1)

def mon_input():
  t = None
  while t != b'\x1b':
    fprint("Appuyer sur 'Echap' : ", end ="")
    sleep(0.1)
    t = getch()
    fprint(f"*{t}*")
    sleep(0.1)

def fonction_callback():
  if DEBUG:
    print("fonction_callback()")


def fonctionretour(numero, fonction):
    def fonction_groupe():
        if DEBUG: fprint(f"Return groupes : {numero}, func : {fonction.__name__}", end="")
        
    return fonction_groupe


def message(texte):
    fprint("- ", end="")
    for x in texte:
        sleep(0.01)
        fprint(x, end="")
    #fprint()


class uneTache(Thread):

    def __init__(self, mode, returnfunc, fonction, *args):
      Thread.__init__(self)
      self.mode = mode
      self.returnfunc = returnfunc
      self.fonction = fonction
      self.params = args

    def run(self):
      if DEBUG: fprint(f"  Début du {self.getName()} en {type_tache(self.mode)} avec *{self.fonction.__name__}*", end=" ")
      self.fonction(*self.params)
      self.end()

    def end(self):
      if DEBUG:
        if self.mode == MULTITACHE:
          fprint(f"  Fin du {self.getName()} : *{self.fonction.__name__}* ", end="")
        else:
          fprint("  Fini ! ", end="")

      if self.returnfunc:
        self.returnfunc()
      fprint()


class Processeur:
    """Processeur()"""
    def __init__(self):
      self.num_groupe = -1
      self.nb_taches = 0
      self.groupes = []

      self.running = False

    def add_groupe(self, mode=MONOTACHE):
      self.num_groupe += 1

      if DEBUG:
        fprint(f"Creation groupes({self.num_groupe}) en {type_tache(mode)}")

      self.groupes.append({"num":self.num_groupe,
        "mode":mode,
        "liste_taches" : []})

      return self.num_groupe
    

    def add_to_group(self, mode, fonction, *args):
      self.add_tache(self.num_groupe, mode, fonction, *args)

    def add_tache(self, num_groupe, mode, fonction, *args):
      if self.is_running():
        fprint("Traitements en cours ...")
        return

      t = uneTache(mode, fonctionretour(self.num_groupe, fonction), fonction, *args)
      # t = uneTache(mode, fonction_callback, fonction, *args)
      if DEBUG:
        fprint(f"  Ajout {t.getName()}  en {type_tache(mode)} : {fonction.__name__}{args}")
      self.groupes[num_groupe]["liste_taches"].append(t)
      self.nb_taches += 1

    def __enter__(self):
      return self

    def __exit__(self, *args):
      pass

    def clear(self):
      self.liste.clear()

    def is_running(self):
      res = False
      for g in self.groupes:
        for t in g["liste_taches"]:
          res = res or t.is_alive() # isAlive()

      return res

    def end(self, num_groupe):
      if DEBUG: fprint(f"Fin groupes({num_groupe})\n")

    def run(self):
      if self.is_running():
          fprint("Traitements en cours ...")
          return

      # Gestion des groupes MONOTACHE
      for g in self.groupes:
        if g["mode"] == MONOTACHE:
          if DEBUG:
            fprint(f"Debut groupes({g['num']})")

          for t in g["liste_taches"]:
            if t.mode == MONOTACHE:
              t.start()
              t.join()

          for t in g["liste_taches"]:
            if t.mode == MULTITACHE:
              t.start()

          for t in g["liste_taches"]:
            if t.mode == MULTITACHE:
              t.join()

          self.end(g["num"])

      # Gestion des groupes MULTITACHE
      for g in self.groupes:
        if g["mode"] == MULTITACHE:
          if DEBUG:
            fprint(f"Debut groupes({g['num']})")

          for t in g["liste_taches"]:
            if t.mode == MONOTACHE:
              t.start()
              t.join()

          for t in g["liste_taches"]:
            if t.mode == MULTITACHE:
              t.start()

      # Gestion de la fin des groupes MULTITACHE
      for g in self.groupes:
        if g["mode"] == MULTITACHE:
          for t in g["liste_taches"]:
            if t.mode == MULTITACHE:
              t.join()

          self.end(g["num"])


if __name__ != "__main__":
  print("ok")

else:

  try:
    p = Processeur()
    p.add_groupe()
    p.add_to_group(MONOTACHE, message, "Premier groupes")
    p.add_to_group(MULTITACHE, message, "Premiere tache")
    p.add_to_group(MONOTACHE, somme, 5, 2)
    p.add_to_group(MULTITACHE, message, "Deuxieme tache")
    p.add_to_group(MONOTACHE, soustraction, 13, 5)
    #p.add_to_group(MONOTACHE, mon_input)

    p.add_groupe(MULTITACHE)
    p.add_to_group(MULTITACHE, message, "Deuxieme groupes")
    p.add_to_group(MULTITACHE, multiplication, 5, 2)

    p.add_groupe(MULTITACHE)
    p.add_to_group(MULTITACHE, message, "Troisieme groupes")
    p.add_to_group(MULTITACHE, division, 7, 3)

    fprint()
    p.run()

  except Exception as e:
    fprint()
    traceback.print_exc()

  else:
    fprint("Fin du code ...")

    # getch()
