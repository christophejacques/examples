from msvcrt import getch
from utils.colors import printXY
import _thread
import time
import sys


class Patience:
    
    def __init__(self):
        self.index = -1
    
    def __str__(self):
        self.index += 1
        if self.index >= 4: self.index = 0
        return ( "|", "/", "─", "\\" )[self.index]


class ClassProperty(property):
    
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class Keyboard:
    
    key_in_buffer = False
    touche = None
    special = None
    
    @classmethod
    def init(self):
        self.key_in_buffer = False
        self.touche = None
        self.special = None
    
    @classmethod
    def has_special(self):
        return self.special is not None
    
    @ClassProperty
    @classmethod
    def last_special(self):
        return self.special
        
    @ClassProperty
    @classmethod
    def last_key(self):
        return self.touche
        
    @classmethod
    def get_key(self):
        self.touche = getch()
        self.special = None
        if self.touche == b'\x00':
            self.special = getch()
            
        self.key_in_buffer = True
    
    @classmethod
    def print(self, x, y, spe=False):
        if self.has_special():
            chaine = "[*] {}    ".format(self.special)
        else:
            chaine = "{}    ".format(self.touche)
            
        printXY(x, y, "Key pressed is : {}".format(chaine))


def main():
    Keyboard.init()
    p = Patience()
    
    _thread.start_new_thread(Keyboard.get_key, ())
    line = 4
    while True:
        if Keyboard.key_in_buffer:
            Keyboard.print(2, 5)
            
            if Keyboard.has_special():
                if Keyboard.last_special == b'k': # Alt-F4
                    exit()
                    
            elif Keyboard.last_key in (b'q',      # 'q'
                        b'\x1b',   # Echap
                        b'\x03',   # Ctrl-c
                        b'\x17'):  # Ctrl-w
                exit()
                
            Keyboard.init()
            _thread.start_new_thread(Keyboard.get_key, ())

        printXY(2, 2, "Program is running ", p)
        printXY(2, 2, "", end="", flush=True)
        time.sleep(0.05)
 
 
if __name__ == "__main__":
    try:
        main()
        
    except Exception as e:
        print("Error:",e)
        getch()