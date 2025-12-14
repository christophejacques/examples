from functools import singledispatch

class UneClasse: ...
class DeuxClasse: ...


@singledispatch
def traiter_donnee(data):
  """Fonction de base pour traiter une donnée."""
  print(f"le type {data.__class__} n'est pas géré par la fonction 'traiter_donnee'")
  # raise Exception(f"le type {data.__class__} n'est pas géré par la fonction 'traiter_donnee'")

@traiter_donnee.register(UneClasse)
def _(data):
  print(f"Traitement spécifique pour UneClasse")

@traiter_donnee.register(int)
def _(data):
  print(f"Traitement spécifique pour un entier : {data + 10}")

@traiter_donnee.register(float)
def _(data):
  print(f"Traitement spécifique pour un float : {data}")

@traiter_donnee.register(str)
def _(data):
  print(f"Traitement spécifique pour une chaîne : {data.upper()}")

@traiter_donnee.register(list)
def _(data):
  print(f"Traitement spécifique pour une liste : {', '.join(map(str, data))}")

@traiter_donnee.register(set)
def _(data):
  print(f"Traitement spécifique pour un set : {data}")

@traiter_donnee.register(dict)
def _(data):
  print(f"Traitement spécifique pour un dict : {data}")


traiter_donnee(15)
traiter_donnee(1.5)
traiter_donnee("bonjour")
traiter_donnee([1, 2, 3])
traiter_donnee({1, 2, 3})
traiter_donnee({"a":1, "b":2, "c":3})
traiter_donnee(UneClasse())

traiter_donnee(DeuxClasse())

