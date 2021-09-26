from msvcrt import getch

def myRange(n):
    x = 0
    while x < n:
        yield x, n-x
        x += 1
        
       
try:
    for x, y in myRange(10):
        print(x, y)
        
    
except Exception as e:
    print("Error:", e)
    
#getch()
