import sys, os, re

if len(sys.argv) > 1:
    todo = sys.argv[1].lower() == "exec"
else:
    todo = False

cmd = ""
import re

rx = re.compile(r'^.*\[.*\].*$')
# rx = re.compile(r'.*\..*')

for x in filter(rx.search, os.listdir('.')): # D:/Mes Documents/Tel
    if "[" and "]" in x:
        newfile = x.replace("[", "").replace("]", "")
        if todo:
            print(f"rename : '{x}'\n    to : '{newfile}'")
        else:
            print(f"find : '{x}'")

        try:
            if todo:
                os.rename(x, newfile)
          
        except Exception as e:
          print(e)
    
    else:
        pass
        # print("OK:{}".format(x))

if not todo:
    print("\nPour renommer les fichiers ajouter le paramètre : exec.")


#from msvcrt import getch
#getch()