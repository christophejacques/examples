from abc import abstractmethod, ABCMeta

print("Debut")


class Program(metaclass=ABCMeta):
  
  @abstractmethod
  def run(self):
    pass


class System(Program):

  def run(self):
    pass
    


s = System()

def dans(liste : list, *valeurs) -> bool:
  for valeur in valeurs:
    if valeur in liste:
      print("found:", valeur)
      return True
  return False

def main() -> None:
  if dans(("-f", "--force"), "--force", "-f"):
    print("dedans")
  else:
    print("Aucun parametre trouvé")
    


if __name__ == "__main__":
  try:
    main()
  except Exception as e:
    print("Error:", e)



print("Fin")
