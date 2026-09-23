from collections import namedtuple


# Définition du namedtuple (nom du type, liste des champs)
Personne = namedtuple('Personne', ['nom', 'age', 'ville'])


# Création d'une instance
p1 = Personne(nom='Alice', age=30, ville='Paris')

# Accès aux champs par attribut ou par index
print(p1.nom)      # Alice
print(p1.age)      # 30
print(p1[2])       # Paris

# Déstructuration (unpacking) directe
nom, age, ville = p1
print(f"{nom} a {age} ans et habite à {ville}.")
