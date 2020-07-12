
class ma_liste:
    
    def __init__(self, liste=[]):
        
        self.liste = liste
        self.idx_max = -1
        self.debut = 0
    
    def __getitem__(self, index):
        if index > self.idx_max:
            raise IndexError(f"Index {index} out of range")
        return self.liste[index]
        
        
    def __setitem__(self, index, valeur):
        if index > self.idx_max:
            raise IndexError(f"Index {index} out of range")
        self.liste[index] = valeur
    
    def __delitem__(self, index):
        if index > self.idx_max:
            raise IndexError(f"Index {index} out of range")
        self.idx_max -= 1
        del self.liste[index]
    
    def __iter__(self):
        # print("__iter__: ", end="")
        self.debut = 0
        return self

    def __next__(self):
        courant = self.debut
        if self.debut > self.idx_max:
            raise StopIteration

        self.debut += 1
        return self.liste[courant]
        
    def __len__(self):
        return self.idx_max+1
        
    def __str__(self):
        return f"{self.__len__()} items: {self.liste}"
        
    def append(self, valeur):
        self.liste.append(valeur)
        self.idx_max += 1

    def clear(self):
        self.__init__([])
        
    def copy(self):
        return self.liste.copy()

    def count(self):
        return self.idx_max+1
        
    def extend(self, autre_liste):
        if type(autre_liste) == type([]):
            self.liste.extend(autre_liste)
            self.idx_max += len(autre_liste)
        else:
            raise TypeError(f"Le paramètre {autre_liste} n'est pas de type liste")
            
    def index(self, valeur):
        return self.liste.index(valeur)
        
    def insert(self, index, valeur):
        if index <= self.idx_max and index >= 0:
            self.liste.insert(index, valeur)
        
    def pop(self, numero=None):
        if numero is None:
            res = self.liste.pop(self.idx_max)
        else:
            res = self.liste.pop(numero)
        
        self.idx_max -= 1
        return res
        
    def remove(self, valeur):
        self.liste.remove(valeur)
        
    def reverse(self):
        self.liste.reverse()
        

try:
    l = ma_liste()
    for i in l: print(i, end=", ")
    print()
    l.append("un")
    l.append("deux")
    l.append("trois")
    l.append("quatre")
    print(l.index("deux"))
    
    print(l)
    l[0] = "zero"
    print(l)
    for i in l: print(i, end=", ")
    print()
    del l[1]
    print(l)
    
    print("\nclear")
    l.clear()
    print(l)
    
    l.extend([9,5,1])
    print(l)
    print("Remove :", l.pop())
    print(l)
    
except Exception as e:
    print("Error:", e)
    
from msvcrt import getch
#getch()