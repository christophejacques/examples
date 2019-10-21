import urllib.request
from msvcrt import getch
import traceback
from definition import printdef


try:
  url = "http://www.google.com/"
  requete = urllib.request.Request(url)
  printdef(requete)
  
  response = urllib.request.urlopen(url)
  html = response.read()
  
  printdef(response)
  

except urllib.error.HTTPError as e:
  print("HTTP Error :")
  print(e.code)
  print(e.read())

except urllib.error.URLError as e:
  print("URL Error :")
  if hasattr(e, "code"):
    print(e.code)
  if hasattr(e, "reason"):
    print(e.reason)
  
except:
  print(traceback.print_exc())
  
print("Press any key.")
#getch()