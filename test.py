

class Test:
  un_attribut = 0
  un_nom = "Class Test"

  def __init__(self):
    self.un_nom = "nom init"

  def procedure(self):
    return "procedure"

  def methode(self):
    return "methode"

  def somme(self, a : int, b : int):
    return a+b



try:
  from utils.definition import printdef

  t = Test()
  printdef(t)

except Exception as e:
  print("Error")
  print(f"{e}")


from msvcrt import getch
print("Press any key.")
# getch()
