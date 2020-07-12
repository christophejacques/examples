import keyboard  # using module keyboard
from utils.colors import printXY

print(dir(keyboard))
#help(keyboard.read_key)
#help(keyboard._queue.Queue)
#print(keyboard.key_to_scan_codes('a'))

index = 0
fin_programme = False

def fin_prog(*arg):
    global fin_programme
    print("fin programme", arg)
    # fin_programme = True

keyboard.on_press_key('a', fin_prog)
k = keyboard._queue.Queue()

help(keyboard.read_key)
def get_key():
    t = None
    try:
        t = k.get(block=False)
        printXY(10,28, "touche appuyée")
    except Exception as e:
        pass
        
    return t

while not fin_programme and True:  # making a loop
    index += 1
    if index > 10000: index = 1
    printXY(10, 30, "{:6}".format(index))
    try:  # used try so that if user pressed other than the given key error will not be shown
        t = get_key()
        if keyboard.is_pressed('q'):  # if key 'q' is pressed 
            print('You Pressed A Key!')
            break  # finishing the loop
    except:
        break  # if user pressed a key other than the given key the loop will break
        