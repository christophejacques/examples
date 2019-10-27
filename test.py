def singleton(classe):
    instances = {}
    
    def get_instance(*args, **kwargs):
        if classe not in instances:
            instances[classe] = classe(*args, **kwargs)
        
        return instances[classe]
    
    return get_instance


@singleton
class MyClass():
    
    def __init__(self, *args):
        print(f"{self.__class__.__name__}.__init__{args}")
        self.liste_val = args
    
    def __repr__(self):
        return f"Valeur = {self.liste_val}"


m = MyClass(1, 2)
n = MyClass(3, 4, 5)
o = MyClass()
print(m)
print(n)


class Test():
    un_attribut = 0
    un_nom = "Class Test"
    
    def __init__(self):
        self.un_nom = "nom init"
    
    def procedure(self):
        return "procedure"
    
    def methode(self):
        return "methode"
    
    def somme(self, a: int, b: int):
        return a + b


try:
    from utils.definition import printdef
    
    t = Test()
    # printdef(t)

except Exception as e:
    print("Error")
    print(f"{e}")

from msvcrt import getch

print("Press any key.", end="")
# getch()
