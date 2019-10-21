import sys, os, re

cmd = ""
import re

rx = re.compile(r'.*\.*')

for x in filter(rx.search, os.listdir('.')):
    if "%20" in x:
        newfile = x.replace("%20", " ")
        print(f"rename : '{x}' en '{newfile}'")
        try:
          os.rename(x, newfile)
          
        except Exception as e:
          print(e)
    

#print(sys.argv)

#from msvcrt import getch
#getch()