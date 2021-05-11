class Form2D:

    version = "1.0"
    index = None
    __rayon = None

    @classmethod
    def __init__(self, vclasse):
        if self.index:
            vclasse.rayon = self.__rayon
        else:
            self.index = 1
            self.__rayon = vclasse.rayon
            
    def perimetre(self):
        return "p={}".format(self.index)
    
    def aire(self):
        return "a={}".format(self.index)
        
    def get_rayon(self):
        return self.__rayon

    
class Cercle(Form2D):
    
    def __init__(self, rayon):
        self.rayon = rayon
        print(f"init({self.rayon}) -> ", end="")
        Form2D.__init__(self)
        print(f"{self.rayon}", end=" : ")

    def get_rayon(self):
        print(dir(self))
        return Form2D.get_rayon(self)
    
try:    
  c = Cercle(2)
  print(c.get_rayon())
  d = Cercle(6)
  print(d.get_rayon())

except Exception as e:
  print("Erreur:", e)
  
input()
