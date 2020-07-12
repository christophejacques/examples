from msvcrt import getch  # try to import Windows version
from utils.colors import printXY
import _thread
import time
import sys

char = None

class Patience:
    
    def __init__(self):
        self.index = -1
    
    def __str__(self):
        self.index += 1
        if self.index >= 4: self.index = 0
        return ( "|", "/", "─", "\\" )[self.index]
 
 
class Keyboard:
    
    touche = None
    
    @classmethod
    def last_key(self):
        return self.touche
        
    @classmethod
    def get_key(self)
        self.touche = getch()
        
 
def keypress():
    global char
    char = getch()


def main():
    global char
    char = None
    p = Patience()
    
    _thread.start_new_thread(keypress, ())
    line = 4
    while True:
        if char is not None:
            if line == 4: line = 5
            else: line = 4
            printXY(2, line, "Key pressed is : {}".format(char)) # .decode('utf-8')
                
            _thread.start_new_thread(keypress, ())
            
            if char == b'\x00':
                char = getch()
                printXY(2, 6, "Special Key pressed is : {}".format(char)) 
                if char == b'k': # Alt-F4
                    exit()
                    
            elif char in (b'q',      # 'q'
                        b'\x1b',   # Echap
                        b'\x03',   # Ctrl-c
                        b'\x17'):  # Ctrl-w
                exit()
                
            char = None
        
        printXY(2, 2, "Program is running ", p)
        printXY(2, 2, "", end="", flush=True)
        time.sleep(0.1)
 
if __name__ == "__main__":
    try:
        main()
        
    except Exception as e:
        print("Error:",e)
        getch()