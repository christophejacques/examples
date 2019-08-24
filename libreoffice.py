import msvcrt

class LibreOfficeFile:

  def __init__(self):
    self.current_feuille = None
    self.feuilles = {}
  
  def save_colonne(self, num_col):
    if self.current_feuille:
      self.feuilles[self.current_feuille].append(num_col)
    else:
      print("Aucune feuille n'est active !")

  def ajouter_feuille(self, nom_feuille):
    if not nom_feuille in self.feuilles:
      self.current_feuille = nom_feuille
      self.feuilles[nom_feuille] = []

      self.save_colonne(5)
      self.save_colonne(7)
      self.save_colonne(2)

      print(f"Feuille : *{nom_feuille}* ajoutée")
      
    else:
      print(f"*{nom_feuille}* déjà présente avec {self.feuilles[nom_feuille]}")

  def restore_colonnes(self):
    print("restauration :")
    for feuille in self.feuilles:
      print(" ", feuille, end=" : ")
      for num_col in self.feuilles[feuille]:
        print(f"{num_col}, ", end="")
      print()
      
    self.feuilles.clear()
    print("colonnes restaurées !")
    
  def __enter__(self):
    return self
    
  def __exit__(self, *args):
    for i, arg in enumerate(args):
      if arg: print(i, arg)
      
    self.restore_colonnes()
  
  def __repr__(self):
    return f"print : {self.feuilles}\n"

try:
  with LibreOfficeFile() as fichier:

    fichier.ajouter_feuille("Feuille 1")
    fichier.ajouter_feuille("Feuille 2")

    print(fichier)
    
    a =1/10

except:
  pass

print(fichier)

msvcrt.getch()
