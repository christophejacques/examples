import sys, os, re
import traceback

# os.system("cls")
if len(sys.argv) > 2:
    todo = sys.argv[2].lower() == "exec"
elif len(sys.argv) > 1:
    todo = False
else:
    print("nombre de parametres incorrectes")
    exit(1)

try:
    expreg = sys.argv[1]
    if todo:
        print("Renommage :", expreg)
    else:
        print("Listing :", expreg)
    cmd = ""
    import re

    # rx = re.compile("\[Thz.la.*()\]")
    rx = re.compile(expreg)

    for f in os.listdir('.'):
        res = rx.search(f)
        if res:
            newf = f.replace(res.group(0), res.group(1))
            print("{:78} > ".format(f), end="")
            print(newf)
            
            if todo:
                os.rename(f, newf)
            

except Exception as e:
    print("\n", traceback.print_exc())


from msvcrt import getch
#getch()