from msvcrt import getch
from utils.colors import printXY
from threading import Thread
import time
import sys
import traceback

class Patience:
    
    def __init__(self, index=-1):
        self.index = index
    
    def __str__(self):
        self.index += 1
        if self.index >= 4: self.index = 0
        return ( "|", "/", "─", "\\" )[self.index]


class ClassProperty(property):
    
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class Keyboard:
        
    @classmethod
    def init(self):
        self.__keypressed = False
        self.__touche = None
        self.__special = None
        Thread(target=self.wait_key).start()
    
    @classmethod
    def get_key(self):
        self.__keypressed = False
        touche, self.__touche = self.__touche, None
        special, self.__special = self.__special, None
        Thread(target=self.wait_key).start()
        return (touche, special)
    
    @classmethod
    def keypressed(self):
        return self.__keypressed
    
    @classmethod
    def has_special(self):
        return self.__special is not None
    
    @ClassProperty
    @classmethod
    def key(self):
        return self.__touche
        
    @ClassProperty
    @classmethod
    def special(self):
        return self.__special
        
    @classmethod
    def wait_key(self):
        self.__touche = getch()
        self.__special = None
        if self.__touche in (b'\x00', b'\xe0'): # b'\xe0' pour F11, F12
            self.__special = getch()
            
        self.__keypressed = True
    
    @classmethod
    def print(self, x, y):
        if self.has_special():
            chaine = "[{}] {}    ".format(self.__touche, self.__special)
        else:
            chaine = "{}                  ".format(self.__touche)
            
        printXY(x, y, "Key pressed is : {}".format(chaine), end="")


def main():
    Keyboard.init()
    tp = []
    for i in range(4):
        tp.append( Patience(i) )
    x, minx = (40,) *2
    y, miny = (2, ) *2
    maxx = 140
    maxy = 10
    line = 4
    tick = 0
    while True:
        if Keyboard.keypressed():
            Keyboard.print(4, line)
            printXY(4, line+1, " " * 32)
            if line >= 20:
                line = 4
            else:
                line += 1
            
            #k, s = Keyboard.get_key()
            if Keyboard.has_special():
                if Keyboard.special == b'k': # Alt-F4
                    exit()
                    
            elif Keyboard.key in (#b'q',      # 'q'
                        b'\x1b',   # Echap
                        b'\x03',   # Ctrl-c
                        b'\x17'):  # Ctrl-w
                exit()
                
            Keyboard.init()
            

        printXY(2, 2, "Program is running ")
        for i in range(4):
            printXY(24+2*i, 2, tp[i])
            
        tick += 1
        if tick == 10:
            tick = 0
            printXY(x, y, " " * 4, end="", flush=True)
            x += 1
            if x > maxx:
                x = minx +1 
                y += 1
                if y > maxy:
                    y= miny
                    
            printXY(x, y,  (x-minx) + (y-miny)*(maxx-minx), end="", flush=True)
        time.sleep(0.01)
 
 
if __name__ == "__main__":
    try:
        main()
        
    except Exception as e:
        print(traceback.print_exc())
        getch()